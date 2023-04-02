#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Spot Funding client"""
from typing import Union

from kraken.base_api import KrakenBaseSpotAPI


class FundingClient(KrakenBaseSpotAPI):
    """
    Class that implements the Spot Funding client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: ``False``)
    :type sandbox: bool
    """

    def get_deposit_methods(self, asset: str) -> dict:
        """
        Get the available deposit methods for a specific asset.

        (see: https://docs.kraken.com/rest/#operation/getDepositMethods)

        :param asset: Asset being deposited
        :type asset: str
        """
        return self._request(
            method="POST", uri="/private/DepositMethods", params={"asset": asset}
        )

    def get_deposit_address(self, asset: str, method: str, new: bool = False) -> dict:
        """
        Get the deposit addresses for a specific asset. New deposit addresses can be generated.

        (see: https://docs.kraken.com/rest/#operation/getDepositAddresses)

        :param asset: Asset being deposited
        :type asset: str
        :param method: Deposit method name
        :type method: str
        :param new: Generate a new address
        :type new: bool
        """
        return self._request(
            method="POST",
            uri="/private/DepositAddresses",
            params={"asset": asset, "method": method, "new": new},
        )

    def get_recend_deposits_status(self, asset: str = None, method: str = None) -> dict:
        """
        Get information about the recend deposit status. The lookback period is 90 days and
        only the last 25 deposits will be returned.

        (see: https://docs.kraken.com/rest/#operation/getStatusRecentDeposits)

        :param asset: Asset being deposited
        :type asset: str
        :param method: Deposit method name
        :type method: str
        """
        params = {}
        if asset is not None:
            params["asset"] = asset
        if method is not None:
            params["method"] = method
        return self._request(method="POST", uri="/private/DepositStatus", params=params)

    def get_withdrawal_info(
        self, asset: str, key: str, amount: Union[str, int, float]
    ) -> dict:
        """
        Get information about a possible withdraw, including fee and limit information.

        (see: https://docs.kraken.com/rest/#operation/getWithdrawalInformation)

        :param asset: Asset to withdraw
        :type asset: str
        :param key: Withdrawal key name as set up in the account
        :type key: str
        :param amount: The amont to withdraw
        :type amount: str | int | float
        """
        return self._request(
            method="POST",
            uri="/private/WithdrawInfo",
            params={"asset": asset, "key": str(key), "amount": str(amount)},
        )

    def withdraw_funds(
        self, asset: str, key: str, amount: Union[str, int, float]
    ) -> dict:
        """
        Create a withdraw request.

        (see: https://docs.kraken.com/rest/#operation/withdrawFund)

        :param asset: Asset to withdraw
        :type asset: str
        :param key: Withdrawal key name as set up in the account
        :type key: str
        :param amount: The amont to withdraw
        :type amount: str | int | float
        """
        return self._request(
            method="POST",
            uri="/private/Withdraw",
            params={"asset": asset, "key": str(key), "amount": str(amount)},
        )

    def get_recend_withdraw_status(
        self, asset: Union[str, None] = None, method: Union[str, None] = None
    ) -> dict:
        """
        Get information about the recend withdraw status, including withdraws of the
        past 90 days but at max 500 results.

        (see: https://docs.kraken.com/rest/#operation/getStatusRecentWithdrawals)

        :param asset: Optional - Filter withdraws by asset
        :type asset: str | None
        :param method: Optional - Filter by withdraw method
        :type method: str | None
        """
        params = {}
        if asset is not None:
            params["asset"] = asset
        if method is not None:
            params["method"] = method
        return self._request(
            method="POST", uri="/private/WithdrawStatus", params=params
        )

    def cancel_withdraw(self, asset: str, refid: str) -> dict:
        """
        Cancel a requested withdraw. This will only be successful if the withdraw
        is not beeing processed so far.

        (see: https://docs.kraken.com/rest/#operation/cancelWithdrawal)

        :param asset: Asset of the pending withdraw
        :type asset: str
        :param refid: The reference ID returned the withdraw was requested
        :type refid: str
        """
        return self._request(
            method="POST",
            uri="/private/WithdrawCancel",
            params={"asset": asset, "refid": str(refid)},
        )

    def wallet_transfer(
        self, asset: str, from_: str, to_: str, amount: Union[str, int, float]
    ) -> dict:
        """
        Transfer assets between the Spot and Futures wallet.

        (see: https://docs.kraken.com/rest/#operation/walletTransfer)

        :param asset: Asset to transfer
        :type asset: str
        :param from_: The wallet to withdraw from
        :type from_: str
        :param to_: The wallet to deposit to
        :type to_: str
        :param amount: The amont to transfer
        :type amount: str | int | float
        """
        return self._request(
            method="POST",
            uri="/private/WalletTransfer",
            params={"asset": asset, "from": from_, "to": to_, "amount": str(amount)},
        )
