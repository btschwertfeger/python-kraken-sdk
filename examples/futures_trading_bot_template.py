#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that provides an example Futures trading bot data structure."""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
import sys
import traceback
from typing import Optional, Union

import requests
import urllib3

from kraken.exceptions import KrakenException
from kraken.futures import Funding, KrakenFuturesWSClient, Market, Trade, User

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class TradingBot(KrakenFuturesWSClient):
    """
    Class that implements the trading strategy

    * The on_message function gets all events from the websocket feed
    * Decisions can be made based on these events
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

    def __init__(self: "TradingBot", config: dict) -> None:
        super().__init__(
            key=config["key"], secret=config["secret"]
        )  # initialize the KakenFuturesWSClient
        self.__config: dict = config

        self.__user: User = User(key=config["key"], secret=config["secret"])
        self.__trade: Trade = Trade(key=config["key"], secret=config["secret"])
        self.__market: Market = Market(key=config["key"], secret=config["secret"])
        self.__funding: Funding = Funding(key=config["key"], secret=config["secret"])

    async def on_message(self: "TradingBot", event: Union[list, dict]) -> None:
        """Receives all events that came form the websocket feed(s)"""
        logging.info(event)
        # ... apply your trading strategy here

        # call functions from self.__trade and other clients if conditions met...

        # response = self.__trade.create_order(
        #     orderType='lmt',
        #     size=2,
        #     symbol='PI_XBTUSD',
        #     side='buy',
        #     limitPrice=10000
        # )
        # ...

        # you can also un-/subscribe here using `self.subscribe(...)` or `self.unsubscribe(...)`

    # add more functions to customize the trading strategy
    # ...
    # ...

    def save_exit(self: "TradingBot", reason: Optional[str] = "") -> None:
        """Controlled shutdown of the strategy"""
        logging.warning(f"Save exit triggered, reason: {reason}")
        # ideas:
        #   * save the bots data
        #   * maybe close trades
        #   * enable dead man's switch
        sys.exit(1)


class ManagedBot:
    """
    Class to manage the trading strategy

    Subscribes to desired feeds, instantiates the strategy and runs until condition met

    ====== P A R A M E T E R S ======
    config: dict
        bot configuration like: {
            'key' 'kraken-futures-key',
            'secret': 'kraken-secret-key',
            'products': ['PI_XBTUSD']
        }
    """

    def __init__(self: "ManagedBot", config: dict) -> None:
        self.__config: dict = config
        self.__trading_strategy: Optional[TradingBot] = None

    def run(self: "ManagedBot") -> None:
        """Runner function"""
        if not self.__check_credentials():
            sys.exit(1)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            asyncio.run(self.__main())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
            if self.__trading_strategy is not None:
                self.__trading_strategy.save_exit(reason="Asyncio loop left")

    async def __main(self: "ManagedBot") -> None:
        """
        Instantiates the trading strategy/algorithm and subscribes to the
        desired websocket feeds. Run the loop while no exception occur.

        Thi variable `exception_occu` which is an attribute of the KrakenFuturesWSClient
        can be set individually but is also beeing set to `True` if the websocket connection
        has some fatal error. This is used to exit the asyncio loop.
        """
        self.__trading_strategy = TradingBot(config=self.__config)

        await self.__trading_strategy.subscribe(
            feed="ticker", products=self.__config["products"]
        )
        await self.__trading_strategy.subscribe(
            feed="book", products=self.__config["products"]
        )

        await self.__trading_strategy.subscribe(feed="fills")
        await self.__trading_strategy.subscribe(feed="open_positions")
        await self.__trading_strategy.subscribe(feed="open_orders")
        await self.__trading_strategy.subscribe(feed="balances")

        while not self.__trading_strategy.exception_occur:
            try:
                # check if bot feels good
                # maybe send a status update every day
                # ...
                pass

            except Exception as exc:
                message: str = f"Exception in main: {exc} {traceback.format_exc()}"
                logging.error(message)
                self.__trading_strategy.save_exit(reason=message)

            await asyncio.sleep(6)
        self.__trading_strategy.save_exit(
            reason="Left main loop because of exception in strategy."
        )
        return

    def __check_credentials(self: "ManagedBot") -> bool:
        """Checks the user credentials and the connection to Kraken"""
        try:
            User(self.__config["key"], self.__config["secret"]).get_wallets()
            logging.info("Client credentials are valid")
            return True
        except urllib3.exceptions.MaxRetryError:
            logging.error("MaxRetryError, cannot connect.")
            return False
        except requests.exceptions.ConnectionError:
            logging.error("ConnectionError, Kraken not available.")
            return False
        except KrakenException.KrakenAuthenticationError:
            logging.error("Invalid credentials!")
            return False

    def save_exit(self: "ManagedBot", reason: Optional[str] = "") -> None:
        """Calls the save exit funtion of the rtading strategy"""
        self.__trading_strategy.save_exit(reason=reason)


def main() -> None:
    """Main"""
    bot_config: dict = {
        "key": os.getenv("FUTURES_API_KEY"),
        "secret": os.getenv("FUTURES_SECRET_KEY"),
        "products": ["PI_XBTUSD", "PF_SOLUSD"],
    }
    try:
        managed_bot: ManagedBot = ManagedBot(config=bot_config)
        managed_bot.run()
    except Exception:
        managed_bot.save_exit(
            reason=f"manageBot.run() has ended: {traceback.format_exc()}"
        )


if __name__ == "__main__":
    main()
