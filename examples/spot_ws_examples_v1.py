#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that provides an example usage for the KrakenSpotWebsocketClient.
It uses the Kraken Websocket API v1.
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
from contextlib import suppress

from kraken.spot import KrakenSpotWSClientV1

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


async def main() -> None:
    """Create a client and subscribe to channels/feeds"""

    key: str = os.getenv("SPOT_API_KEY")
    secret: str = os.getenv("SPOT_SECRET_KEY")

    class Client(KrakenSpotWSClientV1):
        """Can be used to create a custom trading strategy"""

        async def on_message(self: Client, message: list | dict) -> None:
            """Receives the websocket messages"""
            if isinstance(message, dict) and "event" in message:
                topic = message["event"]
                if topic in {"heartbeat", "pong"}:
                    return

            print(message)
            # if condition:
            #     await self.create_order(
            #         ordertype="limit",
            #         side="buy",
            #         pair="BTC/USD",
            #         price=20000,
            #         volume=200
            #     )
            # ... it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient.
            # You can also un-/subscribe here using self.subscribe/self.unsubscribe.

    # ___Public_Websocket_Feed_____
    client: Client = Client()  # only use this one if you don't need private feeds
    # print(client.public_channel_names) # list public subscription names

    await client.subscribe(subscription={"name": "ticker"}, pair=["XBT/USD", "DOT/USD"])
    await client.subscribe(subscription={"name": "spread"}, pair=["XBT/USD", "DOT/USD"])
    await client.subscribe(subscription={"name": "book"}, pair=["BTC/USD"])
    # await client.subscribe(subscription={ "name": "book", "depth": 25}, pair=["BTC/USD"])
    # await client.subscribe(subscription={ "name": "ohlc" }, pair=["BTC/USD"])
    # await client.subscribe(subscription={ "name": "ohlc", "interval": 15}, pair=["XBT/USD", "DOT/USD"])
    # await client.subscribe(subscription={ "name": "trade" }, pair=["BTC/USD"])
    # await client.subscribe(subscription={ "name": "*"} , pair=["BTC/USD"])

    await asyncio.sleep(2)  # wait because unsubscribing is faster than subscribing ...
    # print(client.active_public_subscriptions)
    await client.unsubscribe(
        subscription={"name": "ticker"},
        pair=["XBT/USD", "DOT/USD"],
    )
    await client.unsubscribe(subscription={"name": "spread"}, pair=["XBT/USD"])
    await client.unsubscribe(subscription={"name": "spread"}, pair=["DOT/USD"])
    # ...

    if key and secret:
        client_auth = Client(key=key, secret=secret)
        # print(client_auth.active_private_subscriptions)
        # print(client_auth.private_channel_names) # list private channel names
        # when using the authenticated client, you can also subscribe to public feeds
        await client_auth.subscribe(subscription={"name": "ownTrades"})
        await client_auth.subscribe(subscription={"name": "openOrders"})

        await asyncio.sleep(2)
        await client_auth.unsubscribe(subscription={"name": "ownTrades"})
        await client_auth.unsubscribe(subscription={"name": "openOrders"})

    while not client.exception_occur:  # and not client_auth.exception_occur:
        await asyncio.sleep(6)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
    # The websocket client will send {'event': 'asyncio.CancelledError'}
    # via on_message so you can handle the behavior/next actions
    # individually within your strategy.

# ============================================================
# Alternative - as ContextManager:

# from kraken.spot import KrakenSpotWSClientV1
# import asyncio

# async def on_message(message):
#     print(message)

# async def main() -> None:
#     async with KrakenSpotWSClientV1(callback=on_message) as session:
#         await session.subscribe(subscription={"name": "ticker"}, pair=["XBT/USD"])

#     while True:
#         await asyncio.sleep(6)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass
