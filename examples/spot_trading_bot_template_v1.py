#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger


"""
Module that provides an example Futures trading bot data structure.
It uses the Kraken Websocket API v1.

todo: test this out
"""

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
from kraken.spot import Funding, KrakenSpotWSClient, Market, Staking, Trade, User


class TradingBot(KrakenSpotWSClient):
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

    def __init__(self: TradingBot, config: dict) -> None:
        super().__init__(
            key=config["key"], secret=config["secret"]
        )  # initialize the KakenFuturesWSClient
        self.__config: dict = config

        self.__user: User = User(key=config["key"], secret=config["secret"])
        self.__trade: Trade = Trade(key=config["key"], secret=config["secret"])
        self.__market: Market = Market(key=config["key"], secret=config["secret"])
        self.__funding: Funding = Funding(key=config["key"], secret=config["secret"])
        self.__staking: Staking = Staking(key=config["key"], secret=config["secret"])

    async def on_message(self: TradingBot, message: Union[dict, list]) -> None:
        """Receives all messages that came form the websocket connection"""
        if isinstance(message, dict) and "event" in message:
            if message["event"] in ("heartbeat", "pong"):
                return
            if "error" in message:
                # handle exceptions/errors sent by websocket connection ...
                pass

        logging.info(message)

        # ... apply your trading strategy here

        # call functions from self.__trade and other clients if conditions met...

        # try:
        #     print(self.__trade.create_order(
        #         ordertype='limit',
        #         side='buy',
        #         volume=2,
        #         pair='XBTUSD',
        #         price=12000
        #     ))
        # except KrakenException.KrakenPermissionDeniedError:
        #    # ... handle exceptions
        #    pass

        # The spot websocket client also allow sending orders via websockets
        # this is way faster than using REST endpoints.

        # await self.create_order(
        #     ordertype='limit',
        #     side='buy',
        #     pair='BTC/EUR',
        #     price=20000,
        #     volume=200
        # )

        # you can also un-/subscribe here using `self.subscribe(...)` or `self.unsubscribe(...)`

        # more can be found in the documentation

    # add more functions to customize the trading strategy
    # ...

    def save_exit(self: TradingBot, reason: Optional[str] = "") -> None:
        """controlled shutdown of the strategy"""
        logging.warning(f"Save exit triggered, reason: {reason}")
        # ideas:
        #   * save the bots data
        #   * maybe close trades
        #   * enable dead man's switch
        sys.exit(1)


class ManagedBot:
    """
    Class to manage the trading strategy

    subscribes to desired feeds, instantiates the strategy and runs until condition met

    ====== P A R A M E T E R S ======
    config: dict
        configuration like: {
            'key' 'kraken-futures-key',
            'secret': 'kraken-secret-key',
            'products': ['PI_XBTUSD']
        }
    """

    def __init__(self: ManagedBot, config: dict):
        self.__config: dict = config
        self.__trading_strategy: Optional[TradingBot] = None

    def run(self: ManagedBot) -> None:
        """Starts the event loop and bot"""
        if not self.__check_credentials():
            sys.exit(1)

        try:
            asyncio.run(self.__main())
        except KeyboardInterrupt:
            pass
        finally:
            if self.__trading_strategy is not None:
                self.__trading_strategy.save_exit(reason="Asyncio loop left")

    async def __main(self: ManagedBot) -> None:
        """
        Instantiates the trading strategy (bot) and subscribes to the
        desired websocket feeds. While no exception within the strategy occur
        run the loop.

        This variable `exception_occur` which is an attribute of the KrakenSpotWSClient
        can be set individually but is also being set to True if the websocket connection
        has some fatal error. This is used to exit the asyncio loop.
        """
        self.__trading_strategy = TradingBot(config=self.__config)

        await self.__trading_strategy.subscribe(
            subscription={"name": "ticker"}, pair=self.__config["pairs"]
        )
        await self.__trading_strategy.subscribe(
            subscription={"name": "ohlc", "interval": 15}, pair=self.__config["pairs"]
        )

        await self.__trading_strategy.subscribe(subscription={"name": "ownTrades"})
        await self.__trading_strategy.subscribe(subscription={"name": "openOrders"})

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

    def __check_credentials(self: ManagedBot) -> bool:
        """Checks the user credentials and the connection to Kraken"""
        try:
            User(self.__config["key"], self.__config["secret"]).get_account_balance()
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

    def save_exit(self: ManagedBot, reason: str = "") -> None:
        """Invoke the save exit function of the trading strategy"""
        print(f"Save exit triggered - {reason}")
        if self.__trading_strategy is not None:
            self.__trading_strategy.save_exit(reason=reason)


def main() -> None:
    """Main"""
    bot_config: dict = {
        "key": os.getenv("API_KEY"),
        "secret": os.getenv("SECRET_KEY"),
        "pairs": ["DOT/EUR", "XBT/USD"],
    }
    managed_bot: ManagedBot = ManagedBot(config=bot_config)
    try:
        managed_bot.run()
    except Exception:
        managed_bot.save_exit(
            reason=f"manageBot.run() has ended: {traceback.format_exc()}"
        )


if __name__ == "__main__":
    main()
