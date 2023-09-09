#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that implements the base classes for all Spot and Futures clients"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import urllib.parse
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar
from urllib.parse import urljoin
from uuid import uuid1

import requests

from kraken.exceptions import _get_exception

Self = TypeVar("Self")


def defined(value: Any) -> bool:
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
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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

    def __get_exception(self: KrakenErrorHandler, data: str) -> Optional[Any]:
        """
        Must be called when an error was found in the message, so the corresponding
        KrakenException will be returned.
        """
        return _get_exception(data=data)

    def check(self: KrakenErrorHandler, data: dict) -> dict | Any:
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
        :rtype: dict
        :raises KrakenError: If is the error keyword in the response
        """
        if len(data.get("error", [])) == 0 and "result" in data:
            return data["result"]

        exception: Type[Exception] = self.__get_exception(data=data["error"])
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
            exception: Type[Exception] = self.__get_exception(
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
                    exception: Type[Exception] = self.__get_exception(
                        status["status"],
                    )
                    if exception:
                        raise exception(data)
        return data


class KrakenSpotBaseAPI:
    """
    This class the the base for all Spot clients, handles un-/signed
    requests and returns exception handled results.

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
    API_V: str = "/0"

    def __init__(
        self: KrakenSpotBaseAPI,
        key: str = "",
        secret: str = "",
        url: str = "",
        *,
        sandbox: bool = False,
        use_custom_exceptions: bool = True,
    ):
        if sandbox:
            raise ValueError("Sandbox not available for Kraken Spot trading.")
        if url != "":
            self.url = url
        else:
            self.url = urljoin(self.URL, self.API_V)

        self.__key: str = key
        self.__secret: str = secret
        self.__use_custom_exceptions: bool = use_custom_exceptions

        self.__err_handler: KrakenErrorHandler = KrakenErrorHandler()
        self.__session: requests.Session = requests.Session()
        self.__session.headers.update({"User-Agent": "python-kraken-sdk"})

    def _request(  # noqa: PLR0913
        self: KrakenSpotBaseAPI,
        method: str,
        uri: str,
        params: Optional[dict] = None,
        timeout: int = 10,
        *,
        auth: bool = True,
        do_json: bool = False,
        return_raw: bool = False,
        extra_params: Optional[str | dict] = None,
    ) -> dict[str, Any] | list[str] | list[dict[str, Any]] | requests.Response:
        """
        Handles the requested requests, by sending the request, handling the
        response, and returning the message or in case of an error the
        respective Exception.

        :param method:  The request method, e.g., ``GET``, ``POST``, and ``PUT``
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
        :raise kraken.exceptions.KrakenException.*: If the response contains
            errors
        :return: The response
        :rtype: dict[str, Any] | list[str] | list[dict[str, Any]] |
            requests.Response
        """
        if not defined(params):
            params = {}
        if defined(extra_params):
            params |= (
                json.loads(extra_params)
                if isinstance(extra_params, str)
                else extra_params
            )

        method = method.upper()
        if method in ("GET", "DELETE") and params:
            data_json: str = "&".join(
                [f"{key}={params[key]}" for key in sorted(params)],
            )
            uri += f"?{data_json}".replace(" ", "%20")

        headers: dict = {}
        if auth:
            if (
                not self.__key
                or self.__key == ""
                or not self.__secret
                or self.__secret == ""
            ):
                raise ValueError("Missing credentials.")

            params["nonce"] = str(int(time.time() * 100_000_000))
            content_type: str
            sign_data: str

            if do_json:
                content_type = "application/json; charset=utf-8"
                sign_data = json.dumps(params)
            else:
                content_type = "application/x-www-form-urlencoded; charset=utf-8"
                sign_data = urllib.parse.urlencode(params)

            headers.update(
                {
                    "Content-Type": content_type,
                    "API-Key": self.__key,
                    "API-Sign": self._get_kraken_signature(
                        url_path=f"{self.API_V}{uri}",
                        data=sign_data,
                        nonce=params["nonce"],
                    ),
                },
            )

        url: str = f"{self.url}{uri}"
        if method in ("GET", "DELETE"):
            return self.__check_response_data(
                response=self.__session.request(
                    method=method,
                    url=url,
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

        if response.status_code in ("200", 200):
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


class KrakenFuturesBaseAPI:
    """
    The base class for all Futures clients handles un-/signed requests
    and returns exception handled results.

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

    def __init__(
        self: KrakenFuturesBaseAPI,
        key: str = "",
        secret: str = "",
        url: str = "",
        *,
        sandbox: bool = False,
        use_custom_exceptions: bool = True,
    ):
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
        self.__session.headers.update({"User-Agent": "python-kraken-sdk"})

    def _request(  # noqa: PLR0913
        self: KrakenFuturesBaseAPI,
        method: str,
        uri: str,
        post_params: Optional[dict] = None,
        query_params: Optional[dict] = None,
        timeout: int = 10,
        *,
        auth: bool = True,
        return_raw: bool = False,
        extra_params: Optional[dict] = None,
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
        :raise kraken.exceptions.KrakenException.*: If the response contains
            errors
        :return: The response
        :rtype: dict[str, Any] | list[dict[str, Any]] | list[str] | requests.Response
        """
        method = method.upper()

        post_string: str = ""
        listed_params: list[str]
        if defined(extra_params):
            extra_params = (
                json.loads(extra_params)
                if isinstance(extra_params, str)
                else extra_params
            )
        else:
            extra_params = {}

        if defined(post_params):
            post_params |= extra_params
            listed_params = [f"{key}={post_params[key]}" for key in sorted(post_params)]
            post_string = "&".join(listed_params)
        else:
            post_params = {}
            post_params |= extra_params

        query_string: str = ""
        if query_params is not None:
            listed_params = [
                f"{key}={query_params[key]}" for key in sorted(query_params)
            ]
            query_string = "&".join(listed_params).replace(" ", "%20")
        else:
            query_params = {}

        headers: dict = {}
        if auth:
            if (
                not self.__key
                or self.__key == ""
                or not self.__secret
                or self.__secret == ""
            ):
                raise ValueError("Missing credentials")
            nonce: str = str(int(time.time() * 100_000_000))
            headers.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                    "Nonce": nonce,
                    "APIKey": self.__key,
                    "Authent": self._get_kraken_futures_signature(
                        uri,
                        query_string + post_string,
                        nonce,
                    ),
                },
            )

        if method in ("GET", "DELETE"):
            return self.__check_response_data(
                response=self.__session.request(
                    method=method,
                    url=f"{self.url}{uri}"
                    if query_string == ""
                    else f"{self.url}{uri}?{query_string}",
                    headers=headers,
                    timeout=timeout,
                ),
                return_raw=return_raw,
            )

        if method == "PUT":
            return self.__check_response_data(
                response=self.__session.request(
                    method=method,
                    url=f"{self.url}{uri}",
                    params=str.encode(post_string),
                    headers=headers,
                    timeout=timeout,
                ),
                return_raw=return_raw,
            )

        return self.__check_response_data(
            response=self.__session.request(
                method=method,
                url=f"{self.url}{uri}?{post_string}",
                data=str.encode(post_string),
                headers=headers,
                timeout=timeout,
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

        if response.status_code in ("200", 200):
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
