#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot user client."""

from time import sleep

import pytest

from kraken.spot import Utils


@pytest.mark.spot
@pytest.mark.spot_market
def test_utils_truncate_price() -> None:
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
            Utils.truncate(amount=price, amount_type="price", pair="XBTUSD") == expected
        )
    sleep(3)

    for price, expected in (
        (2, "2.0000"),
        (12.1, "12.1000"),
        (13.105, "13.1050"),
        (4.32595, "4.3259"),
    ):
        assert (
            Utils.truncate(amount=price, amount_type="price", pair="DOTUSD") == expected
        )
    sleep(3)


@pytest.mark.spot
@pytest.mark.spot_market
def test_utils_truncate_volume() -> None:
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
            Utils.truncate(amount=volume, amount_type="volume", pair="XBTUSD")
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
            Utils.truncate(amount=volume, amount_type="volume", pair="DOTUSD")
            == expected
        )
    sleep(3)


@pytest.mark.spot
@pytest.mark.spot_market
def test_utils_truncate_fail_price_costmin() -> None:
    """
    Checks if the truncate function fails if the price is less than the costmin.

    NOTE: This test may break in the future since the lot_decimals, pair_decimals,
    ordermin and costmin attributes could change.
    """
    with pytest.raises(ValueError):
        Utils.truncate(amount=0.001, amount_type="price", pair="XBTUSD")


@pytest.mark.spot
@pytest.mark.spot_market
def test_utils_truncate_fail_volume_ordermin() -> None:
    """
    Checks if the truncate function fails if the volume is less than the ordermin.

    NOTE: This test may break in the future since the lot_decimals, pair_decimals,
    ordermin and costmin attributes could change.
    """
    with pytest.raises(ValueError):
        Utils.truncate(amount=0.00001, amount_type="volume", pair="XBTUSD")


@pytest.mark.spot
@pytest.mark.spot_market
@pytest.mark.selection
def test_utils_truncate_fail_invalid_amount_type() -> None:
    """
    Checks if the truncate function fails when no valid ``amount_type`` was specified.

    NOTE: This test may break in the future since the lot_decimals, pair_decimals,
    ordermin and costmin attributes could change.
    """
    with pytest.raises(ValueError):
        Utils.truncate(amount=1, amount_type="invalid", pair="XBTUSD")
