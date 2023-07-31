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

from .websocket_v1 import KrakenSpotWSClient


class OrderbookClient:
    """
    The orderbook client can be used for instantiation and maintaining
    one or multiple orderbooks for Spot trading on the Kraken cryptocurrency
    exchange. It connects to the websocket feed(s) and receives the book
    updates, calculates the checksum and will publish the changes to the
    :func:`OrderbookClient.on_book_update` function or to the specified
    callback function.

    The :func:`OrderbookClient.get` function can be used to access a specific
    book of this client.

    The client will resubscribe to the book feed(s) if any errors occur and
    publish the changes to the mentioned function(s).

    This class has a fixed book depth. Available depths are: {10, 25, 50, 100}

    - https://support.kraken.com/hc/en-us/articles/360027821131-WebSocket-API-v1-How-to-maintain-a-valid-order-book

    - https://docs.kraken.com/websockets/#book-checksum

    .. code-block:: python
        :linenos:
        :caption: Example: Create and maintain a Spot orderbook as custom class

        from typing import Any, Dict, List, Tuple
        from kraken.spot import OrderbookClient
        import asyncio

        class OrderBook(OrderbookClient):
            async def on_book_update(self: "OrderBook", pair: str, message: list) -> None:
                '''This function must be overloaded to get the recent updates.'''
                book: Dict[str, Any] = self.get(pair=pair)
                bid: List[Tuple[str, str]] = list(book["bid"].items())
                ask: List[Tuple[str, str]] = list(book["ask"].items())

                print("Bid         Volume\t\t Ask         Volume")
                for level in range(self.depth):
                    print(
                        f"{bid[level][0]} ({bid[level][1]}) \t {ask[level][0]} ({ask[level][1]})"
                    )

        async def main() -> None:
            orderbook: OrderBook = OrderBook(depth=10)
            await orderbook.add_book(
                pairs=["XBT/USD"]  # we can also subscribe to more currency pairs
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
        from kraken.spot import OrderbookClient
        import asyncio

        async def my_callback(self: "OrderBook", pair: str, message: list) -> None:
            '''This function do not need to be async.'''
            print(message)

        async def main() -> None:
            orderbook: OrderBook = OrderBook(depth=100, callback=my_callback)
            await orderbook.add_book(
                pairs=["XBT/USD"]  # we can also subscribe to more currency pairs
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
        self: OrderbookClient,
        depth: int = 10,
        callback: Optional[Callable] = None,
    ) -> None:
        super().__init__()
        self.__book: Dict[str, dict] = {}
        self.__depth: int = depth
        self.__callback: Optional[Callable] = callback

        self.ws_client: KrakenSpotWSClient = KrakenSpotWSClient(
            callback=self.on_message
        )

    async def on_message(self: OrderbookClient, message: Union[list, dict]) -> None:
        """
        The on_message function is implemented in the KrakenSpotWSClient
        class and used as callback to receive all messages sent by the
        Kraken API.

        *This function should not be overloaded - this would break this client!*
        """
        if "errorMessage" in message:
            self.LOG.warning(message)

        if "event" in message and isinstance(message, dict):
            # ignore heartbeat / ping - pong messages / any event message
            # ignore errors since they are handled by the parent class
            # just handle the removal of an orderbook
            if (
                message["event"] == "subscriptionStatus"
                and "status" in message
                and "pair" in message
                and message["status"] == "unsubscribed"
                and message["pair"] in self.__book
            ):
                del self.__book[message["pair"]]
                return

        if not isinstance(message, list):
            # The orderbook feed only sends messages with type list,
            # so we can ignore anything else.
            return

        pair: str = message[-1]
        if pair not in self.__book:
            self.__book[pair] = {
                "bid": {},
                "ask": {},
                "valid": True,
            }

        if "as" in message[1]:
            # This will be triggered initially when the
            # first message comes in that provides the initial snapshot
            # of the current orderbook.
            self.__update_book(pair=pair, side="ask", snapshot=message[1]["as"])
            self.__update_book(pair=pair, side="bid", snapshot=message[1]["bs"])
        else:
            checksum: Optional[str] = None
            # This is executed every time a new update comes in.
            for data in message[1 : len(message) - 2]:
                if "a" in data:
                    self.__update_book(pair=pair, side="ask", snapshot=data["a"])
                elif "b" in data:
                    self.__update_book(pair=pair, side="bid", snapshot=data["b"])
                if "c" in data:
                    checksum = data["c"]

            self.__validate_checksum(pair=pair, checksum=checksum)

        if not self.__book[pair]["valid"]:
            await self.on_book_update(
                pair=pair,
                message=[
                    {
                        "error": f"Checksum mismatch - resubscribe to the orderbook {pair}"
                    }
                ],
            )
            # if the orderbook's checksum is invalid, we need re-add the orderbook
            await self.remove_book(pairs=[pair])

            await asyncio_sleep(3)
            await self.add_book(pairs=[pair])
        else:
            await self.on_book_update(pair=pair, message=message)

    async def on_book_update(self: OrderbookClient, pair: str, message: list) -> None:
        """
        This function will be called every time the orderbook gets updated.
        It needs to be overloaded if no callback function was defined
        during the instantiation of this class.

        :param pair: The currency pair of the orderbook that has
            been updated.
        :type pair: str
        """

        if self.__callback:
            if iscoroutinefunction(self.__callback):
                await self.__callback(pair=pair, message=message)
            else:
                self.__callback(pair=pair, message=message)
        else:
            logging.info(message)

    async def add_book(self: OrderbookClient, pairs: List[str]) -> None:
        """
        Add an orderbook to this client. The feed will be subscribed
        and updates will be published to the :func:`on_book_update` function.

        :param pairs: The pair(s) to subscribe to
        :type pairs: List[str]
        :param depth: The book depth
        :type depth: int
        """
        await self.ws_client.subscribe(
            subscription={"name": "book", "depth": self.__depth}, pair=pairs
        )

    async def remove_book(self: OrderbookClient, pairs: List[str]) -> None:
        """
        Unsubscribe from a subscribed orderbook.

        :param pairs: The pair(s) to unsubscribe from
        :type pairs: List[str]
        :param depth: The book depth
        :type depth: int
        """
        await self.ws_client.unsubscribe(
            subscription={"name": "book", "depth": self.__depth}, pair=pairs
        )

    @property
    def depth(self: OrderbookClient) -> int:
        """
        Return the fixed depth of this orderbook client.
        """
        return self.__depth

    @property
    def exception_occur(self: OrderbookClient) -> bool:
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

    def get(self: OrderbookClient, pair: str) -> Optional[dict]:
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
            class Orderbook(OrderbookClient):

                async def on_book_update(
                    self: "Orderbook",
                    pair: str,
                    message: list
                ) -> None:
                    book: Dict[str, Any] = self.get(pair="XBT/USD")
                    ask: List[Tuple[str, str]] = list(book["ask"].items())
                    bid: List[Tuple[str, str]] = list(book["bid"].items())
                    # ask and bid are now in format [price, (volume, timestamp)]
                    # … and include the whole orderbook
        """
        return self.__book.get(pair)

    def __update_book(
        self: OrderbookClient, pair: str, side: str, snapshot: list
    ) -> None:
        """
        This functions updates the local orderbook based on the
        information provided in ``data`` and assigns/update the
        asks and bids in book.

        The ``data`` here looks like:
        [
            ['25026.00000', '2.77183035', '1684658128.013525'],
            ['25028.50000', '0.04725650', '1684658121.180535'],
            ['25030.20000', '0.29527502', '1684658128.018182'],
            ['25030.40000', '2.77134976', '1684658131.751539'],
            ['25032.20000', '0.13978808', '1684658131.751577']
        ]
        … where the first value is the ask or bid price, the second
          represents the volume and the last one is the timestamp.

        :param side: The side to assign the data to,
            either ``ask`` or ``bid``
        :type side: str
        :param data: The data that needs to be assigned.
        :type data: list
        """
        for entry in snapshot:
            price: str = entry[0]
            volume: str = entry[1]
            timestamp: str = entry[2]

            if float(volume) > 0.0:
                # Price level exist or is new
                self.__book[pair][side][price] = (volume, timestamp)
            else:
                # Price level moved out of range
                self.__book[pair][side].pop(price)

            if side == "ask":
                self.__book[pair]["ask"] = OrderedDict(
                    sorted(self.__book[pair]["ask"].items(), key=self.get_first)[
                        : self.__depth
                    ]
                )

            elif side == "bid":
                self.__book[pair]["bid"] = OrderedDict(
                    sorted(
                        self.__book[pair]["bid"].items(),
                        key=self.get_first,
                        reverse=True,
                    )[: self.__depth]
                )

    def __validate_checksum(self: OrderbookClient, pair: str, checksum: str) -> None:
        """
        Function that validates the checksum of the orderbook as described here
        https://docs.kraken.com/websockets/#book-checksum.

        :param pair: The pair that's orderbook checksum should be validated.
        :type pair: str
        :param checksum: The checksum sent by the Kraken API
        :type checksum: str
        """
        book: dict = self.__book[pair]
        ask = list(book["ask"].items())
        bid = list(book["bid"].items())

        local_checksum: str = ""
        for price_level, (volume, _) in ask[:10]:
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".", ""
            ).lstrip("0")

        for price_level, (volume, _) in bid[:10]:
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".", ""
            ).lstrip("0")

        self.__book[pair]["valid"] = checksum == str(crc32(local_checksum.encode()))

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


__all__ = ["OrderbookClient"]
