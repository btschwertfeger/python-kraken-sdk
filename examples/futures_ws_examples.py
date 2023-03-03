#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfegerr
# Github: https://github.com/btschwertfeger
#

"""Module that provides an excample usage for the Kraken Futures websocket client"""
import asyncio
import logging
import logging.config
import time

from dotenv import dotenv_values

from kraken.futures.client import KrakenFuturesWSClient

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

    key = dotenv_values(".env")["Futures_API_KEY"]
    secret = dotenv_values(".env")["Futures_SECRET_KEY"]

    # ___Custom_Trading_Bot__________
    class Bot(KrakenFuturesWSClient):
        """Can be used to create a custom trading strategy/bot"""

        async def on_message(self, event) -> None:
            """receives the websocket events"""
            logging.info(event)
            # ... apply your trading strategy here
            # you can also combine this with the Futures REST clients

    # _____Public_Websocket_Feeds___________________
    bot = Bot()
    # print(bot.get_available_public_subscription_feeds())

    products = ["PI_XBTUSD", "PF_SOLUSD"]
    # subscribe to a public websocket feed
    await bot.subscribe(feed="ticker", products=products)
    await bot.subscribe(feed="book", products=products)
    # await bot.subscribe(feed='trade', products=products)
    # await bot.subscribe(feed='ticker_lite', products=products)
    # await bot.subscribe(feed='heartbeat')
    # time.sleep(2)

    # unsubscribe from a websocket feed
    time.sleep(2)  # in case subscribe is not done yet
    # await bot.unsubscribe(feed='ticker', products=['PI_XBTUSD'])
    await bot.unsubscribe(feed="ticker", products=["PF_SOLUSD"])
    await bot.unsubscribe(feed="book", products=products)
    # ....

    # _____Private_Websocket_Feeds_________________
    auth_bot = Bot(key=key, secret=secret)
    # print(auth_bot.get_available_private_subscription_feeds())

    # subscribe to a private/authenticated websocket feed
    await auth_bot.subscribe(feed="fills")
    await auth_bot.subscribe(feed="open_positions")
    # await auth_bot.subscribe(feed='open_orders')
    # await auth_bot.subscribe(feed='open_orders_verbose')
    # await auth_bot.subscribe(feed='deposits_withdrawals')
    # await auth_bot.subscribe(feed='account_balances_and_margins')
    # await auth_bot.subscribe(feed='balances')
    # await auth_bot.subscribe(feed='account_log')
    # await auth_bot.subscribe(feed='notifications_auth')

    # authenticaed clients can also subscribe to public feeds
    # await auth_bot.subscribe(feed='ticker', products=['PI_XBTUSD', 'PF_ETHUSD'])

    # time.sleep(1)
    # unsubscribe from a private/authenticaed websocket feed
    await auth_bot.unsubscribe(feed="fills")
    await auth_bot.unsubscribe(feed="open_positions")
    # ....

    while not bot.exception_occur and not auth_bot.exception_occur:
        await asyncio.sleep(6)
    return


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # the websocket client will send {'event': 'asyncio.CancelledError'} via on_message
        # so you can handle the behaviour/next actions individually within you bot
        pass
    finally:
        loop.close()
