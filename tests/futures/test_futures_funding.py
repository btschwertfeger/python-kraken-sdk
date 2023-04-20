#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#
import pytest

from .helper import is_not_error, is_success


def test_get_historical_funding_rates(futures_demo_funding) -> None:
    assert is_success(
        futures_demo_funding.get_historical_funding_rates(symbol="PF_SOLUSD")
    )


@pytest.mark.skip(reason="Skipping Futures initiate_wallet_transfer endpoint")
def test_initiate_wallet_transfer(futures_demo_funding) -> None:
    # accounts must exist..
    # print(futures_demo_funding.initiate_wallet_transfer(
    #     amount=200, fromAccount='Futures Wallet', toAccount='Spot Wallet', unit='XBT'
    # ))
    pass


@pytest.mark.skip(reason="Skipping Futures initiate_subaccount_transfer endpoint")
def test_initiate_subccount_transfer(futures_demo_funding) -> None:
    # print(futures_demo_funding.initiate_subccount_transfer(
    #     amount=200,
    #     fromAccount='The wallet (cash or margin account) from which funds should be debited',
    #     fromUser='The user account (this or a sub account) from which funds should be debited',
    #     toAccount='The wallet (cash or margin account) to which funds should be credited',
    #     toUser='The user account (this or a sub account) to which funds should be credited',
    #     unit='XBT',
    # ))
    pass


@pytest.mark.skip(reason="Skipping Futures withdrawal_to_spot_wallet endpoint")
def test_initiate_withdrawal_to_spot_wallet(futures_demo_funding) -> None:
    # print(futures_demo_funding.initiate_withdrawal_to_spot_wallet(
    #     amount=200,
    #     currency='XBT',
    # ))
    pass
