#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot trade client."""

from datetime import datetime, timedelta, timezone
from time import sleep

import pytest

from kraken.exceptions import KrakenException
from kraken.spot import Trade

# todo: Mock skipped tests - or is this to dangerous?


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
def test_create_order(spot_auth_trade: Trade) -> None:
    """
    This test checks the ``create_order`` function by performing
    calls to create an order - but in validate mode - so that
    no real order is placed. The KrakenException.KrakenPermissionDeniedError
    will be raised since the CI does not have trade permission.
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert isinstance(
            spot_auth_trade.create_order(
                ordertype="limit",
                side="buy",
                volume=1.001,
                oflags=["post"],
                pair="BTC/EUR",
                price=1.001,  # this also checks the truncate option
                timeinforce="GTC",
                truncate=True,
                validate=True,  # important to just test this endpoint without risking money
            ),
            dict,
        )

    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert isinstance(
            spot_auth_trade.create_order(
                ordertype="limit",
                side="buy",
                volume=10000000,
                oflags=["post"],
                pair="BTC/EUR",
                price=100,
                expiretm="0",
                displayvol=1000,
                validate=True,  # important to just test this endpoint without risking money
            ),
            dict,
        )

    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert isinstance(
            spot_auth_trade.create_order(
                ordertype="stop-loss",
                side="sell",
                volume="1000",
                trigger="last",
                pair="XBTUSD",
                price="100",
                leverage="2",
                reduce_only=True,
                userref="12345",
                close_ordertype="limit",
                close_price="123",
                close_price2="92",
                validate=True,
            ),
            dict,
        )

    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        deadline = (datetime.now(timezone.utc) + timedelta(seconds=20)).isoformat()
        spot_auth_trade.create_order(
            ordertype="stop-loss-limit",
            pair="XBTUSD",
            side="buy",
            volume=0.001,
            price=25000,
            price2=27000,
            validate=True,
            trigger="last",
            timeinforce="GTC",
            leverage=4,
            deadline=deadline,
        )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
def test_failing_create_order(spot_auth_trade: Trade) -> None:
    """
    Test that checks if the ``create_order`` function raises a ValueError
    because of missing or invalid parameters.
    > stop-loss-limit (and take-profit-limit) require a second price ``price2``)
    """
    with pytest.raises(ValueError):
        spot_auth_trade.create_order(
            ordertype="stop-loss-limit",
            pair="XBTUSD",
            side="buy",
            volume=0.001,
            price=25000,
            timeinforce="GTC",
            leverage=4,
            validate=True,
        )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
def test_create_order_batch(spot_auth_trade: Trade) -> None:
    """
    Checks the ``create_order_batch`` function by executing
    a batch order in validate mode. (Permission denied,
    since the CI does not have trade permissions)
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        spot_auth_trade.create_order_batch(
            orders=[
                {
                    "close": {
                        "ordertype": "stop-loss-limit",
                        "price": 120,
                        "price2": 110,
                    },
                    "ordertype": "limit",
                    "price": 140,
                    "price2": 130,
                    "timeinforce": "GTC",
                    "type": "buy",
                    "userref": 1680953421,
                    "volume": 1000,
                },
                {
                    "ordertype": "limit",
                    "price": 150,
                    "timeinforce": "GTC",
                    "type": "sell",
                    "userref": 1680953421,
                    "volume": 123,
                },
            ],
            pair="BTC/USD",
            validate=True,  # important
        )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
