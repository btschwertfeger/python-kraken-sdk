#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#
from datetime import datetime, timedelta, timezone

import pytest

from kraken.exceptions import KrakenException


def test_create_order(spot_auth_trade) -> None:
    try:
        assert isinstance(
            spot_auth_trade.create_order(
                ordertype="limit",
                side="buy",
                volume=1,
                oflags=["post"],
                pair="BTC/EUR",
                price=0.01,
                timeinforce="GTC",
                validate=True,  # important to just test this endpoint without risking money
            ),
            dict,
        )
    except KrakenException.KrakenPermissionDeniedError:
        pass

    try:
        assert isinstance(
            spot_auth_trade.create_order(
                ordertype="limit",
                side="buy",
                volume=10000000,
                oflags=["post"],
                pair="BTC/EUR",
                price=0.01,
                expiretm="0",
                displayvol=1000,
                validate=True,  # important to just test this endpoint without risking money
            ),
            dict,
        )
    except KrakenException.KrakenPermissionDeniedError:
        pass

    try:
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
    except KrakenException.KrakenPermissionDeniedError:
        pass

    try:
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
    except KrakenException.KrakenPermissionDeniedError:
        pass


def test_failing_create_order(spot_auth_trade) -> None:
    # stop-loss-limit (and take-profit-limit) require a second price `price2`)
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


def test_create_order_batch(spot_auth_trade) -> None:
    assert isinstance(
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
                    "userref": "345dsdfddfgdsgdfgsfdsfsdf",
                    "volume": 1000,
                },
                {
                    "ordertype": "limit",
                    "price": 150,
                    "timeinforce": "GTC",
                    "type": "sell",
                    "userref": "1dfgesggwe5t3",
                    "volume": 123,
                },
            ],
            pair="BTC/USD",
            validate=True,  # important
        ),
        dict,
    )


def test_edit_order(spot_auth_trade) -> None:
    try:
        assert isinstance(
            spot_auth_trade.edit_order(
                txid="OHYO67-6LP66-HMQ437",
                userref="12345678",
                volume=1.25,
                pair="XBTUSD",
                price=27500,
                price2=26500,
                cancel_response=False,
                oflags=["post"],
                validate=True,
            ),
            dict,
        )
    except KrakenException.KrakenPermissionDeniedError:
        pass


def test_cancel_order(spot_auth_trade) -> None:
    # because testing keys are not allowd to trade
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        spot_auth_trade.cancel_order(txid="OB6JJR-7NZ5P-N5SKCB")


@pytest.mark.skip(reason="Skipping Spot test_cancel_all_orders endpoint")
def test_cancel_all_orders(spot_auth_trade) -> None:
    try:
        assert isinstance(spot_auth_trade.cancel_all_orders(), dict)
    except KrakenException.KrakenPermissionDeniedError:
        pass


@pytest.mark.skip(reason="Skipping Spot test_cancel_all_orders_after_x endpoint")
def test_cancel_all_orders_after_x(spot_auth_trade) -> None:
    try:
        assert isinstance(spot_auth_trade.cancel_all_orders_after_x(timeout=6), dict)
    except KrakenException.KrakenPermissionDeniedError:
        pass


def test_cancel_order_batch(spot_auth_trade) -> None:
    assert isinstance(
        spot_auth_trade.cancel_order_batch(
            orders=[
                "O2JLFP-VYFIW-35ZAAE",
                "O523KJ-DO4M2-KAT243",
                "OCDIAL-YC66C-DOF7HS",
                "OVFPZ2-DA2GV-VBFVVI",
            ]
        ),
        dict,
    )
