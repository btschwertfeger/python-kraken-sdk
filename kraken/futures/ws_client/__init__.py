#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Provides the KrakenWsClientCl class to use the Kraken Futures websockets."""

import base64
import hashlib
import hmac
import logging
from copy import deepcopy
from typing import Coroutine, List, Union

from kraken.base_api import KrakenBaseFuturesAPI
from kraken.exceptions import KrakenException
from kraken.futures.websocket import ConnectFuturesWebsocket


class KrakenFuturesWSClient(KrakenBaseFuturesAPI):
    """

    Class to access public and (optional)
    private/authenticated websocket connection.

    So far there are no trade endpoints that can be accessed using the
    Futures Kraken API. If this has changed and not implemented yet,
    please open an issue: https://github.com/btschwertfeger/python-kraken-sdk/issues

    - https://docs.futures.kraken.com/#websocket-api

    :param key: Optional - The Kraken Futures API key to access private endpoints
    :type key: str
    :param secret: Optional - The Kraken Futures Secret key to access private endpoints
    :type secret: str
    :param url: Optional - Set a custum URL (default: ``futures.kraken.com/ws/v1``)
    :type url: str
    :param callback: Optional - The callback method that receives the websocket messages
    :type callback: function
    :param sanbox: Optional - Use the Kraken Futures demo environment (url will switch to ``demo-futures.kraken.com/ws/v1``, default: ``False``)
    :type sandbox: bool

    .. code-block:: python
        :linenos:
        :caption: Example

        >>> import asyncio
        >>> from kraken.futures import KrakenFuturesWSClient
        ...
        >>> async def main() -> None:
        ...
        ...     # Create a custom bot
        ...     class Bot(KrakenFuturesWSClient):
        ...         async def on_message(self, event) -> None:
        ...         print(event)
        ...
        ...     bot = Bot()     # unauthenticated
        ...     auth_bot = Bot( # authenticated
        ...         key="api-key",
        ...         secret="secret-key"
        ...     )
        ...
        ...     # now you can subsribe to channels using
        ...     await bot.subscribe(
        ...         feed='ticker',
        ...         products=["XBTUSD", "DOT/EUR"]
        ...     )
        ...
        ...     while True:
        ...         await asyncio.sleep(6)
        ...
        ... if __name__ == "__main__":
        ...     loop = asyncio.new_event_loop()
        ...     asyncio.set_event_loop(loop)
        ...     try:
        ...         asyncio.run(main())
        ...     except KeyboardInterrupt:
        ...         loop.close()
    """

    PROD_ENV_URL = "futures.kraken.com/ws/v1"
    DEMO_ENV_URL = "demo-futures.kraken.com/ws/v1"

    def __init__(
        self,
        key: str = "",
        secret: str = "",
        url: str = "",
        callback=None,
        sandbox: bool = False,
    ):
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

        self._key = key
        self._secret = secret

        self.exception_occur = False
        self.__callback = callback
        self._conn = ConnectFuturesWebsocket(
            client=self,
            endpoint=url
            if url != ""
            else self.DEMO_ENV_URL
            if sandbox
            else self.PROD_ENV_URL,
            callback=self.on_message,
        )

    def _get_sign_challenge(self, challenge: str) -> str:
        """
        Sign the challenge/message using the secret key

        :param challenge: The challenge/message to sign
        :type challenge: str
        :return: The signed message
        :raises kraken.exceptions.KrakenAuthenticationError: If the credentials are not valid
        :rtype: str
        """
        if not self.is_auth:
            raise KrakenException.KrakenAuthenticationError()

        sha256_hash = hashlib.sha256()
        sha256_hash.update(challenge.encode("utf-8"))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self._secret), sha256_hash.digest(), hashlib.sha512
            ).digest()
        ).decode("utf-8")

    async def on_message(self, msg: dict) -> Coroutine:
        """
        Method that serves as the default callback function Calls the defined callback function (if defined)
        or overload this function.

        This is the default method  which just logs the messages. In production you want to overload this
        with your custom methods, as shown in the Example of :class:`kraken.futures.FuturesWebsocketClient`.

        :param msg: The message that was send by Kraken via the websocket connection.
        :type msg: dict
        :return:
        :rtype:
        """
        if self.__callback is not None:
            await self.__callback(msg)
        else:
            logging.warning("Received event but no callback is defined")
            logging.info(msg)

    async def subscribe(
        self, feed: str, products: Union[List[str], None] = None
    ) -> Coroutine:
        """
        Subscribe to a Futures websocket channel/feed. For some feeds authentication is requried.

        - https://docs.futures.kraken.com/#websocket-api-websocket-api-introduction-subscriptions

        :param feed: The websocket feed/channel to subscribe to
        :type feed: str
        :param products: Optional - The products/futures contracts to subscribe to
        :type products: List[str] | None
        :raises ValueError: If the parameters dont match the requirements set by the Kraken API

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> # ... initialize the bot as described in kraken.futures.FuturesWebsocketClient class
            >>> await bot.subscribe(feed='ticker', products=["XBTUSD", "DOT/EUR"])

        Success or failures are sent over the websocket connection and can be
        received via the default :func:`kraken.futures.FuturesWebsocketClient.on_message`
        or a custom callback function.
        """

        message = {"event": "subscribe", "feed": feed}

        if products is not None:
            if not isinstance(products, list):
                raise ValueError(
                    'Parameter products must be type of List[str] (e.g. products=["PI_XBTUSD"])'
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
        self, feed: str, products: Union[List[str], None] = None
    ) -> Coroutine:
        """
        Subscribe to a Futures websocket channel/feed. For some feeds authentication is requried.

        - https://docs.futures.kraken.com/#websocket-api-websocket-api-introduction-subscriptions

        :param feed: The websocket feed/channel to unsubscribe from
        :type feed: str
        :param products: Optional - The products/futures contracts to unsubscribe from
        :type products: List[str] | None
        :raises ValueError: If the parameters dont match the requirements set by the Kraken API


        .. code-block:: python
            :linenos:
            :caption: Example

            >>> # ... initialize the bot as described in kraken.futures.FuturesWebsocketClient class
            >>> await  bot.unsubscribe(feed='ticker', products=["XBTUSD", "DOT/EUR"])

        Success or failures are sent over the websocket connection and can be
        received via the defailt :func:`kraken.futures.FuturesWebsocketClient.on_message``
        or a custom callback function.
        """

        message = {"event": "unsubscribe", "feed": feed}

        if products is not None:
            if not isinstance(products, list):
                raise ValueError(
                    'Parameter products must be type of List[str]\
                    (e.g. products=["PI_XBTUSD"])'
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
    def get_available_public_subscription_feeds() -> List[str]:
        """
        Return all available public feeds that can be un-/subscribed using the Kraken Futures API.

        :return: List of available public feeds
        :rtype: List[str]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import KrakenFuturesWSClient
            >>> KrakenFuturesWSClient.get_available_private_subscription_feeds()
            ["trade", "book", "ticker", "ticker_lite", "heartbeat"]
        """
        return ["trade", "book", "ticker", "ticker_lite", "heartbeat"]

    @staticmethod
    def get_available_private_subscription_feeds() -> List[str]:
        """
        Return all available private feeds that can be un-/subscribed to/from using the
        Kraken Futures API

        :return: List of available private feeds
        :rtype: List[str]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import KrakenFuturesWSClient
            >>> KrakenFuturesWSClient.get_available_private_subscription_feeds()
            ["fills", "open_positions", "open_orders", "open_orders_verbose", "balances", "deposits_withdrawals", "account_balances_and_margins", "account_log", "notifications_auth"]
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
    def is_auth(self) -> bool:
        """
        Checks if key and secret are set.

        :return: ``True`` if the credentials are set, else ``False``
        :rtype: bool

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import KrakenFuturesWSClient
            >>> KrakenFuturesWSClient().is_auth()
            False
        """
        return (
            self._key is not None
            and self._key != ""
            and self._secret is not None
            and self._secret != ""
        )

    def get_active_subscriptions(self) -> List[dict]:
        """
        Returns the list of acitve subscriptions.

        :return: List of active subscriptions including the feed names, products and additional information.
        :rtype: List[dict]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import KrakenFuturesWSClient
            ...
            >>> # ... initialize the bot and subscribe to ...
            ...
            >>> KrakenFuturesWSClient.get_active_subscriptions()
            [{"event": "subscribe", "feed": "ticker, "product_ids": ["PI_XBTUSD"]}]
        """
        return self._conn._get_active_subscriptions()
