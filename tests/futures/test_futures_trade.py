# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the integration tests for the Futures trade client"""

from collections.abc import Generator
from contextlib import suppress
from time import sleep
from typing import Any, ClassVar, Self

import pytest

from kraken.exceptions import KrakenInsufficientAvailableFundsError
from kraken.futures import Trade

from .helper import is_success


@pytest.fixture(autouse=True)
def _run_before_and_after_tests(
    request: pytest.FixtureRequest,
    futures_demo_available: bool,
) -> Generator:
    """
    Fixture that skips tests depending on the Kraken Futures demo environment
    when it is unavailable and ensures all orders are cancelled after each test.
    """
    # Setup: skip tests that need the demo environment when it is down.
    if "futures_demo_trade" in request.fixturenames and not futures_demo_available:
        pytest.skip("Kraken Futures demo environment is unavailable")

    yield  # this is where the testing happens

    # Teardown: only clean up when the test actually used the demo client.
    if futures_demo_available and "futures_demo_trade" in request.fixturenames:
        request.getfixturevalue("futures_demo_trade").cancel_all_orders()
        sleep(0.25)


@pytest.mark.integration
@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_trade
class TestFuturesTrade:
    """Test class for Futures Trade client functionality."""

    SYMBOL = "PI_XBTUSD"
    ORDER_TYPE_LIMIT = "lmt"
    ORDER_TYPE_MARKET = "mkt"
    ORDER_TYPE_TAKE_PROFIT = "take_profit"
    SIDE_BUY = "buy"
    SIDE_SELL = "sell"
    INVALID_SIDE = "long"
    SIZE = 10
    LIMIT_PRICE = 1
    STOP_PRICE = 10
    LIMIT_PRICE_HIGH = 12000
    STOP_PRICE_HIGH = 13000
    TRIGGER_SIGNAL_LAST = "last"
    TRIGGER_SIGNAL_MARK = "mark"
    TRIGGER_SIGNAL_INVALID = "fail"
    REDUCE_ONLY = True
    PROCESS_BEFORE = "3033-11-08T19:56:35.441899Z"
    LAST_FILL_TIME = "2020-07-21T12:41:52.790Z"
    TEST_ORDER_IDS: ClassVar[list[str]] = [
        "bcaaefce-27a3-44b4-b13a-19df21e3f087",
        "685d5a1a-23eb-450c-bf17-1e4ab5c6fe8a",
    ]

    def _assert_successful_response(self: Self, result: Any) -> None:
        """Helper method to assert a successful response."""
        assert is_success(result)

    def test_get_fills(self: Self, futures_auth_trade: Trade) -> None:
        """
        Checks the ``get_fills`` endpoint.
        """
        self._assert_successful_response(futures_auth_trade.get_fills())
        self._assert_successful_response(
            futures_auth_trade.get_fills(lastFillTime=self.LAST_FILL_TIME),
        )

    def test_dead_mans_switch(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks the ``dead_mans_switch`` endpoint.
        """
        self._assert_successful_response(
            futures_demo_trade.dead_mans_switch(timeout=60),
        )
        self._assert_successful_response(
            futures_demo_trade.dead_mans_switch(timeout=0),
        )  # reset dead mans switch

    def test_get_orders_status(self: Self, futures_auth_trade: Trade) -> None:
        """
        Checks the ``get_orders_status`` endpoint.
        """
        self._assert_successful_response(
            futures_auth_trade.get_orders_status(
                orderIds=self.TEST_ORDER_IDS,
            ),
        )

        self._assert_successful_response(
            futures_auth_trade.get_orders_status(
                cliOrdIds=self.TEST_ORDER_IDS,
            ),
        )

    def test_create_order(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks the ``create_order`` endpoint.
        """
        with suppress(KrakenInsufficientAvailableFundsError):
            futures_demo_trade.create_order(
                orderType=self.ORDER_TYPE_LIMIT,
                size=self.SIZE,
                symbol=self.SYMBOL,
                side=self.SIDE_BUY,
                limitPrice=self.LIMIT_PRICE,
                stopPrice=self.STOP_PRICE,
                reduceOnly=self.REDUCE_ONLY,
                processBefore=self.PROCESS_BEFORE,
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

    def test_create_order_failing(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks ``create_order`` endpoint to fail when using invalid parameters.
        """
        with pytest.raises(
            ValueError,
            match=r"Invalid side. One of \[\('buy', 'sell'\)\] is required!",
        ):
            futures_demo_trade.create_order(
                orderType=self.ORDER_TYPE_MARKET,
                size=self.SIZE,
                symbol=self.SYMBOL,
                side=self.INVALID_SIDE,
            )

        with pytest.raises(
            ValueError,
            match=r"Trigger signal must be in \[\('mark', 'spot', 'last'\)\]!",
        ):
            futures_demo_trade.create_order(
                orderType=self.ORDER_TYPE_TAKE_PROFIT,
                size=self.SIZE,
                side=self.SIDE_BUY,
                symbol=self.SYMBOL,
                limitPrice=self.LIMIT_PRICE_HIGH,
                triggerSignal=self.TRIGGER_SIGNAL_INVALID,
                stopPrice=self.STOP_PRICE_HIGH,
            )

    def test_create_batch_order(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks the ``create_order_batch`` endpoint.
        """
        with suppress(KrakenInsufficientAvailableFundsError):
            self._assert_successful_response(
                futures_demo_trade.create_batch_order(
                    batchorder_list=[
                        {
                            "order": "send",
                            "order_tag": "1",
                            "orderType": self.ORDER_TYPE_LIMIT,
                            "symbol": self.SYMBOL,
                            "side": self.SIDE_BUY,
                            "size": 5,
                            "limitPrice": self.LIMIT_PRICE,
                            "cliOrdId": "my_another_client_id",
                        },
                        {
                            "order": "send",
                            "order_tag": "2",
                            "orderType": "stp",
                            "symbol": self.SYMBOL,
                            "side": self.SIDE_BUY,
                            "size": 1,
                            "limitPrice": 2.00,
                            "stopPrice": 3.00,
                        },
                        {
                            "order": "send",
                            "order_tag": "3",
                            "orderType": "post",
                            "symbol": self.SYMBOL,
                            "side": self.SIDE_BUY,
                            "size": 5,
                            "limitPrice": self.LIMIT_PRICE,
                            "reduceOnly": self.REDUCE_ONLY,
                        },
                    ],
                    processBefore=self.PROCESS_BEFORE,
                ),
            )

    def test_edit_order(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks the ``edit_order`` endpoint.
        """
        self._assert_successful_response(
            futures_demo_trade.edit_order(
                orderId=self.TEST_ORDER_IDS[1],
                limitPrice=3,
            ),
        )

        self._assert_successful_response(
            futures_demo_trade.edit_order(
                cliOrdId=self.TEST_ORDER_IDS[1],
                size=111.0,
                stopPrice=1000,
                processBefore=self.PROCESS_BEFORE,
            ),
        )

        with pytest.raises(
            ValueError,
            match=r"Either orderId or cliOrdId must be set!",
        ):
            futures_demo_trade.edit_order()

    def test_cancel_order(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks the ``cancel_order`` endpoint.
        """
        self._assert_successful_response(
            futures_demo_trade.cancel_order(
                cliOrdId="my_another_client_id",
                processBefore=self.PROCESS_BEFORE,
            ),
        )
        self._assert_successful_response(
            futures_demo_trade.cancel_order(
                order_id=self.TEST_ORDER_IDS[1],
            ),
        )

    def test_cancel_order_failing(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks if the ``cancel_order`` endpoint is failing when
        passing invalid arguments.
        """
        with pytest.raises(
            ValueError,
            match=r"Either order_id or cliOrdId must be set!",
        ):
            futures_demo_trade.cancel_order()

    def test_cancel_all_orders(self: Self, futures_demo_trade: Trade) -> None:
        """
        Checks the ``cancel_all_orders`` endpoint.
        """
        self._assert_successful_response(
            futures_demo_trade.cancel_all_orders(symbol=self.SYMBOL.lower()),
        )
        self._assert_successful_response(futures_demo_trade.cancel_all_orders())
