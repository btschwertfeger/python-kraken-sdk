#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#
from time import sleep

from .helper import is_not_error


def test_get_system_status(spot_auth_market) -> None:
    assert is_not_error(spot_auth_market.get_system_status())


def test_get_assets(spot_auth_market) -> None:
    for params in [
        {},
        {"assets": "USD"},
        {"assets": ["USD"]},
        {"assets": ["XBT", "USD"]},
        {"assets": ["XBT", "USD"], "aclass": "currency"},
    ]:
        assert is_not_error(spot_auth_market.get_assets(**params))
        sleep(1.5)


def test_get_tradable_asset_pair(spot_auth_market) -> None:
    assert is_not_error(spot_auth_market.get_tradable_asset_pair(pair="BTCUSD"))
    assert is_not_error(
        spot_auth_market.get_tradable_asset_pair(pair=["DOTEUR", "BTCUSD"])
    )
    for i in ("info", "leverage", "fees", "margin"):
        assert is_not_error(
            spot_auth_market.get_tradable_asset_pair(pair="DOTEUR", info=i)
        )
        break


def test_get_ticker(spot_auth_market) -> None:
    assert is_not_error(spot_auth_market.get_ticker())
    assert is_not_error(spot_auth_market.get_ticker(pair="XBTUSD"))
    assert is_not_error(spot_auth_market.get_ticker(pair=["DOTUSD", "XBTUSD"]))


def test_get_ohlc(spot_auth_market) -> None:
    assert is_not_error(spot_auth_market.get_ohlc(pair="XBTUSD"))
    assert is_not_error(
        spot_auth_market.get_ohlc(pair="XBTUSD", interval=240, since="1616663618")
    )  # interval in [1 5 15 30 60 240 1440 10080 21600]


def test_get_order_book(spot_auth_market) -> None:
    assert is_not_error(spot_auth_market.get_order_book(pair="XBTUSD"))
    assert is_not_error(
        spot_auth_market.get_order_book(pair="XBTUSD", count=2)
    )  # count in [1...500]


def test_get_recent_trades(spot_auth_market) -> None:
    assert is_not_error(spot_auth_market.get_recent_trades(pair="XBTUSD"))
    assert is_not_error(
        spot_auth_market.get_recent_trades(pair="XBTUSD", since="1616663618")
    )


def test_get_recend_spreads(spot_auth_market) -> None:
    assert is_not_error(spot_auth_market.get_recend_spreads(pair="XBTUSD"))
    assert is_not_error(
        spot_auth_market.get_recend_spreads(pair="XBTUSD", since="1616663618")
    )
