#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that provides the base class for the Kraken Websocket clients v2.
"""

from __future__ import annotations

import logging
from asyncio import sleep as async_sleep
from typing import TYPE_CHECKING, Any, TypeVar

from kraken.spot import SpotAsyncClient
from kraken.spot.websocket.connectors import ConnectSpotWebsocket

if TYPE_CHECKING:
    from collections.abc import Callable

Self = TypeVar("Self")


class SpotWSClientBase(SpotAsyncClient):
    """
    This is the base class for :class:`kraken.spot.SpotWSClient`. It extends
    the REST API base class and is used to provide the base functionalities that
    are used for Kraken Websocket API v2.

    **This is an internal class and should not be used outside.**

    :param key: API Key for the Kraken Spot API (default: ``""``)
    :type key: str, optional
    :param secret: Secret API Key for the Kraken Spot API (default: ``""``)
    :type secret: str, optional
    :param url: Set a specific URL to access the Kraken REST API
    :type url: str, optional
    :param no_public: Disables public connection (default: ``False``). If not
        set or set to ``False``, the client will create a public and a private
        connection per default. If only a private connection is required, this
        parameter should be set to ``True``.
    :param beta: Use the beta websocket channels (maybe not supported anymore,
        default: ``False``)
    :type beta: bool
    """

    LOG: logging.Logger = logging.getLogger(__name__)
    PROD_ENV_URL: str = "ws.kraken.com"
    AUTH_PROD_ENV_URL: str = "ws-auth.kraken.com"

    def __init__(  # nosec: B107
        self: SpotWSClientBase,
        key: str = "",
        secret: str = "",
        callback: Callable | None = None,
        *,
        no_public: bool = False,
    ) -> None:
        super().__init__(key=key, secret=secret)

        self._is_auth: bool = bool(key and secret)
        self.__callback: Callable | None = callback
        self._pub_conn: ConnectSpotWebsocket | None = None
        self._priv_conn: ConnectSpotWebsocket | None = None
        self.__prepare_connect(no_public=no_public)

    @property
    def exception_occur(self: SpotWSClientBase) -> bool:
        """Returns True if any connection was stopped due to an exception."""
        return (self._pub_conn is not None and self._pub_conn.exception_occur) or (
            self._priv_conn is not None and self._priv_conn.exception_occur
        )

    # --------------------------------------------------------------------------
    # Internals
    def __prepare_connect(
        self: SpotWSClientBase,
        *,
        no_public: bool,
    ) -> None:
        """Set up functions and attributes based on the API version."""

        # pylint: disable=invalid-name
        self.PROD_ENV_URL += "/v2"
        self.AUTH_PROD_ENV_URL += "/v2"

        self._pub_conn = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.PROD_ENV_URL,
                is_auth=False,
                callback=self.on_message,
            )
            if not no_public
            else None
        )

        self._priv_conn = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.AUTH_PROD_ENV_URL,
                is_auth=True,
                callback=self.on_message,
            )
            if self._is_auth
            else None
        )

    async def start(self: SpotWSClientBase) -> None:
        """Method to start the websocket connection."""
        if self._pub_conn:
            await self._pub_conn.start()
        if self._priv_conn:
            await self._priv_conn.start()

        # Wait for the connection(s) to be established ...
        while (timeout := 0.0) < 10:
            public_conntection_waiting = True
            if self._pub_conn:
                if self._pub_conn.socket is not None:
                    public_conntection_waiting = False
            else:
                public_conntection_waiting = False

            private_conection_waiting = True
            if self._priv_conn:
                if self._priv_conn.socket is not None:
                    private_conection_waiting = False
            else:
                private_conection_waiting = False

            if not public_conntection_waiting and not private_conection_waiting:
                break
            await async_sleep(0.2)
            timeout += 0.2
        else:
            raise TimeoutError("Could not connect to the Kraken API!")

    async def stop(self: SpotWSClientBase) -> None:
        """Method to stop the websocket connection."""
        if self._pub_conn:
            await self._pub_conn.stop()
        if self._priv_conn:
            await self._priv_conn.stop()

    async def on_message(
        self: SpotWSClientBase,
        message: dict | list,
    ) -> None:
        """
        Calls the defined callback function (if defined). In most cases you
        have to overwrite this function since it will receive all incoming
        messages that will be sent by Kraken.

        See :class:`kraken.spot.SpotWSClient` for examples to use this
        function.

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
            """,
            )
            print(message)  # noqa: T201

    async def __aenter__(self: Self) -> Self:
        """Entrypoint for use as context manager"""
        await super().__aenter__()
        await self.start()  # type: ignore[attr-defined]
        return self

    async def __aexit__(
        self: SpotWSClientBase,
        *exc: object,
        **kwargs: Any,
    ) -> None:
        """Exit if used as context manager"""
        await super().__aexit__()
        await self.stop()

    async def get_ws_token(self: SpotWSClientBase) -> dict:
        """
        Get the authentication token to establish the authenticated
        websocket connection. This is used internally and in most cases not
        needed outside.

        - https://docs.kraken.com/rest/#tag/Websockets-Authentication

        :returns: The authentication token
        :rtype: dict
        """
        return await self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/GetWebSocketsToken",
        )

    def _get_socket(
        self: SpotWSClientBase,
        *,
        private: bool,
    ) -> Any | None:  # noqa: ANN401
        """
        Returns the socket or ``None`` if not connected.

        :param private: Return the socket of the public or private connection
        :type private: bool
        :return: The socket
        """
        if private:
            return self._priv_conn.socket
        if self._pub_conn is not None:
            return self._pub_conn.socket
        raise AttributeError("Could not found any connected websocket!")

    @property
    def active_public_subscriptions(
        self: SpotWSClientBase,
    ) -> list[dict]:
        """
        Returns the active public subscriptions

        :return: List of active public subscriptions
        :rtype: list[dict]
        :raises ConnectionError: If there is no active public connection.
        """
        if self._pub_conn is not None:
            return self._pub_conn.subscriptions
        raise ConnectionError("Public connection does not exist!")

    @property
    def active_private_subscriptions(
        self: SpotWSClientBase,
    ) -> list[dict]:
        """
        Returns the active private subscriptions

        :return: List of active private subscriptions
        :rtype: list[dict]
        :raises ConnectionError: If there is no active private connection
        """
        if self._priv_conn is not None:
            return self._priv_conn.subscriptions
        raise ConnectionError("Private connection does not exist!")

    # --------------------------------------------------------------------------
    # Functions and attributes to overload

    async def send_message(
        self: SpotWSClientBase,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        This functions must be overloaded and should be used to send messages
        via the websocket connection(s).
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable

    async def subscribe(
        self: SpotWSClientBase,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        This function must be overloaded and should be used to subscribe
        to websocket channels/feeds.
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable

    async def unsubscribe(
        self: SpotWSClientBase,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        This function must be overloaded and should be used to unsubscribe
        from websocket channels/feeds.
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable

    @property
    def public_channel_names(self: SpotWSClientBase) -> list[str]:
        """
        This function must be overloaded and return a list of names that can be
        subscribed to (for unauthenticated connections).
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable

    @property
    def private_channel_names(self: SpotWSClientBase) -> list[str]:
        """
        This function must be overloaded and return a list of names that can be
        subscribed to (for authenticated connections).
        """
        raise NotImplementedError("Must be overloaded!")  # coverage: disable


__all__ = ["SpotWSClientBase"]
