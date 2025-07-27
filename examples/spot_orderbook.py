# !/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""

**For websocket API v2**

This module provides an example on how to use the Spot Orderbook client of the
python-kraken-sdk (https://github.com/btschwertfeger/python-kraken-sdk) to
retrieve and maintain a valid Spot order book for (a) specific asset pair(s).
It can be run directly without any credentials if the python-kraken-sdk is
installed.

    python3 -m pip install python-kraken-sdk

The output when running this snippet looks like the following table and updates
the book as soon as Kraken sent any order book update.

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

This can be the basis of an order book based trading strategy where realtime
data and fast price movements are considered.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from kraken.spot import SpotOrderBookClient

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)


class Orderbook(SpotOrderBookClient):
    """
    This is a wrapper class that is used to overload the :func:`on_book_update`
    function. It can also be used as a base for trading strategy. Since the
    :class:`kraken.spot.SpotOrderBookClient` is derived from
    :class:`kraken.spot.SpotWSClient` it can also be used to access the
    :func:`subscribe` function and any other provided utility.
    """

    async def on_book_update(
        self: Orderbook,
        pair: str,
        message: list,  # noqa: ARG002
    ) -> None:
        """
        This function is called every time the order book of ``pair`` gets
        updated.

        The ``pair`` parameter can be used to access the updated order book as
        shown in the function body below.

        :param pair: The currency pair of the updated order book
        :type pair: str
        :param message: The message sent by Kraken (not needed in most cases)
        :type message: list
        """
        book: dict[str, Any] = self.get(pair=pair)
        bid: list[tuple[str, str]] = list(book["bid"].items())
        ask: list[tuple[str, str]] = list(book["ask"].items())

        print("Bid     Volume\t\t  Ask     Volume")
        for level in range(self.depth):
            print(
                f"{bid[level][0]} ({bid[level][1][0]}) \t {ask[level][0]} ({ask[level][1][0]})",
            )

        assert book["valid"]  # ensure that the checksum is valid
        # … the client will automatically resubscribe to a book feed if the
        #   checksum is not valid. The user must not do anything for that, but
        #   will get informed.


async def main() -> None:
    """
    Here we depth of the order book and also a pair. We could
    subscribe to multiple pairs, but for simplicity only XBT/USD is chosen.

    The Orderbook class can be instantiated, which receives the order
    book-related messages, after we subscribed to the book feed.

    Finally we need some "game loop" - so we create a while loop
    that runs as long as there is no error.
    """

    async with Orderbook(depth=10) as orderbook:
        await orderbook.add_book(
            pairs=["BTC/USD"],  # we can also subscribe to more currency pairs
        )

        while not orderbook.exception_occur:
            await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt!")
