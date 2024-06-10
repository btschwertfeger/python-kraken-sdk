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
from functools import wraps
from typing import TYPE_CHECKING, Any, Final, TypeVar
from urllib.parse import urlencode, urljoin
from uuid import uuid1

import requests

from kraken.exceptions import _get_exception

if TYPE_CHECKING:
    from collections.abc import Callable

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
            *args: Any | None,  # noqa: ANN401
            **kwargs: Any | None,  # noqa: ANN401
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


class KrakenErrorHandler:
    """
    Class that checks if the response of a request contains error messages and
    returns either message if there is no error or raises a custom
    KrakenException based on the error message.
    """

    def __get_exception(
        self: KrakenErrorHandler,
        data: str,
    ) -> Any | None:  # noqa: ANN401
        """
        Must be called when an error was found in the message, so the corresponding
        KrakenException will be returned.
        """
        return _get_exception(data=data)

    def check(self: KrakenErrorHandler, data: dict) -> dict | Any:  # noqa: ANN401
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

    def check_send_status(self: KrakenErrorHandler, data: dict) -> dict:
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

    def check_batch_status(self: KrakenErrorHandler, data: dict) -> dict:
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


class KrakenSpotBaseAPI:
    """
    This class the the base for all Spot clients, handles un-/signed
    requests and returns exception handled results.

    If you are facing timeout errors on derived clients, you can make use of the
    ``TIMEOUT`` attribute to deviate from the default ``10`` seconds.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: URL to access the Kraken API (default: https://api.kraken.com)
    :type url: str, optional
    :param sandbox: Use the sandbox (not supported for Spot trading so far,
        default: ``False``)
    :type sandbox: bool, optional
    """

    URL: str = "https://api.kraken.com"
    TIMEOUT: int = 10

    def __init__(
        self: KrakenSpotBaseAPI,
        key: str = "",
        secret: str = "",
        url: str = "",
        *,
        sandbox: bool = False,
        use_custom_exceptions: bool = True,
    ) -> None:
        if sandbox:
            raise ValueError("Sandbox not available for Kraken Spot trading.")
        if url:
            self.URL = url

        self.__key: str = key
        self.__secret: str = secret
        self.__use_custom_exceptions: bool = use_custom_exceptions

        self.__err_handler: KrakenErrorHandler = KrakenErrorHandler()
        self.__session: requests.Session = requests.Session()
        self.__session.headers.update(
            {
                "User-Agent": "python-kraken-sdk"
                " (https://github.com/btschwertfeger/python-kraken-sdk)",
            },
        )

    def _request(  # noqa: PLR0913 # pylint: disable=too-many-arguments
        self: KrakenSpotBaseAPI,
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

        :param method: The request method, e.g., ``GET``, ``POST``, and ``PUT``
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
        :rtype: dict[str, Any] | list[str] | list[dict[str, Any]] |
            requests.Response
        """
        METHOD: str = method.upper()
        URL: str = urljoin(self.URL, uri)

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
            if METHOD in {"GET", "DELETE"} and params
            else ""
        )

        if query_params and query_str:
            query_params += f"&{query_str}"
        elif query_str:
            query_params = query_str

        TIMEOUT: int = self.TIMEOUT if timeout != 10 else timeout
        HEADERS: dict = {}

        if auth:
            if not self.__key or not self.__secret:
                raise ValueError("Missing credentials.")

            params["nonce"] = str(int(time.time() * 100_000_000))
            content_type: str
            sign_data: str

            if do_json:
                content_type = "application/json; charset=utf-8"
                sign_data = json.dumps(params)
            else:
                content_type = "application/x-www-form-urlencoded; charset=utf-8"
                sign_data = urlencode(params, doseq=True)

            HEADERS.update(
                {
                    "Content-Type": content_type,
                    "API-Key": self.__key,
                    "API-Sign": self._get_kraken_signature(
                        url_path=f"{uri}{query_params}",
                        data=sign_data,
                        nonce=params["nonce"],
                    ),
                },
            )

        if METHOD in {"GET", "DELETE"}:
            return self.__check_response_data(
                response=self.__session.request(
                    method=METHOD,
                    url=f"{URL}?{query_params}" if query_params else URL,
                    headers=HEADERS,
                    timeout=TIMEOUT,
                ),
                return_raw=return_raw,
            )

        if do_json:
            return self.__check_response_data(
                response=self.__session.request(
                    method=METHOD,
                    url=URL,
                    headers=HEADERS,
                    json=params,
                    timeout=TIMEOUT,
                ),
                return_raw=return_raw,
            )

        return self.__check_response_data(
            response=self.__session.request(
                method=METHOD,
                url=URL,
                headers=HEADERS,
                data=params,
                timeout=TIMEOUT,
            ),
            return_raw=return_raw,
        )

    def _get_kraken_signature(
        self: KrakenSpotBaseAPI,
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
                base64.b64decode(self.__secret),
                url_path.encode()
                + hashlib.sha256((str(nonce) + data).encode()).digest(),
                hashlib.sha512,
            ).digest(),
        ).decode()

    def __check_response_data(
        self: KrakenSpotBaseAPI,
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
        if not self.__use_custom_exceptions:
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
                return self.__err_handler.check(data)  # type: ignore[arg-type]
            return data

        raise Exception(f"{response.status_code} - {response.text}")

    @property
    def return_unique_id(self: KrakenSpotBaseAPI) -> str:
        """Returns a unique uuid string

        :return: uuid
        :rtype: str
        """
        return "".join(str(uuid1()).split("-"))

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self: KrakenSpotBaseAPI,
        *exc: object,
        **kwargs: dict[str, Any],
    ) -> None:
        pass


class KrakenNFTBaseAPI(KrakenSpotBaseAPI):
    """Inherits from KrakenSpotBaseAPI"""


class KrakenFuturesBaseAPI:
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
    """

    URL: str = "https://futures.kraken.com"
    SANDBOX_URL: str = "https://demo-futures.kraken.com"
    TIMEOUT: int = 10

    def __init__(
        self: KrakenFuturesBaseAPI,
        key: str = "",
        secret: str = "",
        url: str = "",
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

        self.__key: str = key
        self.__secret: str = secret
        self.__use_custom_exceptions: bool = use_custom_exceptions

        self.__err_handler: KrakenErrorHandler = KrakenErrorHandler()
        self.__session: requests.Session = requests.Session()
        self.__session.headers.update(
            {
                "User-Agent": "python-kraken-sdk"
                " (https://github.com/btschwertfeger/python-kraken-sdk)",
            },
        )

    def _request(  # noqa: PLR0913 # pylint: disable=too-many-arguments
        self: KrakenFuturesBaseAPI,
        method: str,
        uri: str,
        post_params: dict | None = None,
        query_params: dict | None = None,
        timeout: int = 10,
        *,
        auth: bool = True,
        return_raw: bool = False,
        extra_params: str | dict | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]] | list[str] | requests.Response:
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
        :rtype: dict[str, Any] | list[dict[str, Any]] | list[str] | requests.Response
        """
        METHOD: Final[str] = method.upper()
        URL: Final[str] = urljoin(self.url, uri)

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

        # post_string: Final[str] = json.dumps(post_params) if post_params else ""
        query_string = (
            "" if query_params is None else urlencode(query_params, doseq=True)
        )

        TIMEOUT: int = self.TIMEOUT if timeout == 10 else timeout
        HEADERS: dict = {}
        if auth:
            if not self.__key or not self.__secret:
                raise ValueError("Missing credentials")
            nonce: str = str(int(time.time() * 100_000_000))
            HEADERS.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "Nonce": nonce,
                    "APIKey": self.__key,
                    "Authent": self._get_kraken_futures_signature(
                        uri,
                        query_string + encoded_payload,
                        nonce,
                    ),
                },
            )
        if METHOD in {"GET", "DELETE"}:
            return self.__check_response_data(
                response=self.__session.request(
                    method=METHOD,
                    url=URL,
                    params=query_string,
                    headers=HEADERS,
                    timeout=TIMEOUT,
                ),
                return_raw=return_raw,
            )

        if METHOD == "PUT":
            return self.__check_response_data(
                response=self.__session.request(
                    method=METHOD,
                    url=URL,
                    params=encoded_payload,
                    headers=HEADERS,
                    timeout=TIMEOUT,
                ),
                return_raw=return_raw,
            )

        return self.__check_response_data(
            response=self.__session.request(
                method=METHOD,
                url=URL,
                data=encoded_payload,
                headers=HEADERS,
                timeout=TIMEOUT,
            ),
            return_raw=return_raw,
        )

    def _get_kraken_futures_signature(
        self: KrakenFuturesBaseAPI,
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
                base64.b64decode(self.__secret),
                sha256_hash.digest(),
                hashlib.sha512,
            ).digest(),
        ).decode()

    def __check_response_data(
        self: KrakenFuturesBaseAPI,
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
        if not self.__use_custom_exceptions:
            return response

        if response.status_code in {"200", 200}:
            if return_raw:
                return response
            try:
                data: dict = response.json()
            except ValueError as exc:
                raise ValueError(response.content) from exc

            if "error" in data:
                return self.__err_handler.check(data)
            if "sendStatus" in data:
                return self.__err_handler.check_send_status(data)
            if "batchStatus" in data:
                return self.__err_handler.check_batch_status(data)
            return data

        raise Exception(f"{response.status_code} - {response.text}")

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(self, *exc: object, **kwargs: dict[str, Any]) -> None:
        pass


__all__ = ["defined", "ensure_string", "KrakenSpotBaseAPI", "KrakenFuturesBaseAPI"]
