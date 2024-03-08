#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that checks the general Spot Base API class."""

import pytest

from kraken.base_api import KrakenSpotBaseAPI
from kraken.exceptions import KrakenInvalidAPIKeyError, KrakenPermissionDeniedError
from kraken.spot import Funding, Market, Trade, User

from .helper import is_not_error


@pytest.mark.spot()
def test_KrakenSpotBaseAPI_without_exception() -> None:
    """
    Checks first if the expected error will be raised and than creates a new
    KrakenSpotBaseAPI instance that do not raise the custom Kraken exceptions.
    This new instance than executes the same request and the returned response
    gets evaluated.
    """
    with pytest.raises(KrakenInvalidAPIKeyError):
        KrakenSpotBaseAPI(
            key="fake",
            secret="fake",
        )._request(method="POST", uri="/0/private/AddOrder", auth=True)

    assert KrakenSpotBaseAPI(
        key="fake",
        secret="fake",
        use_custom_exceptions=False,
    )._request(method="POST", uri="/0/private/AddOrder", auth=True).json() == {
        "error": ["EAPI:Invalid key"],
    }


@pytest.mark.spot()
@pytest.mark.spot_auth()
def test_spot_rest_contextmanager(
    spot_market: Market,
    spot_auth_funding: Funding,
    spot_auth_trade: Trade,
    spot_auth_user: User,
    # spot_auth_staking: Staking,
) -> None:
    """
    Checks if the clients can be used as context manager.
    """
    with spot_market as market:
        result = market.get_assets()
        assert is_not_error(result), result

    with spot_auth_funding as funding:
        assert isinstance(funding.get_deposit_methods(asset="XBT"), list)

    with spot_auth_user as user:
        assert is_not_error(user.get_account_balance())

    # FIXME: does not work; deprecated
    # with spot_auth_staking as staking:
    #     assert isinstance(staking.get_pending_staking_transactions(), list)

    with spot_auth_trade as trade, pytest.raises(KrakenPermissionDeniedError):
        trade.cancel_order(txid="OB6JJR-7NZ5P-N5SKCB")
