#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot market client."""

from time import sleep

import pytest

from kraken.spot import Market

from .helper import is_not_error


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_system_status(spot_market: Market) -> None:
    """
    Checks the ``get_system_status`` endpoint by performing a
    valid request and validating that the response does not
    contain the error key.
    """
    assert is_not_error(spot_market.get_system_status())


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_assets(spot_market: Market) -> None:
    """
    Checks the ``get_assets`` endpoint by performing multiple
    requests with different paramaters and
    validating that the response does not contain the error key.
    """
    for params in (
        {},
        {"assets": "USD"},
        {"assets": ["USD"]},
        {"assets": ["XBT", "USD"]},
        {"assets": ["XBT", "USD"], "aclass": "currency"},
    ):
        assert is_not_error(spot_market.get_assets(**params))
        sleep(1.5)


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_asset_pairs(spot_market: Market) -> None:
    """
    Checks the ``get_tradable_asset_pair`` endpoint by performing multiple
    requests with different paramaters and validating that the response
    does not contain the error key.
    """
    assert is_not_error(spot_market.get_asset_pairs())
    assert is_not_error(spot_market.get_asset_pairs(pair="BTCUSD"))
    assert is_not_error(spot_market.get_asset_pairs(pair=["DOTEUR", "BTCUSD"]))
    for i in ("info", "leverage", "fees", "margin"):
        assert is_not_error(spot_market.get_asset_pairs(pair="DOTEUR", info=i))
        break  # there is no reason for requesting more - but this loop is just for info
    sleep(3)


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_ticker(spot_market: Market) -> None:
    """
    Checks the ``get_ticker`` endpoint by performing multiple
    requests with different paramaters and validating that the response
    does not contain the error key.
    """
    assert is_not_error(spot_market.get_ticker())
    assert is_not_error(spot_market.get_ticker(pair="XBTUSD"))
    assert is_not_error(spot_market.get_ticker(pair=["DOTUSD", "XBTUSD"]))


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_ohlc(spot_market: Market) -> None:
    """
    Checks the ``get_ohlc`` endpoint by performing multiple
    requests with different paramaters and validating that the response
    does not contain the error key.
    """
    assert is_not_error(spot_market.get_ohlc(pair="XBTUSD"))
    assert is_not_error(
        spot_market.get_ohlc(pair="XBTUSD", interval=240, since="1616663618")
    )  # interval in [1 5 15 30 60 240 1440 10080 21600]


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_order_book(spot_market: Market) -> None:
    """
    Checks the ``get_order_book`` endpoint by performing multiple
    requests with different paramaters and validating that the response
    does not contain the error key.
    """
    assert is_not_error(spot_market.get_order_book(pair="XBTUSD"))
    assert is_not_error(
        spot_market.get_order_book(pair="XBTUSD", count=2)
    )  # count in [1...500]


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_recent_trades(spot_market: Market) -> None:
    """
    Checks the ``get_recent_trades`` endpoint by performing multiple
    requests with different paramaters and validating that the response
    does not contain the error key.
    """
    assert is_not_error(spot_market.get_recent_trades(pair="XBTUSD"))
    assert is_not_error(
        spot_market.get_recent_trades(pair="XBTUSD", since="1616663618")
    )


@pytest.mark.spot
@pytest.mark.spot_market
def test_get_recent_spreads(spot_market: Market) -> None:
    """
    Checks the ``get_recent_spreads`` endpoint by performing multiple
    requests with different paramaters and validating that the response
    does not contain the error key.
    """
    assert is_not_error(spot_market.get_recent_spreads(pair="XBTUSD"))
    assert is_not_error(
        spot_market.get_recent_spreads(pair="XBTUSD", since="1616663618")
    )
