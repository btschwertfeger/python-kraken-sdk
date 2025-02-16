# -*- mode: python; coding: utf-8 -*-
# !/usr/bin/env python3
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#
# ruff: noqa: RUF027

"""
Module that provides a template to build a Spot trading algorithm using the
python-kraken-sdk and Kraken Spot websocket API v2.
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
import sys
import traceback

import requests
import urllib3

from kraken.exceptions import KrakenAuthenticationError  # , KrakenPermissionDeniedError
from kraken.spot import Funding, Market, SpotWSClient, Trade, User

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

LOG: logging.Logger = logging.getLogger(__name__)


class TradingBot(SpotWSClient):
    """
    Class that implements the trading strategy

    * The on_message function gets all messages sent by the websocket feeds.
    * Decisions can be made based on these messages
    * Can place trades using the self.__trade client or self.send_message
    * Do everything you want

    ====== P A R A M E T E R S ======
    config: dict
        configuration like: {
            "key": "kraken-spot-key",
            "secret": "kraken-spot-secret",
            "pairs": ["DOT/USD", "BTC/USD"],
        }
    """

    def __init__(
        self: TradingBot,
        config: dict,
        **kwargs: object | dict | set | tuple | list | str | float | None,
    ) -> None:
        super().__init__(
            key=config["key"],
            secret=config["secret"],
            **kwargs,
        )
        self.__config: dict = config

        self.__user: User = User(key=config["key"], secret=config["secret"])
        self.__trade: Trade = Trade(key=config["key"], secret=config["secret"])
        self.__market: Market = Market(key=config["key"], secret=config["secret"])
        self.__funding: Funding = Funding(key=config["key"], secret=config["secret"])

    async def on_message(self: TradingBot, message: dict) -> None:
        """Receives all messages of the websocket connection(s)"""
        if message.get("method") == "pong" or message.get("channel") == "heartbeat":
            return
        if "error" in message:
            # handle exceptions/errors sent by websocket connection …
            pass

        LOG.info(message)

        # == apply your trading strategy here ==

        # Call functions of `self.__trade` and other clients if conditions met …
        # try:
        #     print(self.__trade.create_order(
        #         ordertype='limit',
        #         side='buy',
        #         volume=2,
        #         pair='XBTUSD',
        #         price=12000
        #     ))
        # except KrakenPermissionDeniedError:
        #    # … handle exceptions
        #    pass

        # The spot websocket client also allow sending orders via websockets
        # this is way faster than using REST endpoints.
        # await self.send_message(
        #     message={
        #         "method": "add_order",
        #         "params": {
        #             "limit_price": 1234.56,
        #             "order_type": "limit",
        #             "order_userref": 123456789,
        #             "order_qty": 1.0,
        #             "side": "buy",
        #             "symbol": "BTC/USD",
        #             "validate": True,
        #         },
        #     }
        # )

        # You can also un-/subscribe here using `self.subscribe(...)` or
        # `self.unsubscribe(...)`.
        #
        # … more can be found in the documentation
        #        (https://python-kraken-sdk.readthedocs.io/en/stable/).

    # Add more functions to customize the trading strategy …

    def save_exit(self: TradingBot, reason: str | None = "") -> None:
        """controlled shutdown of the strategy"""
        LOG.warning("Save exit triggered, reason: %s", reason)
        # Some ideas:
        #   * Save the current data
        #   * Close trades
        #   * Enable dead man's switch
        sys.exit(1)


class Manager:
    """
    Class to manage the trading strategy

    … subscribes to desired feeds, instantiates the strategy and runs as long
    as there is no error.

    ====== P A R A M E T E R S ======
    config: dict
        configuration like: {
            "key" "kraken-spot-key",
            "secret": "kraken-secret-key",
            "pairs": ["DOT/USD", "BTC/USD"],
        }
    """

    def __init__(self: Manager, config: dict) -> None:
        self.__config: dict = config
        self.__trading_strategy: TradingBot | None = None

    def run(self: Manager) -> None:
        """Starts the event loop and bot"""
        if not self.__check_credentials():
            sys.exit(1)

        try:
            asyncio.run(self.__main())
        except KeyboardInterrupt:
            self.save_exit(reason="KeyboardInterrupt")
        else:
            self.save_exit(reason="Asyncio loop left")

    async def __main(self: Manager) -> None:
        """
        Instantiates the trading strategy and subscribes to the desired
        websocket feeds. While no exception within the strategy occur run the
        loop.

        The variable `exception_occur` which is an attribute of the SpotWSClient
        can be set individually but is also being set to `True` if the websocket
        connection has some fatal error. This is used to exit the asyncio loop -
        but you can also apply your own reconnect rules.
        """
        try:
            self.__trading_strategy = TradingBot(config=self.__config)
            await self.__trading_strategy.start()

            await self.__trading_strategy.subscribe(
                params={"channel": "ticker", "symbol": self.__config["pairs"]},
            )
            await self.__trading_strategy.subscribe(
                params={
                    "channel": "ohlc",
                    "interval": 15,
                    "symbol": self.__config["pairs"],
                },
            )

            await self.__trading_strategy.subscribe(params={"channel": "executions"})

            while not self.__trading_strategy.exception_occur:
                # Check if the algorithm feels good
                # Send a status update every day via Telegram or Mail
                # …
                await asyncio.sleep(6)

        except Exception as exc:
            LOG.error(message := f"Exception in main: {exc} {traceback.format_exc()}")
            self.__trading_strategy.save_exit(reason=message)
        finally:
            # Close the sessions properly.
            await self.__trading_strategy.close()

    def __check_credentials(self: Manager) -> bool:
        """Checks the user credentials and the connection to Kraken"""
        try:
            User(self.__config["key"], self.__config["secret"]).get_account_balance()
            LOG.info("Client credentials are valid.")
            return True
        except urllib3.exceptions.MaxRetryError:
            LOG.error("MaxRetryError, can't connect.")
            return False
        except requests.exceptions.ConnectionError:
            LOG.error("ConnectionError, Kraken not available.")
            return False
        except KrakenAuthenticationError:
            LOG.error("Invalid credentials!")
            return False

    def save_exit(self: Manager, reason: str = "") -> None:
        """Invoke the save exit function of the trading strategy"""
        print(f"Save exit triggered - {reason}")
        if self.__trading_strategy is not None:
            self.__trading_strategy.save_exit(reason=reason)
        else:
            sys.exit(1)


def main() -> None:
    """Example main - load environment variables and run the strategy."""
    manager: Manager = Manager(
        config={
            "key": os.getenv("SPOT_API_KEY"),
            "secret": os.getenv("SPOT_SECRET_KEY"),
            "pairs": ["DOT/USD", "BTC/USD"],
        },
    )

    try:
        manager.run()
    except Exception:
        manager.save_exit(
            reason=f"manageBot.run() has ended: {traceback.format_exc()}",
        )


if __name__ == "__main__":
    main()
