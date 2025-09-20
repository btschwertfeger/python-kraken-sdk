# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module that implements the unit tests regarding the Spot Orderbook client.
"""

from __future__ import annotations

import asyncio
import json
from asyncio import sleep as async_sleep
from collections import OrderedDict
from typing import TYPE_CHECKING, Self
from unittest import mock

import pytest

from kraken.spot import SpotOrderBookClient

from .helper import FIXTURE_DIR, SpotOrderBookClientWrapper

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_orderbook
class TestSpotOrderBook:
    """Test class for Spot Orderbook client functionality."""

    TEST_PAIR_BTCUSD = "BTC/USD"
    TEST_PAIR_DOTUSD = "DOT/USD"
    TEST_PAIR_ETHUSD = "ETH/USD"
    TEST_PAIR_MATICUSD = "MATIC/USD"
    TEST_PAIR_BTCEUR = "BTC/EUR"
    TEST_DEPTH = 10

    def test_create_public_bot(self: Self, caplog: pytest.LogCaptureFixture) -> None:
        """
        Checks if the websocket client can be instantiated.
        """

        async def create_bot() -> None:
            async with SpotOrderBookClientWrapper() as orderbook:
                await async_sleep(10)
                assert orderbook.depth == self.TEST_DEPTH

        asyncio.run(create_bot())

        for expected in (
            'channel": "status"',
            '"api_version": "v2"',
            '"system": "online",',
            '"type": "update"',
        ):
            assert expected in caplog.text

    def test_get_first(self) -> None:
        """
        Checks the ``get_first`` method.
        """
        assert (
            float(10)
            == SpotOrderBookClientWrapper.get_first(("10", "5"))
            == SpotOrderBookClientWrapper.get_first((10, 5))
        )

    @mock.patch("kraken.spot.orderbook.SpotWSClient", return_value=None)
    @mock.patch(
        "kraken.spot.orderbook.SpotOrderBookClient.remove_book",
        return_value=mock.AsyncMock(),
    )
    @mock.patch(
        "kraken.spot.orderbook.SpotOrderBookClient.add_book",
        return_value=mock.AsyncMock(),
    )
    def test_passing_msg_and_validate_checksum(
        self: Self,
        mock_add_book: mock.MagicMock,  # noqa: ARG002
        mock_remove_book: mock.MagicMock,  # noqa: ARG002
        mock_ws_client: mock.MagicMock,  # noqa: ARG002
    ) -> None:
        """
        This function checks if the initial snapshot and the book updates are
        assigned correctly so that the checksum calculation can validate the
        assigned book updates and values.
        """
        json_file_path: Path = FIXTURE_DIR / "orderbook-v2.json"
        with json_file_path.open("r", encoding="utf-8") as json_file:
            orderbook: dict = json.load(json_file)

        async def assign() -> None:
            client: SpotOrderBookClient = SpotOrderBookClient(depth=self.TEST_DEPTH)
            # starting the client is not necessary for this test

            await client.on_message(message=orderbook["init"])
            assert client.get(pair=self.TEST_PAIR_BTCUSD)["valid"]

            for update in orderbook["updates"]:
                await client.on_message(message=update)
                assert client.get(pair=self.TEST_PAIR_BTCUSD)["valid"]

            bad_message: dict = {
                "channel": "book",
                "type": "update",
                "data": [
                    {
                        "symbol": self.TEST_PAIR_BTCUSD,
                        "bids": [{"price": 29430.3, "qty": 1.69289565}],
                        "asks": [],
                        "checksum": 2438868880,
                        "timestamp": "2023-07-30T15:30:49.008834Z",
                    },
                ],
            }
            await client.on_message(message=bad_message)
            assert not client.get(pair=self.TEST_PAIR_BTCUSD)["valid"]

        asyncio.run(assign())

    def test_add_book(self: Self, caplog: pytest.LogCaptureFixture) -> None:
        """
        Checks if the orderbook client is able to add a book by subscribing.
        The logs are then checked for the expected results.
        """

        async def execute_add_book() -> None:
            async with SpotOrderBookClientWrapper() as orderbook:
                await orderbook.add_book(
                    pairs=[
                        self.TEST_PAIR_BTCUSD,
                        self.TEST_PAIR_DOTUSD,
                        self.TEST_PAIR_ETHUSD,
                        self.TEST_PAIR_MATICUSD,
                        self.TEST_PAIR_BTCEUR,
                    ],
                )
                await async_sleep(4)

                book: dict | None = orderbook.get(pair=self.TEST_PAIR_BTCUSD)
                assert isinstance(book, dict)

                assert all(
                    key in book
                    for key in ("ask", "bid", "valid", "price_decimals", "qty_decimals")
                ), book

                assert isinstance(book["ask"], OrderedDict)
                assert isinstance(book["bid"], OrderedDict)

                for ask, bid in zip(book["ask"], book["bid"], strict=True):
                    assert isinstance(ask, str)
                    assert isinstance(bid, str)

        asyncio.run(execute_add_book())

        for expected in (
            '{"method": "subscribe", "result": {"channel": "book", "depth": 10, '
            '"snapshot": true, "symbol": "BTC/USD"}, "success": true, "time_in": ',
            '{"channel": "book", "type": "snapshot", "data": '
            '[{"symbol": "BTC/USD", "bids": ',
        ):
            assert expected in caplog.text

    def test_remove_book(self: Self, caplog: pytest.LogCaptureFixture) -> None:
        """
        Checks if the orderbook client is able to add a book by subscribing to a book
        and unsubscribing right after + validating using the logs.
        """

        async def execute_remove_book() -> None:
            async with SpotOrderBookClientWrapper() as orderbook:
                await orderbook.add_book(pairs=[self.TEST_PAIR_BTCUSD])
                await async_sleep(2)

                await orderbook.remove_book(pairs=[self.TEST_PAIR_BTCUSD])
                await async_sleep(2)

        asyncio.run(execute_remove_book())

        assert (
            '{"method": "unsubscribe", "result": {"channel": "book", "depth": 10, "symbol": "BTC/USD"}, "success": true, "time_in":'
            in caplog.text
        )
