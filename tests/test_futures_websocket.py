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
            f.write(log + "\n" + str(event))


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
        async def create_bot():
            bot = Bot()
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    def test_create_private_bot(self) -> None:
        async def create_bot():
            Bot(key=self.__key, secret=self.__secret)
            await self.__wait(1.5)

        self.__create_loop(coro=create_bot)

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
