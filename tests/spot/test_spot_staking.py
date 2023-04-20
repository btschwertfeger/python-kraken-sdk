#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#
import pytest

from kraken.exceptions import KrakenException

from .helper import is_not_error


def test_list_stakeable_assets(spot_auth_staking) -> None:
    try:
        assert isinstance(spot_auth_staking.list_stakeable_assets(), list)
    except KrakenException.KrakenPermissionDeniedError:
        pass


@pytest.mark.skip(reason="Skipping Spot test_stake_asset endpoint")
def test_stake_asset(spot_auth_staking) -> None:
    try:
        assert is_not_error(
            spot_auth_staking.stake_asset(
                asset="DOT", amount="4500000", method="polkadot-staked"
            )
        )
    except KrakenException.KrakenInvalidAmountError:
        pass


@pytest.mark.skip(reason="Skipping Spot test_unstake_asset endpoint")
def test_unstake_asset(spot_auth_staking) -> None:
    try:
        assert is_not_error(
            spot_auth_staking.unstake_asset(asset="DOT", amount="4500000")
        )
    except KrakenException.KrakenInvalidAmountError:
        pass


@pytest.mark.skip(reason="Skipping Spot test_get_pending_staking_transactions endpoint")
def test_get_pending_staking_transactions(spot_auth_staking) -> None:
    assert isinstance(spot_auth_staking.get_pending_staking_transactions(), list)


@pytest.mark.skip(reason="Skipping Spot test_list_staking_transactions endpoint")
def test_list_staking_transactions(spot_auth_staking) -> None:
    assert isinstance(spot_auth_staking.list_staking_transactions(), list)
