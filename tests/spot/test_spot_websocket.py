#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that tests the Kraken Spot websocket client
(Kraken Spot Websocket API v2)

NOTE:
*   The custom SpotWebsocketClientTestWrapper class is used that wraps around
    the websocket client. To validate the functions the responses are logged and
    finally the logs are read out and its input is checked for the expected
    output.

"""

from __future__ import annotations

import logging
import re
from asyncio import run as asyncio_run
from asyncio import sleep as async_sleep
from copy import deepcopy
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

from kraken.exceptions import KrakenAuthenticationError
from kraken.spot.websocket.connectors import ConnectSpotWebsocket

from .helper import SpotWebsocketClientTestWrapper


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_create_public_client(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks if the websocket client can be instantiated.
    """

    async def create_client() -> None:
        client = SpotWebsocketClientTestWrapper()
        await client.start()
        await async_sleep(5)
        await client.close()

    asyncio_run(create_client())

    for expected in (
        'channel": "status"',
        '"api_version": "v2"',
        '"system": "online", "version": "2.',
        '"type": "update"',
    ):
        assert expected in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_create_public_client_as_context_manager(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Checks if the websocket client can be instantiated as context manager.
    """

    async def create_client_as_context_manager() -> None:
        async with SpotWebsocketClientTestWrapper():
            await async_sleep(5)

    asyncio_run(create_client_as_context_manager())

    for expected in (
        'channel": "status"',
        '"api_version": "v2"',
        '"system": "online", "version": "2.',
        '"type": "update"',
    ):
        assert expected in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_access_public_client_attributes() -> None:
    """
    Checks the ``access_public_client_attributes`` function
    works as expected.
    """

    async def check_access() -> None:
        async with SpotWebsocketClientTestWrapper() as client:
            assert client.public_channel_names == [
                "book",
                "instrument",
                "ohlc",
                "ticker",
                "trade",
            ]
            assert client.active_public_subscriptions == []
            await async_sleep(1)
            with pytest.raises(ConnectionError):
                # can't access private subscriptions on unauthenticated client
                assert isinstance(client.active_private_subscriptions, list)

            await async_sleep(1.5)

    asyncio_run(check_access())


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_access_public_subscriptions_no_conn_failing() -> None:
    """
    Checks if ``active_public_subscriptions`` fails, because there is no
    public connection
    """

    async def check_access() -> None:
        async with SpotWebsocketClientTestWrapper(
            no_public=True,
        ) as client:
            with pytest.raises(ConnectionError):
                assert isinstance(client.active_public_subscriptions, list)

            await async_sleep(1.5)

    asyncio_run(check_access())


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
def test_access_private_client_attributes(
    spot_api_key: str,
    spot_secret_key: str,
) -> None:
    """
    Checks the ``access_private_client_attributes`` function
    works as expected.
    """

    async def check_access() -> None:
        async with SpotWebsocketClientTestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        ) as auth_client:
            assert isinstance(auth_client.private_channel_names, list)
            assert isinstance(auth_client.private_methods, list)
            assert auth_client.active_private_subscriptions == []
            await async_sleep(2.5)

    asyncio_run(check_access())


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_send_message_missing_method_failing() -> None:
    """
    Checks if the send_message function fails when specific keys or values
    are incorrect formatted or missing.
    """

    async def create_client() -> None:
        async with SpotWebsocketClientTestWrapper() as client:
            with pytest.raises(TypeError):  # wrong message format
                await client.send_message(message=[])
            with pytest.raises(TypeError):  # method value not string
                await client.send_message(message={"method": 1})
            with pytest.raises(TypeError):  # missing params for '*subscribe'
                await client.send_message(message={"method": "subscribe"})
            with pytest.raises(TypeError):  # params not dict
                await client.send_message(message={"method": "subscribe", "params": []})
            with pytest.raises(TypeError):  # params missing channel key
                await client.send_message(
                    message={"method": "subscribe", "params": {"test": 1}},
                )
            with pytest.raises(TypeError):  # channel key must be str
                await client.send_message(
                    message={"method": "subscribe", "params": {"channel": 1}},
                )
            await async_sleep(1)

    asyncio_run(create_client())


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_send_message_raw(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks if the send_message function fails when the socket is not available.
    """

    async def create_client() -> None:
        async with SpotWebsocketClientTestWrapper() as client:
            await client.send_message(
                message={"method": "ping", "req_id": 123456789},
                raw=True,
            )
            await async_sleep(1)

    asyncio_run(create_client())

    assert '{"method": "pong", "req_id": 123456789' in caplog.text
    assert '"success": false' not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_public_subscribe(caplog: pytest.LogCaptureFixture) -> None:
    """
    Function that checks if the websocket client is able to subscribe to public
    feeds.
    """

    async def test_subscription() -> None:
        async with SpotWebsocketClientTestWrapper() as client:
            await client.subscribe(
                params={"channel": "ticker", "symbol": ["BTC/USD"]},
                req_id=12345678,
            )
            await async_sleep(3)

    asyncio_run(test_subscription())

    assert (
        '{"method": "subscribe", "req_id": 12345678, "result": {"channel":'
        ' "ticker", "event_trigger": "trades", "snapshot": true, "symbol":'
        ' "BTC/USD"}, "success": true' in caplog.text
    )
    assert '"success": false' not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
def test_private_subscribe_failing_on_public_connection() -> None:
    """
    Ensures that the public websocket connection can't subscribe to private
    feeds.
    """

    async def test_subscription() -> None:
        async with SpotWebsocketClientTestWrapper() as client:
            with pytest.raises(KrakenAuthenticationError):
                await client.subscribe(
                    params={"channel": "executions"},
                    req_id=123456789,
                )

            await async_sleep(2)

    asyncio_run(test_subscription())


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
def test_private_subscribe(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Checks if the authenticated websocket client can subscribe to private feeds.
    """

    async def test_subscription() -> None:
        async with SpotWebsocketClientTestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
            no_public=True,
        ) as auth_client:
            await auth_client.subscribe(
                params={"channel": "executions"},
                req_id=123456789,
            )

            await async_sleep(2)

    asyncio_run(test_subscription())

    assert re.search(
        r'\{"method": "subscribe", "req_id": 123456789, "result": \{"channel": "executions".*"success": true',
        caplog.text,
    )
    assert '"success": false' not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_public_unsubscribe(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks if the websocket client can unsubscribe from public feeds.
    """

    async def test_unsubscribe() -> None:
        async with SpotWebsocketClientTestWrapper() as client:
            params: dict = {"channel": "ticker", "symbol": ["BTC/USD"]}
            await client.subscribe(params=params, req_id=123456789)
            await async_sleep(3)

            await client.unsubscribe(params=params, req_id=987654321)
            await async_sleep(2)

    asyncio_run(test_unsubscribe())

    for expected in (
        '{"method": "subscribe", "req_id": 123456789, "result": {"channel": "ticker", "event_trigger": "trades", "snapshot": true, "symbol": "BTC/USD"}, "success": true',
        '{"channel": "ticker", "type": "snapshot", "data": [{"symbol": "BTC/USD", ',
        '{"method": "unsubscribe", "req_id": 987654321, "result": {"channel": "ticker", "event_trigger": "trades", "symbol": "BTC/USD"}, "success": true',
    ):
        assert expected in caplog.text
    assert '"success": false' not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_public_unsubscribe_failure(caplog: pytest.LogCaptureFixture) -> None:
    """
    Checks if the websocket client responses with failures
    when the ``unsubscribe`` function receives invalid parameters.
    """

    async def check_unsubscribe_fail() -> None:
        async with SpotWebsocketClientTestWrapper() as client:
            # We did not subscribed to this ticker but it will work,
            # and the response will inform us that there is no such subscription.
            await client.unsubscribe(
                params={"channel": "ticker", "symbol": ["BTC/USD"]},
                req_id=123456789,
            )

            await async_sleep(2)

    asyncio_run(check_unsubscribe_fail())

    assert (
        '{"error": "Subscription Not Found", "method": "subscribe", "req_id": 123456789, "success": false, "symbol": "BTC/USD", "time_in": '
        in caplog.text
    )


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
def test_private_unsubscribe(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Checks if private unsubscriptions are available.
    """

    async def check_unsubscribe() -> None:
        async with SpotWebsocketClientTestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
            no_public=True,
        ) as client:
            await client.subscribe(params={"channel": "executions"}, req_id=123456789)
            await async_sleep(2)

            await client.unsubscribe(params={"channel": "executions"}, req_id=987654321)
            await async_sleep(2)
            # todo: check if subs are removed from known list - Dec 2023: obsolete?

    asyncio_run(check_unsubscribe())

    for expected in (
        '{"method": "subscribe", "req_id": 123456789, "result": {"channel": "executions"',
        '{"method": "unsubscribe", "req_id": 987654321, "result": {"channel": "executions"}, "success": true',
    ):
        assert expected in caplog.text
    assert '"success": false' not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
def test___transform_subscription() -> None:
    """
    Checks if the subscription transformation works properly by checking
    the condition for multiple channels. This test may be trivial but in case
    Kraken changes anything on that implementation, this will break and makes it
    easier to track down the change.
    """

    incoming_subscription: dict
    target_subscription: dict
    for channel in ("book", "ticker", "ohlc", "trade"):
        incoming_subscription = {
            "method": "subscribe",
            "result": {
                "channel": channel,
                "depth": 10,
                "snapshot": True,
                "symbol": "BTC/USD",
            },
            "success": True,
            "time_in": "2023-08-30T04:59:14.052226Z",
            "time_out": "2023-08-30T04:59:14.052263Z",
        }

        target_subscription = deepcopy(incoming_subscription)
        target_subscription["result"]["symbol"] = ["BTC/USD"]

        assert (
            ConnectSpotWebsocket._ConnectSpotWebsocket__transform_subscription(
                ConnectSpotWebsocket,
                subscription=incoming_subscription,
            )
            == target_subscription
        )


@pytest.mark.spot
@pytest.mark.spot_websocket
def test___transform_subscription_no_change() -> None:
    """
    Similar to the test above -- but verifying that messages that don't need an
    adjustment remain unchanged.

    This test must be extended in case Kraken decides to changes more
    parameters.
    """

    incoming_subscription: dict
    for channel in ("book", "ticker", "ohlc", "trade"):
        incoming_subscription = {
            "method": "subscribe",
            "result": {
                "channel": channel,
                "depth": 10,
                "snapshot": True,
                "symbol": ["BTC/USD"],
            },
            "success": True,
            "time_in": "2023-08-30T04:59:14.052226Z",
            "time_out": "2023-08-30T04:59:14.052263Z",
        }

        assert (
            ConnectSpotWebsocket._ConnectSpotWebsocket__transform_subscription(
                ConnectSpotWebsocket,
                subscription=incoming_subscription,
            )
            == incoming_subscription
        )


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
def test_reconnect(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: pytest.LogCaptureFixture,
    mocker: MockerFixture,
) -> None:
    """
    Checks if the reconnect works properly when forcing a closed connection.
    """
    caplog.set_level(logging.INFO)

    async def check_reconnect() -> None:
        async with SpotWebsocketClientTestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        ) as client:
            await async_sleep(2)

            await client.subscribe(params={"channel": "ticker", "symbol": ["BTC/USD"]})
            await client.subscribe(params={"channel": "executions"})
            await async_sleep(2)

            for obj in (client._priv_conn, client._pub_conn):
                mocker.patch.object(
                    obj,
                    "_ConnectSpotWebsocketBase__get_reconnect_wait",
                    return_value=2,
                )
            await client._pub_conn.close_connection()
            await client._priv_conn.close_connection()

            await async_sleep(5)

    asyncio_run(check_reconnect())

    for phrase in (
        "Recover public subscriptions []: waiting",
        "Recover authenticated subscriptions []: waiting",
        "Recover public subscriptions []: done",
        "Recover authenticated subscriptions []: done",
        "Websocket connected!",
        '{"channel": "status", "data": [{"api_version": "v2", "connection_id": ',
        '"system": "online", "version": ',  # "2.0.x"
        '"type": "update"}',
        '{"method": "subscribe", "result": {"channel": "ticker", "event_trigger": "trades", "snapshot": true, "symbol": "BTC/USD"}, "success": true,',
        '"channel": "ticker", "type": "snapshot", "data": [{"symbol": "BTC/USD", ',
        "got an exception sent 1000 (OK); then received 1000 (OK)",
        "Recover public subscriptions [{'channel': 'ticker', 'event_trigger': 'trades', 'snapshot': True, 'symbol': ['BTC/USD']}]: waiting",
        "Recover public subscriptions [{'channel': 'ticker', 'event_trigger': 'trades', 'snapshot': True, 'symbol': ['BTC/USD']}]: done",
    ):
        assert phrase in caplog.text

    assert re.search(
        r"Recover authenticated subscriptions .*'channel': 'executions'.* waiting",
        caplog.text,
    )
    assert re.search(
        r"Recover authenticated subscriptions .*'channel': 'executions'.* done",
        caplog.text,
    )
    assert '"success": False' not in caplog.text
