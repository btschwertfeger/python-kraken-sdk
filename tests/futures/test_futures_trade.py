#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#
from time import sleep

import pytest

from kraken.exceptions import KrakenException

from .helper import is_success


@pytest.fixture(autouse=True)
def run_before_and_after_tests(futures_demo_trade):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    futures_demo_trade.cancel_all_orders()


def test_get_fills(futures_demo_trade) -> None:
    assert is_success(futures_demo_trade.get_fills())
    assert is_success(
        futures_demo_trade.get_fills(lastFillTime="2020-07-21T12:41:52.790Z")
    )


def test_dead_mans_switch(futures_demo_trade) -> None:
    assert is_success(futures_demo_trade.dead_mans_switch(timeout=60))
    assert is_success(
        futures_demo_trade.dead_mans_switch(timeout=0)
    )  # reset dead mans switch


def test_get_orders_status(futures_demo_trade) -> None:
    assert is_success(
        futures_demo_trade.get_orders_status(
            orderIds=[
                "d47e7fb4-aed0-4f3d-987b-9e3ca78ba74e",
                "fc589be9-5095-48f0-b6f1-a2dfad6d9677",
            ]
        )
    )
    assert is_success(
        futures_demo_trade.get_orders_status(
            cliOrdIds=[
                "2c611222-bfe6-42d1-9f55-77bddc01a313",
                "fc589be9-5095-48f0-b6f1-a2dfad6d9677",
            ]
        )
    )


def test_create_order(futures_demo_trade) -> None:
    try:
        futures_demo_trade.create_order(
            orderType="lmt",
            size=10,
            symbol="PI_XBTUSD",
            side="buy",
            limitPrice=1,
            stopPrice=10,
            reduceOnly=True,
        )
    except KrakenException.KrakenInsufficientAvailableFundsError:
        pass

    try:
        futures_demo_trade.create_order(
            orderType="take_profit",
            size=10,
            side="buy",
            symbol="PI_XBTUSD",
            limitPrice=12000,
            triggerSignal="last",
            stopPrice=13000,
        )
    except KrakenException.KrakenInsufficientAvailableFundsError:
        pass

    # try:
    #     # does not work,  400 repsonse "invalid order type"
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
    # except KrakenException.KrakenInsufficientAvailableFundsError:
    #     pass


def test_failing_create_order(futures_demo_trade) -> None:
    with pytest.raises(ValueError):
        futures_demo_trade.create_order(
            orderType="mkt",
            size=10,
            symbol="PI_XBTUSD",
            side="long",
        )

    with pytest.raises(ValueError):
        futures_demo_trade.create_order(
            orderType="take-profit",
            size=10,
            side="buy",
            symbol="PI_XBTUSD",
            limitPrice=12000,
            triggerSignal="fail",
            stopPrice=13000,
        )


def test_create_batch_order(futures_demo_trade) -> None:
    try:
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
                    {
                        "order": "cancel",
                        "order_id": "e35d61dd-8a30-4d5f-a574-b5593ef0c050",
                    },
                    {
                        "order": "cancel",
                        "cliOrdId": "my_client_id",
                    },
                ],
            )
        )
    except KrakenException.KrakenInsufficientAvailableFundsError:
        pass


def test_edit_order(futures_demo_trade) -> None:
    # success, because kraken received the correct message, even if the id is invalid
    assert is_success(
        futures_demo_trade.edit_order(orderId="my_another_client_id", limitPrice=3)
    )

    assert is_success(
        futures_demo_trade.edit_order(
            cliOrdId="myclientorderid", size=111.0, stopPrice=1000
        )
    )


def test_failing_edit_order(futures_demo_trade) -> None:
    with pytest.raises(ValueError):
        futures_demo_trade.edit_order()


def test_cancel_order(futures_demo_trade) -> None:
    assert is_success(futures_demo_trade.cancel_order(cliOrdId="my_another_client_id"))
    assert is_success(futures_demo_trade.cancel_order(order_id="1234"))


def test_failing_cancel_order(futures_demo_trade) -> None:
    with pytest.raises(ValueError):
        futures_demo_trade.cancel_order()


def test_cancel_all_orders(futures_demo_trade) -> None:
    assert is_success(futures_demo_trade.cancel_all_orders(symbol="pi_xbtusd"))
    assert is_success(futures_demo_trade.cancel_all_orders())
