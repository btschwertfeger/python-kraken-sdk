#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that tests the Kraken Spot websocket client
(Kraken Spot Websocket API v1)

NOTE:
*   Since there is no sandbox environment for the Spot trading API,
    some tests are adjusted, so that there is a `validate` switch to not risk
    funds.
*   The custom SpotWebsocketClientV1TestWrapper class is used that wraps around
    the websocket client. To validate the functions the responses are logged and
    finally the logs are read out and its input is checked for the expected
    output.

todo: check also if reqid matches
"""

from __future__ import annotations

import logging
from asyncio import run as asyncio_run
from typing import Any

import pytest

from kraken.exceptions import KrakenAuthenticationError

from .helper import SpotWebsocketClientV1TestWrapper, async_wait


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_create_public_client(caplog: Any) -> None:
    """
    Checks if the websocket client can be instantiated.
    """

    async def create_client() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        await async_wait(seconds=5)

    asyncio_run(create_client())

    for expected in (
        "'connectionID",
        "'event': 'systemStatus', 'status': 'online'",
        "'version': '1.",
        "'event': 'pong'",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v2()
def test_create_public_client_as_context_manager(caplog: Any) -> None:
    """
    Checks if the websocket client can be instantiated as context manager.
    """

    async def create_client_as_context_manager() -> None:
        with SpotWebsocketClientV1TestWrapper() as client:
            await async_wait(seconds=5)

    asyncio_run(create_client_as_context_manager())

    for expected in (
        "'connectionID",
        "'event': 'systemStatus', 'status': 'online'",
        "'version': '1.",
        "'event': 'pong'",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_create_private_client(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: Any,
) -> None:
    """
    Checks if the authenticated websocket client can be instantiated.
    """

    async def create_client() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )
        await async_wait(seconds=5)

    asyncio_run(create_client())
    for expected in (
        "'connectionID",
        "'event': 'systemStatus', 'status': 'online'",
        "'event': 'pong'",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_access_public_client_attributes() -> None:
    """
    Checks the ``access_public_client_attributes`` function
    works as expected.
    """

    async def check_access() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()

        assert client.public_channel_names == [
            "ticker",
            "spread",
            "book",
            "ohlc",
            "trade",
            "*",
        ]
        assert client.active_public_subscriptions == []
        await async_wait(seconds=1)
        with pytest.raises(ConnectionError):
            # cannot access private subscriptions on unauthenticated client
            assert isinstance(client.active_private_subscriptions, list)

        await async_wait(seconds=1.5)

    asyncio_run(check_access())


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_access_private_client_attributes(
    spot_api_key: str,
    spot_secret_key: str,
) -> None:
    """
    Checks the ``access_private_client_attributes`` function
    works as expected.
    """

    async def check_access() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )
        assert client.private_channel_names == ["ownTrades", "openOrders"]
        assert client.active_private_subscriptions == []
        await async_wait(seconds=2.5)

    asyncio_run(check_access())


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_public_subscribe(caplog: Any) -> None:
    """
    Function that checks if the websocket client
    is able to subscribe to public feeds.
    """

    async def test_subscription() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        subscription: dict[str, str] = {"name": "ticker"}

        with pytest.raises(AttributeError):
            # Invalid subscription format
            await client.subscribe(subscription={})

        with pytest.raises(TypeError):
            # Pair must be type list[str]
            await client.subscribe(subscription=subscription, pair="XBT/USD")  # type: ignore[arg-type]

        await client.subscribe(subscription=subscription, pair=["XBT/EUR"])
        await async_wait(seconds=2)

    asyncio_run(test_subscription())

    for expected in (
        "'channelName': 'ticker', 'event': 'subscriptionStatus', 'pair': 'XBT/EUR'",
        "'status': 'subscribed', 'subscription': {'name': 'ticker'}}",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_public_subscribe_without_pair_failing() -> None:
    """
    Checks that subscribing without specifying a pair fails.
    """

    async def test_subscription() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()

        with pytest.raises(
            ValueError,
            match=r"At least one pair must be specified when subscribing to public feeds.",
        ):
            await client.subscribe(subscription={"name": "ticker"})
        await async_wait(seconds=2)

    asyncio_run(test_subscription())


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_private_subscribe(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: Any,
) -> None:
    """
    Checks if the authenticated websocket client can subscribe to private feeds.
    """

    async def test_subscription() -> None:
        subscription: dict[str, str] = {"name": "ownTrades"}

        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(
            KrakenAuthenticationError,
            match=r"Credentials are invalid.",
        ):
            await client.subscribe(subscription=subscription)

        with pytest.raises(
            KrakenAuthenticationError,
            match=r"Credentials are invalid.",
        ):
            # same here also using a pair for coverage ...
            await client.subscribe(subscription=subscription, pair=["XBT/EUR"])

        auth_client: SpotWebsocketClientV1TestWrapper = (
            SpotWebsocketClientV1TestWrapper(key=spot_api_key, secret=spot_secret_key)
        )
        with pytest.raises(
            ValueError,
            match=r"Cannot subscribe to private endpoint with specific pair!",
        ):
            await auth_client.subscribe(subscription=subscription, pair=["XBT/EUR"])

        await async_wait(seconds=1)

        await auth_client.subscribe(subscription=subscription)
        await async_wait(seconds=2)

    asyncio_run(test_subscription())
    for expected in (
        "'status': 'subscribed', 'subscription': {'name': 'ownTrades'}}",
        "{'channelName': 'ownTrades', 'event': 'subscriptionStatus'",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_public_unsubscribe(caplog: Any) -> None:
    """
    Checks if the websocket client can unsubscribe from public feeds.
    """

    async def test_unsubscribe() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()

        subscription: dict[str, str] = {"name": "ticker"}
        pair: list[str] = ["XBT/USD"]
        await client.subscribe(subscription=subscription, pair=pair)
        await async_wait(seconds=3)

        await client.unsubscribe(subscription=subscription, pair=pair)

        await async_wait(seconds=2)

    asyncio_run(test_unsubscribe())

    # todo: regex!
    for expected in (
        "'channelName': 'ticker', 'event': 'subscriptionStatus', 'pair': 'XBT/USD'",
        "'status': 'subscribed', 'subscription': {'name': 'ticker'}",
        "'unsubscribed', 'subscription': {'name': 'ticker'}}",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_public_unsubscribe_failure(caplog: Any) -> None:
    """
    Checks if the websocket client responses with failures
    when the ``unsubscribe`` function receives invalid parameters.
    """

    async def check_unsubscribe_fail() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()

        # We did not subscribed to this tickers but it will work,
        # and the response will inform us that there are no subscriptions.
        await client.unsubscribe(
            subscription={"name": "ticker"},
            pair=["DOT/USD", "ETH/USD"],
        )

        with pytest.raises(
            AttributeError,
            match=r"Subscription requires a \"name\" key.",
        ):
            await client.unsubscribe(subscription={})

        with pytest.raises(
            TypeError,
            match=r"Parameter pair must be type of list\[str\] \(e.g. pair=\[\"XBTUSD\"\]\)",
        ):
            await client.unsubscribe(subscription={"name": "ticker"}, pair="XBT/USD")  # type: ignore[arg-type]

        await async_wait(seconds=2)

    asyncio_run(check_unsubscribe_fail())

    # todo: regex!
    for expected in (
        "{'errorMessage': 'Subscription Not Found', 'event': 'subscriptionStatus', 'pair': 'DOT/USD'",
        "{'errorMessage': 'Subscription Not Found', 'event': 'subscriptionStatus', 'pair': 'ETH/USD'",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_public_unsubscribe_without_pair_failing() -> None:
    """
    Checks that subscribing without specifying a pair fails.
    """

    async def test_subscription() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()

        with pytest.raises(
            ValueError,
            match=r"At least one pair must be specified when unsubscribing from public feeds.",
        ):
            await client.unsubscribe(subscription={"name": "ticker"})
        await async_wait(seconds=2)

    asyncio_run(test_subscription())


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_private_unsubscribe(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: Any,
) -> None:
    """
    Checks if private subscriptions are available.
    """

    async def check_unsubscribe() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )

        await client.subscribe(subscription={"name": "ownTrades"})
        await async_wait(seconds=1)

        await client.unsubscribe(subscription={"name": "ownTrades"})
        await async_wait(seconds=2)
        # todo: check if subs are removed from known list

    asyncio_run(check_unsubscribe())

    for expected in (
        "{'channelName': 'ownTrades', 'event': 'subscriptionStatus'",
        "'status': 'subscribed', 'subscription': {'name': 'ownTrades'}}",
        "'status': 'unsubscribed', 'subscription': {'name': 'ownTrades'}}",
    ):
        assert expected in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_private_unsubscribe_failing(spot_api_key: str, spot_secret_key: str) -> None:
    """
    Checks if the ``unsubscribe`` function fails when invalid
    parameters are passed.
    """

    async def check_unsubscribe_failing() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        auth_client: SpotWebsocketClientV1TestWrapper = (
            SpotWebsocketClientV1TestWrapper(key=spot_api_key, secret=spot_secret_key)
        )

        with pytest.raises(
            KrakenAuthenticationError,
            match=r"Credentials are invalid.",
        ):
            # private feed on unauthenticated client
            await client.unsubscribe(subscription={"name": "ownTrades"})

        with pytest.raises(
            ValueError,
            match=r"Cannot unsubscribe from private endpoint with specific pair!",
        ):
            await auth_client.unsubscribe(
                subscription={"name": "ownTrades"},
                pair=["XBTUSD"],
            )

        await async_wait(seconds=2)

    asyncio_run(check_unsubscribe_failing())


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_send_private_message_raw(caplog: Any) -> None:
    """
    Checks that the send_message function is able to send raw messages.
    """

    async def test_send_message() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        await client.send_message(
            message={
                "event": "subscribe",
                "pair": ["XBT/USD"],
                "subscription": {"name": "ticker"},
            },
            private=False,
            raw=True,
        )

        await async_wait(seconds=2)

    asyncio_run(test_send_message())

    assert (
        "'channelName': 'ticker', 'event': 'subscriptionStatus', 'pair': 'XBT/USD', 'status': 'subscribed', 'subscription': {'name': 'ticker'}"
        in caplog.text
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_send_private_message_from_public_connection_failing() -> None:
    """
    Ensures that the public websocket connection can't send messages that
    need authentication.
    """

    async def test_send_message() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(KrakenAuthenticationError):
            await client.send_message(message={}, private=True)

        await async_wait(seconds=2)

    asyncio_run(test_send_message())


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_reconnect(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: Any,
    mocker: Any,
) -> None:
    """
    Checks if the reconnect works properly when forcing a closed connection.
    """
    caplog.set_level(logging.INFO)

    async def check_reconnect() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )
        await async_wait(seconds=2)

        await client.subscribe(subscription={"name": "ticker"}, pair=["XBT/USD"])
        await client.subscribe(subscription={"name": "openOrders"})
        await async_wait(seconds=2)

        for obj in (client._priv_conn, client._pub_conn):
            mocker.patch.object(
                obj,
                "_ConnectSpotWebsocketBase__get_reconnect_wait",
                return_value=2,
            )
        await client._pub_conn.close_connection()
        await client._priv_conn.close_connection()

        await async_wait(seconds=5)

    asyncio_run(check_reconnect())

    for phrase in (
        "Recover public subscriptions []: waiting",
        "Recover authenticated subscriptions []: waiting",
        "Recover public subscriptions []: done",
        "Recover authenticated subscriptions []: done",
        "Websocket connected!",
        "'event': 'systemStatus', 'status': 'online', 'version': ",  # '1.9.x'}
        "'openOrders', 'event': 'subscriptionStatus', 'status': 'subscribed',",
        "'channelName': 'ticker', 'event': 'subscriptionStatus', 'pair': 'XBT/USD', 'status': 'subscribed', 'subscription': {'name': 'ticker'}",
        "got an exception sent 1000 (OK); then received 1000 (OK)",
        "Recover public subscriptions [{'event': 'subscribe', 'pair': ['XBT/USD'], 'subscription': {'name': 'ticker'}}]: waiting",
        "Recover authenticated subscriptions [{'event': 'subscribe', 'subscription': {'name': 'openOrders'}}]: waiting",
        "{'event': 'subscribe', 'pair': ['XBT/USD'], 'subscription': {'name': 'ticker'}}: OK",
        "{'event': 'subscribe', 'subscription': {'name': 'openOrders'}}: OK",
        "Recover public subscriptions [{'event': 'subscribe', 'pair': ['XBT/USD'], 'subscription': {'name': 'ticker'}}]: done",
        "Recover authenticated subscriptions [{'event': 'subscribe', 'subscription': {'name': 'openOrders'}}]: done",
    ):
        assert phrase in caplog.text


# ------------------------------------------------------------------------------
# Executables


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_create_order(spot_api_key: str, spot_secret_key: str, caplog: Any) -> None:
    """
    Checks the ``create_order`` function by submitting a
    new order - but in validate mode.

    The order submission will fail, because the testing API keys do not have
    trade permission - but it is also checked that error messages
    starting with "EGeneral:Invalid" are not included in the received
    messages. This ensures that the Kraken API received the message and the only
    problem is the permission.

    NOTE: This function is not disabled, since the function is executed in
          validate mode.
    """

    async def execute_create_order() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )
        params: dict = {
            "ordertype": "limit",
            "side": "buy",
            "pair": "XBT/USD",
            "volume": "2",
            "price": "1000",
            "price2": "1200",
            "leverage": "2",
            "oflags": "viqc",
            "starttm": "0",
            "expiretm": "1000",
            "userref": "12345678",
            "validate": True,
            "close_ordertype": "limit",
            "close_price": "1000",
            "close_price2": "1200",
            "timeinforce": "GTC",
        }
        await client.create_order(**params)
        await async_wait(seconds=2)

    asyncio_run(execute_create_order())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'addOrderStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_create_order_failing_no_connection(caplog: Any) -> None:
    """
    Checks the ``create_order`` function by submitting a
    new order - it is intended to check what happens when there is no open
    authenticated connection - it should fail.

    The order submission will fail, because the testing API keys do not have
    trade permission - but it is also checked that error messages
    starting with "EGeneral:Invalid" are not included in the received
    messages. This ensures that the Kraken API received the message and the only
    problem is the permission.

    NOTE: This function is not disabled, since the function is executed in
          validate mode.
    """

    async def execute_create_order() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(KrakenAuthenticationError):
            await client.create_order(
                ordertype="limit",
                side="buy",
                pair="XBT/USD",
                volume="2",
                price="1000",
                validate=True,
            )
        await async_wait(seconds=2)

    asyncio_run(execute_create_order())

    assert (
        "Can't place order - Authenticated websocket not connected!" not in caplog.text
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_edit_order(spot_api_key: str, spot_secret_key: str, caplog: Any) -> None:
    """
    Checks the edit order function by editing an order in validate mode.

    Same as with the trade endpoint - the response will include
    a permission denied error - but it is also checked that no other
    error includes the "invalid" string which means that the only problem
    is the permission.

    NOTE: This function is not disabled, since the orderId does not
          exist and would not cause any problems.
    """

    async def execute_edit_order() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )

        await client.edit_order(
            orderid="OHSAUDZ-ASJKGD-EPAFUIH",
            reqid=1244,
            pair="XBT/USD",
            price="120",
            price2="1300",
            oflags="fok",
            newuserref="833773",
            validate=True,
        )
        await async_wait(seconds=2)

    asyncio_run(execute_edit_order())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'editOrderStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_edit_order_failing_no_connection(caplog: Any) -> None:
    """
    Checks the ``edit_order`` function by editing an order - it is intended to
    check what happens when there is no open authenticated connection - it
    should fail.

    Same as with the trade endpoint - the response will include
    a permission denied error - but it is also checked that no other
    error includes the "invalid" string which means that the only problem
    is the permission.
    """

    async def execute_edit_order() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(KrakenAuthenticationError):
            await client.edit_order(
                orderid="OHSAUDZ-ASJKGD-EPAFUIH",
                reqid=1244,
                pair="XBT/USD",
                price="120",
                price2="1300",
                oflags="fok",
                newuserref="833773",
                validate=True,
            )
        await async_wait(seconds=2)

    asyncio_run(execute_edit_order())

    assert (
        "Can't edit order - Authenticated websocket not connected!" not in caplog.text
    )


# @pytest.mark.skip("CI does not have trade/cancel permission")
@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_cancel_order(spot_api_key: str, spot_secret_key: str, caplog: Any) -> None:
    """
    Checks the ``cancel_order`` function by canceling some orders.

    Same permission denied reason as for create and edit error.

    NOTE: This function is not disabled, since the txid does not
          exist and would not cause any problems.
    """

    async def execute_cancel_order() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )
        await client.cancel_order(txid=["AOUEHF-ASLBD-A6B4A"])
        await async_wait(seconds=2)

    asyncio_run(execute_cancel_order())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'cancelOrderStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


# @pytest.mark.skip("CI does not have trade/cancel permission")
@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_cancel_order_failing_no_connection(caplog: Any) -> None:
    """
    Checks the ``cancel_order`` function - it is intended to check what happens
    when there is no open authenticated connection - it should fail.


    Same permission denied reason as for create and edit error.

    NOTE: This function is not disabled, since the txid does not
          exist and would not cause any problems.
    """

    async def execute_cancel_order() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(KrakenAuthenticationError):
            await client.cancel_order(txid=["AOUEHF-ASLBD-A6B4A"])
        await async_wait(seconds=2)

    asyncio_run(execute_cancel_order())

    assert (
        "Can't cancel order - Authenticated websocket not connected!" not in caplog.text
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
@pytest.mark.skip("CI does not have trade/cancel permission")
def test_cancel_all_orders(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: Any,
) -> None:
    """
    Check the ``cancel_all_orders`` function by executing the function.

    Same permission denied reason as for create, edit and cancel error.
    """

    async def execute_cancel_all() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )
        await client.cancel_all_orders()
        await async_wait(seconds=2)

    asyncio_run(execute_cancel_all())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'cancelAllStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_cancel_all_orders_failing_no_connection(caplog: Any) -> None:
    """
    Checks the ``cancel_all_orders`` function - it is intended to check what
    happens when there is no open authenticated connection - it should fail.

    Same permission denied reason as for create, edit and cancel error.
    """

    async def execute_cancel_all_orders() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(KrakenAuthenticationError):
            await client.cancel_all_orders()
        await async_wait(seconds=2)

    asyncio_run(execute_cancel_all_orders())

    assert (
        "Can't cancel all orders - Authenticated websocket not connected!"
        not in caplog.text
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_cancel_all_orders_after(
    spot_api_key: str,
    spot_secret_key: str,
    caplog: Any,
) -> None:
    """
    Checking the ``cancel_all_orders_after`` function by
    executing it.

    NOTE: This function is not disabled, since the value 0 is
          submitted which would reset the timer and would not cause
          any problems.
    """

    async def execute_cancel_after() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key,
            secret=spot_secret_key,
        )
        await client.cancel_all_orders_after(0)
        await async_wait(seconds=3)

    asyncio_run(execute_cancel_after())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'cancelAllOrdersAfterStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text in caplog.text


@pytest.mark.spot()
@pytest.mark.spot_websocket()
@pytest.mark.spot_websocket_v1()
def test_cancel_all_orders_after_failing_no_connection(caplog: Any) -> None:
    """
    Checks the ``cancel_all_orders_after`` function - it is intended to check
    what happens when there is no open authenticated connection - it should
    fail.

    NOTE: This function is not disabled, since the value 0 is
          submitted which would reset the timer and would not cause
          any problems.
    """

    async def execute_cancel_all_orders() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(KrakenAuthenticationError):
            await client.cancel_all_orders_after()
        await async_wait(seconds=2)

    asyncio_run(execute_cancel_all_orders())

    assert (
        "Can't cancel all orders after - Authenticated websocket not connected!"
        not in caplog.text
    )
