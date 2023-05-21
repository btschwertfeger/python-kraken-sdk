#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that provides an excample usage for the Kraken Spot websocket client."""

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

    key: str = os.getenv("API_KEY")
    secret: str = os.getenv("SECRET_KEY")

    # ___Custom_Trading_Bot______________
    class Bot(KrakenSpotWSClient):
        """Can be used to create a custom trading strategy/bot"""

        async def on_message(self: "Bot", event: Union[list, dict]) -> None:
            """receives the websocket events"""
            if "event" in event:
                topic = event["event"]
                if topic == "heartbeat":
                    return
                if topic == "pong":
                    return

            print(event)
            # if condition:
            #     await self.create_order(
            #         ordertype='limit',
            #         side='buy',
            #         pair='BTC/EUR',
            #         price=20000,
            #         volume=200
            #     )
            # ... it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient
            # you can also un/subscribe here using self.subscribe/self-unsubscribe

    # ___Public_Websocket_Feed_____
    bot: Bot = Bot()  # only use this one if you dont need private feeds
    # print(bot.public_sub_names) # list public subscription names

    await bot.subscribe(subscription={"name": "ticker"}, pair=["XBT/EUR", "DOT/EUR"])
    await bot.subscribe(subscription={"name": "spread"}, pair=["XBT/EUR", "DOT/EUR"])
    await bot.subscribe(subscription={"name": "book"}, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "book", "depth": 25}, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "ohlc" }, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "ohlc", "interval": 15}, pair=["XBT/EUR", "DOT/EUR"])
    # await bot.subscribe(subscription={ "name": "trade" }, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "*"} , pair=["BTC/EUR"])

    time.sleep(2)  # wait because unsubscribing is faster than subscribing ...
    # print(bot.active_public_subscriptions)
    await bot.unsubscribe(subscription={"name": "ticker"}, pair=["XBT/EUR", "DOT/EUR"])
    await bot.unsubscribe(subscription={"name": "spread"}, pair=["XBT/EUR"])
    await bot.unsubscribe(subscription={"name": "spread"}, pair=["DOT/EUR"])
    # ....

    auth_bot = Bot(key=key, secret=secret)
    # print(bot.active_private_subscriptions)
    # print(auth_bot.private_sub_names) # list private subscription names
    # when using the authenticated bot, you can also subscribe to public feeds
    await auth_bot.subscribe(subscription={"name": "ownTrades"})
    await auth_bot.subscribe(subscription={"name": "openOrders"})

    time.sleep(2)
    await auth_bot.unsubscribe(subscription={"name": "ownTrades"})
    await auth_bot.unsubscribe(subscription={"name": "openOrders"})

    while not bot.exception_occur and not auth_bot.exception_occur:
        await asyncio.sleep(6)
    return


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
        # the websocket client will send {'event': 'asyncio.CancelledError'} via on_message
        # so you can handle the behaviour/next actions individually within you bot
    finally:
        loop.close()

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
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass
#     finally:
#         loop.close()
