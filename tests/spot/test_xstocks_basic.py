# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2025 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot xStocks features."""

from typing import ClassVar, Self

import pytest

from kraken.exceptions import KrakenPermissionDeniedError
from kraken.spot import Market, SpotClient, Trade


@pytest.mark.spot
@pytest.mark.xstocks
@pytest.mark.skip(reason="xStocks is only available in certain regions!")
class TestSpotXStocks:
    """Test class for Spot xStocks client functionality."""

    SAVE_ORDER: ClassVar[dict[str, str]] = {
        "pair": "AAPLxUSD",
        "ordertype": "limit",
        "volume": "1",
        "price": "100.0",
        "validate": True,
    }

    def test_get_asset_pairs_market_client(
        self: Self,
        xstocks_market_client: Market,
    ) -> None:
        """
        Checks the ``get_asset_pairs`` endpoint by performing a valid request
        and validating that the response does not contain the error key.
        """
        # internal exception handling would catch any errors
        result = xstocks_market_client.get_asset_pairs(
            extra_params={"aclass_base": "tokenized_asset"},
        )
        assert isinstance(result, dict), result

    def test_get_asset_pairs_spot_client(
        self: Self,
        xstocks_client: SpotClient,
    ) -> None:
        """
        Checks the ``get_asset_pairs`` endpoint by performing a valid request
        and validating that the response does not contain the error key.
        """
        # internal exception handling would catch any errors
        result = xstocks_client.request(
            "GET",
            "/0/public/AssetPairs",
            params={"aclass_base": "tokenized_asset"},
            auth=False,
        )
        assert isinstance(result, dict), result

    @pytest.mark.spot_auth
    def test_create_order_trade_client(
        self: Self,
        xstocks_trade_client: Trade,
    ) -> None:
        """Checks if the endpoint is basically available."""
        with pytest.raises(
            KrakenPermissionDeniedError,
            match=r".*API key doesn't have permission to make this request.*",
        ):
            xstocks_trade_client.create_order(
                **self.SAVE_ORDER,
                side="buy",
                extra_params={"asset_class": "tokenized_asset"},
            )

    @pytest.mark.spot_auth
    def test_create_order_spot_client(
        self: Self,
        xstocks_client: SpotClient,
    ) -> None:
        """Checks if the endpoint is basically available."""
        with pytest.raises(
            KrakenPermissionDeniedError,
            match=r".*API key doesn't have permission to make this request.*",
        ):
            xstocks_client.request(
                "POST",
                "/0/private/AddOrder",
                params={"type": "buy", "asset_class": "tokenized_asset"}
                | self.SAVE_ORDER,
            )
