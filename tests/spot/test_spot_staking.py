#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot staking client."""

import pytest

from kraken.exceptions import KrakenException  # noqa: F401
from kraken.spot import Staking

from .helper import is_not_error  # noqa: F401

# todo: Mock skipped tests - or is this to dangerous?


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_staking()
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_list_stakeable_assets(spot_auth_staking: Staking) -> None:
    """
    Checks if the ``list_stakeable_assets`` endpoint returns the
    expected data type or raises the KrakenException.KrakenPermissionDeniedError.

    The error will be raised if some permissions of the API keys are not set.
    """
    assert isinstance(spot_auth_staking.list_stakeable_assets(), list)


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_staking()
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_stake_asset(spot_auth_staking: Staking) -> None:
    """
    Checks the ``stake_asset`` endpoint by requesting a stake.

    This test is skipped since staking is not the desired result.
    """
    # assert is_not_error(
    #     spot_auth_staking.stake_asset(
    #         asset="DOT",
    #         amount="4500000",
    #         method="polkadot-staked",
    #     ),
    # )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_staking()
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_unstake_asset(spot_auth_staking: Staking) -> None:
    """
    Checks if the ``unstake_asset`` endpoints returns a response that does
    not contain the error key.

    This test is skipped since unstaking is not wanted in the CI.
    """
    # with pytest.raises(KrakenException.KrakenPermissionDeniedError, "API key doesn't have permission to make this request."):
    # assert is_not_error(
    #     spot_auth_staking.unstake_asset(asset="DOT", amount="4500000"),
    # )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_staking()
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_get_pending_staking_transactions(spot_auth_staking: Staking) -> None:
    """
    Checks the ``get_pending_staking_transactions`` endpoint by validating
    that the response is of type list. This test is also skipped since
    the withdraw/stake permission is not set on the CI api keys.
    """
    assert isinstance(spot_auth_staking.get_pending_staking_transactions(), list)


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_staking()
@pytest.mark.skip(reason="CI does not have withdraw/stake permission")
def test_list_staking_transactions(spot_auth_staking: Staking) -> None:
    """
    Checks the ``list_staking_transactions`` endpoint by performing a regular
    request. This test is skipped since the CI API keys do not have the
    withdraw/stake permission.
    """
    assert isinstance(spot_auth_staking.list_staking_transactions(), list)
