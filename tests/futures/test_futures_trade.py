# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures trade client"""

from collections.abc import Generator
from contextlib import suppress
from time import sleep

import pytest

from kraken.exceptions import KrakenInsufficientAvailableFundsError
from kraken.futures import Trade

from .helper import is_success


@pytest.fixture(autouse=True)
def _run_before_and_after_tests(futures_demo_trade: Trade) -> Generator:
    """
    Fixture that ensures all orders are cancelled after test.
    """
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    # Teardown: fill with any logic you want
    futures_demo_trade.cancel_all_orders()
    sleep(0.25)


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_get_fills(futures_demo_trade: Trade) -> None:
    """
    Checks the ``get_fills`` endpoint.
    """
    assert is_success(futures_demo_trade.get_fills())
    assert is_success(
        futures_demo_trade.get_fills(lastFillTime="2020-07-21T12:41:52.790Z"),
    )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_dead_mans_switch(futures_demo_trade: Trade) -> None:
    """
    Checks the ``dead_mans_switch`` endpoint.
    """
    assert is_success(futures_demo_trade.dead_mans_switch(timeout=60))
    assert is_success(
        futures_demo_trade.dead_mans_switch(timeout=0),
    )  # reset dead mans switch


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_get_orders_status(futures_demo_trade: Trade) -> None:
    """
    Checks the ``get_orders_status`` endpoint.
    """
    assert is_success(
        futures_demo_trade.get_orders_status(
            orderIds=[
                "bcaaefce-27a3-44b4-b13a-19df21e3f087",
                "685d5a1a-23eb-450c-bf17-1e4ab5c6fe8a",
            ],
        ),
    )

    assert is_success(
        futures_demo_trade.get_orders_status(
            cliOrdIds=[
                "bcaaefce-27a3-44b4-b13a-19df21e3f087",
                "685d5a1a-23eb-450c-bf17-1e4ab5c6fe8a",
            ],
        ),
    )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_create_order(futures_demo_trade: Trade) -> None:
    """
    Checks the ``create_order`` endpoint.
    """
    with suppress(KrakenInsufficientAvailableFundsError):
        futures_demo_trade.create_order(
            orderType="lmt",
            size=10,
            symbol="PI_XBTUSD",
            side="buy",
            limitPrice=1,
            stopPrice=10,
            reduceOnly=True,
            processBefore="3033-11-08T19:56:35.441899Z",
        )

    # FIXME: why are these commented out?
    # with suppress(KrakenInsufficientAvailableFundsError):
    #     futures_demo_trade.create_order(
    #         orderType="take_profit",
    #         size=10,
    #         side="buy",
    #         symbol="PI_XBTUSD",
    #         limitPrice=12000,
    #         triggerSignal="last",
    #         stopPrice=13000,
    #     )

    # try:
    #     # does not work,  400 response "invalid order type"
    #     # but it is documented here: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order
    #     # Kraken needs to fix this
    #     futures_demo_trade.create_order(
    #         orderType="trailing_stop",
    #         size=10,
    #         side="buy",
    #         symbol="PI_XBTUSD",
    #         limitPrice=12000,
    #         triggerSignal="mark",
    #         trailingStopDeviationUnit="PERCENT",
    #         trailingStopMaxDeviation=10,
    #     )
    # except KrakenException.KrakenException.KrakenInsufficientAvailableFundsError:
    #     pass


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_create_order_failing(futures_demo_trade: Trade) -> None:
    """
    Checks ``create_order`` endpoint to fail when using invalid parameters.
    """
    with pytest.raises(
        ValueError,
        match=r"Invalid side. One of \[\('buy', 'sell'\)\] is required!",
    ):
        futures_demo_trade.create_order(
            orderType="mkt",
            size=10,
            symbol="PI_XBTUSD",
            side="long",
        )

    with pytest.raises(
        ValueError,
        match=r"Trigger signal must be in \[\('mark', 'spot', 'last'\)\]!",
    ):
        futures_demo_trade.create_order(
            orderType="take-profit",
            size=10,
            side="buy",
            symbol="PI_XBTUSD",
            limitPrice=12000,
            triggerSignal="fail",
            stopPrice=13000,
        )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_create_batch_order(futures_demo_trade: Trade) -> None:
    """
    Checks the ``create_order_batch`` endpoint.
    """
    with suppress(KrakenInsufficientAvailableFundsError):
        assert is_success(
            futures_demo_trade.create_batch_order(
                batchorder_list=[
                    {
                        "order": "send",
                        "order_tag": "1",
                        "orderType": "lmt",
                        "symbol": "PI_XBTUSD",
                        "side": "buy",
                        "size": 5,
                        "limitPrice": 1.00,
                        "cliOrdId": "my_another_client_id",
                    },
                    {
                        "order": "send",
                        "order_tag": "2",
                        "orderType": "stp",
                        "symbol": "PI_XBTUSD",
                        "side": "buy",
                        "size": 1,
                        "limitPrice": 2.00,
                        "stopPrice": 3.00,
                    },
                ],
                processBefore="3033-11-08T19:56:35.441899Z",
            ),
        )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_edit_order(futures_demo_trade: Trade) -> None:
    """
    Checks the ``edit_order`` endpoint.
    """
    assert is_success(
        futures_demo_trade.edit_order(
            orderId="685d5a1a-23eb-450c-bf17-1e4ab5c6fe8a",
            limitPrice=3,
        ),
    )

    assert is_success(
        futures_demo_trade.edit_order(
            cliOrdId="685d5a1a-23eb-450c-bf17-1e4ab5c6fe8a",
            size=111.0,
            stopPrice=1000,
            processBefore="3033-11-08T19:56:35.441899Z",
        ),
    )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_edit_order_failing(futures_demo_trade: Trade) -> None:
    """
    Checks if the ``edit_order`` endpoint fails when using invalid parameters.
    """
    with pytest.raises(ValueError, match=r"Either orderId or cliOrdId must be set!"):
        futures_demo_trade.edit_order()


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_cancel_order(futures_demo_trade: Trade) -> None:
    """
    Checks the ``cancel_order`` endpoint.
    """
    assert is_success(
        futures_demo_trade.cancel_order(
            cliOrdId="my_another_client_id",
            processBefore="3033-11-08T19:56:35.441899Z",
        ),
    )
    assert is_success(
        futures_demo_trade.cancel_order(
            order_id="685d5a1a-23eb-450c-bf17-1e4ab5c6fe8a",
        ),
    )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_cancel_order_failing(futures_demo_trade: Trade) -> None:
    """
    Checks if the ``cancel_order`` endpoint is failing when
    passing invalid arguments.
    """
    with pytest.raises(ValueError, match=r"Either order_id or cliOrdId must be set!"):
        futures_demo_trade.cancel_order()


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_cancel_all_orders(futures_demo_trade: Trade) -> None:
    """
    Checks the ``cancel_all_orders`` endpoint.
    """
    assert is_success(futures_demo_trade.cancel_all_orders(symbol="pi_xbtusd"))
    assert is_success(futures_demo_trade.cancel_all_orders())


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
def test_get_max_order_size(futures_auth_trade: Trade) -> None:
    """
    Checks the ``cancel_all_orders`` endpoint.
    """
    assert is_success(
        futures_auth_trade.get_max_order_size(
            orderType="lmt",
            symbol="PF_XBTUSD",
            limitPrice=10000,
        ),
    )
    assert is_success(
        futures_auth_trade.get_max_order_size(
            orderType="mkt",
            symbol="PF_XBTUSD",
        ),
    )
