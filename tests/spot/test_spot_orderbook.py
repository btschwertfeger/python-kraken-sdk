#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that implements the unit tests regarding the Spot Orderbook client.
"""

import asyncio
import json
import os
from collections import OrderedDict
from typing import Any, Optional
from unittest import mock

import pytest

from kraken.spot import OrderbookClient

from .helper import FIXTURE_DIR, OrderbookClientWrapper, async_wait


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_orderbook
def test_create_public_bot(caplog: Any) -> None:
    """
    Checks if the websocket client can be instantiated.
    """

    async def create_bot() -> None:
        orderbook: OrderbookClientWrapper = OrderbookClientWrapper()
        await async_wait(seconds=4)

        assert orderbook.depth == 10

    asyncio.run(create_bot())

    for expected in (
        "'connectionID",
        "'event': 'systemStatus', 'status': 'online'",
        "'event': 'pong', 'reqid':",
    ):
        assert expected in caplog.text
    assert "Kraken websockets at full capacity, try again later" not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_orderbook
def test_get_first() -> None:
    """
    Checks the ``get_first`` method.
    """

    assert (
        float(10)
        == OrderbookClientWrapper.get_first(("10", "5"))
        == OrderbookClientWrapper.get_first((10, 5))
    )


@mock.patch("kraken.spot.orderbook.KrakenSpotWSClient", return_value=None)
@pytest.mark.spot
@pytest.mark.spot_orderbook
def test_assing_msg_and_validate_checksum(mock_ws_client: mock.MagicMock) -> None:
    """
    This function checks if the initial snapshot and the book updates are
    assigned correctly so that the checksum calculation can validate the
    assigned book updates and values.
    """
    with open(
        os.path.join(FIXTURE_DIR, "orderbook.json"), "r", encoding="utf-8"
    ) as json_file:
        orderbook: dict = json.load(json_file)

    async def assign() -> None:
        client: OrderbookClient = OrderbookClient(depth=10)

        await client.on_message(msg=orderbook["init"])
        assert client.get(pair="XBT/USD")["valid"]

        for update in orderbook["updates"]:
            await client.on_message(msg=update)
            assert client.get(pair="XBT/USD")["valid"]

    asyncio.run(assign())


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_orderbook
def test_add_book(caplog: Any) -> None:
    """
    Checks if the orderbook client is able to add a book by subscribing.
    The logs are then checked for the expected results.
    """

    async def execute_add_book() -> None:
        orderbook: OrderbookClientWrapper = OrderbookClientWrapper()

        await orderbook.add_book(pairs=["XBT/USD"])
        await async_wait(seconds=2)

        book: Optional[dict] = orderbook.get(pair="XBT/USD")
        assert isinstance(book, dict)

        assert all(key in book for key in ("ask", "bid", "valid")), book

        assert isinstance(book["ask"], OrderedDict)
        assert isinstance(book["bid"], OrderedDict)

        for ask, bid in zip(book["ask"], book["bid"]):
            assert isinstance(ask, str)
            assert isinstance(bid, str)

    asyncio.run(execute_add_book())

    for expected in (
        "'channelName': 'book-10', 'event': 'subscriptionStatus', 'pair': 'XBT/USD', 'reqid':",
        "'status': 'subscribed', 'subscription': {'depth': 10, 'name': 'book'}}",
    ):
        assert expected in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_orderbook
def test_remove_book(caplog: Any) -> None:
    """
    Checks if the orderbook client is able to add a book by subscribing to a book
    and unsubscribing right after + validating using the logs.
    """

    async def execute_remove_book() -> None:
        orderbook: OrderbookClientWrapper = OrderbookClientWrapper()

        await orderbook.add_book(pairs=["XBT/USD"])
        await async_wait(seconds=2)

        await orderbook.remove_book(pairs=["XBT/USD"])
        await async_wait(seconds=2)

    asyncio.run(execute_remove_book())

    for expected in (
        "'channelName': 'book-10', 'event': 'subscriptionStatus', 'pair': 'XBT/USD', 'reqid':",
        "'status': 'subscribed', 'subscription': {'depth': 10, 'name': 'book'}}",
        "'status': 'unsubscribed', 'subscription': {'depth': 10, 'name': 'book'}}",
    ):
        assert expected in caplog.text
