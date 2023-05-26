#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""This module provides the Spot websocket client. """

from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any, Callable, List, Optional, Union

from ..base_api import KrakenBaseSpotAPI, defined, ensure_string
from .websocket import ConnectSpotWebsocket


class SpotWsClientCl(KrakenBaseSpotAPI):
    """
    Class that implements the Spot Kraken Websocket client.

    This class should not be used, since it only provides
    functions to the :class:`kraken.spot.KrakenSpotWSClient`.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: url to access the Kraken API (default: "https://api.kraken.com")
    :type url: str, optional
    :param sandbox: Use the sandbox (not supported for Spot trading so far, default: ``False``)
    :type sandbox: bool, optional

    This is just the class in which the Spot websocket methods are defined. It is derived
    in :func:`kraken.spot.KrakenSpotWSClient`.
    """

    def __init__(
        self: "SpotWsClientCl",
        key: str = "",
        secret: str = "",
        url: str = "",
        sandbox: bool = False,
    ):
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

        self._pub_conn: Optional[ConnectSpotWebsocket] = None
        self._priv_conn: Optional[ConnectSpotWebsocket] = None

    def get_ws_token(self: "SpotWsClientCl") -> dict:
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

    @ensure_string("oflags")
    async def create_order(
        self: "SpotWsClientCl",
        ordertype: str,
        side: str,
        pair: str,
        volume: Union[str, int, float],
        price: Optional[Union[str, int, float]] = None,
        price2: Optional[Union[str, int, float]] = None,
        leverage: Optional[Union[str, int, float]] = None,
        oflags: Optional[Union[str, List[str]]] = None,
        starttm: Optional[Union[str, int]] = None,
        expiretm: Optional[Union[str, int]] = None,
        deadline: Optional[str] = None,
        userref: Optional[Union[str, int]] = None,
        validate: bool = False,
        close_ordertype: Optional[str] = None,
        close_price: Optional[Union[str, int, float]] = None,
        close_price2: Optional[Union[str, int, float]] = None,
        timeinforce: Optional[Union[str, int]] = None,
    ) -> None:
        """
        Create an order and submit it.

        Requires the ``Access WebSockets API`` and ``Create and modify orders`` API key permissions.

        - https://docs.kraken.com/websockets/#message-addOrder

        :param ordertype: The type of order, one of: ``limit``, ``market`` ``stop-loss``,
            ``take-profit``, ``stop-loss-limit``, ``settle-position``, ``take-profit-limit``
            (see: https://support.kraken.com/hc/en-us/sections/200577136-Order-types)
        :type ordertype: str
        :param side: The side - one of ``buy``, ``sell``
        :type side: str
        :param pair: The asset pair to trade
        :type pair: str
        :param volume: The volume of the order that is being created
        :type volume: str | int | float
        :param price: The limit price for ``limit`` orders or the trigger price for orders with
            ``ordertype`` one of ``stop-loss``, ``stop-loss-limit``, ``take-profit``, and ``take-profit-limit``
        :type price: str | int | float, optional
        :param price2: The second price for ``stop-loss-limit`` and ``take-profit-limit``
            orders (see the referenced Kraken documentation for more information)
        :type price2: str | int | float, optional
        :param leverage: The leverage
        :type leverage: str | int | float, optional
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``, ``viqc``
            (see the referenced Kraken documentation for more information)
        :type oflags: str | List[str], optional
        :param starttm: Unix timestamp or seconds defining the start time (default: ``"0"``)
        :type starttm: str | int, optional
        :param expiretim: Unix timestamp or time in seconds defining the expiration of
            the order (default: ``"0"`` - i.e., no expiration)
        :type expiretim: str
        :param deadline: RFC3339 timestamp + {0..60} seconds that defines when the matching
            engine should reject the order.
        :type deadline: str
        :param userref: User reference id for example to group orders
        :type userref: int
        :param validate: Validate the order without placing on the market (default: ``False``)
        :type validate: bool, optional
        :param close_ordertype:  Conditional close order type, one of: ``limit``, ``stop-loss``,
            ``take-profit``, ``stop-loss-limit``, ``take-profit-limit``
        :type close_ordertype: str, optional
        :param close_price: Conditional close price
        :type close_price: str | int | float, optional
        :param close_price2: Second conditional close price
        :type close_price2: str | int | float, optional
        :param timeinforce: How long the order remains in the orderbook, one of: ``GTC``, ``IOC``,
            ``GTD`` (see the referenced Kraken documentation for more information)
        :type timeinforce: str, optional
        :raises ValueError: If input is not correct
        :rtype: None

        Initialize your client as described in :class:`kraken.spot.KrakenSpotWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Create an order

            >>> await auth_bot.create_order(
            ...     ordertype="market",
            ...     pair="XBTUSD",
            ...     side="buy",
            ...     volume=0.001
            ... )
            >>> await auth_bot.create_order(
            ...     ordertype="limit",
            ...     side="buy",
            ...     pair="XBTUSD",
            ...     volume=0.02,
            ...     price=23000,
            ...     expiretm=120,
            ...     oflags=["post", "fcib"]
            ... )

        """
        if not self._priv_conn:
            logging.warning("Websocket not connected!")
            return
        if not self._priv_conn.is_auth:
            raise ValueError("Cannot create_order on public websocket client!")

        payload: dict = {
            "event": "addOrder",
            "ordertype": str(ordertype),
            "type": str(side),
            "pair": str(pair),
            "price": str(price),
            "volume": str(volume),
            "validate": str(validate),
        }
        if defined(price2):
            payload["price2"] = str(price2)
        if defined(oflags):
            if isinstance(oflags, str):
                payload["oflags"] = oflags
            else:
                raise ValueError(
                    "oflags must be a comma delimited list of order flags as str. Available flags: viqc, fcib, fciq, nompp, post"
                )
        if defined(starttm):
            payload["starttm"] = str(starttm)
        if defined(expiretm):
            payload["expiretm"] = str(expiretm)
        if defined(deadline):
            payload["deadline"] = str(deadline)
        if defined(userref):
            payload["userref"] = str(userref)
        if defined(leverage):
            payload["leverage"] = str(leverage)
        if defined(close_ordertype):
            payload["close[ordertype]"] = close_ordertype
        if defined(close_price):
            payload["close[price]"] = str(close_price)
        if defined(close_price2):
            payload["close[price2]"] = str(close_price2)
        if defined(timeinforce):
            payload["timeinforce"] = timeinforce

        await self._priv_conn.send_message(msg=payload, private=True)

    @ensure_string("oflags")
    async def edit_order(
        self: "SpotWsClientCl",
        orderid: str,
        reqid: Optional[Union[str, int]] = None,
        pair: Optional[str] = None,
        price: Optional[Union[str, int, float]] = None,
        price2: Optional[Union[str, int, float]] = None,
        volume: Optional[Union[str, int, float]] = None,
        oflags: Optional[Union[str, List[str]]] = None,
        newuserref: Optional[Union[str, int]] = None,
        validate: bool = False,
    ) -> None:
        """
        Edit an open order that was placed on the Spot market.

        Requires the ``Access WebSockets API`` and ``Create and modify orders`` API key permissions.

        - https://docs.kraken.com/websockets/#message-editOrder

        :param orderId: The orderId of the order to edit
        :type orderId: str
        :param reqid: Filter by reqid
        :type reqid: str | int, optional
        :param pair: Filter by pair
        :type pair: str, optional
        :param price: Set a new price
        :type price: str | int | float, optional
        :param price2: Set a new second price
        :type price2: str | int | float, optional
        :param volume: Set a new volume
        :type volume: str | int | float, optional
        :param oflags: Set new oflags (overwrite old ones)
        :type oflags: str | List[str], optional
        :param newuserref: Set a new user reference id
        :type newuserref: str | int, optional
        :param validate: Validate the input without applying the changes (default: ``False``)
        :type validate: bool, optional
        :raises ValueError: If input is not correct
        :rtype: None

        Initialize your client as described in :class:`kraken.spot.KrakenSpotWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Edit an order

            >>> await auth_bot.edit_order(
            ...     orderId="OBGFYP-XVQNL-P4GMWF",
            ...     volume=0.75,
            ...     pair="XBTUSD",
            ...     price=20000
            ... )
        """
        if not self._priv_conn:
            logging.warning("Websocket not connected!")
            return
        if not self._priv_conn.is_auth:
            raise ValueError("Cannot edit_order on public websocket client!")

        payload: dict = {
            "event": "editOrder",
            "orderid": orderid,
            "validate": str(validate),
        }
        if defined(reqid):
            payload["reqid"] = reqid
        if defined(pair):
            payload["pair"] = pair
        if defined(price):
            payload["price"] = str(price)
        if defined(price2):
            payload["price2"] = str(price2)
        if defined(volume):
            payload["volume"] = str(volume)
        if defined(oflags):
            payload["oflags"] = oflags
        if defined(newuserref):
            payload["newuserref"] = str(newuserref)

        await self._priv_conn.send_message(msg=payload, private=True)

    async def cancel_order(self: "SpotWsClientCl", txid: List[str]) -> None:
        """
        Cancel a specific order or a list of orders.

        Requires the ``Access WebSockets API`` and ``Cancel/close orders`` API key permissions.

        - https://docs.kraken.com/websockets/#message-cancelOrder

        :param txid: A single or multiple transaction ids as list
        :type txid: List[str]
        :raises ValueError: If the websocket is not connected or the connection is not authenticated
        :return: None

        Initialize your client as described in :class:`kraken.spot.KrakenSpotWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Cancel an order

            >>> await auth_bot.cancel_order(txid=["OBGFYP-XVQNL-P4GMWF"])
        """
        if not self._priv_conn:
            logging.warning("Websocket not connected!")
            return
        if not self._priv_conn.is_auth:
            raise ValueError("Cannot cancel_order on public websocket client!")
        await self._priv_conn.send_message(
            msg={"event": "cancelOrder", "txid": txid}, private=True
        )

    async def cancel_all_orders(self: "SpotWsClientCl") -> None:
        """
        Cancel all open Spot orders.

        Requires the ``Access WebSockets API`` and ``Cancel/close orders`` API key permissions.

        - https://docs.kraken.com/websockets/#message-cancelAll

        :raises ValueError: If the websocket is not connected or the connection is not authenticated
        :return: None

        Initialize your client as described in :class:`kraken.spot.KrakenSpotWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Cancel all Orders

            >>> await auth_bot.cancel_all_orders()
        """

        if not self._priv_conn:
            logging.warning("Websocket not connected!")
            return
        if not self._priv_conn.is_auth:
            raise ValueError("Cannot use cancel_all_orders on public websocket client!")
        await self._priv_conn.send_message(msg={"event": "cancelAll"}, private=True)

    async def cancel_all_orders_after(self: "SpotWsClientCl", timeout: int = 0) -> None:
        """
        Set a Death Man's Switch

        Requires the ``Access WebSockets API`` and ``Cancel/close orders`` API key permissions.

        - https://docs.kraken.com/websockets/#message-cancelAllOrdersAfter

        :param timeout: Set the timeout in seconds to cancel the orders after, set to ``0`` to reset.
        :type timeout: int
        :raises ValueError: If the websocket is not connected or the connection is not authenticated
        :return: None

        Initialize your client as described in :class:`kraken.spot.KrakenSpotWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Death Man's Switch

            >>> await auth_bot.cancel_all_orders_after(timeout=60)
        """
        if not self._priv_conn:
            logging.warning("Websocket not connected!")
            return
        if not self._priv_conn.is_auth:
            raise ValueError(
                "Cannot use cancel_all_orders_after on public websocket client!"
            )
        await self._priv_conn.send_message(
            msg={"event": "cancelAllOrdersAfter", "timeout": timeout}, private=True
        )


class KrakenSpotWSClient(SpotWsClientCl):
    """
    Class to access public and (optional)
    private/authenticated websocket connection.

    - https://docs.kraken.com/websockets/#overview

    This class holds up to two websocket connections, one private
    and one public.

    When accessing private endpoints that need authentication make sure,
    that the ``Access WebSockets API`` API key permission is set in the user's
    account.

    :param key: API Key for the Kraken Spot API (default: ``""``)
    :type key: str, optional
    :param secret: Secret API Key for the Kraken Spot API (default: ``""``)
    :type secret: str, optional
    :param url: Set a specific/custom url to access the Kraken API
    :type url: str, optional
    :param beta: Use the beta websocket channels (maybe not supported anymore, default: ``False``)
    :type beta: bool

    .. code-block:: python
        :linenos:
        :caption: HowTo: Create a Bot and integrate the python-kraken-sdk Spot Websocket Client

        import asyncio
        from kraken.spot import KrakenSpotWSClient

        async def main() -> None:
            class Bot(KrakenSpotWSClient):

                async def on_message(self, event: dict) -> None:
                    print(event)

            bot = Bot()         # unauthenticated
            auth_bot = Bot(     # authenticated
                key='kraken-api-key',
                secret='kraken-secret-key'
            )

            # subscribe to the desired feeds:
            await bot.subscribe(
                subscription={"name": ticker},
                pair=["XBTUSD", "DOT/EUR"]
            )
            # from now on the on_message function receives the ticker feed

            while True:
                await asyncio.sleep(6)

        if __name__ == '__main__':
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass

    .. code-block:: python
        :linenos:
        :caption: HowTo: Use the websocket client as context manager

        import asyncio
        from kraken.spot import KrakenSpotWSClient

        async def on_message(msg):
            print(msg)

        async def main() -> None:
            async with KrakenSpotWSClient(
                key="api-key",
                secret="secret-key",
                callback=on_message
            ) as session:
                await session.subscribe(
                    subscription={"name": "ticker"},
                    pair=["XBT/USD"]
                )

            while True:
                await asyncio.sleep(6)


        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    PROD_ENV_URL: str = "ws.kraken.com"
    AUTH_PROD_ENV_URL: str = "ws-auth.kraken.com"
    BETA_ENV_URL: str = "beta-ws.kraken.com"
    AUTH_BETA_ENV_URL: str = "beta-ws-auth.kraken.com"

    def __init__(
        self: "KrakenSpotWSClient",
        key: str = "",
        secret: str = "",
        url: str = "",
        callback: Optional[Callable] = None,
        beta: bool = False,
    ):
        super().__init__(key=key, secret=secret, url=url, sandbox=beta)
        self.__callback: Any = callback
        self.__is_auth: bool = bool(key and secret)
        self.exception_occur: bool = False
        self._pub_conn: ConnectSpotWebsocket = ConnectSpotWebsocket(
            client=self,
            endpoint=self.PROD_ENV_URL if not beta else self.BETA_ENV_URL,
            is_auth=False,
            callback=self.on_message,
        )

        self._priv_conn: Optional[ConnectSpotWebsocket] = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.AUTH_PROD_ENV_URL if not beta else self.AUTH_BETA_ENV_URL,
                is_auth=True,
                callback=self.on_message,
            )
            if self.__is_auth
            else None
        )

    async def on_message(self: "KrakenSpotWSClient", msg: dict) -> None:
        """
        Calls the defined callback function (if defined)
        or overload this function.

        Can be overloaded as described in :class:`kraken.spot.KrakenSpotWSClient`

        :param msg: The message received sent by Kraken via the websocket connection
        :type msg: dict
        """
        if self.__callback is not None:
            await self.__callback(msg)
        else:
            self.LOG.warning("Received event but no callback is defined.")
            print(msg)

    async def subscribe(
        self: "KrakenSpotWSClient", subscription: dict, pair: List[str] = None
    ) -> None:
        """
        Subscribe to a channel

        Success or failures are sent over the websocket connection and can be
        received via the on_message callback function.

        When accessing private endpoints and subscription feeds that need authentication
        make sure, that the ``Access WebSockets API`` API key permission is set
        in the users Kraken account.

        - https://docs.kraken.com/websockets-beta/#message-subscribe

        :param subscription: The subscription message
        :type subscription: dict
        :param pair: The pair to subscribe to
        :type pair: List[str] | None, optional

        Initialize your client as described in :class:`kraken.spot.KrakenSpotWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Subscribe to a websocket feed

            >>> await bot.subscribe(
            ...     subscription={"name": ticker},
            ...     pair=["XBTUSD", "DOT/EUR"]
            ... )
        """

        if "name" not in subscription:
            raise AttributeError('Subscription requires a "name" key."')
        private: bool = bool(subscription["name"] in self.private_sub_names)

        payload: dict = {"event": "subscribe", "subscription": subscription}
        if pair is not None:
            if not isinstance(pair, list):
                raise ValueError(
                    'Parameter pair must be type of List[str] (e.g. pair=["XBTUSD"])'
                )
            payload["pair"] = pair

        if private:  # private == without pair
            if not self.__is_auth:
                raise ValueError(
                    "Cannot subscribe to private feeds without valid credentials!"
                )
            if pair is not None:
                raise ValueError(
                    "Cannot subscribe to private endpoint with specific pair!"
                )
            await self._priv_conn.send_message(payload, private=True)

        elif pair is not None:  # public with pair
            for symbol in pair:
                sub = deepcopy(payload)
                sub["pair"] = [symbol]
                await self._pub_conn.send_message(sub, private=False)

        else:
            await self._pub_conn.send_message(payload, private=False)

    async def unsubscribe(
        self: "KrakenSpotWSClient", subscription: dict, pair: Optional[List[str]] = None
    ) -> None:
        """
        Unsubscribe from a topic

        Success or failures are sent over the websocket connection and can be
        received via the on_message callback function.

        When accessing private endpoints and subscription feeds that need authentication
        make sure, that the ``Access WebSockets API`` API key permission is set
        in the users Kraken account.

        - https://docs.kraken.com/websockets/#message-unsubscribe

        :param subscription: The subscription to unsubscribe from
        :type subscription: dict
        :param pair: The pair or list of pairs to unsubscribe
        :type pair: List[str], optional

        Initialize your client as described in :class:`kraken.spot.KrakenSpotWSClient` to
        run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Unsubscribe from a websocket feed

            >>> await bot.unsubscribe(
            ...     subscription={"name": ticker},
            ...     pair=["XBTUSD", "DOT/EUR"]
            ... )
        """
        if "name" not in subscription:
            raise AttributeError('Subscription requires a "name" key."')
        private: bool = bool(subscription["name"] in self.private_sub_names)

        payload: dict = {"event": "unsubscribe", "subscription": subscription}
        if pair is not None:
            if not isinstance(pair, list):
                raise ValueError(
                    'Parameter pair must be type of List[str] (e.g. pair=["XBTUSD"])'
                )
            payload["pair"] = pair

        if private:  # private == without pair
            if not self.__is_auth:
                raise ValueError(
                    "Cannot unsubscribe from private feeds without valid credentials!"
                )
            if pair is not None:
                raise ValueError(
                    "Cannot unsubscribe from private endpoint with specific pair!"
                )
            await self._priv_conn.send_message(payload, private=True)

        elif pair is not None:  # public with pair
            for symbol in pair:
                sub = deepcopy(payload)
                sub["pair"] = [symbol]
                await self._pub_conn.send_message(sub, private=False)

        else:
            await self._pub_conn.send_message(payload, private=False)

    @property
    def private_sub_names(self: "KrakenSpotWSClient") -> List[str]:
        """
        Returns the private subscription names

        :return: List of private subscription names (``ownTrades``, ``openOrders``)
        :rtype: List[str]
        """
        return ["ownTrades", "openOrders"]

    @property
    def public_sub_names(self: "KrakenSpotWSClient") -> List[str]:
        """
        Returns the public subscription names

        :return: List of public subscription names (``ticker``,
         ``spread``, ``book``, ``ohlc``, ``trade``, ``*``)
        :rtype: List[str]
        """
        return ["ticker", "spread", "book", "ohlc", "trade", "*"]

    @property
    def active_public_subscriptions(
        self: "KrakenSpotWSClient",
    ) -> Union[List[dict], Any]:
        """
        Returns the active public subscriptions

        :return: List of active public subscriptions
        :rtype: Union[List[dict], Any]
        :raises ConnectionError: If there is no public connection.
        """
        if self._pub_conn is not None:
            return self._pub_conn.subscriptions
        raise ConnectionError("Public connection does not exist!")

    @property
    def active_private_subscriptions(
        self: "KrakenSpotWSClient",
    ) -> Union[List[dict], Any]:
        """
        Returns the active private subscriptions

        :return: List of active private subscriptions
        :rtype: Union[List[dict], Any]
        :raises ConnectionError: If there is no private connection
        """
        if self._priv_conn is not None:
            return self._priv_conn.subscriptions
        raise ConnectionError("Private connection does not exist!")

    async def __aenter__(self: "KrakenSpotWSClient") -> "KrakenSpotWSClient":
        return self

    async def __aexit__(self, *exc: tuple, **kwargs: dict) -> None:
        pass
