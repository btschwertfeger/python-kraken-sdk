#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
This module provides an example on how to use the Spot websocket
client of the python-kraken-sdk (https://github.com/btschwertfeger/python-kraken-sdk)
to retrieve and maintain a valid Spot order book for a specific
asset pair. It can be run directly without any credentials if the
python-kraken-sdk is installed.

    python3 -m pip install python-kraken-sdk

The output when running this snippet looks like the following table and
updates the book every 0.1 seconds.

Bid             Volume          Ask             Volume
27076.00000 (8.28552127)         27076.10000 (2.85897056)
27075.90000 (3.75748052)         27077.30000 (0.57243521)
27074.40000 (0.57249652)         27080.80000 (0.00100000)
27072.90000 (0.01200917)         27081.00000 (0.00012345)
27072.80000 (0.25000000)         27081.70000 (0.30000000)
27072.30000 (4.89735970)         27082.70000 (0.05539777)
27072.20000 (2.65896716)         27082.80000 (0.00400000)
27072.10000 (2.77037635)         27082.90000 (0.57231684)
27072.00000 (0.81770000)         27083.00000 (0.38934000)
27071.50000 (0.07194657)         27083.80000 (2.76918992)

This can be the basis of an order book based trading strategy where
realtime data and fast price movements are considered.

References
- https://support.kraken.com/hc/en-us/articles/360027821131-WebSocket-API-v1-How-to-maintain-a-valid-order-book
- https://docs.kraken.com/websockets/#book-checksum
"""

from __future__ import annotations

import asyncio
import binascii
from itertools import islice
from typing import Dict, List, Optional, Union

from kraken.spot import KrakenSpotWSClient


class Orderbook(KrakenSpotWSClient):
    """
    The Orderbook class inherts the subscribe function from the
    KrakenSpotWSClient class. This function is used to subscribe to the
    order book feed will initially send the current order book
    and then send updates when anything changes.
    """

    def __init__(self: "Orderbook", depth: int = 10) -> None:
        super().__init__()
        self.__book: Dict[str, dict] = {}
        self.__depth: int = depth

    async def on_message(self: "Orderbook", msg: Union[list, dict]) -> None:
        """
        The on_message function is implemented in the KrakenSpotWSClient
        class and used as callback to receive all messages sent by the
        Kraken API.
        """
        if "errorMessage" in msg:
            print(msg)
            return

        if "event" in msg:
            # ignore heartbeat / ping - pong messages
            return

        if not isinstance(msg, list):
            # The order book feed only sends messages with type list,
            # so we can ignore anything else.
            return

        pair: str = msg[-1]
        if pair not in self.__book:
            self.__book[pair] = {"bid": {}, "ask": {}, "valid": True}

        if "as" in msg[1]:
            # This will be triggered initially when the
            # first message comes in that provides the initial snapshot
            # of the current order book.
            self.__update_book(pair=pair, side="ask", snapshot=msg[1]["as"])
            self.__update_book(pair=pair, side="bid", snapshot=msg[1]["bs"])
        else:
            # This is executed every time a new update comes in.
            for data in msg[1 : len(msg) - 2]:
                if "a" in data:
                    self.__update_book(pair=pair, side="ask", snapshot=data["a"])
                elif "b" in data:
                    self.__update_book(pair=pair, side="bid", snapshot=data["b"])

            self.__validate_checksum(pair=pair, checksum=msg[1]["c"])

    def get(self: "Orderbook", pair: str) -> Optional[dict]:
        """
        Returns the order book for a specific ``pair``.

        :param pair: The pair to get the order book from
        :type pair: str
        :return: The order book of that ``pair``.
        :rtype: dict
        """
        return self.__book.get(pair)

    def __update_book(self: "Orderbook", pair: str, side: str, snapshot: list) -> None:
        """
        This functions updates the local order book based on the
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
        ... where the first value is the ask or bid price, the second
            represents the volume and the last one is the time stamp.

        :param side: The side to assign the data to,
            either ``ask`` or ``bid``
        :type side: str
        :param data: The data that needs to be assigned.
        :type data: list
        """
        for entry in snapshot:
            price: str = entry[0]
            volume: str = entry[1]

            if float(volume) > 0.0:
                # Price level exist or is new
                self.__book[pair][side][price] = volume
            else:
                # Price level moved out of range
                self.__book[pair][side].pop(price)

            if side == "ask":
                self.__book[pair]["ask"] = dict(
                    sorted(
                        self.__book[pair]["ask"].items(), key=self.get_first  # type: ignore[arg-type]
                    )[: self.__depth]
                )

            elif side == "bid":
                self.__book[pair]["bid"] = dict(
                    sorted(
                        self.__book[pair]["bid"].items(),
                        key=self.get_first,  # type: ignore[arg-type]
                        reverse=True,
                    )[: self.__depth]
                )

    def __validate_checksum(self: "Orderbook", pair: str, checksum: str) -> None:
        """
        Function that validates the checksum of the orderbook as described here
        https://docs.kraken.com/websockets/#book-checksum.

        :param pair: The pair that's order book checksum should be validated.
        :type pair: str
        :param checksum: The checksum sent by the Kraken API
        :type checksum: str
        """
        book: dict = self.__book[pair]

        # sort ask (desc) and bid (asc)
        ask: List[dict] = sorted(book["ask"].items(), key=self.get_first)  # type: ignore[arg-type]
        bid: List[dict] = sorted(
            book["bid"].items(),
            key=self.get_first,  # type: ignore[arg-type]
            reverse=True,
        )

        local_checksum: str = ""
        for price_level, volume in islice(ask, 10):
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".", ""
            ).lstrip("0")

        for price_level, volume in islice(bid, 10):
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".", ""
            ).lstrip("0")

        self.__book[pair]["valid"] = checksum == str(
            binascii.crc32(local_checksum.encode())
        )
        # assert self.__book[pair]["valid"]

    @staticmethod
    def get_first(values: List[float]) -> float:
        """
        This function is used as callback for the ``sorted`` method
        to sort a list by its first value and while ensuring
        that the values are floats and comparable.

        :param values: A list oft string or float values
        :type values: List[float]
        :return: The first value of ``values`` as float.
        :rtype: float
        """
        return float(values[0])


async def main() -> None:
    """
    This is the actual main function where we define the depth of the
    order book and also a pair. We could subscribe to multiple pairs,
    but for simplicity only XBT/USD is coosen.

    After defined some constants, the order book class can be instantiated,
    which receives the order book-related messages, after we subscribed
    to the book feed.

    Finally we need some "game loop" - so we create a while loop
    that runs until the KrakenSpotWSClient class encounters some error
    which will be indicated by the ``exception_occur`` flag. Within this
    loop we print out the order book on the console - but this is the place
    where some could implement or call an order book depending strategy.
    """
    DEPTH: int = 10  # we can also change the depth to 100
    PAIR: str = "XBT/USD"

    orderbook: Orderbook = Orderbook(depth=DEPTH)
    await orderbook.subscribe(
        subscription={"name": "book", "depth": DEPTH},
        pair=[PAIR],  # we can also subscribe to more currency pairs
    )

    while not orderbook.exception_occur:
        book: Optional[dict] = orderbook.get(PAIR)
        if not book or len(book["bid"]) < DEPTH or len(book["ask"]) < DEPTH:
            pass
        else:
            bid: List[dict] = sorted(
                book["bid"].items(),
                key=orderbook.get_first,  # type: ignore[arg-type]
                reverse=True,
            )
            ask: List[dict] = sorted(book["ask"].items(), key=orderbook.get_first)  # type: ignore[arg-type]
            print("Bid\t\tVolume\t\tAsk\t\tVolume")
            for level in range(DEPTH):
                print(
                    f"{bid[level][0]} ({bid[level][1]}) \t {ask[level][0]} ({ask[level][1]})"
                )
            assert book["valid"]

        # This following sleep statement is very important to not having a million calls a second.
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
