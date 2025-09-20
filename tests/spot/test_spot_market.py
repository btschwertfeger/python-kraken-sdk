# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot market client."""

from time import sleep
from typing import Any, Self

import pytest

from kraken.spot import Market

from .helper import is_not_error


@pytest.mark.spot
@pytest.mark.spot_market
class TestSpotMarket:
    """Test class for Spot Market client functionality."""

    TEST_PAIR_BTCUSD = "XBTUSD"
    TEST_PAIR_DOTUSD = "DOTUSD"
    TEST_PAIR_DOTEUR = "DOTEUR"
    TEST_ASSET_BTC = "XBT"
    TEST_ASSET_ETH = "ETH"
    TEST_ASSET_USD = "USD"
    TEST_INTERVAL = 240
    TEST_SINCE = "1616663618"
    TEST_COUNT = 2

    def _assert_not_error(self: Self, result: Any) -> None:  # noqa: ANN401
        """Helper method to assert responses without errors."""
        assert is_not_error(result)

    def test_get_system_status(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_system_status`` endpoint by performing a
        valid request and validating that the response does not
        contain the error key.
        """
        self._assert_not_error(spot_market.get_system_status())

    def test_get_assets(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_assets`` endpoint by performing multiple
        requests with different parameters and
        validating that the response does not contain the error key.
        """
        for params in (
            {},
            {"assets": self.TEST_ASSET_USD},
            {"assets": [self.TEST_ASSET_USD]},
            {"assets": [f"{self.TEST_ASSET_BTC},{self.TEST_ASSET_USD}"]},
            {
                "assets": [self.TEST_ASSET_BTC, self.TEST_ASSET_USD],
                "aclass": "currency",
            },
        ):
            self._assert_not_error(spot_market.get_assets(**params))
        sleep(3)

    def test_get_asset_pairs(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_asset_pairs`` endpoint by performing multiple
        requests with different parameters and validating that the response
        does not contain the error key.
        """
        self._assert_not_error(spot_market.get_asset_pairs())
        self._assert_not_error(spot_market.get_asset_pairs(pair=self.TEST_PAIR_BTCUSD))
        self._assert_not_error(
            spot_market.get_asset_pairs(
                pair=[self.TEST_PAIR_DOTEUR, self.TEST_PAIR_BTCUSD],
            ),
        )
        for i in ("info", "leverage", "fees", "margin"):
            self._assert_not_error(
                spot_market.get_asset_pairs(pair=self.TEST_PAIR_DOTEUR, info=i),
            )
            break  # there is not reason for requesting more, this is just for info
        sleep(3)

    def test_get_ticker(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_ticker`` endpoint by performing multiple
        requests with different parameters and validating that the response
        does not contain the error key.
        """
        self._assert_not_error(spot_market.get_ticker())
        self._assert_not_error(spot_market.get_ticker(pair=self.TEST_PAIR_BTCUSD))
        self._assert_not_error(
            spot_market.get_ticker(pair=[self.TEST_PAIR_DOTUSD, self.TEST_PAIR_BTCUSD]),
        )

    def test_get_ohlc(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_ohlc`` endpoint by performing multiple
        requests with different parameters and validating that the response
        does not contain the error key.
        """
        self._assert_not_error(spot_market.get_ohlc(pair=self.TEST_PAIR_BTCUSD))
        self._assert_not_error(
            spot_market.get_ohlc(
                pair=self.TEST_PAIR_BTCUSD,
                interval=self.TEST_INTERVAL,
                since=self.TEST_SINCE,
            ),
        )

    def test_get_order_book(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_order_book`` endpoint by performing multiple
        requests with different parameters and validating that the response
        does not contain the error key.
        """
        self._assert_not_error(spot_market.get_order_book(pair=self.TEST_PAIR_BTCUSD))
        self._assert_not_error(
            spot_market.get_order_book(
                pair=self.TEST_PAIR_BTCUSD,
                count=self.TEST_COUNT,
            ),
        )

    def test_get_recent_trades(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_recent_trades`` endpoint by performing multiple
        requests with different parameters and validating that the response
        does not contain the error key.
        """
        self._assert_not_error(
            spot_market.get_recent_trades(pair=self.TEST_PAIR_BTCUSD),
        )
        self._assert_not_error(
            spot_market.get_recent_trades(
                pair=self.TEST_PAIR_BTCUSD,
                since=self.TEST_SINCE,
                count=self.TEST_COUNT,
            ),
        )

    def test_get_recent_spreads(self: Self, spot_market: Market) -> None:
        """
        Checks the ``get_recent_spreads`` endpoint by performing multiple
        requests with different parameters and validating that the response
        does not contain the error key.
        """
        self._assert_not_error(
            spot_market.get_recent_spreads(pair=self.TEST_PAIR_BTCUSD),
        )
        self._assert_not_error(
            spot_market.get_recent_spreads(
                pair=self.TEST_PAIR_BTCUSD,
                since=self.TEST_SINCE,
            ),
        )

    def test_extra_parameter(self: Self, spot_market: Market) -> None:
        """
        Checks if the extra parameter can be used to overwrite an existing one.
        This also checks ensure_string for this parameter.
        """
        result: dict = spot_market.get_assets(
            assets=self.TEST_ASSET_BTC,
            extra_params={"asset": self.TEST_ASSET_ETH},
        )
        assert self.TEST_ASSET_BTC not in result
        assert f"X{self.TEST_ASSET_ETH}" in result