def test_edit_order(spot_auth_trade: Trade) -> None:
    """
    Test the ``edit_order`` function by editing an order.

    KrakenException.KrakenPermissionDeniedError: since CI does not have
    trade permissions. If the request would be malformed, another
    exception could be observed.
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        spot_auth_trade.edit_order(
            txid="OHYO67-6LP66-HMQ437",
            userref="12345678",
            volume=1.25,
            pair="XBTUSD",
            price=27500,
            price2=26500,
            cancel_response=False,
            truncate=True,
            oflags=["post"],
            validate=True,
        )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
def test_cancel_order(spot_auth_trade: Trade) -> None:
    """
    Checks the ``cancel_order`` function by canceling an order.

    A KrakenException.KrakenPermissionDeniedError is expected since CI keys are
    not allowed to trade/cancel/withdraw/stake.
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        spot_auth_trade.cancel_order(txid="OB6JJR-7NZ5P-N5SKCB")


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
@pytest.mark.skip(reason="CI does not have trade/cancel permission")
def test_cancel_all_orders(spot_auth_trade: Trade) -> None:
    """
    Checks the ``cancel_all_orders`` endpoint by executing the function.
    A KrakenException.KrakenPermissionDeniedError will be raised since the CI API keys
    do not have cancel permission.
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert isinstance(spot_auth_trade.cancel_all_orders(), dict)


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
@pytest.mark.skip(reason="CI does not have trade/cancel permission")
def test_cancel_all_orders_after_x(spot_auth_trade: Trade) -> None:
    """
    Checks the ``cancel_all_orders_after_x`` function by validating its response data
    type.

    THe KrakenException.KrakenPermissionDeniedError will be caught since the CI API keys are not
    allowed to cancel orders.
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert isinstance(spot_auth_trade.cancel_all_orders_after_x(timeout=0), dict)


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_trade()
def test_cancel_order_batch(spot_auth_trade: Trade) -> None:
    """
    Tests the ``cancel_order_batch`` function by cancelling dummy orders that
    do not exist anymore. Error will be raised since the CI do not have trade
    permissions.
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert isinstance(
            spot_auth_trade.cancel_order_batch(
                orders=[
                    "O2JLFP-VYFIW-35ZAAE",
                    "O523KJ-DO4M2-KAT243",
                    "OCDIAL-YC66C-DOF7HS",
                    "OVFPZ2-DA2GV-VBFVVI",
                ],
            ),
            dict,
        )


@pytest.mark.spot()
@pytest.mark.spot_trade()
def test_truncate_price(spot_trade: Trade) -> None:
    """
    Checks if the truncate function returns the expected results by
    checking different inputs for price.

    NOTE: This test may break in the future since the lot_decimals, pair_decimals,
    ordermin and costmin attributes could change.
    """
    for price, expected in (
        (10000, "10000.0"),
        (1000.1, "1000.1"),
        (1000.01, "1000.0"),
        (1000.001, "1000.0"),
    ):
        assert (
            spot_trade.truncate(amount=price, amount_type="price", pair="XBTUSD")
            == expected
        )
    sleep(3)

    for price, expected in (
        (2, "2.0000"),
        (12.1, "12.1000"),
        (13.105, "13.1050"),
        (4.32595, "4.3259"),
    ):
        assert (
            spot_trade.truncate(amount=price, amount_type="price", pair="DOTUSD")
            == expected
        )
    sleep(3)


@pytest.mark.spot()
@pytest.mark.spot_trade()
def test_truncate_volume(spot_trade: Trade) -> None:
    """
    Checks if the truncate function returns the expected results by
    checking different inputs for volume.

    NOTE: This test may break in the future since the lot_decimals, pair_decimals,
    ordermin and costmin attributes could change.
    """
    for volume, expected in (
        (1, "1.00000000"),
        (1.1, "1.10000000"),
        (1.67, "1.67000000"),
        (1.9328649837, "1.93286498"),
    ):
        assert (
            spot_trade.truncate(amount=volume, amount_type="volume", pair="XBTUSD")
            == expected
        )
    sleep(3)

    for volume, expected in (
        (2, "2.00000000"),
        (12.158, "12.15800000"),
        (13.1052093, "13.10520930"),
        (4.32595342455, "4.32595342"),
    ):
        assert (
            spot_trade.truncate(amount=volume, amount_type="volume", pair="DOTUSD")
            == expected
        )
    sleep(3)


@pytest.mark.spot()
@pytest.mark.spot_trade()
def test_truncate_fail_price_costmin(spot_trade: Trade) -> None:
    """
    Checks if the truncate function fails if the price is less than the costmin.

    NOTE: This test may break in the future since the lot_decimals, pair_decimals,
    ordermin and costmin attributes could change.
    """
    with pytest.raises(ValueError):
        spot_trade.truncate(amount=0.001, amount_type="price", pair="XBTUSD")


@pytest.mark.spot()
@pytest.mark.spot_trade()
def test_truncate_fail_volume_ordermin(spot_trade: Trade) -> None:
    """
    Checks if the truncate function fails if the volume is less than the ordermin.

    NOTE: This test may break in the future since the lot_decimals, pair_decimals,
    ordermin and costmin attributes could change.
    """
    with pytest.raises(ValueError):
        spot_trade.truncate(amount=0.00001, amount_type="volume", pair="XBTUSD")


@pytest.mark.spot()
@pytest.mark.spot_trade()
def test_truncate_fail_invalid_amount_type(spot_trade: Trade) -> None:
    """
    Checks if the truncate function fails when no valid ``amount_type`` was specified.
    """
    with pytest.raises(ValueError):
        spot_trade.truncate(amount=1, amount_type="invalid", pair="XBTUSD")
