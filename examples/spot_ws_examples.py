# -*- mode: python; coding: utf-8 -*-
# !/usr/bin/env python3
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module that provides an example usage for the KrakenSpotWebsocketClient.
It uses the Kraken Websocket API v2.
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
from contextlib import suppress

from kraken.spot import SpotWSClient

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Client(SpotWSClient):
    """Can be used to create a custom trading strategy"""

    async def on_message(self: Client, message: dict) -> None:
        """Receives the websocket messages"""
        if message.get("method") == "pong" or message.get("channel") == "heartbeat":
            return

        print(message)
        # now you can access lots of methods, for example to create an order:
        # if self._is_auth:  # only if the client is authenticated …
        #     await self.send_message(
        #         message={
        #             "method": "add_order",
        #             "params": {
        #                 "limit_price": 1234.56,
        #                 "order_type": "limit",
        #                 "order_userref": 123456789,
        #                 "order_qty": 1.0,
        #                 "side": "buy",
        #                 "symbol": "BTC/USD",
        #                 "validate": True,
        #             },
        #         }
        #     )
        # ... it is also possible to call regular REST endpoints
        # but using the websocket messages is more efficient.
        # You can also un-/subscribe here using self.subscribe/self.unsubscribe.


async def main() -> None:
    key: str = os.getenv("SPOT_API_KEY")
    secret: str = os.getenv("SPOT_SECRET_KEY")

    # Public/unauthenticated websocket client
    client: Client = Client()  # only use this one if you don't need private feeds
    await client.start()
    # print(client.public_channel_names)  # list public subscription names

    await client.subscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]},
    )
    await client.subscribe(
        params={"channel": "book", "depth": 25, "symbol": ["BTC/USD"]},
    )
    # await client.subscribe(params={"channel": "ohlc", "symbol": ["BTC/USD"]})
    await client.subscribe(
        params={
            "channel": "ohlc",
            "interval": 15,
            "snapshot": False,
            "symbol": ["BTC/USD", "DOT/USD"],
        },
    )
    await client.subscribe(params={"channel": "trade", "symbol": ["BTC/USD"]})

    # wait because unsubscribing is faster than unsubscribing ... (just for that example)
    await asyncio.sleep(3)
    # print(client.active_public_subscriptions) # … to list active subscriptions
    await client.unsubscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]},
    )
    # ...

    if key and secret:
        # Per default, the authenticated client starts two websocket connections,
        # one for authenticated and one for public messages. If there is no need
        # for a public connection, it can be disabled using the ``no_public``
        # parameter.
        client_auth = Client(key=key, secret=secret, no_public=True)
        await client_auth.start()
        # print(client_auth.private_channel_names)  # … list private channel names
        # when using the authenticated client, you can also subscribe to public feeds
        await client_auth.subscribe(params={"channel": "executions"})

        await asyncio.sleep(5)
        await client_auth.unsubscribe(params={"channel": "executions"})

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

# from kraken.spot import SpotWSClient
# import asyncio


# async def on_message(message: dict) -> None:
#     print(message)


# async def main() -> None:
#     async with SpotWSClient(callback=on_message) as session:
#         await session.subscribe(params={"channel": "ticker", "symbol": ["BTC/USD"]})

#     while True:
#         await asyncio.sleep(6)


# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass
