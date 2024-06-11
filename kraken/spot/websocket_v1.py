#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
This module provides the Spot websocket client (Websocket API V1 as
documented in https://docs.kraken.com/websockets).
"""

from __future__ import annotations

import asyncio
import json
import warnings
from copy import deepcopy
from typing import TYPE_CHECKING, Any

from kraken.base_api import defined, ensure_string
from kraken.exceptions import KrakenAuthenticationError
from kraken.spot.trade import Trade
from kraken.spot.websocket import SpotWSClientBase

if TYPE_CHECKING:
    from collections.abc import Callable


class SpotWSClientV1(SpotWSClientBase):
    """
    .. deprecated:: v2.2.0

    Class to access public and private/authenticated websocket connections.

    **This client only supports the Kraken Websocket API v1.**

    - https://docs.kraken.com/websockets

    … please use :class:`SpotWSClientV2` for accessing the Kraken
    Websockets API v2.

    This class holds up to two websocket connections, one private and one
    public.

    When accessing private endpoints that need authentication make sure, that
    the ``Access WebSockets API`` API key permission is set in the user's
    account. To place or cancel orders, querying ledger information or accessing
    live portfolio changes (fills, new orders, ...) there are separate
    permissions that must be enabled if required.

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

    .. code-block:: python
        :linenos:
        :caption: HowTo: Use the Kraken Spot websocket client (v1)

        import asyncio
        from kraken.spot import SpotWSClientV1


        class Client(SpotWSClientV1):

            async def on_message(self, message):
                print(message)


        async def main():

            client = Client()         # unauthenticated
            client_auth = Client(     # authenticated
                key="kraken-api-key",
                secret="kraken-secret-key"
            )

            # subscribe to the desired feeds:
            await client.subscribe(
                subscription={"name": ticker},
                pair=["XBTUSD", "DOT/EUR"]
            )
            # from now on the on_message function receives the ticker feed

            while not client.exception_occur:
                await asyncio.sleep(6)

        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass

    .. code-block:: python
        :linenos:
        :caption: HowTo: Use the websocket client (v1) as instance

        import asyncio
        from kraken.spot import SpotWSClientV1


        async def main() -> None:
            async def on_message(message) -> None:
                print(message)

            client = SpotWSClientV1(callback=on_message)
            await client.subscribe(
                subscription={"name": "ticker"},
                pair=["XBT/USD"]
            )

            while not client.exception_occur:
                await asyncio.sleep(10)


        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass


    .. code-block:: python
        :linenos:
        :caption: HowTo: Use the websocket client (v1) as context manager

        import asyncio
        from kraken.spot import SpotWSClientV1

        async def on_message(message):
            print(message)

        async def main() -> None:
            async with SpotWSClientV1(
                key="api-key",
                secret="secret-key",
                callback=on_message
            ) as session:
                await session.subscribe(
                    subscription={"name": "ticker"},
                    pair=["XBT/USD"]
                )

            while True
                await asyncio.sleep(6)


        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass
    """

    def __init__(
        self: SpotWSClientV1,
        key: str = "",
        secret: str = "",
        callback: Callable | None = None,
        *,
        no_public: bool = False,
    ) -> None:
        warnings.warn(
            "The Kraken websocket API v1 is marked as deprecated and "
            "its support could be removed in the future. "
            "Please migrate to websocket API v2.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(
            key=key,
            secret=secret,
            callback=callback,
            no_public=no_public,
            api_version="v1",
        )

    async def send_message(  # pylint: disable=arguments-differ
        self: SpotWSClientV1,
        message: dict,
        *,
        private: bool = False,
        raw: bool = False,
    ) -> None:
        """
        Sends a message via the websocket connection. For private messages the
        authentication token will be assigned automatically if ``raw=False``.

        The user can specify a ``reqid`` within the message to identify
        corresponding responses via websocket feed.

        :param message: The content to send
        :type message: dict
        :param private: Use authentication (default: ``False``)
        :type private: bool, optional
        :param raw: If set to ``True`` the ``message`` will be sent directly.
        :type raw: bool, optional
        """

        if private and not self._is_auth:
            raise KrakenAuthenticationError

        socket: Any = self._get_socket(private=private)
        while not socket:
            socket = self._get_socket(private=private)
            await asyncio.sleep(0.4)

        if raw:
            await socket.send(json.dumps(message))
            return

        if private and "subscription" in message:
            message["subscription"]["token"] = self._priv_conn.ws_conn_details["token"]
        elif private:
            message["token"] = self._priv_conn.ws_conn_details["token"]
        await socket.send(json.dumps(message))

    async def subscribe(  # pylint: disable=arguments-differ
        self: SpotWSClientV1,
        subscription: dict,
        pair: list[str] | None = None,
    ) -> None:
        """
        Subscribe to a channel

        Success or failures are sent over the websocket connection and can be
        received via the on_message callback function.

        When accessing private endpoints and subscription feeds that need
        authentication make sure, that the ``Access WebSockets API`` API key
        permission is set in the users Kraken account.

        - https://docs.kraken.com/websockets/#message-subscribe

        :param subscription: The subscription message
        :type subscription: dict
        :param pair: The pair to subscribe to
        :type pair: list[str], optional

        Initialize your client as described in
        :class:`kraken.spot.SpotWSClientV1` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v1: Subscribe to a websocket feed

            >>> await client.subscribe(
            ...     subscription={"name": ticker},
            ...     pair=["XBTUSD", "DOT/EUR"]
            ... )
        """

        if "name" not in subscription:
            raise AttributeError('Subscription requires a "name" key."')
        private: bool = bool(subscription["name"] in self.private_channel_names)

        payload: dict = {"event": "subscribe", "subscription": subscription}
        if pair is not None:
            if not isinstance(pair, list):
                raise TypeError(
                    'Parameter pair must be type of list[str] (e.g. pair=["XBTUSD"])',
                )
            payload["pair"] = pair

        if private:  # private == without pair
            if not self._is_auth:
                raise KrakenAuthenticationError(
                    "Cannot subscribe to private feeds without valid credentials!",
                )
            if pair is not None:
                raise ValueError(
                    "Cannot subscribe to private endpoint with specific pair!",
                )
            await self.send_message(payload, private=True)

        elif pair is not None:  # public with pair
            for symbol in pair:
                sub = deepcopy(payload)
                sub["pair"] = [symbol]
                await self.send_message(sub, private=False)

        else:
            raise ValueError(
                "At least one pair must be specified when subscribing to public feeds.",
            )
            # Currently there is no possibility to public subscribe without a
            # pair (July 2023).
            # await self.send_message(payload, private=False)

    async def unsubscribe(  # pylint: disable=arguments-differ
        self: SpotWSClientV1,
        subscription: dict,
        pair: list[str] | None = None,
    ) -> None:
        """
        Unsubscribe from a feed

        Success or failures are sent via the websocket connection and can be
        received via the on_message or callback function.

        When accessing private endpoints and subscription feeds that need
        authentication make sure, that the ``Access WebSockets API`` API key
        permission is set in the users Kraken account.

        - https://docs.kraken.com/websockets/#message-unsubscribe

        :param subscription: The subscription to unsubscribe from
        :type subscription: dict
        :param pair: The pair or list of pairs to unsubscribe
        :type pair: list[str], optional

        Initialize your client as described in
        :class:`kraken.spot.SpotWSClientV1` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v1: Unsubscribe from a websocket feed

            >>> await client.unsubscribe(
            ...     subscription={"name": ticker},
            ...     pair=["XBTUSD", "DOT/EUR"]
            ... )
        """
        if "name" not in subscription:
            raise AttributeError('Subscription requires a "name" key.')
        private: bool = bool(subscription["name"] in self.private_channel_names)

        payload: dict = {"event": "unsubscribe", "subscription": subscription}
        if pair is not None:
            if not isinstance(pair, list):
                raise TypeError(
                    'Parameter pair must be type of list[str] (e.g. pair=["XBTUSD"])',
                )
            payload["pair"] = pair

        if private:  # private == without pair
            if not self._is_auth:
                raise KrakenAuthenticationError(
                    "Cannot unsubscribe from private feeds without valid credentials!",
                )
            if pair is not None:
                raise ValueError(
                    "Cannot unsubscribe from private endpoint with specific pair!",
                )
            await self.send_message(payload, private=True)

        elif pair is not None:  # public with pair
            for symbol in pair:
                sub = deepcopy(payload)
                sub["pair"] = [symbol]
                await self.send_message(sub, private=False)

        else:
            raise ValueError(
                "At least one pair must be specified when unsubscribing "
                "from public feeds.",
            )
            # Currently there is no possibility to public unsubscribe without a
            # pair (July 2023).
            # await self.send_message(payload, private=False)

    @property
    def public_channel_names(self: SpotWSClientV1) -> list[str]:
        """
        Returns the public subscription names

        :return: List of public subscription names (``ticker``,
            ``spread``, ``book``, ``ohlc``, ``trade``, ``*``)
        :rtype: list[str]
        """
        return ["ticker", "spread", "book", "ohlc", "trade", "*"]

    @property
    def private_channel_names(self: SpotWSClientV1) -> list[str]:
        """
        Returns the private subscription names

        :return: List of private subscription names (``ownTrades``,
            ``openOrders``)
        :rtype: list[str]
        """
        return ["ownTrades", "openOrders"]

    @ensure_string("oflags")
    async def create_order(  # pylint: disable=too-many-arguments # noqa: PLR0913, PLR0917
        self: SpotWSClientV1,
        ordertype: str,
        side: str,
        pair: str,
        volume: str | float,
        price: str | float | None = None,
        price2: str | float | None = None,
        leverage: str | float | None = None,
        oflags: str | list[str] | None = None,
        starttm: str | int | None = None,
        expiretm: str | int | None = None,
        deadline: str | None = None,
        userref: str | int | None = None,
        close_ordertype: str | None = None,
        close_price: str | float | None = None,
        close_price2: str | float | None = None,
        timeinforce: str | int | None = None,
        *,
        truncate: bool = False,
        validate: bool = False,
    ) -> None:
        """
        Create an order and submit it.

        Requires the ``Access WebSockets API`` and ``Create and modify orders``
        API key permissions.

        - https://docs.kraken.com/websockets/#message-addOrder

        :param ordertype: The type of order, one of: ``limit``, ``market``,
            ``stop-loss``, ``take-profit``, ``stop-loss-limit``,
            ``settle-position``, ``take-profit-limit`` (see:
            https://support.kraken.com/hc/en-us/sections/200577136-Order-types)
        :type ordertype: str
        :param side: The side - one of ``buy``, ``sell``
        :type side: str
        :param pair: The asset pair to trade
        :type pair: str
        :param volume: The volume of the order that is being created
        :type volume: str | float
        :param price: The limit price for ``limit`` orders or the trigger price
            for orders with ``ordertype`` one of ``stop-loss``,
            ``stop-loss-limit``, ``take-profit``, and ``take-profit-limit``
        :type price: str | float, optional
        :param price2: The second price for ``stop-loss-limit`` and
            ``take-profit-limit`` orders (see the referenced Kraken
            documentation for more information)
        :type price2: str | float, optional
        :param leverage: The leverage
        :type leverage: str | float, optional
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``,
            ``viqc`` (see the referenced Kraken documentation for more
            information)
        :type oflags: str | list[str], optional
        :param starttm: Unix timestamp or seconds defining the start time
            (default: ``"0"``)
        :type starttm: str | int, optional
        :param expiretim: Unix timestamp or time in seconds defining the
            expiration of the order (default: ``"0"`` - i.e., no expiration)
        :type expiretim: str
        :param deadline: RFC3339 timestamp + {0..60} seconds that defines when
            the matching engine should reject the order.
        :type deadline: str
        :param userref: User reference id for example to group orders
        :type userref: int
        :param close_ordertype:  Conditional close order type, one of:
            ``limit``, ``stop-loss``, ``take-profit``, ``stop-loss-limit``,
            ``take-profit-limit``
        :type close_ordertype: str, optional
        :param close_price: Conditional close price
        :type close_price: str | float, optional
        :param close_price2: Second conditional close price
        :type close_price2: str | float, optional
        :param timeinforce: How long the order remains in the orderbook, one of:
            ``GTC``, ``IOC``, ``GTD`` (see the referenced Kraken documentation
            for more information)
        :type timeinforce: str, optional
        :param truncate: If enabled: round the ``price`` and ``volume`` to
            Kraken's maximum allowed decimal places. See
            https://support.kraken.com/hc/en-us/articles/4521313131540 fore more
            information about decimals.
        :type truncate: bool, optional
        :param validate: Validate the order without placing on the market
            (default: ``False``)
        :type validate: bool, optional
        :raises KrakenAuthenticationError: If the websocket is not connected or
            the connection is not authenticated
        :raises ValueError: If input is not correct

        Initialize your client as described in
        :class:`kraken.spot.SpotWSClientV1` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Create an order

            >>> await client_auth.create_order(
            ...     ordertype="market",
            ...     pair="XBTUSD",
            ...     side="buy",
            ...     volume=0.001
            ... )
            >>> await client_auth.create_order(
            ...     ordertype="limit",
            ...     side="buy",
            ...     pair="XBTUSD",
            ...     volume=0.02,
            ...     price=23000,
            ...     expiretm=120,
            ...     oflags=["post", "fcib"]
            ... )

        """
        if not self._priv_conn or not self._priv_conn.is_auth:
            raise KrakenAuthenticationError(
                "Can't place order - Authenticated websocket not connected!",
            )

        payload: dict = {
            "event": "addOrder",
            "ordertype": str(ordertype),
            "type": str(side),
            "pair": str(pair),
            "volume": (
                str(volume)
                if not truncate
                else Trade().truncate(amount=volume, amount_type="volume", pair=pair)
            ),
            "validate": str(validate),
        }
        if defined(price):
            payload["price"] = (
                str(price)
                if not truncate
                else Trade().truncate(amount=price, amount_type="price", pair=pair)
            )
        if defined(price2):
            payload["price2"] = str(price2)
        if defined(oflags):
            if not isinstance(oflags, str):
                raise ValueError(
                    "oflags must be a comma delimited list of order flags as "
                    "str. Available flags: {viqc, fcib, fciq, nompp, post}",
                )
            payload["oflags"] = oflags
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

        await self.send_message(message=payload, private=True)

    @ensure_string("oflags")
    async def edit_order(  # pylint: disable=too-many-arguments # noqa: PLR0913
        self: SpotWSClientV1,
        orderid: str,
        reqid: str | int | None = None,
        pair: str | None = None,
        price: str | float | None = None,
        price2: str | float | None = None,
        volume: str | float | None = None,
        oflags: str | list[str] | None = None,
        newuserref: str | int | None = None,
        *,
        truncate: bool = False,
        validate: bool = False,
    ) -> None:
        """
        Edit an open order that was placed on the Spot market.

        Requires the ``Access WebSockets API`` and ``Create and modify orders``
        API key permissions.

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
        :type oflags: str | list[str], optional
        :param newuserref: Set a new user reference id
        :type newuserref: str | int, optional
        :param truncate: If enabled: round the ``price`` and ``volume`` to
            Kraken's maximum allowed decimal places. See
            https://support.kraken.com/hc/en-us/articles/4521313131540 fore more
            information about decimals.
        :type truncate: bool, optional
        :param validate: Validate the input without applying the changes
            (default: ``False``)
        :type validate: bool, optional
        :raises KrakenAuthenticationError: If the websocket is not connected or
            the connection is not authenticated
        :raises ValueError: If input is not correct

        Initialize your client as described in
        :class:`kraken.spot.SpotWSClientV1` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Edit an order

            >>> await client_auth.edit_order(
            ...     orderId="OBGFYP-XVQNL-P4GMWF",
            ...     volume=0.75,
            ...     pair="XBTUSD",
            ...     price=20000
            ... )
        """
        if not self._priv_conn or not self._priv_conn.is_auth:
            raise KrakenAuthenticationError(
                "Can't edit order - Authenticated websocket not connected!",
            )

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
            payload["price"] = (
                str(price)
                if not truncate
                else Trade().truncate(amount=price, amount_type="price", pair=pair)
            )
        if defined(price2):
            payload["price2"] = str(price2)
        if defined(volume):
            payload["volume"] = (
                str(volume)
                if not truncate
                else Trade().truncate(amount=volume, amount_type="volume", pair=pair)
            )
        if defined(oflags):
            payload["oflags"] = oflags
        if defined(newuserref):
            payload["newuserref"] = str(newuserref)

        await self.send_message(message=payload, private=True)

    async def cancel_order(self: SpotWSClientV1, txid: list[str]) -> None:
        """
        Cancel a specific order or a list of orders.

        Requires the ``Access WebSockets API`` and ``Cancel/close orders`` API
        key permissions.

        - https://docs.kraken.com/websockets/#message-cancelOrder

        :param txid: A single or multiple transaction ids as list
        :type txid: list[str]
        :raises KrakenAuthenticationError: If the websocket is not connected or
            the connection is not authenticated

        Initialize your client as described in
        :class:`kraken.spot.SpotWSClientV1` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Cancel an order

            >>> await client_auth.cancel_order(txid=["OBGFYP-XVQNL-P4GMWF"])
        """
        if not self._priv_conn or not self._priv_conn.is_auth:
            raise KrakenAuthenticationError(
                "Can't cancel order - Authenticated websocket not connected!",
            )
        await self.send_message(
            message={"event": "cancelOrder", "txid": txid},
            private=True,
        )

    async def cancel_all_orders(self: SpotWSClientV1) -> None:
        """
        Cancel all open Spot orders.

        Requires the ``Access WebSockets API`` and ``Cancel/close orders`` API
        key permissions.

        - https://docs.kraken.com/websockets/#message-cancelAll

        :raises KrakenAuthenticationError: If the websocket is not connected or
            the connection is not authenticated

        Initialize your client as described in
        :class:`kraken.spot.SpotWSClientV1` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Cancel all Orders

            >>> await client_auth.cancel_all_orders()
        """
        if not self._priv_conn or not self._priv_conn.is_auth:
            raise KrakenAuthenticationError(
                "Can't cancel all orders - Authenticated websocket not connected!",
            )
        await self.send_message(message={"event": "cancelAll"}, private=True)

    async def cancel_all_orders_after(
        self: SpotWSClientV1,
        timeout: int = 0,
    ) -> None:
        """
        Set a Death Man's Switch

        Requires the ``Access WebSockets API`` and ``Cancel/close orders`` API
        key permissions.

        - https://docs.kraken.com/websockets/#message-cancelAllOrdersAfter

        :param timeout: Set the timeout in seconds to cancel the orders after,
            set to ``0`` to reset.
        :type timeout: int
        :raises KrakenAuthenticationError: If the websocket is not connected or
            the connection is not authenticated

        Initialize your client as described in
        :class:`kraken.spot.SpotWSClientV1` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket: Death Man's Switch

            >>> await client_auth.cancel_all_orders_after(timeout=60)
        """
        if not self._priv_conn or not self._priv_conn.is_auth:
            raise KrakenAuthenticationError(
                "Can't cancel all orders after - Authenticated websocket not connected!",
            )
        await self.send_message(
            message={"event": "cancelAllOrdersAfter", "timeout": timeout},
            private=True,
        )


__all__ = ["SpotWSClientV1"]
