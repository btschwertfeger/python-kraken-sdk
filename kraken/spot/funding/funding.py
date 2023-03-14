#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Spot Funding client"""
from kraken.base_api.base_api import KrakenBaseSpotAPI


class FundingClient(KrakenBaseSpotAPI):
    """Class that implements the Spot Funding client"""

    def get_deposit_methods(self, asset: str) -> dict:
        """https://docs.kraken.com/rest/#operation/getDepositMethods"""
        return self._request(
            method="POST", uri="/private/DepositMethods", params={"asset": asset}
        )

    def get_deposit_address(self, asset: str, method: str, new: bool = False) -> dict:
        """https://docs.kraken.com/rest/#operation/getDepositAddresses"""
        return self._request(
            method="POST",
            uri="/private/DepositAddresses",
            params={"asset": asset, "method": method, "new": new},
        )

    def get_recend_deposits_status(self, asset: str, method: str = None) -> dict:
        """https://docs.kraken.com/rest/#operation/getStatusRecentDeposits"""
        params = {"asset": asset}
        if method is not None:
            params["method"] = method
        return self._request(method="POST", uri="/private/DepositStatus", params=params)

    def withdraw_funds(self, asset: str, key: str, amount: str) -> dict:
        """https://docs.kraken.com/rest/#operation/withdrawFund"""
        return self._request(
            method="POST",
            uri="/private/Withdraw",
            params={"asset": asset, "key": str(key), "amount": str(amount)},
        )

    def get_withdrawal_info(self, asset: str, key: str, amount: str) -> dict:
        """https://docs.kraken.com/rest/#operation/getWithdrawalInformation"""
        return self._request(
            method="POST",
            uri="/private/WithdrawInfo",
            params={"asset": asset, "key": str(key), "amount": str(amount)},
        )

    def get_recend_withdraw_status(self, asset: str, method: str = None) -> dict:
        """https://docs.kraken.com/rest/#operation/getStatusRecentWithdrawals"""
        params = {"asset": asset}
        if method is not None:
            params["method"] = method
        return self._request(
            method="POST", uri="/private/WithdrawStatus", params=params
        )

    def cancel_withdraw(self, asset: str, refid: str) -> dict:
        """https://docs.kraken.com/rest/#operation/cancelWithdrawal"""
        return self._request(
            method="POST",
            uri="/private/WithdrawCancel",
            params={"asset": asset, "refid": str(refid)},
        )

    def wallet_transfer(self, asset: str, from_: str, to_: str, amount: str) -> dict:
        """https://docs.kraken.com/rest/#operation/walletTransfer"""
        return self._request(
            method="POST",
            uri="/private/WalletTransfer",
            params={"asset": asset, "from": from_, "to": to_, "amount": amount},
        )
