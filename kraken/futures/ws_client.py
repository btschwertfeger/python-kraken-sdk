#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Provides the websocket client for Kraken Futures"""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
from copy import deepcopy
from typing import TYPE_CHECKING, Any, TypeVar

from kraken.base_api import FuturesClient
from kraken.exceptions import KrakenAuthenticationError
from kraken.futures.websocket import ConnectFuturesWebsocket

if TYPE_CHECKING:
    from collections.abc import Callable

Self = TypeVar("Self")


class FuturesWSClient(FuturesClient):
    """
    Class to access public and (optional)
    private/authenticated websocket connection.

    So far there are no trade endpoints that can be accessed using the Futures
    Kraken API. If this has changed and is not implemented yet, please open an
    issue at https://github.com/btschwertfeger/python-kraken-sdk/issues

    - https://docs.futures.kraken.com/#websocket-api

    :param key: The Kraken Futures API key to access private endpoints
    :type key: str, optional
    :param secret: The Kraken Futures Secret key to access private endpoints
    :type secret: str, optional
    :param url: Set a custom URL (default: ``futures.kraken.com/ws/v1``)
    :type url: str, optional
    :param sandbox: Use the Kraken Futures demo environment (URL will switch to
        ``demo-futures.kraken.com/ws/v1``, default: ``False``)
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Futures Websocket: Create the websocket client

        import asyncio
        from kraken.futures import FuturesWSClient

        async def main() -> None:

            # Create the custom client
            class Client(FuturesWSClient):
                async def on_message(self, event: dict) -> None:
                    print(event)

            client = Client()     # unauthenticated
            auth_client = Client( # authenticated
                key="api-key",
                secret="secret-key"
            )

            # now you can subscribe to channels using
            await client.subscribe(
                feed='ticker',
                products=["XBTUSD", "DOT/EUR"]
            )
            # the messages can be used within the `on_message` callback method

            while True:
                await asyncio.sleep(6)

        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass

    .. code-block:: python
        :linenos:
        :caption: Futures Websocket: Create the websocket client as context manager

        import asyncio
        from kraken.futures import FuturesWSClient

        async def on_message(message):
            print(message)

        async def main() -> None:
            async with FuturesWSClient(callback=on_message) as session:
                await session.subscribe(feed="ticker", products=["PF_XBTUSD"])

            while True:
                await asyncio.sleep(6)

        if __name__ == "__main__":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass
            finally:
                loop.close()
    """

    PROD_ENV_URL: str = "futures.kraken.com/ws/v1"
    DEMO_ENV_URL: str = "demo-futures.kraken.com/ws/v1"

    def __init__(
        self: FuturesWSClient,
        key: str = "",
        secret: str = "",
        url: str = "",
        callback: Callable | None = None,
        *,
        sandbox: bool = False,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

        self.__key: str = key
        self.__secret: str = secret

        self.exception_occur: bool = False
        self.__callback: Any = callback
        self._conn: ConnectFuturesWebsocket = ConnectFuturesWebsocket(
            client=self,
            endpoint=(
                url if url else self.DEMO_ENV_URL if sandbox else self.PROD_ENV_URL
            ),
            callback=self.on_message,
        )

    @property
    def key(self: FuturesClient) -> str:
        """Returns the API key"""
        return self._key

    def get_sign_challenge(self: FuturesWSClient, challenge: str) -> str:
        """
        Sign the challenge/message using the secret key

        :param challenge: The challenge/message to sign
        :type challenge: str
        :return: The signed message
        :raises kraken.exceptions.KrakenAuthenticationError: If the credentials
            are not valid
        :rtype: str
        """
        if not self.is_auth:
            raise KrakenAuthenticationError

        sha256_hash = hashlib.sha256()
        sha256_hash.update(challenge.encode("utf-8"))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self.__secret),
                sha256_hash.digest(),
                hashlib.sha512,
            ).digest(),
        ).decode("utf-8")

    async def on_message(self: FuturesWSClient, message: dict) -> None:
        """
        Method that serves as the default callback function Calls the defined
        callback function (if defined) or overload this function.

        This is the default method  which just logs the messages. In production
        you want to overload this with your custom methods, as shown in the
        Example of :class:`kraken.futures.FuturesWSClient`.

        :param message: The message that was send by Kraken via the websocket
            connection.
        :type message: dict
        :rtype: None
        """
        if self.__callback is not None:
            await self.__callback(message)
        else:
            logging.warning("Received event but no callback is defined")
            logging.info(message)

    async def subscribe(
        self: FuturesWSClient,
        feed: str,
        products: list[str] | None = None,
    ) -> None:
        """
        Subscribe to a Futures websocket channel/feed. For some feeds
        authentication is required.

        - https://docs.futures.kraken.com/#websocket-api-websocket-api-introduction-subscriptions

        :param feed: The websocket feed/channel to subscribe to
        :type feed: str
        :param products: The products/futures contracts to subscribe to
        :type products: list[str], optional
        :raises TypeError: If the parameters don't match the requirements set by
            the Kraken API

        Initialize your client as described in
        :class:`kraken.futures.FuturesWSClient` to run the following
        example:

        .. code-block:: python
            :linenos:
            :caption: Futures Websocket: Subscribe to a feed

            >>> await bot.subscribe(feed='ticker', products=["XBTUSD", "DOT/EUR"])

        Success or failures are sent over the websocket connection and can be
        received via the default
        :func:`kraken.futures.FuturesWSClient.on_message` or a custom
        callback function.
        """

        message: dict = {"event": "subscribe", "feed": feed}

        if products is not None:
            if not isinstance(products, list):
                raise TypeError(
                    "Parameter products must be type of list[str] "
                    '(e.g. products=["PI_XBTUSD"])',
                )
            message["product_ids"] = products

        if feed in self.get_available_private_subscription_feeds():
            if products is not None:
                raise ValueError("There is no private feed that accepts products!")
            await self._conn.send_message(message, private=True)
        elif feed in self.get_available_public_subscription_feeds():
            if products is not None:
                for product in products:
                    sub = deepcopy(message)
                    sub["product_ids"] = [product]
                    await self._conn.send_message(sub, private=False)
            else:
                await self._conn.send_message(message, private=False)
        else:
            raise ValueError(f"Feed: {feed} not found. Not subscribing to it.")

    async def unsubscribe(
        self: FuturesWSClient,
        feed: str,
        products: list[str] | None = None,
    ) -> None:
        """
        Subscribe to a Futures websocket channel/feed. For some feeds
        authentication is required.

        - https://docs.futures.kraken.com/#websocket-api-websocket-api-introduction-subscriptions

        :param feed: The websocket feed/channel to unsubscribe from
        :type feed: str
        :param products: The products/futures contracts to unsubscribe from
        :type products: list[str], optional
        :raises TypeError: If the parameters don't match the requirements set
            by the Kraken API

        Initialize your client as described in
        :class:`kraken.futures.FuturesWSClient` to run the following
        example:

        .. code-block:: python
            :linenos:
            :caption: Futures Websocket: Unsubscribe from a feed

            >>> await bot.unsubscribe(feed='ticker', products=["XBTUSD", "DOT/EUR"])

        Success or failures are sent over the websocket connection and can be
        received via the default
        :func:`kraken.futures.FuturesWSClient.on_message`` or a custom
        callback function.
        """

        message: dict = {"event": "unsubscribe", "feed": feed}

        if products is not None:
            if not isinstance(products, list):
                raise TypeError(
                    'Parameter products must be type of list[str]\
                    (e.g. products=["PI_XBTUSD"])',
                )
            message["product_ids"] = products

        if feed in self.get_available_private_subscription_feeds():
            if products is not None:
                raise ValueError("There is no private feed that accepts products!")
            await self._conn.send_message(message, private=True)
        elif feed in self.get_available_public_subscription_feeds():
            if products is not None:
                for product in products:
                    sub = deepcopy(message)
                    sub["product_ids"] = [product]
                    await self._conn.send_message(sub, private=False)
            else:
                await self._conn.send_message(message, private=False)
        else:
            raise ValueError(f"Feed: {feed} not found. Not unsubscribing it.")

    @staticmethod
    def get_available_public_subscription_feeds() -> list[str]:
        """
        Return all available public feeds that can be un-/subscribed using the
        Kraken Futures API.

        :return: List of available public feeds
        :rtype: list[str]

        .. code-block:: python
            :linenos:
            :caption: Futures Websocket: Get the available public subscription feeds

            >>> from kraken.futures import FuturesWSClient
            >>> FuturesWSClient.get_available_private_subscription_feeds()
            [
                "trade", "book", "ticker",
                "ticker_lite", "heartbeat"
            ]
        """
        return ["trade", "book", "ticker", "ticker_lite", "heartbeat"]

    @staticmethod
    def get_available_private_subscription_feeds() -> list[str]:
        """
        Return all available private feeds that can be un-/subscribed to/from
        using the Kraken Futures API

        :return: List of available private feeds
        :rtype: list[str]

        .. code-block:: python
            :linenos:
            :caption: Futures Websocket: Get the available private subscription feeds

            >>> from kraken.futures import FuturesWSClient
            >>> FuturesWSClient.get_available_private_subscription_feeds()
            [
                "fills", "open_positions", "open_orders",
                "open_orders_verbose", "balances",
                "deposits_withdrawals", "account_balances_and_margins",
                "account_log", "notifications_auth"
            ]
        """
        return [
            "fills",
            "open_positions",
            "open_orders",
            "open_orders_verbose",
            "balances",
            "deposits_withdrawals",
            "account_balances_and_margins",
            "account_log",
            "notifications_auth",
        ]

    @property
    def is_auth(self: FuturesWSClient) -> bool:
        """
        Checks if key and secret are set.

        :return: ``True`` if the credentials are set, else ``False``
        :rtype: bool

        .. code-block:: python
            :linenos:
            :caption: Futures Websocket: Check if the credentials are set

            >>> from kraken.futures import FuturesWSClient
            >>> FuturesWSClient().is_auth()
            False
        """
        return bool(self.__key and self.__secret)

    def get_active_subscriptions(self: FuturesWSClient) -> list[dict]:
        """
        Returns the list of active subscriptions.

        :return: List of active subscriptions including the feed names, products
            and additional information.
        :rtype: list[dict]

        Initialize your client as described in :class:`kraken.futures.FuturesWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Futures Websocket: Get the active subscriptions

            >>> from kraken.futures import FuturesWSClient
            ...
            >>> FuturesWSClient.get_active_subscriptions()
            [
                {
                    "event": "subscribe",
                    "feed": "ticker,
                    "product_ids": ["PI_XBTUSD"]
                }, {
                    "event": "subscribe",
                    "feed": "open_orders,
                }, ...
            ]
        """
        return self._conn.get_active_subscriptions()

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(
        self: FuturesWSClient,
        *exc: object,
        **kwargs: dict[str, Any],
    ) -> None:
        pass


__all__ = ["FuturesWSClient"]
