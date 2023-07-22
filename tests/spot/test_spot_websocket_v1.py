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
todo: check recover subscriptions
"""

from __future__ import annotations

from asyncio import run as asyncio_run
from typing import Any, Dict, List

import pytest

from .helper import SpotWebsocketClientV1TestWrapper, async_wait


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
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


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_create_private_client(
    spot_api_key: str, spot_secret_key: str, caplog: Any
) -> None:
    """
    Checks if the authenticated websocket client can be instantiated.
    """

    async def create_client() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key, secret=spot_secret_key
        )
        await async_wait(seconds=5)

    asyncio_run(create_client())
    for expected in (
        "'connectionID",
        "'event': 'systemStatus', 'status': 'online'",
        "'event': 'pong'",
    ):
        assert expected in caplog.text


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
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


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_access_private_client_attributes(
    spot_api_key: str, spot_secret_key: str
) -> None:
    """
    Checks the ``access_private_client_attributes`` function
    works as expected.
    """

    async def check_access() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key, secret=spot_secret_key
        )
        assert client.private_channel_names == ["ownTrades", "openOrders"]
        assert client.active_private_subscriptions == []
        await async_wait(seconds=2.5)

    asyncio_run(check_access())


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_public_subscribe(caplog: Any) -> None:
    """
    Function that checks if the websocket client
    is able to subscribe to public feeds.
    """

    async def test_subscription() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        subscription: Dict[str, str] = {"name": "ticker"}

        with pytest.raises(AttributeError):
            # Invalid subscription format
            await client.subscribe(subscription={})

        with pytest.raises(ValueError):
            # Pair must be type List[str]
            await client.subscribe(subscription=subscription, pair="XBT/USD")  # type: ignore[arg-type]

        await client.subscribe(subscription=subscription, pair=["XBT/EUR"])
        await async_wait(seconds=2)

    asyncio_run(test_subscription())

    for expected in (
        "'channelName': 'ticker', 'event': 'subscriptionStatus', 'pair': 'XBT/EUR'",
        "'status': 'subscribed', 'subscription': {'name': 'ticker'}}",
    ):
        assert expected in caplog.text


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_private_subscribe(
    spot_api_key: str, spot_secret_key: str, caplog: Any
) -> None:
    """
    Checks if the authenticated websocket client can subscribe to private feeds.
    """

    async def test_subscription() -> None:
        subscription: Dict[str, str] = {"name": "ownTrades"}

        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        with pytest.raises(ValueError):
            # unauthenticated
            await client.subscribe(subscription=subscription)

        with pytest.raises(ValueError):
            # same here also using a pair for coverage ...
            await client.subscribe(subscription=subscription, pair=["XBT/EUR"])

        auth_client: SpotWebsocketClientV1TestWrapper = (
            SpotWebsocketClientV1TestWrapper(key=spot_api_key, secret=spot_secret_key)
        )
        with pytest.raises(ValueError):
            # private conns does not accept pairs
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


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_public_unsubscribe(caplog: Any) -> None:
    """
    Checks if the websocket client can unsubscribe from public feeds.
    """

    async def test_unsubscribe() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()

        subscription: Dict[str, str] = {"name": "ticker"}
        pair: List[str] = ["XBT/USD"]
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


@pytest.mark.spot
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
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
            subscription={"name": "ticker"}, pair=["DOT/USD", "ETH/USD"]
        )

        with pytest.raises(AttributeError):
            # invalid subscription
            await client.unsubscribe(subscription={})

        with pytest.raises(ValueError):
            # pair must be List[str]
            await client.unsubscribe(subscription={"name": "ticker"}, pair="XBT/USD")  # type: ignore[arg-type]

        await async_wait(seconds=2)

    asyncio_run(check_unsubscribe_fail())

    # todo: regex!
    for expected in (
        "{'errorMessage': 'Subscription Not Found', 'event': 'subscriptionStatus', 'pair': 'DOT/USD'",
        "{'errorMessage': 'Subscription Not Found', 'event': 'subscriptionStatus', 'pair': 'ETH/USD'",
    ):
        assert expected in caplog.text


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_private_unsubscribe(
    spot_api_key: str, spot_secret_key: str, caplog: Any
) -> None:
    """
    Checks if private subscriptions are available.
    """

    async def check_unsubscribe() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key, secret=spot_secret_key
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


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_private_unsubscribe_failing(
    spot_api_key: str, spot_secret_key: str, caplog: Any
) -> None:
    """
    Checks if the ``unsubscribe`` function fails when invalid
    parameters are passed.
    """

    async def check_unsubscribe_failing() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
        auth_client: SpotWebsocketClientV1TestWrapper = (
            SpotWebsocketClientV1TestWrapper(key=spot_api_key, secret=spot_secret_key)
        )

        with pytest.raises(ValueError):
            # private feed on unauthenticated client
            await client.unsubscribe(subscription={"name": "ownTrades"})

        with pytest.raises(ValueError):
            # private subscriptions does not have a pair
            await auth_client.unsubscribe(
                subscription={"name": "ownTrades"}, pair=["XBTUSD"]
            )

        await async_wait(seconds=2)

    asyncio_run(check_unsubscribe_failing())


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
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
            key=spot_api_key, secret=spot_secret_key
        )
        params: dict = dict(
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
        await client.create_order(**params)
        await async_wait(seconds=2)

    asyncio_run(execute_create_order())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'addOrderStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
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
            key=spot_api_key, secret=spot_secret_key
        )

        params: dict = dict(
            orderid="OHSAUDZ-ASJKGD-EPAFUIH",
            reqid=1244,
            pair="XBT/USD",
            price="120",
            price2="1300",
            oflags="fok",
            newuserref="833773",
            validate=True,
        )

        await client.edit_order(**params)
        await async_wait(seconds=2)

    asyncio_run(execute_edit_order())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'editOrderStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


# @pytest.mark.skip("CI does not have trade/cancel permission")
@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_cancel_order(spot_api_key: str, spot_secret_key: str, caplog: Any) -> None:
    """
    Checks the ``cancel_order`` function by canceling some orders.

    Same permission denied reason as for create and edit error.

    NOTE: This function is not disabled, since the txid does not
          exist and would not cause any problems.
    """

    async def execute_cancel_order() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key, secret=spot_secret_key
        )
        await client.cancel_order(txid=["AOUEHF-ASLBD-A6B4A"])
        await async_wait(seconds=2)

    asyncio_run(execute_cancel_order())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'cancelOrderStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
@pytest.mark.skip("CI does not have trade/cancel permission")
def test_cancel_all_orders(
    spot_api_key: str, spot_secret_key: str, caplog: Any
) -> None:
    """
    Check the ``cancel_all_orders`` function by executing the function.

    Same permission denied reason as for create, edit and cancel error.
    """

    async def execute_cancel_all() -> None:
        client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper(
            key=spot_api_key, secret=spot_secret_key
        )
        await client.cancel_all_orders()
        await async_wait(seconds=2)

    asyncio_run(execute_cancel_all())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'cancelAllStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_websocket
@pytest.mark.spot_websocket_v1
def test_cancel_all_orders_after(
    spot_api_key: str, spot_secret_key: str, caplog: Any
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
            key=spot_api_key, secret=spot_secret_key
        )
        await client.cancel_all_orders_after(0)
        await async_wait(seconds=3)

    asyncio_run(execute_cancel_after())

    assert (
        "{'errorMessage': 'EGeneral:Permission denied', 'event': 'cancelAllOrdersAfterStatus'"
        in caplog.text
    )
    assert "'errorMessage': 'EGeneral:Invalid" not in caplog.text in caplog.text


# todo: Create a test that kills the websocket connection
#       to test the reconnect.
# from unittest import mock
# import json
# @pytest.mark.spot
# @pytest.mark.spot_websocket
# @pytest.mark.spot_websocket_v1
# @pytest.mark.wip
# @mock.patch(
#     "kraken.spot.websocket.json.loads",
# )
# def test_reconnect(mock_json_loads: mock.MagicMock, caplog: Any) -> None:
#     mock_json_loads.side_effect = (
#         [json.dumps({"valid": "message"})]
#         + [AttributeError("Test Error")]
#         + [json.dumps({"valid": "message"})] * 10000
#     )

#     async def check_reconnect() -> None:
#         client: SpotWebsocketClientV1TestWrapper = SpotWebsocketClientV1TestWrapper()
#         await async_wait(seconds=60)

#     asyncio_run(check_reconnect())
#     # with open("x.log", "w") as f:
#     #     f.write(caplog.text)
