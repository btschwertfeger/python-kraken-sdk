#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that implements the unit tests regarding the Spot Orderbook client.
"""

from __future__ import annotations

import asyncio
import json
import os
from collections import OrderedDict
from typing import Any, Optional
from unittest import mock

import pytest

from kraken.spot import OrderbookClientV2

from .helper import FIXTURE_DIR, OrderbookClientV2Wrapper, async_wait


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_orderbook()
def test_create_public_bot(caplog: Any) -> None:
    """
    Checks if the websocket client can be instantiated.
    """

    async def create_bot() -> None:
        orderbook: OrderbookClientV2Wrapper = OrderbookClientV2Wrapper()
        await async_wait(seconds=4)

        assert orderbook.depth == 10

    asyncio.run(create_bot())

    for expected in (
        'channel": "status"',
        '"api_version": "v2"',
        '"system": "online", "version": "2.',
        '"type": "update"',
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_orderbook()
def test_get_first() -> None:
    """
    Checks the ``get_first`` method.
    """

    assert (
        float(10)
        == OrderbookClientV2Wrapper.get_first(("10", "5"))
        == OrderbookClientV2Wrapper.get_first((10, 5))
    )


@pytest.mark.wip()
@pytest.mark.spot()
@pytest.mark.spot_orderbook()
@mock.patch("kraken.spot.orderbook_v2.KrakenSpotWSClientV2", return_value=None)
@mock.patch(
    "kraken.spot.orderbook_v2.OrderbookClientV2.remove_book",
    return_value=mock.AsyncMock(),
)
@mock.patch(
    "kraken.spot.orderbook_v2.OrderbookClientV2.add_book",
    return_value=mock.AsyncMock(),
)
def test_passing_msg_and_validate_checksum(
    mock_add_book: mock.MagicMock,  # noqa: ARG001
    mock_remove_bookv,  # noqa: ARG001
    mock_ws_client: mock.MagicMock,  # noqa: ARG001
) -> None:
    """
    This function checks if the initial snapshot and the book updates are
    assigned correctly so that the checksum calculation can validate the
    assigned book updates and values.
    """
    with open(
        os.path.join(FIXTURE_DIR, "orderbook-v2.json"),
        "r",
        encoding="utf-8",
    ) as json_file:
        orderbook: dict = json.load(json_file)

    async def assign() -> None:
        client: OrderbookClientV2 = OrderbookClientV2(depth=10)

        await client.on_message(message=orderbook["init"])
        assert client.get(pair="BTC/USD")["valid"]

        for update in orderbook["updates"]:
            await client.on_message(message=update)
            assert client.get(pair="BTC/USD")["valid"]

        bad_message: dict = {
            "channel": "book",
            "type": "update",
            "data": [
                {
                    "symbol": "BTC/USD",
                    "bids": [{"price": 29430.3, "qty": 1.69289565}],
                    "asks": [],
                    "checksum": 2438868880,
                    "timestamp": "2023-07-30T15:30:49.008834Z",
                },
            ],
        }
        await client.on_message(message=bad_message)
        assert not client.get(pair="BTC/USD")["valid"]

    asyncio.run(assign())


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_orderbook()
def test_add_book(caplog: Any) -> None:
    """
    Checks if the orderbook client is able to add a book by subscribing.
    The logs are then checked for the expected results.
    """

    async def execute_add_book() -> None:
        orderbook: OrderbookClientV2Wrapper = OrderbookClientV2Wrapper()

        await orderbook.add_book(pairs=["BTC/USD"])
        await async_wait(seconds=2)

        book: Optional[dict] = orderbook.get(pair="BTC/USD")
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
        '{"method": "subscribe", "result": {"channel": "book", "depth": 10, "snapshot": true, "symbol": "BTC/USD"}, "success": true, "time_in": ',
        '{"channel": "book", "type": "snapshot", "data": [{"symbol": "BTC/USD", "bids": ',
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_orderbook()
def test_remove_book(caplog: Any) -> None:
    """
    Checks if the orderbook client is able to add a book by subscribing to a book
    and unsubscribing right after + validating using the logs.
    """

    async def execute_remove_book() -> None:
        orderbook: OrderbookClientV2Wrapper = OrderbookClientV2Wrapper()

        await orderbook.add_book(pairs=["BTC/USD"])
        await async_wait(seconds=2)

        await orderbook.remove_book(pairs=["BTC/USD"])
        await async_wait(seconds=2)

    asyncio.run(execute_remove_book())

    assert (
        '{"method": "unsubscribe", "result": {"channel": "book", "depth": 10, "symbol": "BTC/USD"}, "success": true, "time_in":'
        in caplog.text
    )
