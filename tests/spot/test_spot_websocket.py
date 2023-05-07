#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that tests the Kraken Spot websocket client
NOTE:
*   Since there is no sandbox environment for the Spot trading API,
    some tests are adjusted, so that there is a `validate` switch to not risk funds.
*   Also there is a KrakenPermissionDeniedError class which will be raised when
    the websocket client receives a message about missing auhtntification. Since the
    API keys have no trade permission, this will be excepted to exit the asyncio event loop.
    A asyncio.CancelledError will be raised and excepted during this procedure.

todo: Create fixtures for the custom exception and the Bot class.
"""

import asyncio
import os
import time
import unittest

import pytest

from kraken.spot import KrakenSpotWSClient


class KrakenPermissionDeniedError(Exception):
    """This Error will cancel the ws connection by closing the event loop
    asyncio.CancelledError will be raised
    """

    def __init__(self):
        try:
            pending = asyncio.all_tasks()
            for task in pending:
                task.cancel()

            loop = asyncio.get_event_loop()
            loop.run(self.kill_pending_tasks(pending))
        except AttributeError:
            # AttributeError: '_UnixSelectorEventLoop' object has no attribute 'run'
            # when there is no event loop
            pass

    @classmethod
    async def kill_pending_tasks(cls, tasks) -> None:
        await asyncio.gather(tasks, return_exceptions=True)


class Bot(KrakenSpotWSClient):
    """Class to create a websocket bot"""

    async def on_message(self, event) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        # The following comments are only used for debugging while
        # implementing tests.
        # log = ""
        # try:
        #     with open("spot_ws_log.log", "r", encoding="utf-8") as f:
        #         log = f.read()
        # except FileNotFoundError:
        #     pass

        # with open("spot_ws_log.log", "w", encoding="utf-8") as f:
        #     f.write(log + "\n" + str(event))

        if isinstance(event, dict) and "error" in event.keys():
            if "KrakenPermissionDeniedError" in event["error"]:
                raise KrakenPermissionDeniedError()


class WebsocketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__key = os.getenv("SPOT_API_KEY")
        self.__secret = os.getenv("SPOT_SECRET_KEY")
        self.__full_ws_access = os.getenv("FULLACCESS") == "True"

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

    @pytest.mark.spot
    @pytest.mark.spot_websocket
    def test_create_public_bot(self) -> None:
        """
        Checks if the websocket client can be instantiated.
        """

        async def create_bot():
            bot = Bot()
            await self.__wait(seconds=2.5)

        self.__create_loop(coro=create_bot)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    def test_create_private_bot(self) -> None:
        """
        Checks if the authenticated websocket client can be instantiated.
        """

        async def create_bot():
            if self.__full_ws_access:
                Bot(key=self.__key, secret=self.__secret)
                await self.__wait(seconds=2.5)
            else:
                # with pytest.raises(asyncio.CancelledError):
                Bot(key=self.__key, secret=self.__secret)
                await self.__wait(seconds=2.5)

        self.__create_loop(coro=create_bot)

    @pytest.mark.spot
    @pytest.mark.spot_websocket
    def test_access_public_bot_attributes(self) -> None:
        """
        Checks the ``access_public_bot_attributes`` function
        works as expected.
        """

        async def checkit() -> None:
            bot = Bot()

            assert bot.private_sub_names == ["ownTrades", "openOrders"]
            assert bot.public_sub_names == [
                "ticker",
                "spread",
                "book",
                "ohlc",
                "trade",
                "*",
            ]
            assert bot.active_public_subscriptions == []
            await self.__wait(seconds=1)
            with pytest.raises(ConnectionError):
                # cannot access private subscriptions on unauthenticated client
                bot.active_private_subscriptions

            await self.__wait(seconds=1.5)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    def test_access_private_bot_attributes(self) -> None:
        """
        Checks the ``access_private_bot_attributes`` function
        works as expected.
        """

        async def checkit() -> None:
            if self.__full_ws_access:
                auth_bot = Bot(key=self.__key, secret=self.__secret)
                assert auth_bot.active_private_subscriptions == []
                await self.__wait(seconds=2.5)
            else:
                # with pytest.raises(asyncio.CancelledError):
                auth_bot = Bot(key=self.__key, secret=self.__secret)
                assert auth_bot.active_private_subscriptions == []
                await self.__wait(seconds=2.5)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_websocket
    def test_public_subscribe(self) -> None:
        """
        Function that checks if the websocket client
        is able to subscribe to public feeds.
        """

        async def checkit() -> None:
            bot = Bot()
            subscription = {"name": "ticker"}

            with pytest.raises(AttributeError):
                await bot.subscribe(subscription={})

            with pytest.raises(ValueError):
                await bot.subscribe(subscription=subscription, pair="XBT/USD")

            await bot.subscribe(subscription=subscription, pair=["XBT/EUR"])
            await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    def test_private_subscribe(self) -> None:
        """
        Checks if the authenticated websocket client can subscribe to private feeds.
        """

        async def checkit() -> None:
            subscription = {"name": "ownTrades"}

            bot = Bot()
            with pytest.raises(ValueError):  # unauthenticated
                await bot.subscribe(subscription=subscription)
            with pytest.raises(ValueError):  # unauthenticated and pair and pair is list
                await bot.subscribe(subscription=subscription, pair=["XBT/EUR"])

            auth_bot = Bot(key=self.__key, secret=self.__secret)
            with pytest.raises(ValueError):  # private conns does not accept pairs
                await auth_bot.subscribe(subscription=subscription, pair=["XBT/EUR"])
                await self.__wait(seconds=1)

            if self.__full_ws_access:
                await auth_bot.subscribe(subscription=subscription)
                await self.__wait(seconds=2)
            else:
                # with pytest.raises(asyncio.CancelledError):
                await auth_bot.subscribe(subscription=subscription)
                await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_websocket
    def test_public_unsubscribe(self) -> None:
        """
        Checks if the websocket client can unsubscrube from public feeds.
        """

        async def checkit() -> None:
            bot = Bot()

            # since we have no subscriptions, this will work, but the response will inform us that there are no subscriptions
            await bot.unsubscribe(subscription={"name": "ticker"}, pair=["XBT/USD"])
            await bot.unsubscribe(
                subscription={"name": "ticker"}, pair=["DOT/USD", "ETH/USD"]
            )

            await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_websocket
    def test_public_unsubscribe_failure(self) -> None:
        """
        Checks if the websocket client responses with failures
        when the ``unsubscribe`` funciton receives invalid parameters.
        """

        async def checkit() -> None:
            bot = Bot()

            with pytest.raises(AttributeError):
                await bot.unsubscribe(subscription={})

            with pytest.raises(ValueError):
                await bot.unsubscribe(subscription={"name": "ticker"}, pair="XBT/USD")

            await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    def test_private_unsubscribe(self) -> None:
        async def checkit() -> None:
            bot = Bot()
            auth_bot = Bot(key=self.__key, secret=self.__secret)

            if self.__full_ws_access:
                await auth_bot.unsubscribe(subscription={"name": "ownTrades"})
            else:
                # with pytest.raises(asyncio.CancelledError):
                await auth_bot.unsubscribe(subscription={"name": "ownTrades"})
            await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    def test_private_unsubscribe_failing(self) -> None:
        """
        Checks if the ``unsubscribe`` function fails when invalid
        parameters are passed.
        """

        async def checkit() -> None:
            bot = Bot()
            auth_bot = Bot(key=self.__key, secret=self.__secret)

            with pytest.raises(ValueError):  # private feed on unauthenticated client
                await bot.unsubscribe(subscription={"name": "ownTrades"})

            with pytest.raises(ValueError):
                await auth_bot.unsubscribe(  # private subscriptions does not have a pair
                    subscription={"name": "ownTrades"}, pair=["XBTUSD"]
                )

            await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    def test_create_order(self) -> None:
        """
        Checks the ``create_order`` function by submitting a
        new order - but in validate mode.
        """

        async def checkit() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)
            params = dict(
                ordertype="limit",
                side="buy",
                pair="XBT/USD",
                volume="2",
                price="1000",
                price2="1200",
                leverage="2",
                oflags="viqc",
                starttm="0",
                expiretm="1000",
                userref="12345678",
                validate=True,
                close_ordertype="limit",
                close_price="1000",
                close_price2="1200",
                timeinforce="GTC",
            )
            if self.__full_ws_access:
                await auth_bot.create_order(**params)
                await self.__wait(seconds=2)
            else:
                # with pytest.raises(asyncio.CancelledError):
                await auth_bot.create_order(**params)
                await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    def test_edit_order(self) -> None:
        """
        Checks the edit order function by editing an order in validate mode.
        """

        async def checkit() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)

            params = dict(
                orderid="OHSAUDZ-ASJKGD-EPAFUIH",
                reqid=1244,
                pair="XBT/USD",
                price="120",
                price2="1300",
                oflags="fok",
                newuserref="833773",
                validate=True,
            )

            if self.__full_ws_access:
                await auth_bot.edit_order(**params)
                await self.__wait(seconds=2)
            else:
                # with pytest.raises(asyncio.CancelledError):
                await auth_bot.edit_order(**params)
                await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    @unittest.skip("CI does not have trade/cancel permission")
    def test_cancel_order(self) -> None:
        """
        Checks the ``cancel_order`` function by canceling some orders.
        """

        async def checkit() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)
            if self.__full_ws_access:
                await auth_bot.cancel_order(txid="AOUEHF-ASLBD-A6B4A")
                await self.__wait(seconds=2)
            else:
                # with pytest.raises(asyncio.CancelledError):
                await auth_bot.cancel_order(txid="AOUEHF-ASLBD-A6B4A")
                await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    @unittest.skip("CI does not have trade/cancel permission")
    def test_cancel_all_orders(self) -> None:
        """
        Check the ``cancel_all_orders`` function by executing the function.
        """

        async def checkit() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)
            if self.__full_ws_access:
                await auth_bot.cancel_all_orders()
                await self.__wait(seconds=2)
            else:
                # with pytest.raises(asyncio.CancelledError):
                await auth_bot.cancel_all_orders()
                await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    @pytest.mark.spot
    @pytest.mark.spot_auth
    @pytest.mark.spot_websocket
    @unittest.skip("CI does not have trade/cancel permission")
    def test_cancel_all_orders_after(self) -> None:
        """
        Checking the ``cancel_all_orders_after`` function by
        executing it.
        """

        async def checkit() -> None:
            auth_bot = Bot(key=self.__key, secret=self.__secret)
            if self.__full_ws_access:
                await auth_bot.cancel_all_orders_after(0)
                await self.__wait(seconds=2)
            else:
                # with pytest.raises(asyncio.CancelledError):
                await auth_bot.cancel_all_orders_after(0)
                await self.__wait(seconds=2)

        self.__create_loop(coro=checkit)

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    asyncio.run(unittest.main)
