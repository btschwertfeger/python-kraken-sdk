#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that provides an example usage for the KrakenSpotWebsocketClient.
It uses the Kraken Websocket API v1.

todo: test this out
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
import time
from typing import Union

from kraken.spot import KrakenSpotWSClient

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


async def main() -> None:
    """Create bot and subscribe to topics/feeds"""

    key: str = os.getenv("SPOT_API_KEY")
    secret: str = os.getenv("SPOT_SECRET_KEY")

    # ___Custom_Trading_Bot/Client______________
    class Client(KrakenSpotWSClient):
        """Can be used to create a custom trading strategy/bot"""

        async def on_message(self: "Client", message: Union[list, dict]) -> None:
            """Receives the websocket messages"""
            if isinstance(message, dict) and "event" in message:
                topic = message["event"]
                if topic in ("heartbeat", "pong"):
                    return

            print(message)
            # if condition:
            #     await self.create_order(
            #         ordertype="limit",
            #         side="buy",
            #         pair="BTC/EUR",
            #         price=20000,
            #         volume=200
            #     )
            # ... it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient
            # you can also un/subscribe here using self.subscribe/self-unsubscribe

    # ___Public_Websocket_Feed_____
    client: Client = Client()  # only use this one if you don't need private feeds
    # print(bot.public_sub_names) # list public subscription names

    await client.subscribe(subscription={"name": "ticker"}, pair=["XBT/EUR", "DOT/EUR"])
    await client.subscribe(subscription={"name": "spread"}, pair=["XBT/EUR", "DOT/EUR"])
    await client.subscribe(subscription={"name": "book"}, pair=["BTC/EUR"])
    # await client.subscribe(subscription={ "name": "book", "depth": 25}, pair=["BTC/EUR"])
    # await client.subscribe(subscription={ "name": "ohlc" }, pair=["BTC/EUR"])
    # await client.subscribe(subscription={ "name": "ohlc", "interval": 15}, pair=["XBT/EUR", "DOT/EUR"])
    # await client.subscribe(subscription={ "name": "trade" }, pair=["BTC/EUR"])
    # await client.subscribe(subscription={ "name": "*"} , pair=["BTC/EUR"])

    time.sleep(2)  # wait because unsubscribing is faster than subscribing ...
    # print(bot.active_public_subscriptions)
    await client.unsubscribe(
        subscription={"name": "ticker"}, pair=["XBT/EUR", "DOT/EUR"]
    )
    await client.unsubscribe(subscription={"name": "spread"}, pair=["XBT/EUR"])
    await client.unsubscribe(subscription={"name": "spread"}, pair=["DOT/EUR"])
    # ...

    client_auth = Client(key=key, secret=secret)
    # print(client.active_private_subscriptions)
    # print(client_auth.private_sub_names) # list private subscription names
    # when using the authenticated bot, you can also subscribe to public feeds
    await client_auth.subscribe(subscription={"name": "ownTrades"})
    await client_auth.subscribe(subscription={"name": "openOrders"})

    time.sleep(2)
    await client_auth.unsubscribe(subscription={"name": "ownTrades"})
    await client_auth.unsubscribe(subscription={"name": "openOrders"})

    while not client.exception_occur and not client_auth.exception_occur:
        await asyncio.sleep(6)
    return


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
        # the websocket client will send {'event': 'asyncio.CancelledError'} via on_message
        # so you can handle the behavior/next actions individually within you bot

# ============================================================
# Alternative - as ContextManager:

# from kraken.spot import KrakenSpotWSClient
# import asyncio

# async def on_message(msg):
#     print(msg)

# async def main() -> None:
#     async with KrakenSpotWSClient(callback=on_message) as session:
#         await session.subscribe(subscription={"name": "ticker"}, pair=["XBT/USD"])

#     while True:
#         await asyncio.sleep(6)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass