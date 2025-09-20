# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures market client."""

from typing import Any, Self

import pytest

from kraken.futures import Market

from .helper import is_not_error, is_success


@pytest.mark.futures
@pytest.mark.futures_market
class TestFuturesMarket:
    """Test class for Futures Market client functionality."""

    SYMBOL = "PI_XBTUSD"
    TRADEABLE = "PF_SOLUSD"
    SINCE = "1668989233"
    BEFORE = "1668999999"

    def _assert_successful_response(self: Self, result: Any) -> None:
        """Helper method to assert a successful response."""
        assert is_success(result)

    def _assert_not_error_response(self: Self, result: Any) -> None:
        """Helper method to assert a response without errors."""
        assert is_not_error(result)

    def test_get_ohlc(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_ohlc`` endpoint.
        """
        assert isinstance(
            futures_market.get_ohlc(
                tick_type="trade",
                symbol=self.SYMBOL,
                resolution="1m",
                from_=self.SINCE,
                to=self.BEFORE,
            ),
            dict,
        )

    def test_get_ohlc_failing_wrong_tick_type(
        self: Self,
        futures_market: Market,
    ) -> None:
        """
        Checks the ``get_ohlc`` function by passing an invalid tick type.
        """
        with pytest.raises(
            ValueError,
            match=r"tick_type must be in \('spot', 'mark', 'trade'\)",
        ):
            futures_market.get_ohlc(
                symbol=self.SYMBOL,
                resolution="240",
                tick_type="fail",
            )

    def test_get_ohlc_failing_wrong_resolution(
        self: Self,
        futures_market: Market,
    ) -> None:
        """
        Checks the ``get_ohlc`` function by passing an invalid resolution.
        """
        with pytest.raises(
            ValueError,
            match=r"resolution must be in \('1m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w'\)",
        ):
            futures_market.get_ohlc(
                symbol=self.SYMBOL,
                resolution="1234",
                tick_type="trade",
            )

    def test_get_tick_types(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_tick_types`` endpoint.
        """
        assert isinstance(futures_market.get_tick_types(), list)

    def test_get_tradeable_products(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_tradeable_products`` endpoint.
        """
        assert isinstance(futures_market.get_tradeable_products(tick_type="mark"), list)

    def test_get_resolutions(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_resolutions`` endpoint.
        """
        assert isinstance(
            futures_market.get_resolutions(tick_type="trade", tradeable=self.SYMBOL),
            list,
        )

    def test_get_fee_schedules(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_fee_schedules`` endpoint.
        """
        self._assert_successful_response(futures_market.get_fee_schedules())

    @pytest.mark.futures
    @pytest.mark.futures_auth
    @pytest.mark.futures_market
    def test_get_fee_schedules_vol(self: Self, futures_auth_market: Market) -> None:
        """
        Checks the ``get_fee_schedules_vol`` endpoint.
        """
        self._assert_successful_response(futures_auth_market.get_fee_schedules_vol())

    def test_get_orderbook(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_orderbook`` endpoint.
        """
        # assert type(market.get_orderbook()) == dict # raises 500-INTERNAL_SERVER_ERROR on Kraken,
        # but symbol is optional as described in the API documentation (Dec, 2022)
        self._assert_successful_response(
            futures_market.get_orderbook(symbol=self.SYMBOL),
        )

    def test_get_tickers(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_tickers`` endpoint.
        """
        self._assert_successful_response(futures_market.get_tickers())

    def test_get_instruments(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_instruments`` endpoint.
        """
        self._assert_successful_response(futures_market.get_instruments())

    def test_get_instruments_status(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_instruments_status`` endpoint.
        """
        self._assert_successful_response(futures_market.get_instruments_status())
        self._assert_successful_response(
            futures_market.get_instruments_status(instrument=self.SYMBOL),
        )

    def test_get_trade_history(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_trade_history`` endpoint.
        """
        self._assert_successful_response(
            futures_market.get_trade_history(symbol=self.SYMBOL),
        )

    def test_get_historical_funding_rates(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_historical_funding_rates`` endpoint.
        """
        self._assert_successful_response(
            futures_market.get_historical_funding_rates(symbol=self.SYMBOL),
        )

    @pytest.mark.futures_auth
    def test_get_leverage_preference(self: Self, futures_auth_market: Market) -> None:
        """
        Checks the ``get_leverage_preference`` endpoint.
        """
        self._assert_not_error_response(futures_auth_market.get_leverage_preference())

    @pytest.mark.futures_auth
    @pytest.mark.skip(reason="Tests do not have trade permission")
    def test_set_leverage_preference(self: Self, futures_auth_market: Market) -> None:
        """
        Checks the ``set_leverage_preference`` endpoint.
        """
        old_preferences = futures_auth_market.get_leverage_preference()
        assert "result" in old_preferences
        assert old_preferences["result"] == "success"
        try:
            self._assert_successful_response(
                futures_auth_market.set_leverage_preference(
                    symbol=self.SYMBOL,
                    maxLeverage=2,
                ),
            )

            new_preferences = futures_auth_market.get_leverage_preference()
            assert "result" in new_preferences
            assert new_preferences["result"] == "success"
            assert "leveragePreferences" in new_preferences
            assert {"symbol": self.SYMBOL, "maxLeverage": 2.0} in new_preferences[
                "leveragePreferences"
            ]
        finally:
            if "leveragePreferences" in old_preferences:
                for setting in old_preferences["leveragePreferences"]:
                    if "symbol" in setting and setting["symbol"] == self.SYMBOL:
                        self._assert_successful_response(
                            futures_auth_market.set_leverage_preference(
                                symbol=self.SYMBOL,
                            ),
                        )
                        break

    @pytest.mark.futures_auth
    def test_get_pnl_preference(self: Self, futures_auth_market: Market) -> None:
        """
        Checks the ``get_pnl_preference`` endpoint.
        """
        self._assert_not_error_response(futures_auth_market.get_pnl_preference())

    @pytest.mark.futures_auth
    @pytest.mark.skip(reason="Tests do not have trade permission")
    def test_set_pnl_preference(self: Self, futures_auth_market: Market) -> None:
        """
        Checks the ``set_pnl_preference`` endpoint.
        """
        old_preference = futures_auth_market.get_pnl_preference()
        assert "result" in old_preference
        assert old_preference["result"] == "success"
        try:
            self._assert_successful_response(
                futures_auth_market.set_pnl_preference(
                    symbol=self.SYMBOL,
                    pnlPreference="BTC",
                ),
            )

            new_preference = futures_auth_market.get_pnl_preference()
            assert "result" in new_preference
            assert new_preference["result"] == "success"
            assert "preferences" in new_preference
            assert {"symbol": self.SYMBOL, "pnlCurrency": "BTC"} in new_preference[
                "preferences"
            ]
        finally:
            if "preferences" in old_preference:
                for setting in old_preference["preferences"]:
                    if "symbol" in setting and setting["symbol"] == self.SYMBOL:
                        self._assert_successful_response(
                            futures_auth_market.set_pnl_preference(
                                symbol=self.SYMBOL,
                                pnlPreference=setting["pnlCurrency"],
                            ),
                        )
                        break

    def test_get_public_execution_events(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_public_execution_events`` endpoint.
        """
        self._assert_not_error_response(
            futures_market.get_public_execution_events(
                tradeable=self.TRADEABLE,
                since=int(self.SINCE),
                before=int(self.BEFORE),
            ),
        )

    def test_get_public_order_events(self: Self, futures_market: Market) -> None:
        """
        Checks the ``public_order_events`` endpoint.
        """
        self._assert_not_error_response(
            futures_market.get_public_order_events(
                tradeable=self.TRADEABLE,
                since=int(self.SINCE),
                sort="asc",
            ),
        )

    def test_get_public_mark_price_events(self: Self, futures_market: Market) -> None:
        """
        Checks the ``get_public_mark_price_events`` endpoint.
        """
        self._assert_not_error_response(
            futures_market.get_public_mark_price_events(
                tradeable=self.TRADEABLE,
                since=int(self.SINCE),
            ),
        )
