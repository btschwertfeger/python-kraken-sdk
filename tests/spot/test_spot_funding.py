#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#
import pytest

from kraken.exceptions import KrakenException

from .helper import is_not_error


def test_get_deposit_methods(spot_auth_funding) -> None:
    assert isinstance(spot_auth_funding.get_deposit_methods(asset="XBT"), list)


def test_get_deposit_address(spot_auth_funding) -> None:
    assert isinstance(
        spot_auth_funding.get_deposit_address(asset="XBT", method="Bitcoin", new=False),
        list,
    )


def test_get_recent_deposits_status(spot_auth_funding) -> None:
    assert isinstance(spot_auth_funding.get_recent_deposits_status(), list)
    assert isinstance(spot_auth_funding.get_recent_deposits_status(asset="XLM"), list)
    assert isinstance(
        spot_auth_funding.get_recent_deposits_status(method="Stellar XLM"), list
    )
    assert isinstance(
        spot_auth_funding.get_recent_deposits_status(asset="XLM", method="Stellar XLM"),
        list,
    )


@pytest.mark.skip(reason="Skipping Spot test_withdraw_funds endpoint")
def test_withdraw_funds(spot_auth_funding) -> None:
    # CI API Keys are not allowd to withdraw, trade and cancel
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert is_not_error(
            spot_auth_funding.withdraw_funds(
                asset="XLM", key="enter-withdraw-key", amount=10000000
            )
        )


@pytest.mark.skip(reason="Skipping Spot test_get_withdrawal_info endpoint")
def test_get_withdrawal_info(spot_auth_funding) -> None:
    # CI API Keys are not allowd to withdraw, trade and cancel
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        assert is_not_error(
            spot_auth_funding.get_withdrawal_info(
                asset="XLM", amount=10000000, key="enter-withdraw-key"
            )
        )


@pytest.mark.skip(reason="Skipping Spot test_get_recent_withdraw_status endpoint")
def test_get_recent_withdraw_status(spot_auth_funding) -> None:
    assert isinstance(spot_auth_funding.get_recent_withdraw_status(), list)
    assert isinstance(spot_auth_funding.get_recent_withdraw_status(asset="XLM"), list)
    assert isinstance(
        spot_auth_funding.get_recent_withdraw_status(method="Stellar XLM"), list
    )


@pytest.mark.skip(reason="Skipping Spot test_wallet_transfer endpoint")
def test_wallet_transfer(spot_auth_funding) -> None:
    # CI API Keys are not allowd to withdraw, trade and cancel
    # this endpoint is broken, even the provided example on the kraken doc does not work
    with pytest.raises(KrakenException.KrakenInvalidArgumentsError):
        # only works if futures wallet exists
        assert is_not_error(
            spot_auth_funding.wallet_transfer(
                asset="XLM", from_="Futures Wallet", to_="Spot Wallet", amount=10000
            )
        )
