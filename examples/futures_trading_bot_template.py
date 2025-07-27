# !/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module that provides a template to build a Futures trading algorithm using the
python-kraken-sdk.
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

from kraken.exceptions import KrakenAuthenticationError
from kraken.futures import FuturesWSClient, User

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOG: logging.Logger = logging.getLogger(__name__)


class TradingBot(FuturesWSClient):
    """
    Class that implements the trading strategy

    * The on_message function gets all messages sent by the websocket feeds.
    * Decisions can be made based on these messages
    * Can place trades using the self.__trade client
    * Do everything you want

    ====== P A R A M E T E R S ======
    config: dict
        configuration like: {
            'key' 'kraken-futures-key',
            'secret': 'kraken-secret-key',
            'products': ['PI_XBTUSD']
        }
    """

    def __init__(self: TradingBot, config: dict) -> None:
        super().__init__(  # initialize the KrakenFuturesWSClient
            key=config["key"],
            secret=config["secret"],
        )

    async def on_message(self: TradingBot, message: list | dict) -> None:
        """Receives all messages that came form the websocket feed(s)"""
        LOG.info(message)

        # == apply your trading strategy here ==
        # Hint: You can execute requests using the `request` function directly:
        # print(await self.request(
        #     "GET", "/api/charts/v1/spot/PI_XBTUSD/1d",
        # ))

        # You can also un-/subscribe here using `self.subscribe(...)` or
        # `self.unsubscribe(...)`
        # … more can be found in the documentation
        #        (https://python-kraken-sdk.readthedocs.io/en/stable/).

    # Add more functions to customize the trading strategy …

    def save_exit(self: TradingBot, reason: str = "") -> None:
        """Controlled shutdown of the strategy"""
        LOG.warning("Save exit triggered, reason: %s", reason)
        # Some ideas:
        #   * Save the bots data
        #   * Close trades
        #   * Enable dead man's switch
        sys.exit(1)


class ManagedBot:
    """
    Class to manage the trading strategy

    … subscribes to desired feeds, instantiates the strategy and runs as long
    as there is no error.

    ====== P A R A M E T E R S ======
    config: dict
        bot configuration like: {
            'key' 'kraken-futures-key',
            'secret': 'kraken-secret-key',
            'products': ['PI_XBTUSD']
        }
    """

    def __init__(self: ManagedBot, config: dict) -> None:
        self.__config: dict = config
        self.__trading_strategy: TradingBot | None = None

    def run(self: ManagedBot) -> None:
        """Runner function"""
        if not self.__check_credentials():
            sys.exit(1)

        try:
            asyncio.run(self.__main())
        except KeyboardInterrupt:
            self.save_exit(reason="KeyboardInterrupt")
        else:
            self.save_exit(reason="Asyncio loop left")

    async def __main(self: ManagedBot) -> None:
        """
        Instantiates the trading strategy/algorithm and subscribes to the
        desired websocket feeds. Run the loop while no exception occur.

        The variable `exception_occur` which is an attribute of the
        KrakenFuturesWSClient can be set individually but is also being set to
        `True` if the websocket connection has some fatal error. This is used to
        exit the asyncio loop - but you can also apply your own reconnect rules.
        """
        try:
            self.__trading_strategy = TradingBot(config=self.__config)
            await self.__trading_strategy.start()

            await self.__trading_strategy.subscribe(
                feed="ticker",
                products=self.__config["products"],
            )
            await self.__trading_strategy.subscribe(
                feed="book",
                products=self.__config["products"],
            )

            await self.__trading_strategy.subscribe(feed="fills")
            await self.__trading_strategy.subscribe(feed="open_positions")
            await self.__trading_strategy.subscribe(feed="open_orders")
            await self.__trading_strategy.subscribe(feed="balances")

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

    def __check_credentials(self: ManagedBot) -> bool:
        """Checks the user credentials and the connection to Kraken"""
        try:
            User(self.__config["key"], self.__config["secret"]).get_wallets()
            LOG.info("Client credentials are valid.")
            return True
        except urllib3.exceptions.MaxRetryError:
            LOG.error("MaxRetryError, cannot connect.")
            return False
        except requests.exceptions.ConnectionError:
            LOG.error("ConnectionError, Kraken not available.")
            return False
        except KrakenAuthenticationError:
            LOG.error("Invalid credentials!")
            return False

    def save_exit(self: ManagedBot, reason: str = "") -> None:
        """Calls the save exit function of the trading strategy"""
        print(f"Save exit triggered - {reason}")
        if self.__trading_strategy is not None:
            self.__trading_strategy.save_exit(reason=reason)
        else:
            sys.exit(1)


def main() -> None:
    """Example main - load environment variables and run the strategy."""

    managed_bot: ManagedBot = ManagedBot(
        config={
            "key": os.getenv("FUTURES_API_KEY"),
            "secret": os.getenv("FUTURES_SECRET_KEY"),
            "products": ["PI_XBTUSD", "PF_SOLUSD"],
        },
    )

    try:
        managed_bot.run()
    except Exception:
        managed_bot.save_exit(
            reason=f"manageBot.run() has ended: {traceback.format_exc()}",
        )


if __name__ == "__main__":
    main()
