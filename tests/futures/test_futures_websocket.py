# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures websocket client"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

from asyncio import sleep as async_sleep

import pytest

from .helper import FuturesWebsocketClientTestWrapper


@pytest.mark.futures
@pytest.mark.futures_websocket
def test_create_public_client(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks if the unauthenticated websocket client
    can be instantiated.
    """

    async def instantiate_client() -> None:
        client = FuturesWebsocketClientTestWrapper()
        await client.start()
        await async_sleep(4)
        assert not client.is_auth
        await client.close()
        await async_sleep(2)

    asyncio.run(instantiate_client())

    assert "{'event': 'info', 'version': 1}" in caplog.text


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_websocket
def test_create_private_client(
    futures_api_key: str,
    futures_secret_key: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Checks if the authenticated websocket client
    can be instantiated.
    """

    async def instantiate_client() -> None:
        async with FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        ) as client:
            assert client.is_auth
            await async_sleep(4)

    asyncio.run(instantiate_client())

    assert "{'event': 'info', 'version': 1}" in caplog.text


@pytest.mark.futures
@pytest.mark.futures_websocket
def test_get_available_public_subscriptions() -> None:
    """
    Checks the ``get_available_public_subscription_feeds`` function.
    """

    expected: list[str] = [
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


@pytest.mark.futures
@pytest.mark.futures_websocket
def test_get_available_private_subscriptions() -> None:
    """
    Checks the ``get_available_private_subscription_feeds`` function.
    """

    expected: list[str] = [
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


@pytest.mark.futures
@pytest.mark.futures_websocket
def test_subscribe_public(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks if the client is able to subscribe to a public feed.
    """

    async def check_subscription() -> None:
        async with FuturesWebsocketClientTestWrapper() as client:
            with pytest.raises(
                TypeError,
                match=r"Parameter products must be type of list\[str\] \(e.g. products=\[\"PI_XBTUSD\"\]\)",
            ):
                await client.subscribe(feed="ticker", products="PI_XBTUSD")  # type: ignore[arg-type]

        async with FuturesWebsocketClientTestWrapper() as client:
            await client.subscribe(feed="ticker", products=["PI_XBTUSD", "PF_SOLUSD"])
            await async_sleep(2)

            subs: list[dict] = client.get_active_subscriptions()
            assert isinstance(subs, list)

            expected_subscriptions: list[dict] = [
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


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_websocket
def test_subscribe_private(
    futures_api_key: str,
    futures_secret_key: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Checks if the authenticated websocket client is able to subscribe
    to private feeds.
    """

    async def submit_subscription() -> None:
        async with FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        ) as client:
            with pytest.raises(
                ValueError,
                match=r"There is no private feed that accepts products!",
            ):
                await client.subscribe(feed="fills", products=["PI_XBTUSD"])

        async with FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        ) as client:
            await client.subscribe(feed="open_orders")
            await async_sleep(2)

            assert len(client.get_active_subscriptions()) == 1

    asyncio.run(submit_subscription())

    for expected in (
        "{'event': 'subscribed', 'feed': 'open_orders'}",
        "{'feed': 'open_orders_snapshot', 'account':",
    ):
        assert expected in caplog.text


@pytest.mark.futures
@pytest.mark.futures_websocket
def test_unsubscribe_public(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks if the unauthenticated websocket client is able to unsubscribe
    from public feeds.
    """

    async def execute_unsubscribe() -> None:
        products: list[str] = ["PI_XBTUSD", "PF_SOLUSD"]
        async with FuturesWebsocketClientTestWrapper() as client:
            await client.subscribe(feed="ticker", products=products)
            await async_sleep(2)

            await client.unsubscribe(feed="ticker", products=products)
            await async_sleep(2)  # need to get the message before error

            with pytest.raises(
                TypeError,
                match=r"Parameter products must be type of list\[str\]",
            ):
                await client.unsubscribe(feed="ticker", products="PI_XBTUSD")  # type: ignore[arg-type]

        await async_sleep(4)

    asyncio.run(execute_unsubscribe())

    for expected in (
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PF_SOLUSD']}",
        "{'event': 'unsubscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
        "{'event': 'unsubscribed', 'feed': 'ticker', 'product_ids': ['PF_SOLUSD']}",
    ):
        assert expected in caplog.text


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_websocket
def test_unsubscribe_private(
    futures_api_key: str,
    futures_secret_key: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Checks if the authenticated websocket client is able to unsubscribe
    from private feeds.
    """

    async def execute_unsubscribe() -> None:
        async with FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        ) as client:
            await client.subscribe(feed="open_orders")

            await async_sleep(2)
            await client.unsubscribe(feed="open_orders")

            with pytest.raises(
                ValueError,
                match=r"There is no private feed that accepts products!",
            ):
                await client.unsubscribe(feed="open_orders", products=["PI_XBTUSD"])

            await async_sleep(2)

    asyncio.run(execute_unsubscribe())

    for expected in (
        "{'event': 'subscribed', 'feed': 'open_orders'}",
        "{'event': 'unsubscribed', 'feed': 'open_orders'}",
    ):
        assert expected in caplog.text


@pytest.mark.futures
@pytest.mark.futures_websocket
def test_get_active_subscriptions(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks the ``get_active_subscriptions`` function.
    """

    async def check_subscriptions() -> None:
        async with FuturesWebsocketClientTestWrapper() as client:
            assert client.get_active_subscriptions() == []

            await client.subscribe(feed="ticker", products=["PI_XBTUSD"])
            await async_sleep(1)
            assert len(client.get_active_subscriptions()) == 1

            await client.unsubscribe(feed="ticker", products=["PI_XBTUSD"])
            await async_sleep(1)
            assert client.get_active_subscriptions() == []

    asyncio.run(check_subscriptions())

    for expected in (
        "{'event': 'subscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
        "{'event': 'unsubscribed', 'feed': 'ticker', 'product_ids': ['PI_XBTUSD']}",
    ):
        assert expected in caplog.text


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_websocket
def test_resubscribe(
    futures_api_key: str,
    futures_secret_key: str,
    caplog: pytest.LogCaptureFixture,
    mocker: MockerFixture,
) -> None:
    """
    Test that forces a reconnect by closing the connection to check if the
    authenticated feeds will be resubscribed correctly.
    """
    caplog.set_level(logging.INFO)

    async def check_resubscribe() -> None:
        async with FuturesWebsocketClientTestWrapper(
            key=futures_api_key,
            secret=futures_secret_key,
        ) as client:
            assert client.get_active_subscriptions() == []
            await async_sleep(1)

            await client.subscribe(feed="open_orders")
            await async_sleep(2)
            assert len(client.get_active_subscriptions()) == 1

            mocker.patch.object(
                client._conn,
                "_ConnectFuturesWebsocket__get_reconnect_wait",
                return_value=2,
            )

            await client._conn.close_connection()
            await async_sleep(5)
            assert len(client.get_active_subscriptions()) == 1

    asyncio.run(check_resubscribe())
    for phrase in (
        "Websocket connected!",
        "got an exception sent 1000 (OK); then received 1000 (OK)",
        "Connection closed",
        "Recover subscriptions [{'event': 'subscribe', 'feed': 'open_orders'}]: waiting",
        "Recover subscriptions [{'event': 'subscribe', 'feed': 'open_orders'}]: done",
    ):
        assert phrase in caplog.text

    assert (
        "{'event': 'alert', 'message': 'Failed to subscribe to authenticated feed'}"
        not in caplog.text
    )
