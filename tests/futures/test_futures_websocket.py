#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures websocket client"""

import asyncio
import os
import time
import unittest

import pytest

from kraken.futures import KrakenFuturesWSClient


class Bot(KrakenFuturesWSClient):
    """Class to create a websocket bot"""

    async def on_message(self, event) -> None:
        # The following comments are only for debugging.
        # log = ""
        # try:
        #     with open("futures_ws_log.log", "r", encoding="utf-8") as f:
        #         log = f.read()
        # except FileNotFoundError:
        #     pass

        # with open("futures_ws_log.log", "w", encoding="utf-8") as f:
        #     f.write(f"{log}\n{event}")
        pass


class WebsocketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__key = os.getenv("FUTURES_API_KEY")
        self.__secret = os.getenv("FUTURES_SECRET_KEY")
        self.__full_ws_access = os.getenv("FULLACCESS") is not None

    def __create_loop(self, coro) -> None:
        """Function that creates an event loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(coro())
        loop.close()

    async def __wait(self, seconds: float = 1.0) -> None:
        """Function that realizes the wait for ``seconds``."""
        start = time.time()
        while time.time() - seconds < start:
            await asyncio.sleep(0.2)
        return

    @pytest.mark.futures
    @pytest.mark.futures_websocket
    def test_create_public_bot(self) -> None:
        """
        Checks if the unauthenticated websocket client
        can be instantiated.
        """

        async def create_bot() -> None:
            bot = Bot()
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_auth
    @pytest.mark.futures_websocket
    def test_create_private_bot(self) -> None:
        """
        Checks if the authenticated websocket client
        can be instantiated.
        """

        async def create_bot() -> None:
            Bot(key=self.__key, secret=self.__secret)
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_websocket
    def test_get_subscriptions(self) -> None:
        """
        Checks the ``get_subscriptions`` function.
        """

        async def create_bot() -> None:
            bot = Bot()
            bot.get_active_subscriptions
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_websocket
    def test_get_available_public_subscriptions(self) -> None:
        """
        Checks the ``get_available_public_subscriptions`` function.
        """

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

    @pytest.mark.futures
    @pytest.mark.futures_websocket
    def test_get_available_private_subscriptions(self) -> None:
        """
        Checks the ``get_available_private_subscriptions`` function.
        """

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

    @pytest.mark.futures
    @pytest.mark.futures_auth
    @pytest.mark.futures_websocket
    def test_get_auth_state(self) -> None:
        """
        Checks if the ``is_auth`` attribute is set correctly.
        """

        async def create_bot() -> None:
            bot = Bot()
            assert not bot.is_auth

            auth_bot = Bot(key=self.__key, secret=self.__secret)
            assert auth_bot.is_auth

            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_websocket
    def test_subscribe_public(self) -> None:
        """
        Checks if the unauthenticated websocket client is able to subscribe
        to public feeds.
        """

        async def create_bot() -> None:
            bot = Bot()
            products = ["PI_XBTUSD", "PF_SOLUSD"]

            with pytest.raises(ValueError):  # products must be List[str]
                await bot.subscribe(feed="ticker", products="PI_XBTUSD")

            await bot.subscribe(feed="heartbeat")
            await bot.subscribe(feed="ticker", products=products)
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_auth
    @pytest.mark.futures_websocket
    def test_subscribe_private(self) -> None:
        """
        Checks if the authenticated websocket client is able to subscribe
        to private feeds.
        """

        async def create_bot() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)

            with pytest.raises(
                ValueError
            ):  # private subscriptions does not use products
                await auth_bot.subscribe(feed="fills", products=["PI_XBTUSD"])

            await auth_bot.subscribe(feed="open_orders")
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_websocket
    def test_unsubsribe_public(self) -> None:
        """
        Checks if the unauthenticated websocket client is able to unsubscribe
        from public feeds.
        """

        async def create_bot() -> None:
            bot = Bot()
            products = ["PI_XBTUSD", "PF_SOLUSD"]

            with pytest.raises(ValueError):  # products must be type List[str]
                await bot.unsubscribe(feed="ticker", products="PI_XBTUSD")

            await bot.subscribe(feed="ticker", products=products)
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_auth
    @pytest.mark.futures_websocket
    def test_unsubscribe_private(self) -> None:
        """
        Checks if the authenticated websocket client is able to unsubscribe
        from private feeds.
        """

        async def create_bot() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)

            with pytest.raises(
                ValueError
            ):  # private un/-subscriptions does not accept a product
                await auth_bot.unsubscribe(feed="open_orders", products=["PI_XBTUSD"])

            await auth_bot.unsubscribe(feed="open_orders")
            await self.__wait(2)

        self.__create_loop(coro=create_bot)

    @pytest.mark.futures
    @pytest.mark.futures_websocket
    def test_get_active_subscriptions(self) -> None:
        """
        Checks the ``get_active_subscriptions`` function.
        """

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
