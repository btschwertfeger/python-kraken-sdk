#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that checks the general Spot Base API class."""

import pytest

from kraken.base_api import KrakenBaseSpotAPI
from kraken.exceptions import KrakenException

from .helper import is_not_error


@pytest.mark.spot
def test_KrakenBaseSpotAPI_without_exception() -> None:
    """
    Checks first if the expected error will be raised and than
    creates a new KrakenBaseSpotAPI instance that do not raise
    the custom Kraken exceptions. This new instance thant executes
    the same request and the returned response gets evaluated.
    """
    with pytest.raises(KrakenException.KrakenInvalidAPIKeyError):
        KrakenBaseSpotAPI(
            key="fake",
            secret="fake",
        )._request(method="POST", uri="/private/AddOrder", auth=True)

    assert KrakenBaseSpotAPI(
        key="fake", secret="fake", use_custom_exceptions=False
    )._request(method="POST", uri="/private/AddOrder", auth=True).json() == {
        "error": ["EAPI:Invalid key"]
    }


@pytest.mark.spot
@pytest.mark.spot_auth
def test_spot_rest_contextmanager(
    spot_market, spot_auth_funding, spot_auth_trade, spot_auth_user, spot_auth_staking
) -> None:
    """
    Checks if the clients can be used as context manager.
    """
    with spot_market as market:
        assert is_not_error(market.get_assets())

    with spot_auth_funding as funding:
        isinstance(funding.get_deposit_methods(asset="XBT"), list)

    with spot_auth_user as user:
        assert is_not_error(user.get_account_balance())

    with spot_auth_staking as staking:
        assert isinstance(staking.get_pending_staking_transactions(), list)

    with spot_auth_trade as trade:
        with pytest.raises(KrakenException.KrakenPermissionDeniedError):
            trade.cancel_order(txid="OB6JJR-7NZ5P-N5SKCB")
