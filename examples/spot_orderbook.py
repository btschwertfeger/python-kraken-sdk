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
updates the book as soon as Kraken sent any order book update. The
stdout refreshes every 0.1 seconds.

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

References
- https://support.kraken.com/hc/en-us/articles/360027821131-WebSocket-API-v1-How-to-maintain-a-valid-order-book
- https://docs.kraken.com/websockets/#book-checksum
"""

from __future__ import annotations

import asyncio
from typing import List, Optional

from kraken.spot import Orderbook


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
            print("Bid         Volume\t\t Ask         Volume")
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
