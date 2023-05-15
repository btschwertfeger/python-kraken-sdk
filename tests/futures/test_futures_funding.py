#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures funding client."""

import pytest

from kraken.futures import Funding

from .helper import is_success

# todo: Mocking? Or is this to dangerous?


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_funding
def test_get_historical_funding_rates(futures_demo_funding: Funding) -> None:
    """
    Checks the ``get_historical_funding_rates`` function.
    """
    assert is_success(
        futures_demo_funding.get_historical_funding_rates(symbol="PF_SOLUSD")
    )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_funding
@pytest.mark.skip(reason="CI does not have withdraw permission")
def test_initiate_wallet_transfer(futures_demo_funding: Funding) -> None:
    """
    Checks the ``initiate_wallet_transfer`` function - skipped since
    a transfer in testing is not desired.
    """
    # accounts must exist..
    # print(futures_demo_funding.initiate_wallet_transfer(
    #     amount=200, fromAccount='Futures Wallet', toAccount='Spot Wallet', unit='XBT'
    # ))
    pass


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_funding
@pytest.mark.skip(reason="CI does not have withdraw permission")
def test_initiate_subccount_transfer(futures_demo_funding: Funding) -> None:
    """
    Checks the ``initiate_subaccount_transfer`` function.
    """
    # print(futures_demo_funding.initiate_subccount_transfer(
    #     amount=200,
    #     fromAccount='The wallet (cash or margin account) from which funds should be debited',
    #     fromUser='The user account (this or a sub account) from which funds should be debited',
    #     toAccount='The wallet (cash or margin account) to which funds should be credited',
    #     toUser='The user account (this or a sub account) to which funds should be credited',
    #     unit='XBT',
    # ))
    pass


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_funding
@pytest.mark.skip(reason="CI does not have withdraw permission")
def test_initiate_withdrawal_to_spot_wallet(futures_demo_funding: Funding) -> None:
    """
    Checks the ``initiate_withdrawal_to_spot_wallet`` function.
    """
    # print(futures_demo_funding.initiate_withdrawal_to_spot_wallet(
    #     amount=200,
    #     currency='XBT',
    # ))
    pass
