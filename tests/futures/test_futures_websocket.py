#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures websocket client"""

from __future__ import annotations

import asyncio
from typing import Any, List

import pytest

from .helper import FuturesWebsocketClientTestWrapper, async_wait


@pytest.mark.futures()
@pytest.mark.futures_websocket()
def test_create_public_client(caplog: Any) -> None:
    """
    Checks if the unauthenticated websocket client
    can be instantiated.
    """

    async def instantiate_client() -> None:
        client: FuturesWebsocketClientTestWrapper = FuturesWebsocketClientTestWrapper()
        await async_wait(5)

        assert not client.is_auth

    asyncio.run(instantiate_client())

    assert "{'event': 'info', 'version': 1}" in caplog.text


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_websocket()
def test_create_private_client(
    futures_api_key: str,
    futures_secret_key: str,
    caplog: Any,
) -> None:
    """
    Checks if the authenticated websocket client
    can be instantiated.
    """

    async def instantiate_client() -> None:
        client: FuturesWebsocketClientTestWrapper = FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        )
        assert client.is_auth
        await async_wait(5)

    asyncio.run(instantiate_client())

    assert "{'event': 'info', 'version': 1}" in caplog.text


@pytest.mark.futures()
@pytest.mark.futures_websocket()
def test_get_available_public_subscriptions() -> None:
    """
    Checks the ``get_available_public_subscription_feeds`` function.
    """

    expected: List[str] = [
        "trade",
        "book",
        "ticker",
        "ticker_lite",
        "heartbeat",
    ]
    assert all(
        feed in expected
        for feed in FuturesWebsocketClientTestWrapper.get_available_public_subscription_feeds()
    )


@pytest.mark.futures()
@pytest.mark.futures_websocket()
def test_get_available_private_subscriptions() -> None:
    """
    Checks the ``get_available_private_subscription_feeds`` function.
    """

    expected: List[str] = [
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
    assert all(
        feed in expected
        for feed in FuturesWebsocketClientTestWrapper.get_available_private_subscription_feeds()
    )


@pytest.mark.futures()
@pytest.mark.futures_websocket()
def test_subscribe_public(caplog: Any) -> None:
    """
    Checks if the client is able to subscribe to a public feed.
    """

    async def check_subscription() -> None:
        client: FuturesWebsocketClientTestWrapper = FuturesWebsocketClientTestWrapper()
        await async_wait(2)

        with pytest.raises(
            TypeError,
            match=r"Parameter products must be type of list\[str\] \(e.g. products=\[\"PI_XBTUSD\"\]\)",
        ):
            await client.subscribe(feed="ticker", products="PI_XBTUSD")  # type: ignore[arg-type]

        await client.subscribe(feed="ticker", products=["PI_XBTUSD", "PF_SOLUSD"])
        await async_wait(seconds=2)

        subs: List[dict] = client.get_active_subscriptions()
        assert isinstance(subs, list)

        expected_subscriptions: List[dict] = [
            {"event": "subscribe", "feed": "ticker", "product_ids": ["PI_XBTUSD"]},
            {"event": "subscribe", "feed": "ticker", "product_ids": ["PF_SOLUSD"]},
        ]
        assert all(sub in subs for sub in expected_subscriptions)

    asyncio.run(check_subscription())

    for expected in (
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PF_SOLUSD']}",
    ):
        assert expected in caplog.text


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_websocket()
def test_subscribe_private(
    futures_api_key: str,
    futures_secret_key: str,
    caplog: Any,
) -> None:
    """
    Checks if the authenticated websocket client is able to subscribe
    to private feeds.
    """

    async def submit_subscription() -> None:
        client: FuturesWebsocketClientTestWrapper = FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        )

        with pytest.raises(
            ValueError,
            match=r"There is no private feed that accepts products!",
        ):
            await client.subscribe(feed="fills", products=["PI_XBTUSD"])

        await client.subscribe(feed="open_orders")
        await async_wait(2)

    asyncio.run(submit_subscription())

    for expected in (
        "{'event': 'subscribed', 'feed': 'open_orders'}",
        "{'feed': 'open_orders_snapshot', 'account':",
    ):
        assert expected in caplog.text


@pytest.mark.futures()
@pytest.mark.futures_websocket()
def test_unsubscribe_public(caplog: Any) -> None:
    """
    Checks if the unauthenticated websocket client is able to unsubscribe
    from public feeds.
    """

    async def execute_unsubscribe() -> None:
        client: FuturesWebsocketClientTestWrapper = FuturesWebsocketClientTestWrapper()
        products: List[str] = ["PI_XBTUSD", "PF_SOLUSD"]

        await client.subscribe(feed="ticker", products=products)
        await async_wait(seconds=2)

        with pytest.raises(
            TypeError,
            match=r"Parameter products must be type of list\[str\ ",
        ):
            await client.unsubscribe(feed="ticker", products="PI_XBTUSD")  # type: ignore[arg-type]

        await client.unsubscribe(feed="ticker", products=products)
        await async_wait(seconds=2)

    asyncio.run(execute_unsubscribe())

    for expected in (
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PF_SOLUSD']}",
        "{'event': 'unsubscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
        "{'event': 'unsubscribed', 'feed': 'ticker', 'product_ids': ['PF_SOLUSD']}",
    ):
        assert expected in caplog.text


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_websocket()
def test_unsubscribe_private(
    futures_api_key: str,
    futures_secret_key: str,
    caplog: Any,
) -> None:
    """
    Checks if the authenticated websocket client is able to unsubscribe
    from private feeds.
    """

    async def execute_unsubscribe() -> None:
        client: FuturesWebsocketClientTestWrapper = FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        )
        await client.subscribe(feed="open_orders")

        await async_wait(seconds=2)
        with pytest.raises(
            ValueError,
            match=r"There is no private feed that accepts products!",
        ):
            await client.unsubscribe(feed="open_orders", products=["PI_XBTUSD"])

        await client.unsubscribe(feed="open_orders")
        await async_wait(seconds=2)

    asyncio.run(execute_unsubscribe())

    for expected in (
        "{'event': 'subscribed', 'feed': 'open_orders'}",
        "{'event': 'unsubscribed', 'feed': 'open_orders'}",
    ):
        assert expected in caplog.text


@pytest.mark.futures()
@pytest.mark.futures_websocket()
def test_get_active_subscriptions(caplog: Any) -> None:
    """
    Checks the ``get_active_subscriptions`` function.
    """

    async def check_subscriptions() -> None:
        client: FuturesWebsocketClientTestWrapper = FuturesWebsocketClientTestWrapper()
        assert client.get_active_subscriptions() == []
        await async_wait(seconds=1)

        await client.subscribe(feed="ticker", products=["PI_XBTUSD"])
        await async_wait(seconds=1)
        assert len(client.get_active_subscriptions()) == 1

        await client.unsubscribe(feed="ticker", products=["PI_XBTUSD"])
        await async_wait(seconds=1)
        assert client.get_active_subscriptions() == []

    asyncio.run(check_subscriptions())

    for expected in (
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
        "{'event': 'unsubscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
    ):
        assert expected in caplog.text
