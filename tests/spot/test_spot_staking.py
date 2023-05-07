#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#
import pytest

from kraken.exceptions import KrakenException

from .helper import is_not_error

# todo: Mock skipped tests - or is this to dangerous?


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_staking
def test_list_stakeable_assets(spot_auth_staking) -> None:
    """
    Checks if the ``list_stakeable_assets`` endpoint returns the
    expected data type or raises the KrakenPermissionDeniedError.

    The error will be raised if some permissions of the API keys are not set.
    """
    try:
        assert isinstance(spot_auth_staking.list_stakeable_assets(), list)
    except KrakenException.KrakenPermissionDeniedError:
        pass


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_staking
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_stake_asset(spot_auth_staking) -> None:
    """
    Checks the ``stake_asset`` endpoint by requesting a stake.

    This test is skipped since staking is not the desired result.
    """
    try:
        assert is_not_error(
            spot_auth_staking.stake_asset(
                asset="DOT", amount="4500000", method="polkadot-staked"
            )
        )
    except KrakenException.KrakenInvalidAmountError:
        pass


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_staking
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_unstake_asset(spot_auth_staking) -> None:
    """
    Checks if the ``unstake_asset`` endpoints returns a response that does
    not contain the error key.

    This test is skipped since unstakign is not wanted in the CI.
    """
    try:
        assert is_not_error(
            spot_auth_staking.unstake_asset(asset="DOT", amount="4500000")
        )
    except KrakenException.KrakenInvalidAmountError:
        pass


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_staking
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_get_pending_staking_transactions(spot_auth_staking) -> None:
    """
    Checks the ``get_pending_staking_transactions`` endpoint by validating
    that the response is of type list. This test is also skipped since
    the withdraw/stake permission is not set on the CI api keys.
    """
    assert isinstance(spot_auth_staking.get_pending_staking_transactions(), list)


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_staking
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_list_staking_transactions(spot_auth_staking) -> None:
    """
    Checks the ``list_staking_transactions`` endpoint by performing a regular
    request. This test is skipped since the CI API keys do not have the
    withdraw/stake permission.
    """
    assert isinstance(spot_auth_staking.list_staking_transactions(), list)
