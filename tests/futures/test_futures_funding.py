# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures funding client."""

from typing import Self

import pytest

from kraken.futures import Funding

from .helper import is_success


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_funding
class TestFuturesFunding:
    def test_get_historical_funding_rates(
        self: Self,
        futures_demo_funding: Funding,
    ) -> None:
        """
        Checks the ``get_historical_funding_rates`` function.
        """
        assert is_success(
            futures_demo_funding.get_historical_funding_rates(symbol="PF_XBTUSD"),
        )

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_initiate_wallet_transfer(
        self: Self,
        futures_demo_funding: Funding,
    ) -> None:
        """
        Checks the ``initiate_wallet_transfer`` function - skipped since
        a transfer in testing is not desired.
        """
        # accounts must exist..
        # print(futures_demo_funding.initiate_wallet_transfer(
        #     amount=200, fromAccount='Futures Wallet', toAccount='Spot Wallet', unit='XBT'
        # ))

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_initiate_subccount_transfer(
        self: Self,
        futures_demo_funding: Funding,
    ) -> None:
        """
        Checks the ``initiate_subaccount_transfer`` function.
        """
        # print(futures_demo_funding.initiate_subaccount_transfer(
        #     amount=200,
        #     fromAccount='The wallet (cash or margin account) from which funds should be debited',
        #     fromUser='The user account (this or a sub account) from which funds should be debited',
        #     toAccount='The wallet (cash or margin account) to which funds should be credited',
        #     toUser='The user account (this or a sub account) to which funds should be credited',
        #     unit='XBT',
        # ))

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_initiate_withdrawal_to_spot_wallet(
        self: Self,
        futures_demo_funding: Funding,
    ) -> None:
        """
        Checks the ``initiate_withdrawal_to_spot_wallet`` function.
        """
        # print(futures_demo_funding.initiate_withdrawal_to_spot_wallet(
        #     amount=200,
        #     currency='XBT',
        # ))
