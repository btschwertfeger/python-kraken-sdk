#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger


"""
Module that provides an example Spot trading bot structure. It uses the Kraken
Kraken Websocket API v2.
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
import sys
import traceback
from typing import Any, Optional

import requests
import urllib3

from kraken.exceptions import KrakenException
from kraken.spot import Funding, KrakenSpotWSClientV2, Market, Staking, Trade, User

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class TradingBot(KrakenSpotWSClientV2):
    """
    Class that implements the trading strategy

    * The on_message function gets all messages sent by the websocket feed
    * Decisions can be made based on these messages
    * Can place trades using the self.__trade client
    * Do everything you want

    ====== P A R A M E T E R S ======
    config: dict
        configuration like: {
            "key": "kraken-spot-key",
            "secret": "kraken-spot-secret",
            "pairs": ["DOT/USD", "BTC/USD"],
        }
    """

    def __init__(self: TradingBot, config: dict, **kwargs: Any) -> None:
        super().__init__(
            key=config["key"], secret=config["secret"], **kwargs
        )  # initialize the KrakenSpotWSClientV2
        self.__config: dict = config

        self.__user: User = User(key=config["key"], secret=config["secret"])
        self.__trade: Trade = Trade(key=config["key"], secret=config["secret"])
        self.__market: Market = Market(key=config["key"], secret=config["secret"])
        self.__funding: Funding = Funding(key=config["key"], secret=config["secret"])
        self.__staking: Staking = Staking(key=config["key"], secret=config["secret"])

    async def on_message(self: TradingBot, message: dict) -> None:
        """Receives all messages of the websocket connection(s)"""
        if message.get("method") == "pong" or message.get("channel") == "heartbeat":
            return
        if "error" in message:
            # handle exceptions/errors sent by websocket connection ...
            pass

        logging.info(message)

        # ... apply your trading strategy here

        # call functions from self.__trade and other clients if conditions met …

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

        # You can also un-/subscribe here using `self.subscribe(...)` or `self.unsubscribe(...)`
        # … more can be found in the documentation (https://python-kraken-sdk.readthedocs.io/en/stable/).

    # Add more functions to customize the trading strategy …

    def save_exit(self: TradingBot, reason: Optional[str] = "") -> None:
        """controlled shutdown of the strategy"""
        logging.warning(f"Save exit triggered, reason: {reason}")
        # ideas:
        #   * save the current data
        #   * maybe close trades
        #   * enable dead man's switch
        sys.exit(1)


class ManagedBot:
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
            params={"channel": "ticker", "symbol": self.__config["pairs"]}
        )
        await self.__trading_strategy.subscribe(
            params={"channel": "ohlc", "interval": 15, "symbol": self.__config["pairs"]}
        )

        await self.__trading_strategy.subscribe(params={"channel": "executions"})

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
        "key": os.getenv("SPOT_API_KEY"),
        "secret": os.getenv("SPOT_SECRET_KEY"),
        "pairs": ["DOT/USD", "BTC/USD"],
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
