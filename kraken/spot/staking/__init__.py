#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Spot Stakung client"""
from typing import Union

from kraken.base_api import KrakenBaseSpotAPI


class StakingClient(KrakenBaseSpotAPI):
    """
    Class that implements the Kraken Spot Stakung client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: False)
    :type sandbox: bool
    """

    def stake_asset(
        self, asset: str, amount: Union[str, int, float], method: str
    ) -> dict:
        """
        Stake the specified asset from the Spot wallet.
        Requires the ``Withdraw funds`` permission in the API key settings.

        (see: https://docs.kraken.com/rest/#operation/stake)

        :param asset: The asset to stake
        :type asset: str
        :param amount: The amount to stake
        :type amount: str | int | float
        :param method: The staking method
        :type method: str
        """
        return self._request(
            method="POST",
            uri="/private/Stake",
            params={"asset": asset, "amount": amount, "method": method},
            auth=True,
        )

    def unstake_asset(
        self,
        asset: str,
        amount: Union[str, int, float],
        method: Union[str, None] = None,
    ) -> dict:
        """
        Unstake an asset and transfer the amount to the Spot wallet.
        Requires the ``Withdraw funds`` permission in the API key settings.

        (see: https://docs.kraken.com/rest/#operation/unstake)

        :param asset: The asset to stake
        :type asset: str
        :param amount: The amount to stake
        :type amount: str | int | float
        :param method: Optional - Filter by staking method (default: None)
        :type method: str | None
        """
        params = {"asset": asset, "amount": amount}
        if method is not None:
            params["method"] = method

        return self._request(
            method="POST", uri="/private/Unstake", params=params, auth=True
        )

    def list_stakeable_assets(self) -> dict:
        """
        Get a list of stakable assets. Only assets that the user is able to stake
        will be shown.

        Requires the ``Withdraw funds`` and ``Query funds`` API key permissions.

        (see: https://docs.kraken.com/rest/#operation/getStakingAssetInfo)
        """
        return self._request(method="POST", uri="/private/Staking/Assets", auth=True)

    def get_pending_staking_transactions(self) -> dict:
        """
        Get the list of pendin staking transactions of the user.

        Requires the ``Withdraw funds`` and ``Query funds`` API key permissions.

        (see: https://docs.kraken.com/rest/#operation/getStakingPendingDeposits)
        """
        return self._request(method="POST", uri="/private/Staking/Pending", auth=True)

    def list_staking_transactions(self) -> dict:
        """
        List the last 1000 staking transactions of the past 90 days.

        Requires the ``Query funds`` API key permission.

        (see: https://docs.kraken.com/rest/#operation/getStakingTransactions)
        """
        return self._request(
            method="POST", uri="/private/Staking/Transactions", auth=True
        )
