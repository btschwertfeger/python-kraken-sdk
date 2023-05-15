#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that checks the general Futures Base API class."""

import pytest

from kraken.base_api import KrakenBaseFuturesAPI
from kraken.exceptions import KrakenException
from kraken.futures import Funding, Market, Trade, User

from .helper import is_success


@pytest.mark.futures
def test_KrakenBaseFuturesAPI_without_exception() -> None:
    """
    Checks first if the expected error will be raised and than
    creates a new KrakenBaseFuturesAPI instance that do not raise
    the custom Kraken exceptions. This new instance thant executes
    the same request and the returned response gets evaluated.
    """
    with pytest.raises(KrakenException.KrakenRequiredArgumentMissingError):
        KrakenBaseFuturesAPI(
            key="fake",
            secret="fake",
        )._request(method="POST", uri="/derivatives/api/v3/sendorder", auth=True)

    result: dict = (
        KrakenBaseFuturesAPI(key="fake", secret="fake", use_custom_exceptions=False)  # type: ignore[union-attr]
        ._request(method="POST", uri="/derivatives/api/v3/sendorder", auth=True)
        .json()
    )

    assert (
        result.get("result") == "error"
        and result.get("error") == "requiredArgumentMissing"
    )


@pytest.mark.futures
@pytest.mark.futures_auth
def test_futures_rest_contextmanager(
    futures_market: Market,
    futures_auth_funding: Funding,
    futures_demo_trade: Trade,
    futures_auth_user: User,
) -> None:
    """
    Checks if the clients can be used as context manager.
    """
    with futures_market as market:
        assert isinstance(market.get_tick_types(), list)

    with futures_auth_funding as funding:
        assert is_success(funding.get_historical_funding_rates(symbol="PF_SOLUSD"))

    with futures_auth_user as user:
        assert is_success(user.get_wallets())

    with futures_demo_trade as trade:
        assert is_success(trade.get_fills())
