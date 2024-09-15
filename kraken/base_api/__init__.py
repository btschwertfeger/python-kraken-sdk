#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that implements the base classes for all Spot and Futures clients"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from copy import deepcopy
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar
from urllib.parse import urlencode, urljoin
from uuid import uuid1

import aiohttp
import requests

from kraken.exceptions import _get_exception

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Coroutine
    from typing import Final

Self = TypeVar("Self")


def defined(value: Any) -> bool:  # noqa: ANN401
    """Returns ``True`` if ``value`` is not ``None``"""
    return value is not None


def ensure_string(parameter_name: str) -> Callable:
    """
    This function is intended to be used as decorator
    to ensure that a specific parameter is of type string.

    .. code-block:: python
        :linenos:
        :caption: Example

        @ensure_string("assets")
        @lru_cache()
        def get_assets(
            self: "Market",
            assets: Optional[str | list[str]] = None,
            aclass: Optional[str] = None,
        ) -> dict:
            # If the function was called using
            # get_assets(assets=["BTC","USD","ETH"])
            # there will be no error because of the non-hashable
            # parameters, because the decorator transforms the
            # list into: "BTC,USD,ETH"

    :param parameter_name: The parameter name to transform into string
    :type parameter_name: str
    :return: The called function
    :rtype: Callable
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)  # required for sphinx to discover the func
        def wrapper(
            *args: Any | None,
            **kwargs: Any | None,
        ) -> Any | None:  # noqa: ANN401
            if parameter_name in kwargs:
                value: Any = kwargs[parameter_name]
                if parameter_name == "extra_params":
                    if not isinstance(value, dict):
                        raise TypeError("'extra_params must be type dict.")
                    kwargs[parameter_name] = json.dumps(value)
                elif isinstance(value, str) or value is None:
                    pass
                elif isinstance(value, list):
                    kwargs[parameter_name] = ",".join(value)
                else:
                    raise TypeError(
                        f"{parameter_name} can't be {type(kwargs[parameter_name])}!",
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator


class ErrorHandler:
    """
    Class that checks if the response of a request contains error messages and
    returns either message if there is no error or raises a custom
    KrakenException based on the error message.
    """

    def __get_exception(
        self: ErrorHandler,
        data: str,
    ) -> Any | None:  # noqa: ANN401
        """
        Must be called when an error was found in the message, so the corresponding
        KrakenException will be returned.
        """
        return _get_exception(data=data)

    def check(self: ErrorHandler, data: dict) -> dict | Any:  # noqa: ANN401
        """
        Check if the error message is a known KrakenError response and than
        raise a custom exception or return the data containing the "error".
        This is only for the Spot REST endpoints, since the Futures API
        serves kinds of errors.

        :param data: The response as dict to check for an error
        :type data: dict
        :raise kraken.exceptions.KrakenException.*: raises a KrakenError if the
            response contains an error
        :return: The response as dict
        :rtype: Any
        :raises KrakenError: If is the error keyword in the response
        """
        if len(data.get("error", [])) == 0 and "result" in data:
            return data["result"]

        exception: type[Exception] = self.__get_exception(data=data["error"])
        if exception:
            raise exception(data)
        return data

    def check_send_status(self: ErrorHandler, data: dict) -> dict:
        """
        Checks the responses of Futures REST endpoints

        :param data: The response as dict to check for an error
        :type data: dict
        :raise kraken.exceptions.KrakenException.*: raises a KrakenError if the
            response contains an error
        :return: The response as dict
        :rtype: dict
        """
        if "sendStatus" in data and "status" in data["sendStatus"]:
            exception: type[Exception] = self.__get_exception(
                data["sendStatus"]["status"],
            )
            if exception:
                raise exception(data)
            return data
        return data

    def check_batch_status(self: ErrorHandler, data: dict) -> dict:
        """
        Used to check the Futures batch order responses for errors

        :param data: The response as dict to check for an error
        :type data: dict
        :raise kraken.exceptions.KrakenException.*: raises a KrakenError if the
            response contains an error
        :return: The response as list[dict]
        :rtype: dict
        """
        if "batchStatus" in data:
            batch_status: list[dict[str, Any]] = data["batchStatus"]
            for status in batch_status:
                if "status" in status:
                    exception: type[Exception] = self.__get_exception(
                        status["status"],
                    )
                    if exception:
                        raise exception(data)
        return data


class SpotClient:
    """
    This class is the base for all Spot clients, handles un-/signed
    requests and returns exception handled results.

    If you are facing timeout errors on derived clients, you can make use of the
    ``TIMEOUT`` attribute to deviate from the default ``10`` seconds.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: URL to access the Kraken API (default: https://api.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional
    """

    URL: str = "https://api.kraken.com"
    TIMEOUT: int = 10
    HEADERS: Final[dict] = {
        "User-Agent": "python-kraken-sdk (https://github.com/btschwertfeger/python-kraken-sdk)",
    }

    def __init__(  # nosec: B107
        self: SpotClient,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
        *,
        use_custom_exceptions: bool = True,
    ) -> None:
        if url:
            self.URL = url

        self._key: str = key
        self._secret: str = secret
        self._use_custom_exceptions: bool = use_custom_exceptions
        self._err_handler: ErrorHandler = ErrorHandler()
        self.__session: requests.Session = requests.Session()
        if proxy is not None:
            self.__session.proxies.update(
                {
                    "http": proxy,
                    "https": proxy,
                },
            )
        self.__session.headers.update(self.HEADERS)

    def _prepare_request(
        self: SpotClient,
        *,
        method: str,
        uri: str,
        params: dict | None = None,
        auth: bool = True,
        do_json: bool = False,
        query_str: str | None = None,
        extra_params: str | dict | None = None,
    ) -> tuple[str, str, dict, dict, str]:
        method: str = method.upper()  # type: ignore[no-redef]
        url: str = urljoin(self.URL, uri)

        if not defined(params):
            params = {}
        if defined(extra_params):
            params |= (
                json.loads(extra_params)
                if isinstance(extra_params, str)
                else extra_params
            )
        query_params: str = (
            urlencode(params, doseq=True)
            if method in {"GET", "DELETE"} and params
            else ""
        )

        if query_params and query_str:
            query_params += f"&{query_str}"
        elif query_str:
            query_params = query_str

        headers: dict = deepcopy(self.HEADERS)

        if auth:
            if not self._key or not self._secret:
                raise ValueError("Missing credentials.")

            params["nonce"] = self.get_nonce()
            content_type: str
            sign_data: str

            if do_json:
                content_type = "application/json; charset=utf-8"
                sign_data = json.dumps(params)
            else:
                content_type = "application/x-www-form-urlencoded; charset=utf-8"
                sign_data = urlencode(params, doseq=True)

            headers.update(
                {
                    "Content-Type": content_type,
                    "API-Key": self._key,
                    "API-Sign": self._get_kraken_signature(
                        url_path=f"{uri}{query_params}",
                        data=sign_data,
                        nonce=params["nonce"],
                    ),
                },
            )
        return method, url, headers, params, query_params

    def request(  # noqa: PLR0913 # pylint: disable=too-many-arguments
        self: SpotClient,
        method: str,
        uri: str,
        params: dict | None = None,
        timeout: int = 10,
        *,
        auth: bool = True,
        do_json: bool = False,
        return_raw: bool = False,
        query_str: str | None = None,
        extra_params: str | dict | None = None,
    ) -> dict[str, Any] | list[str] | list[dict[str, Any]] | requests.Response:
        """
        Handles the requested requests, by sending the request, handling the
        response, and returning the message or in case of an error the
        respective Exception.

        :param method: The request method, e.g., ``GET``, ``POST``, ``PUT``, ...
        :type method: str
        :param uri: The endpoint to send the message
        :type uri: str
        :param auth: If the requests needs authentication (default: ``True``)
        :type auth: bool
        :param params: The query or post parameter of the request (default:
            ``None``)
        :type params: dict, optional
        :param extra_params: Additional query or post parameter of the request
            (default: ``None``)
        :type extra_params: str | dict, optional
        :param timeout: Timeout for the request (default: ``10``)
        :type timeout: int
        :param do_json: If the ``params`` must be "jsonified" - in case of
            nested dict style
        :type do_json: bool
        :param return_raw: If the response should be returned without parsing.
            This is used for example when requesting an export of the trade
            history as .zip archive.
        :type return_raw: bool, optional
        :param query_str: Add custom values to the query
            /0/public/Nfts?filter%5Bcollection_id%5D=NCQNABO-XYCA7-JMMSDF&page_size=10
        :type query_str: str, optional
        :raise kraken.exceptions.KrakenException.*: If the response contains
            errors
        :return: The response
        :rtype: dict | list | requests.Response
        """
        method, url, headers, params, query_params = self._prepare_request(
            method=method,
            uri=uri,
            params=params,
            auth=auth,
            do_json=do_json,
            query_str=query_str,
            extra_params=extra_params,
        )
        timeout: int = self.TIMEOUT if timeout != 10 else timeout  # type: ignore[no-redef]

        if method in {"GET", "DELETE"}:
            return self.__check_response_data(
                response=self.__session.request(
                    method=method,
                    url=f"{url}?{query_params}" if query_params else url,
                    headers=headers,
                    timeout=timeout,
                ),
                return_raw=return_raw,
            )

        if do_json:
            return self.__check_response_data(
                response=self.__session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=params,
                    timeout=timeout,
                ),
                return_raw=return_raw,
            )

        return self.__check_response_data(
            response=self.__session.request(
                method=method,
                url=url,
                headers=headers,
                data=params,
                timeout=timeout,
            ),
            return_raw=return_raw,
        )

    def _get_kraken_signature(
        self: SpotClient,
        url_path: str,
        data: str,
        nonce: int,
    ) -> str:
        """
        Creates the signature of the data. This is required for authenticated
        requests to verify the user.

        :param url_path: The endpoint including the api version
        :type url_path: str
        :param data: Data of the request to sign, including the nonce.
        :type data: str
        :param nonce: The nonce to sign with
        :type nonce: int
        :return: The signed string
        :rtype: str
        """
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self._secret),
                url_path.encode()
                + hashlib.sha256((str(nonce) + data).encode()).digest(),
                hashlib.sha512,
            ).digest(),
        ).decode()

    def __check_response_data(
        self: SpotClient,
        response: requests.Response,
        *,
        return_raw: bool = False,
    ) -> dict | list | requests.Response:
        """
        Checks the response, handles the error (if exists) and returns the response data.

        :param response: The response of a request, requested by the requests module
        :type response: requests.Response
        :param return_raw: Defines if the return should be the raw response if there is no error
        :type data: bool, optional
        :return: The response in raw or parsed to dict
        :rtype: dict | list | requests.Response
        """
        if not self._use_custom_exceptions:
            return response

        if response.status_code in {"200", 200}:
            if return_raw:
                return response
            try:
                data: dict | list = response.json()
            except ValueError as exc:
                raise ValueError(response.content) from exc

            if "error" in data:
                # can only be dict if error is present:
                return self._err_handler.check(data)  # type: ignore[arg-type]
            return data

        raise Exception(f"{response.status_code} - {response.text}")

    def get_nonce(self: SpotClient) -> str:
        """Return a new nonce"""
        return str(int(time.time() * 100_000_000))

    @property
    def return_unique_id(self: SpotClient) -> str:
        """Returns a unique uuid string

        :return: uuid
        :rtype: str
        """
        return "".join(str(uuid1()).split("-"))

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self: SpotClient,
        *exc: object,
        **kwargs: dict[str, Any],
    ) -> None:
        pass


class SpotAsyncClient(SpotClient):
    """
    This class provides the base client for accessing the Kraken Spot and NFT
    API using asynchronous requests.

    If you are facing timeout errors on derived clients, you can make use of the
    ``TIMEOUT`` attribute to deviate from the default ``10`` seconds.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: URL to access the Kraken API (default: https://api.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional
    """

    def __init__(  # nosec: B107
        self: SpotAsyncClient,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
        *,
        use_custom_exceptions: bool = True,
    ) -> None:
        super().__init__(
            key=key,
            secret=secret,
            url=url,
            use_custom_exceptions=use_custom_exceptions,
        )
        self.__session = aiohttp.ClientSession(headers=self.HEADERS)
        self.proxy = proxy

    async def request(  # type: ignore[override] # pylint: disable=invalid-overridden-method,too-many-arguments # noqa: PLR0913
        self: SpotAsyncClient,
        method: str,
        uri: str,
        params: dict | None = None,
        timeout: int = 10,  # noqa: ASYNC109
        *,
        auth: bool = True,
        do_json: bool = False,
        return_raw: bool = False,
        query_str: str | None = None,
        extra_params: str | dict | None = None,
    ) -> Coroutine:
        """
        Handles the requested requests, by sending the request, handling the
        response, and returning the message or in case of an error the
        respective Exception.

        :param method: The request method, e.g., ``GET``, ``POST``, ``PUT``, ...
        :type method: str
        :param uri: The endpoint to send the message
        :type uri: str
        :param auth: If the requests needs authentication (default: ``True``)
        :type auth: bool
        :param params: The query or post parameter of the request (default:
            ``None``)
        :type params: dict, optional
        :param timeout: Timeout for the request (default: ``10``)
        :type timeout: int
        :param do_json: If the ``params`` must be "jsonified" - in case of
            nested dict style
        :type do_json: bool
        :param return_raw: If the response should be returned without parsing.
            This is used for example when requesting an export of the trade
            history as .zip archive.
        :type return_raw: bool, optional
        :param query_str: Add custom values to the query
            /0/public/Nfts?filter%5Bcollection_id%5D=NCQNABO-XYCA7-JMMSDF&page_size=10
        :type query_str: str, optional
        :raise kraken.exceptions.KrakenException.*: If the response contains
            errors
        :return: The response
        :rtype: dict | list | aiohttp.ClientResponse
        """
        method, url, headers, params, query_params = self._prepare_request(
            method=method,
            uri=uri,
            params=params,
            auth=auth,
            do_json=do_json,
            query_str=query_str,
            extra_params=extra_params,
        )
        timeout: int = self.TIMEOUT if timeout != 10 else timeout  # type: ignore[no-redef]

        if method in {"GET", "DELETE"}:
            return await self.__check_response_data(  # type: ignore[return-value]
                response=await self.__session.request(  # type: ignore[misc,call-arg]
                    method=method,
                    url=f"{url}?{query_params}" if query_params else url,
                    headers=headers,
                    timeout=timeout,
                    proxy=self.proxy,
                ),
                return_raw=return_raw,
            )

        if do_json:
            return await self.__check_response_data(  # type: ignore[return-value]
                response=await self.__session.request(  # type: ignore[misc,call-arg]
                    method=method,
                    url=url,
                    headers=headers,
                    json=params,
                    timeout=timeout,
                    proxy=self.proxy,
                ),
                return_raw=return_raw,
            )

        return await self.__check_response_data(  # type: ignore[return-value]
            response=await self.__session.request(  # type: ignore[misc,call-arg]
                method=method,
                url=url,
                headers=headers,
                data=params,
                timeout=timeout,
                proxy=self.proxy,
            ),
            return_raw=return_raw,
        )

    async def __check_response_data(  # pylint: disable=invalid-overridden-method
        self: SpotAsyncClient,
        response: aiohttp.ClientResponse,
        *,
        return_raw: bool = False,
    ) -> dict | list | aiohttp.ClientResponse:
        """
        Checks the response, handles the error (if exists) and returns the
        response data.

        :param response: The response of a request, requested by the requests
            module
        :type response: aiohttp.ClientResponse
        :param return_raw: Defines if the return should be the raw response if
            there is no error
        :type data: bool, optional
        :return: The response in raw or parsed to dict
        :rtype: dict | list | aiohttp.ClientResponse
        """
        if not self._use_custom_exceptions:
            return response

        if response.status in {"200", 200}:
            if return_raw:
                return response
            try:
                data: dict | list = await response.json()
            except ValueError as exc:
                raise ValueError(response.content) from exc

            if "error" in data:
                return self._err_handler.check(data)  # type: ignore[arg-type]
            return data

        raise Exception(f"{response.status} - {response.text}")

    async def async_close(self: SpotAsyncClient) -> None:
        """Closes the aiohttp session"""
        await self.__session.close()  # type: ignore[func-returns-value]

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(self: SpotAsyncClient, *args: object) -> None:
        await self.async_close()


class NFTClient(SpotClient):
    """Inherits from SpotClient"""


class FuturesClient:
    """
    The base class for all Futures clients handles un-/signed requests
    and returns exception handled results.

    If you are facing timeout errors on derived clients, you can make use of the
    ``TIMEOUT`` attribute to deviate from the default ``10`` seconds.

    If the sandbox environment is chosen, the keys must be generated from here:
        https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str, optional
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str, optional
    :param url: The URL to access the Futures Kraken API (default: https://futures.kraken.com)
    :type url: str, optional
    :param sandbox: If set to ``True`` the URL will be https://demo-futures.kraken.com (default: ``False``)
    :type sandbox: bool, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional
    """

    URL: str = "https://futures.kraken.com"
    SANDBOX_URL: str = "https://demo-futures.kraken.com"
    TIMEOUT: int = 10
    HEADERS: Final[dict] = {
        "User-Agent": "python-kraken-sdk (https://github.com/btschwertfeger/python-kraken-sdk)",
    }

    def __init__(  # nosec: B107
        self: FuturesClient,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
        *,
        sandbox: bool = False,
        use_custom_exceptions: bool = True,
    ) -> None:
        self.sandbox: bool = sandbox
        self.url: str
        if url:
            self.url = url
        elif self.sandbox:
            self.url = self.SANDBOX_URL
        else:
            self.url = self.URL

        self._key: str = key
        self._secret: str = secret
        self._use_custom_exceptions: bool = use_custom_exceptions

        self._err_handler: ErrorHandler = ErrorHandler()
        self.__session: requests.Session = requests.Session()
        self.__session.headers.update(
            {
                "User-Agent": "python-kraken-sdk (https://github.com/btschwertfeger/python-kraken-sdk)",
            },
        )
        if proxy is not None:
            self.__session.proxies.update(
                {
                    "http": proxy,
                    "https": proxy,
                },
            )

    def _prepare_request(
        self: FuturesClient,
        method: str,
        uri: str,
        post_params: dict,
        query_params: str | dict,
        extra_params: str | dict | None = None,
        auth: bool = True,  # noqa: FBT001,FBT002
    ) -> tuple[str, str, dict, str, str]:
        method: str = method.upper()  # type: ignore[no-redef]
        url: Final[str] = urljoin(self.url, uri)

        if defined(extra_params):
            extra_params = (
                json.loads(extra_params)
                if isinstance(extra_params, str)
                else extra_params
            )
        else:
            extra_params = {}

        if post_params is None:
            post_params = {}
            post_params |= extra_params

        encoded_payload: Final[str] = urlencode(post_params, doseq=True)

        query_string = (
            "" if query_params is None else urlencode(query_params, doseq=True)  # type: ignore[arg-type]
        )

        headers: dict = deepcopy(self.HEADERS)

        if auth:
            if not self._key or not self._secret:
                raise ValueError("Missing credentials")
            nonce: str = self.get_nonce()
            headers.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "Nonce": nonce,
                    "APIKey": self._key,
                    "Authent": self._get_kraken_futures_signature(
                        uri,
                        query_string + encoded_payload,
                        nonce,
                    ),
                },
            )

        return method, url, headers, encoded_payload, query_string

    def request(  # pylint: disable=too-many-arguments
        self: FuturesClient,
        method: str,
        uri: str,
        post_params: dict | None = None,
        query_params: dict | None = None,
        timeout: int = 10,
        *,
        auth: bool = True,
        return_raw: bool = False,
        extra_params: str | dict | None = None,
    ) -> dict | list | requests.Response:
        """
        Handles the requested requests, by sending the request, handling the
        response, and returning the message or in case of an error the
        respective Exception.

        :param method:  The request method, e.g., ``GET``, ``POST``, and ``PUT``
        :type method: str
        :param uri: The endpoint to send the message
        :type uri: str
        :param post_params: The query parameter of the request (default:
            ``None``)
        :type post_params: dict, optional
        :param extra_params: Additional query parameter of the request (default:
            ``None``)
        :type extra_params: str | dict, optional
        :param query_params: The query parameter of the request (default:
            ``None``)
        :type query_params: dict, optional
        :param timeout: Timeout for the request (default: ``10``)
        :type timeout: int
        :param auth: If the request needs authentication (default: ``True``)
        :type auth: bool
        :param return_raw: If the response should be returned without parsing.
            This is used for example when requesting an export of the trade
            history as .zip archive.
        :type return_raw: bool, optional
        :raise kraken.exceptions.*: If the response contains
            errors
        :return: The response
        :rtype: dict | list | requests.Response
        """
        method, url, headers, encoded_payload, query_string = self._prepare_request(
            method=method,
            uri=uri,
            post_params=post_params,
            query_params=query_params,
            auth=auth,
            extra_params=extra_params,
        )
        timeout: int = self.TIMEOUT if timeout == 10 else timeout  # type: ignore[no-redef]

        if method in {"GET", "DELETE"}:
            return self.__check_response_data(
                response=self.__session.request(
                    method=method,
                    url=url,
                    params=query_string,
                    headers=headers,
                    timeout=timeout,
                ),
                return_raw=return_raw,
            )

        if method == "PUT":
            return self.__check_response_data(
                response=self.__session.request(
                    method=method,
                    url=url,
                    params=encoded_payload,
                    headers=headers,
                    timeout=timeout,
                ),
                return_raw=return_raw,
            )

        return self.__check_response_data(
            response=self.__session.request(
                method=method,
                url=url,
                data=encoded_payload,
                headers=headers,
                timeout=timeout,
            ),
            return_raw=return_raw,
        )

    def _get_kraken_futures_signature(
        self: FuturesClient,
        endpoint: str,
        data: str,
        nonce: str,
    ) -> str:
        """
        Creates the signature of the data. This is required for authenticated
        requests to verify the user.

        :param endpoint: The endpoint including the api version
        :type endpoint: str
        :param data: Data of the request to sign, including the nonce.
        :type data: dict
        :param nonce: The nonce to use for this signature
        :type nonce: str
        :return: The signed string
        :rtype: str
        """
        if endpoint.startswith("/derivatives"):
            endpoint = endpoint[len("/derivatives") :]

        sha256_hash = hashlib.sha256()
        sha256_hash.update((data + nonce + endpoint).encode("utf8"))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self._secret),
                sha256_hash.digest(),
                hashlib.sha512,
            ).digest(),
        ).decode()

    def __check_response_data(
        self: FuturesClient,
        response: requests.Response,
        *,
        return_raw: bool = False,
    ) -> dict | requests.Response:
        """
        Checks the response, handles the error (if exists) and returns the
        response data.

        :param response: The response of a request, requested by the requests
            module
        :type response: requests.Response
        :param return_raw: Defines if the return should be the raw response if
            there is no error
        :type return_raw: dict, optional
        :raise kraken.exceptions.KrakenException.*: If the response contains the
            error key
        :return: The signed string
        :rtype: dict | requests.Response
        """
        if not self._use_custom_exceptions:
            return response

        if response.status_code in {"200", 200}:
            if return_raw:
                return response
            try:
                data: dict = response.json()
            except ValueError as exc:
                raise ValueError(response.content) from exc

            if "error" in data:
                return self._err_handler.check(data)
            if "sendStatus" in data:
                return self._err_handler.check_send_status(data)
            if "batchStatus" in data:
                return self._err_handler.check_batch_status(data)
            return data

        raise Exception(f"{response.status_code} - {response.text}")

    def get_nonce(self: FuturesClient) -> str:
        """Return a new nonce"""
        return str(int(time.time() * 100_000_000))

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(self, *exc: object, **kwargs: dict[str, Any]) -> None:
        pass


class FuturesAsyncClient(FuturesClient):
    """
    This class provides the base client for accessing the Kraken Futures API
    using asynchronous requests.

    If you are facing timeout errors on derived clients, you can make use of the
    ``TIMEOUT`` attribute to deviate from the default ``10`` seconds.

    If the sandbox environment is chosen, the keys must be generated from here:
        https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str, optional
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str, optional
    :param url: The URL to access the Futures Kraken API (default:
        https://futures.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional
    :param sandbox: If set to ``True`` the URL will be
        https://demo-futures.kraken.com (default: ``False``)
    :type sandbox: bool, optional
    """

    def __init__(  # nosec: B107
        self: FuturesAsyncClient,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
        *,
        sandbox: bool = False,
        use_custom_exceptions: bool = True,
    ) -> None:
        super().__init__(
            key=key,
            secret=secret,
            url=url,
            sandbox=sandbox,
            use_custom_exceptions=use_custom_exceptions,
        )
        self.__session = aiohttp.ClientSession(headers=self.HEADERS)
        self.proxy = proxy

    async def request(  # type: ignore[override] # pylint: disable=arguments-differ,invalid-overridden-method
        self: FuturesAsyncClient,
        method: str,
        uri: str,
        post_params: dict | None = None,
        query_params: dict | None = None,
        timeout: int = 10,  # noqa: ASYNC109
        *,
        auth: bool = True,
        return_raw: bool = False,
    ) -> dict | list | aiohttp.ClientResponse | Awaitable:
        method, url, headers, encoded_payload, query_string = self._prepare_request(
            method=method,
            uri=uri,
            post_params=post_params,
            query_params=query_params,
            auth=auth,
        )
        timeout: int = self.TIMEOUT if timeout != 10 else timeout  # type: ignore[no-redef]

        if method in {"GET", "DELETE"}:
            return await self.__check_response_data(
                response=await self.__session.request(  # type: ignore[misc,call-arg]
                    method=method,
                    url=url,
                    params=query_string,
                    headers=headers,
                    timeout=timeout,
                    proxy=self.proxy,
                ),
                return_raw=return_raw,
            )

        if method == "PUT":
            return await self.__check_response_data(
                response=await self.__session.request(  # type: ignore[misc,call-arg]
                    method=method,
                    url=url,
                    params=encoded_payload,
                    headers=headers,
                    timeout=timeout,
                    proxy=self.proxy,
                ),
                return_raw=return_raw,
            )

        return await self.__check_response_data(
            response=await self.__session.request(  # type: ignore[misc,call-arg]
                method=method,
                url=url,
                data=encoded_payload,
                headers=headers,
                timeout=timeout,
                proxy=self.proxy,
            ),
            return_raw=return_raw,
        )

    async def __check_response_data(  # pylint: disable=invalid-overridden-method
        self: FuturesAsyncClient,
        response: aiohttp.ClientResponse,
        *,
        return_raw: bool = False,
    ) -> dict | aiohttp.ClientResponse:
        """
        Checks the response, handles the error (if exists) and returns the
        response data.

        :param response: The response of a request, requested by the requests
            module
        :type response: requests.Response
        :param return_raw: Defines if the return should be the raw response if
            there is no error
        :type return_raw: dict, optional
        :raise kraken.exceptions.KrakenException.*: If the response contains the
            error key
        :return: The signed string
        :rtype: dict | aiohttp.ClientResponse
        """
        if not self._use_custom_exceptions:
            return response

        if response.status in {"200", 200}:
            if return_raw:
                return response
            try:
                data: dict = await response.json()
            except ValueError as exc:
                raise ValueError(response.content) from exc

            if "error" in data:
                return self._err_handler.check(data)
            if "sendStatus" in data:
                return self._err_handler.check_send_status(data)
            if "batchStatus" in data:
                return self._err_handler.check_batch_status(data)
            return data

        raise Exception(f"{response.status} - {response.text}")

    async def async_close(self: FuturesAsyncClient) -> None:
        """Closes the aiohttp session"""
        await self.__session.close()  # type: ignore[func-returns-value]

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(self: FuturesAsyncClient, *args: object) -> None:
        return await self.async_close()


__all__ = [
    "defined",
    "ensure_string",
    "SpotClient",
    "SpotAsyncClient",
    "NFTClient",
    "FuturesClient",
    "FuturesAsyncClient",
]
