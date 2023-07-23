#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that provides the base class for the Kraken Websocket clients v1 and v2.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, List, Optional, Type, Union

from kraken.base_api import KrakenBaseSpotAPI
from kraken.spot.websocket.connectors import (
    ConnectSpotWebsocketV1,
    ConnectSpotWebsocketV2,
)


class KrakenSpotWSClientBase(KrakenBaseSpotAPI):
    """
    This is the base class for :class:`kraken.spot.KrakenSpotWSClient` and
    :class:`kraken.spot.KrakenSpotWSClientV2`. It extends the REST API base
    class and is used to provide the base functionalities that are used
    for Kraken Websocket API v1 and v2.

    **This is an internal class and should not be used outside.**

    :param key: API Key for the Kraken Spot API (default: ``""``)
    :type key: str, optional
    :param secret: Secret API Key for the Kraken Spot API (default: ``""``)
    :type secret: str, optional
    :param url: Set a specific URL to access the Kraken REST API
    :type url: str, optional
    :param no_public: Disables public connection (default: ``False``).
        If not set or set to ``False``, the client will create a public and
        a private connection per default. If only a private connection is
        required, this parameter should be set to ``True``.
    :param beta: Use the beta websocket channels (maybe not supported anymore,
        default: ``False``)
    :type beta: bool
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    PROD_ENV_URL: str = "ws.kraken.com"
    AUTH_PROD_ENV_URL: str = "ws-auth.kraken.com"
    BETA_ENV_URL: str = "beta-ws.kraken.com"
    AUTH_BETA_ENV_URL: str = "beta-ws-auth.kraken.com"

    def __init__(
        self: KrakenSpotWSClientBase,
        key: str = "",
        secret: str = "",
        callback: Optional[Callable] = None,
        no_public: bool = False,
        beta: bool = False,
        api_version: str = "v2",
    ) -> None:
        super().__init__(key=key, secret=secret, sandbox=beta)

        self._is_auth: bool = bool(key and secret)
        self.__callback: Optional[Callable] = callback
        self.exception_occur: bool = False
        self._pub_conn: Optional[
            Union[ConnectSpotWebsocketV1, ConnectSpotWebsocketV2]
        ] = None
        self._priv_conn: Optional[
            Union[ConnectSpotWebsocketV1, ConnectSpotWebsocketV2]
        ] = None

        self.__connect(version=api_version, beta=beta, no_public=no_public)

    # --------------------------------------------------------------------------
    # Internals
    def __connect(
        self: "KrakenSpotWSClientBase", version: str, beta: bool, no_public: bool
    ) -> None:
        """
        Set up functions and attributes based on the API version.

        :param version: The Websocket API version to use (one of ``v1``, ``v2``)
        :type version: str
        """
        ConnectSpotWebsocket: Union[
            Type[ConnectSpotWebsocketV1], Type[ConnectSpotWebsocketV2]
        ]

        if version == "v1":
            ConnectSpotWebsocket = ConnectSpotWebsocketV1

        elif version == "v2":
            # pylint: disable=invalid-name
            self.PROD_ENV_URL += "/v2"
            self.AUTH_PROD_ENV_URL += "/v2"
            self.BETA_ENV_URL += "/v2"
            self.AUTH_BETA_ENV_URL += "/v2"
            ConnectSpotWebsocket = ConnectSpotWebsocketV2
        else:
            raise ValueError("Websocket API version must be one of ``v1``, ``v2``")

        self._pub_conn = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.PROD_ENV_URL if not beta else self.BETA_ENV_URL,
                is_auth=False,
                callback=self.on_message,
            )
            if not no_public
            else None
        )

        self._priv_conn = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.AUTH_PROD_ENV_URL if not beta else self.AUTH_BETA_ENV_URL,
                is_auth=True,
                callback=self.on_message,
            )
            if self._is_auth
            else None
        )

    async def on_message(
        self: KrakenSpotWSClientBase, message: Union[dict, list]
    ) -> None:
        """
        Calls the defined callback function (if defined) or overload this
        function.

        Can be overloaded as described in :class:`kraken.spot.KrakenSpotWSClient`
        and :class:`kraken.spot.KrakenSpotWSClientV2`.

        :param message: The message received sent by Kraken via the websocket connection
        :type message: dict | list
        """
        if self.__callback is not None:
            await self.__callback(message)
        else:
            self.LOG.warning(
                """
                Received message but no callback is defined! Either use a
                callback when initializing the websocket client or overload
                its ``on_message`` function.
            """
            )
            print(message)

    async def __aenter__(self: KrakenSpotWSClientBase) -> KrakenSpotWSClientBase:
        """Entrypoint for use as context manager"""
        return self

    async def __aexit__(
        self: KrakenSpotWSClientBase, *exc: tuple, **kwargs: dict
    ) -> None:
        """Exit if used as context manager"""

    def get_ws_token(self: KrakenSpotWSClientBase) -> dict:
        """
        Get the authentication token to establish the authenticated
        websocket connection.

        - https://docs.kraken.com/rest/#tag/Websockets-Authentication

        :returns: The authentication token
        :rtype: dict
        """
        return self._request(  # type: ignore[return-value]
            "POST", "/private/GetWebSocketsToken"
        )

    def _get_socket(self: KrakenSpotWSClientBase, private: bool) -> Any:
        """
        Returns the socket or ``None`` if not connected.

        :param private: Return the socket of the public or private connection
        :type private: bool
        :return: The socket
        :rtype: Any
        """
        if private:
            return self._priv_conn.socket
        if self._pub_conn is not None:
            return self._pub_conn.socket
        raise AttributeError("Could not found any connected websocket!")

    @property
    def active_public_subscriptions(
        self: KrakenSpotWSClientBase,
    ) -> Union[List[dict], Any]:
        """
        Returns the active public subscriptions

        :return: List of active public subscriptions
        :rtype: list[dict] | Any
        :raises ConnectionError: If there is no active public connection.
        """
        if self._pub_conn is not None:
            return self._pub_conn._subscriptions
        raise ConnectionError("Public connection does not exist!")

    @property
    def active_private_subscriptions(
        self: KrakenSpotWSClientBase,
    ) -> Union[List[dict], Any]:
        """
        Returns the active private subscriptions

        :return: List of active private subscriptions
        :rtype: list[dict] | Any
        :raises ConnectionError: If there is no active private connection
        """
        if self._priv_conn is not None:
            return self._priv_conn._subscriptions
        raise ConnectionError("Private connection does not exist!")

    # --------------------------------------------------------------------------
    # Functions and attributes to overload

    async def send_message(
        self: KrakenSpotWSClientBase, *args: Any, **kwargs: Any
    ) -> None:
        """
        This functions must be overloaded and should be used to send messages
        via the websocket connection(s).
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable

    async def subscribe(
        self: KrakenSpotWSClientBase, *args: Any, **kwargs: Any
    ) -> None:
        """
        This function must be overloaded and should be used to subscribe
        to websocket channels/feeds.
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable

    async def unsubscribe(
        self: KrakenSpotWSClientBase, *args: Any, **kwargs: Any
    ) -> None:
        """
        This function must be overloaded and should be used to unsubscribe
        from websocket channels/feeds.
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable

    @property
    def public_channel_names(self: KrakenSpotWSClientBase) -> List[str]:
        """
        This function must be overloaded and return a list of names that can be
        subscribed to (for unauthenticated connections).
        """
        raise NotImplementedError("Must be overloaded!")  # codecov: disable

    @property
    def private_channel_names(self: KrakenSpotWSClientBase) -> List[str]:
        """
        This function must be overloaded and return a list of names that can be
        subscribed to (for authenticated connections).
        """
        raise NotImplementedError("Must be overloaded!")  # codecov: disable


__all__ = ["KrakenSpotWSClientBase"]
