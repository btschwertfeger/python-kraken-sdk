#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
This module provides an example on how to use the Spot websocket
client of the python-kraken-sdk (https://github.com/btschwertfeger/python-kraken-sdk)
to retrieve and maintain a valid Spot order book for (a) specific
asset pair(s). It can be run directly without any credentials if the
python-kraken-sdk is installed.

    python3 -m pip install python-kraken-sdk

The output when running this snippet looks like the following table and
updates the book as soon as Kraken sent any order book update.

Bid         Volume               Ask         Volume
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
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Tuple

from kraken.spot import SpotOrderBookClient


class OrderBook(SpotOrderBookClient):
    """
    This is a wrapper class that is used to overload the :func:`on_book_update`
    function. It can also be used as a base for trading strategy. Since the
    :class:`SpotOrderBookClient` is derived from :class:`KrakenWSClient`
    it can also be used to access the :func:`subscribe` function and any
    other provided utility.
    """

    async def on_book_update(self: "OrderBook", pair: str, message: list) -> None:
        """
        This function is called every time the order book of ``pair`` gets
        updated.

        The ``pair`` parameter can be used to access the updated order book
        as shown in the function body below.

        :param pair: The currency pair of the updated order book
        :type pair: str
        :param message: The message sent by Kraken (not needed in most cases)
        :type message: list
        """
        book: Dict[str, Any] = self.get(pair=pair)
        bid: List[Tuple[str, str]] = list(book["bid"].items())
        ask: List[Tuple[str, str]] = list(book["ask"].items())

        print("Bid         Volume\t\t Ask         Volume")
        for level in range(self.depth):
            print(
                f"{bid[level][0]} ({bid[level][1]}) \t {ask[level][0]} ({ask[level][1]})"
            )

        assert book["valid"]  # ensure that the checksum is valid


async def main() -> None:
    """
    Here we depth of the order book and also a pair. We could
    subscribe to multiple pairs, but for simplicity only XBT/USD is chosen.

    The OrderBook class can be instantiated, which receives the order
    book-related messages, after we subscribed to the book feed.

    Finally we need some "game loop" - so we create a while loop
    that runs as long as there is no error.
    """
    orderbook: OrderBook = OrderBook()

    await orderbook.add_book(
        pairs=["XBT/USD"]  # we can also subscribe to more currency pairs
    )

    while not orderbook.exception_occur:
        await asyncio.sleep(10)

    # If this here gets executed, the Websocket connection had some
    # serious troubles.


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
