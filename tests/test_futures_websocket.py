#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfegerr
# Github: https://github.com/btschwertfeger
#
"""Module that tests the Kraken Futures websocket client"""
import asyncio
import os
import time
import unittest

import pytest

from kraken.futures.client import KrakenFuturesWSClient


class Bot(KrakenFuturesWSClient):
    """Class to create a websocket bot"""

    async def on_message(self, event) -> None:
        log = ""
        try:
            with open("futures_ws_log.log", "r", encoding="utf-8") as f:
                log = f.read()
        except FileNotFoundError:
            pass

        with open("futures_ws_log.log", "w", encoding="utf-8") as f:
            f.write(f"{log}\n{event}")


class WebsocketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__key = os.getenv("FUTURES_API_KEY")
        self.__secret = os.getenv("FUTURES_SECRET_KEY")
        self.__full_ws_access = os.getenv("FULLACCESS") is not None

    def __create_loop(self, coro) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(coro())
        loop.close()

    async def __wait(self, seconds: float = 1) -> None:
        start = time.time()
        while time.time() - seconds < start:
            await asyncio.sleep(0.2)
        return

    def test_create_public_bot(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    def test_create_private_bot(self) -> None:
        async def create_bot() -> None:
            Bot(key=self.__key, secret=self.__secret)
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    def test_get_subscriptions(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            bot.get_active_subscriptions
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    def test_get_available_public_subscriptions(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            assert bot.get_available_public_subscription_feeds() == [
                "trade",
                "book",
                "ticker",
                "ticker_lite",
                "heartbeat",
            ]
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    def test_get_available_private_subscriptions(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            assert bot.get_available_private_subscription_feeds() == [
                "fills",
                "open_positions",
                "open_orders",
                "open_orders_verbose",
                "balances",
                "deposits_withdrawals",
                "account_balances_and_margins",
                "account_log",
                "notifications_auth",
            ]
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    def test_get_auth_state(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            assert not bot.is_auth

            auth_bot = Bot(key=self.__key, secret=self.__secret)
            assert auth_bot.is_auth

            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    def test_subscribe_public(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            products = ["PI_XBTUSD", "PF_SOLUSD"]

            with pytest.raises(ValueError):  # products must be List[str]
                await bot.subscribe(feed="ticker", products="PI_XBTUSD")

            await bot.subscribe(feed="heartbeat")
            await bot.subscribe(feed="ticker", products=products)
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    def test_subscribe_private(self) -> None:
        async def create_bot() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)

            with pytest.raises(
                ValueError
            ):  # private subscriptions does not use products
                await auth_bot.subscribe(feed="fills", products=["PI_XBTUSD"])

            await auth_bot.subscribe(feed="open_orders")
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    def test_unsubsribe_public(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            products = ["PI_XBTUSD", "PF_SOLUSD"]

            with pytest.raises(ValueError):  # products must be type List[str]
                await bot.unsubscribe(feed="ticker", products="PI_XBTUSD")

            await bot.subscribe(feed="ticker", products=products)
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    def test_unsubscribe_private(self) -> None:
        async def create_bot() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)

            with pytest.raises(
                ValueError
            ):  # private un/-subscriptions does not accept a product
                await auth_bot.unsubscribe(feed="open_orders", products=["PI_XBTUSD"])

            await auth_bot.unsubscribe(feed="open_orders")
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    def test_get_active_subscriptions(self) -> None:
        async def create_bot() -> None:
            bot = Bot()
            assert bot.get_active_subscriptions() == []
            await self.__wait(2)
            await bot.subscribe(feed="ticker", products=["PI_XBTUSD"])
            await self.__wait(5)
            assert len(bot.get_active_subscriptions()) == 1
            await bot.unsubscribe(feed="ticker", products=["PI_XBTUSD"])
            await self.__wait(5)
            assert bot.get_active_subscriptions() == []

        self.__create_loop(coro=create_bot)

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
