# -*- mode: python; coding: utf-8 -*-
# !/usr/bin/env python3
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module that provides an example usage for the Kraken Futures websocket client.
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
import time

from kraken.futures import FuturesWSClient

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOG: logging.Logger = logging.getLogger(__name__)

clients = []


# Custom client
class Client(FuturesWSClient):
    """Can be used to create a custom trading strategy"""

    async def on_message(self: Client, message: list | dict) -> None:
        """Receives the websocket messages"""
        LOG.info(message)
        # … apply your trading strategy in this class
        # … you can also combine this with the Futures REST clients


async def main() -> None:
    """Create a client and subscribe to channels/feeds"""

    key = os.getenv("FUTURES_API_KEY")
    secret = os.getenv("FUTURES_SECRET_KEY")

    try:
        # _____Public_Websocket_Feeds___________________
        client = Client()
        clients.append(client)
        await client.start()
        # print(client.get_available_public_subscription_feeds())

        products = ["PI_XBTUSD", "PF_SOLUSD"]
        # subscribe to a public websocket feed
        await client.subscribe(feed="ticker", products=products)
        await client.subscribe(feed="book", products=products)
        # await client.subscribe(feed='trade', products=products)
        # await client.subscribe(feed='ticker_lite', products=products)
        # await client.subscribe(feed='heartbeat')
        # time.sleep(2)

        # unsubscribe from a websocket feed
        time.sleep(2)  # in case subscribe is not done yet
        # await client.unsubscribe(feed='ticker', products=['PI_XBTUSD'])
        await client.unsubscribe(feed="ticker", products=["PF_XBTUSD"])
        await client.unsubscribe(feed="book", products=products)
        # ...

        # _____Private_Websocket_Feeds_________________
        if key and secret:
            client_auth = Client(key=key, secret=secret)
            clients.append(client_auth)
            await client_auth.start()
            # print(client_auth.get_available_private_subscription_feeds())

            # subscribe to a private/authenticated websocket feed
            await client_auth.subscribe(feed="fills")
            await client_auth.subscribe(feed="open_positions")
            # await client_auth.subscribe(feed='open_orders')
            # await client_auth.subscribe(feed='open_orders_verbose')
            # await client_auth.subscribe(feed='deposits_withdrawals')
            # await client_auth.subscribe(feed='account_balances_and_margins')
            # await client_auth.subscribe(feed='balances')
            # await client_auth.subscribe(feed='account_log')
            # await client_auth.subscribe(feed='notifications_auth')

            # authenticated clients can also subscribe to public feeds
            # await client_auth.subscribe(feed='ticker', products=['PI_XBTUSD', 'PF_ETHUSD'])

            # time.sleep(1)
            # unsubscribe from a private/authenticated websocket feed
            await client_auth.unsubscribe(feed="fills")
            await client_auth.unsubscribe(feed="open_positions")
            # ...

        while not client.exception_occur:  # and not client_auth.exception_occur:
            await asyncio.sleep(6)
    except Exception:
        pass
    finally:
        # Close the sessions properly.
        for _client in clients:
            await _client.close()


if __name__ == "__main__":
    asyncio.run(main())
    # the websocket client will send {'event': 'asyncio.CancelledError'} via on_message
    # so you can handle the behavior/next actions individually within you strategy

# ============================================================
# Alternative - as ContextManager:

# from kraken.futures import KrakenFuturesWSClient
# import asyncio

# async def on_message(message):
#     print(message)

# async def main() -> None:
#     async with KrakenFuturesWSClient(callback=on_message) as session:
#         await session.subscribe(feed="ticker", products=["PF_XBTUSD"])
#     while True:
#         await asyncio.sleep(6)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass
