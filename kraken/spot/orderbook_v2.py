#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Spot Orderbook client"""

from __future__ import annotations

import logging
from asyncio import sleep as asyncio_sleep
from binascii import crc32
from collections import OrderedDict
from inspect import iscoroutinefunction
from typing import Callable, Dict, List, Optional, Union

from kraken.spot import Market
from kraken.spot.websocket_v2 import KrakenSpotWSClientV2


class OrderbookClientV2:
    """
    **This client is using the Kraken Websocket API v2**

    The orderbook client can be used for instantiation and maintaining one or
    multiple order books for Spot trading on the Kraken cryptocurrency exchange.
    It uses websockets to subscribe to book feeds and receives book updates,
    calculates the checksum and will publish the raw message to the
    :func:`on_book_update` function or to the specified callback
    function.

    :func:`get` can be used to access a specific book of this
    client - they will always be up-to date when used from within
    :func:`on_book_update`.

    The client will resubscribe to the book feed(s) if any errors occur and
    publish the changes to the mentioned function(s). This is required to
    compute the correct checksum internally.

    This class has a default book depth of 10. Available depths are: 10, 25, 50,
    100, 500, 1000. This client can handle multiple books - but only for one
    depth. When subscribing to books with different depths, please use separate
    instances of this class.

    - https://docs.kraken.com/websockets-v2/#calculate-book-checksum

    .. code-block:: python
        :linenos:
        :caption: Example: Create and maintain a Spot orderbook as custom class

        from typing import Any, Dict, List, Tuple
        from kraken.spot import OrderbookClientV2
        import asyncio

        class OrderBook(OrderbookClientV2):
            async def on_book_update(self: "OrderBook", pair: str, message:
            list) -> None:
                '''This function must be overloaded to get the recent
                updates.''' book: Dict[str, Any] = self.get(pair=pair) bid:
                List[Tuple[str, str]] = list(book["bid"].items()) ask:
                List[Tuple[str, str]] = list(book["ask"].items())

                print("Bid         Volume\t\t Ask         Volume") for level in
                range(self.depth):
                    print(
                        f"{bid[level][0]} ({bid[level][1]}) \t {ask[level][0]}
                        ({ask[level][1]})"
                    )

        async def main() -> None:
            orderbook: OrderBook = OrderBook(depth=10) await orderbook.add_book(
                pairs=["XBT/USD"]  # we can also subscribe to more currency
                pairs
            )

            while not orderbook.exception_occur:
                await asyncio.sleep(10)

        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass


    .. code-block:: python
        :linenos:
        :caption: Example: Create and maintain a Spot orderbook using a callback

        from typing import Any, Dict, List, Tuple
        from kraken.spot import OrderbookClientV2
        import asyncio

        async def my_callback(self: "OrderBook", pair: str, message: list) ->
        None:
            '''This function do not need to be async.''' print(message)

        async def main() -> None:
            orderbook: OrderBook = OrderBook(depth=100, callback=my_callback)
            await orderbook.add_book(
                pairs=["XBT/USD"]  # we can also subscribe to more currency
                pairs
            )

            while not orderbook.exception_occur:
                await asyncio.sleep(10)

        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: OrderbookClientV2,
        depth: int = 10,
        callback: Optional[Callable] = None,
    ) -> None:
        super().__init__()
        self.__book: Dict[str, dict] = {}
        self.__depth: int = depth
        self.__callback: Optional[Callable] = callback

        self.__market: Market = Market()
        self.ws_client: KrakenSpotWSClientV2 = KrakenSpotWSClientV2(
            callback=self.on_message,
        )

    async def on_message(self: OrderbookClientV2, message: Union[list, dict]) -> None:
        """
        The on_message function is implemented within the KrakenSpotWSClient
        class and used as callback to receive all messages sent by the
        Kraken API.

        *This function must not be overloaded - it would break this client!*
        """

        if not isinstance(message, dict):
            return

        if (
            message.get("method") == "unsubscribe"
            and message.get("result")
            and message["result"].get("channel") == "book"
            and message.get("success")
            and message["result"]["symbol"] in self.__book
        ):
            del self.__book[message["result"]["symbol"]]
            return

        if (  # pylint: disable=too-many-boolean-expressions)
            message.get("channel") != "book"
            or not message.get("data")
            or not message.get("type")
            or not isinstance(message["data"], list)
            or len(message["data"]) == 0
            or not isinstance(message["data"][0], dict)
            or not message["data"][0].get("checksum")
        ):
            # we are only interested in book related messages
            return

        # ----------------------------------------------------------------------
        pair: str = message["data"][0]["symbol"]
        if pair not in self.__book:
            # retrieve the decimal places required for checksum calculation
            sym_info: dict = self.__market.get_asset_pairs(pair=pair)

            self.__book[pair] = {
                "bid": {},
                "ask": {},
                "valid": True,
                "price_decimals": int(sym_info[pair]["pair_decimals"]),
                "qty_decimals": int(sym_info[pair]["lot_decimals"]),
            }

        timestamp: Optional[str] = message["data"][0].get(
            "timestamp",
            None,  # snapshot does not provide a timestamp
        )

        # ----------------------------------------------------------------------
        self.__update_book(
            orders=message["data"][0]["asks"],
            side="ask",
            symbol=pair,
            timestamp=timestamp,
        )
        self.__update_book(
            orders=message["data"][0]["bids"],
            side="bid",
            symbol=pair,
            timestamp=timestamp,
        )

        if message["type"] != "snapshot":
            self.__validate_checksum(
                pair=pair,
                checksum=int(message["data"][0]["checksum"]),
            )

        await self.on_book_update(pair=pair, message=message)

        if not self.__book[pair]["valid"]:
            await self.on_book_update(
                pair=pair,
                message={
                    "error": f"Checksum mismatch - resubscribing to the orderbook for {pair}",
                },
            )
            # if the orderbook's checksum is invalid, we need re-add the orderbook
            await self.remove_book(pairs=[pair])

            await asyncio_sleep(3)
            await self.add_book(pairs=[pair])

    async def on_book_update(self: OrderbookClientV2, pair: str, message: dict) -> None:
        """
        This function will be called every time the orderbook gets updated.
        It needs to be overloaded if no callback function was defined
        during the instantiation of this class.

        :param pair: The currency pair of the orderbook that has
            been updated.
        :type pair: str
        :param message: The book message sent by Kraken
        :type message: dict
        """

        if self.__callback:
            if iscoroutinefunction(self.__callback):
                await self.__callback(pair=pair, message=message)
            else:
                self.__callback(pair=pair, message=message)
        else:
            print(message)  # noqa: T201

    async def add_book(self: OrderbookClientV2, pairs: List[str]) -> None:
        """
        Add an orderbook to this client. The feed will be subscribed
        and updates will be published to the :func:`on_book_update` function.

        :param pairs: The pair(s) to subscribe to
        :type pairs: list[str]
        :param depth: The book depth
        :type depth: int
        """
        await self.ws_client.subscribe(
            params={"channel": "book", "depth": self.__depth, "symbol": pairs},
        )

    async def remove_book(self: OrderbookClientV2, pairs: List[str]) -> None:
        """
        Unsubscribe from a subscribed orderbook.

        :param pairs: The pair(s) to unsubscribe from
        :type pairs: list[str]
        :param depth: The book depth
        :type depth: int
        """
        await self.ws_client.unsubscribe(
            params={"channel": "book", "depth": self.__depth, "symbol": pairs},
        )

    @property
    def depth(self: OrderbookClientV2) -> int:
        """
        Return the fixed depth of this orderbook client.
        """
        return self.__depth

    @property
    def exception_occur(self: OrderbookClientV2) -> bool:
        """
        Can be used to determine if any critical error occurred within the
        websocket connection. If so, the function will return ``True``
        and the client instance is most likely not useable anymore. So this
        is the switch lets the user know, when to delete the current one and
        create a new one.

        :return: ``True`` if any critical error occurred else ``False``
        :rtype: bool
        """
        return bool(self.ws_client.exception_occur)

    def get(self: OrderbookClientV2, pair: str) -> Optional[dict]:
        """
        Returns the orderbook for a specific ``pair``.

        :param pair: The pair to get the orderbook from
        :type pair: str
        :return: The orderbook of that ``pair``.
        :rtype: dict

        .. code-block::python
            :linenos:
            :caption: Orderbook: Get ask and bid

            …
            class Orderbook(OrderbookClientV2):

                async def on_book_update(
                    self: "Orderbook",
                    pair: str,
                    message: list
                ) -> None:
                    book: Dict[str, Any] = self.get(pair="XBT/USD")
                    ask: list[Tuple[str, str]] = list(book["ask"].items())
                    bid: list[Tuple[str, str]] = list(book["bid"].items())
                    # ask and bid are now in format [price, (volume, timestamp)]
                    # … and include the whole orderbook
        """
        return self.__book.get(pair)

    def __update_book(
        self: OrderbookClientV2,
        orders: List[dict],
        side: str,
        symbol: str,
        timestamp: Optional[str] = None,
    ) -> None:
        """
        This functions updates the local orderbook based on the
        information provided in ``orders`` and assigns or updates the
        asks and bids of the book.

        :param orders: List of asks or bids like [{"price":1, "qty": 2}]
        :type orders: list[dict]
        :param side: The type of orders (``ask`` or ``bid``)
        :type side: str
        :param symbol: The currency pair / symbol
        :type symbol: str
        :param timestamp: The timestamp of that order(s)
        :type timestamp: str, optional
        """
        for order in orders:
            volume = "{:.{}f}".format(  # pylint: disable=consider-using-f-string
                order["qty"],
                self.__book[symbol]["qty_decimals"],
            )
            price = "{:.{}f}".format(  # pylint: disable=consider-using-f-string
                order["price"],
                self.__book[symbol]["price_decimals"],
            )

            if float(volume) > 0.0:
                # Price level exists or is new
                self.__book[symbol][side][price] = (volume, timestamp)
            else:
                # Price level moved out of range
                self.__book[symbol][side].pop(price, None)

            # Sort and limit the depth of the order book
            self.__book[symbol][side] = OrderedDict(
                sorted(
                    self.__book[symbol][side].items(),
                    key=self.get_first,
                    reverse=side == "bid",
                )[: self.__depth],
            )

    def __validate_checksum(self: OrderbookClientV2, pair: str, checksum: int) -> None:
        """
        Function that validates the checksum of the order book as described here
        https://docs.kraken.com/websockets-v2/#calculate-book-checksum.

        :param pair: The pair that's order book checksum should be validated.
        :type pair: str
        :param checksum: The checksum sent by the Kraken API
        :type checksum: int
        """
        book: dict = self.__book[pair]
        ask = list(book["ask"].items())
        bid = list(book["bid"].items())

        local_checksum: str = ""
        for price_level, (volume, _) in ask[:10]:
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".",
                "",
            ).lstrip("0")

        for price_level, (volume, _) in bid[:10]:
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".",
                "",
            ).lstrip("0")

        self.__book[pair]["valid"] = checksum == crc32(local_checksum.encode())

    @staticmethod
    def get_first(values: tuple) -> float:
        """
        This function is used as callback for the ``sorted`` method
        to sort a tuple/list by its first value and while ensuring
        that the values are floats and comparable.

        :param values: A tuple of string values
        :type values: tuple
        :return: The first value of ``values`` as float.
        :rtype: float
        """
        return float(values[0])


__all__ = ["OrderbookClientV2"]
