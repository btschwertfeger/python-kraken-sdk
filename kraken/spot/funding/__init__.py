#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Spot Funding client"""
from typing import List, Union

from kraken.base_api import KrakenBaseSpotAPI


class Funding(KrakenBaseSpotAPI):
    """
    Class that implements the Spot Funding client.

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: ``False``)
    :type sandbox: bool

    .. code-block:: python
        :linenos:
        :caption: Example

        >>> from kraken.spot import Funding
        >>> funding = Funding() # unauthenticated
        >>> auth_funding = Funding(key="api-key", secret="secret-key") # authenticated
    """

    def get_deposit_methods(self, asset: str) -> dict:
        """
        Get the available deposit methods for a specific asset.

        - https://docs.kraken.com/rest/#operation/getDepositMethods

        :param asset: Asset being deposited
        :type asset: str
        :return: List of available deposit methods of the asset
        :rtype: List[dict[str, any]]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_deposit_methods(asset="XLM")
            [
                {
                    'method': 'Stellar XLM',
                    'limit': False,
                    'gen-address': True
                }, {
                    'method': 'Stellar XLM (muxed)',
                    'limit': False,
                    'gen-address': True
                }
            ]
        """
        return self._request(
            method="POST", uri="/private/DepositMethods", params={"asset": asset}
        )

    def get_deposit_address(
        self, asset: str, method: str, new: bool = False
    ) -> List[dict[str, any]]:
        """
        Get the deposit addresses for a specific asset. New deposit addresses can be generated.

        - https://docs.kraken.com/rest/#operation/getDepositAddresses

        :param asset: Asset being deposited
        :type asset: str
        :param method: Deposit method name
        :type method: str
        :param new: Optional - Generate a new deposit address (default: ``False``)
        :type new: bool
        :return: The user and asset specific deposit addresses
        :rtype: List[dict[str, any]]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_deposit_address(asset="XLM", method="Stellar XLM")
            [
                {
                    'address': 'GA5XIGA5C7QTPTWXQHY6MCJRMTRZDOSHR6EFIBNDQTCQHG262N4GGKTM',
                    'expiretm': '0',
                    'new': True,
                    'tag': '1668814718654064928'
                }, {
                    'address': 'GA5XIGA5C7QTPTWXQHY6MCJRMTRZDOSHR6EFIBNDQTCQHG262N4GGKTM',
                    'expiretm': '0',
                    'new': True,
                    'tag': '1668815609618044006'
                },  ...
            ]
        """
        return self._request(
            method="POST",
            uri="/private/DepositAddresses",
            params={"asset": asset, "method": method, "new": new},
        )

    def get_recend_deposits_status(
        self, asset: Union[str, None] = None, method: Union[str, None] = None
    ) -> List[dict[str, any]]:
        """
        Get information about the recend deposit status. The lookback period is 90 days and
        only the last 25 deposits will be returned.

        - https://docs.kraken.com/rest/#operation/getStatusRecentDeposits

        :param asset: Optional - Filter by asset
        :type asset: str
        :param method: Optional - Filter by deposit method
        :type method: str
        :return: The user specific deposit history
        :rtype: List[dict[str, any]]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_recend_deposits_status()
            [
                {
                    'method': 'Bank Frick (SEPA)',
                    'aclass': 'currency',
                    'asset': 'ZEUR',
                    'refid': 'QDFN2EK-XMFWQ4-GPB7SG',
                    'txid': '7702226',
                    'info': 'NTSBDEB1XXX',
                    'amount': '1000.0000',
                    'fee': '0.0000',
                    'time': 1680245166,
                    'status': 'Success'
                }, {
                    'method': 'Bank Frick (SEPA)',
                    'aclass': 'currency',
                    'asset': 'ZEUR',
                    'refid': 'QDFO35O-O4IU7K-ZEP77Y',
                    'txid': '7559797',
                    'info': 'NTSBDEB1XXX',
                    'amount': '500.0000',
                    'fee': '0.0000',
                    'time': 1677827980,
                    'status': 'Success'
                }, {
                    'method': 'Ethereum (ERC20)',
                    'aclass': 'currency',
                    'asset': 'XETH',
                    'refid': 'Q5QTWMS-GXER37-ZI4IH6',
                    'txid': '0x2abb04dafd3caed53d4f2912651391c53b912cc4bca1f8b30d09a5cebec5c2d6',
                    'info': '0x35be16f2340c97c02c0cf4dcd9279f2eaa4a0980',
                    'amount': '0.0119328120',
                    'fee': '0.0000000000',
                    'time': 1672901534,
                    'status': 'Success'
                }, ...
            ]
        """
        params = {}
        if asset is not None:
            params["asset"] = asset
        if method is not None:
            params["method"] = method
        return self._request(method="POST", uri="/private/DepositStatus", params=params)

    def get_withdrawal_info(
        self, asset: str, key: str, amount: Union[str, int, float]
    ) -> List[dict[str, any]]:
        """
        Get information about a possible withdraw, including fee and limit information.
        The ``key`` must be the name of the key defined in the account. You can add
        a new key for any asset listed on Kraken here: https://www.kraken.com/u/funding/withdraw.

        - https://docs.kraken.com/rest/#operation/getWithdrawalInformation

        :param asset: Asset to withdraw
        :type asset: str
        :param key: Withdrawal key name as set up in the user account
        :type key: str
        :param amount: The amont to withdraw
        :type amount: str | int | float

        :return: Information about a possible withdraw including the fee and amount.
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_withdrawal_info(
            ...     asset="DOT",
            ...     key="MyPolkadotWallet",
            ...     amount="4"
            ... )
            {
                'method': 'Polkadot',
                'limit': '4.49880000',
                'amount': '3.95000000',
                'fee': '0.05000000'
            }
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
        Create a new withdraw. The key must be the name of the withdraw key
        defined in the withdraw section of the Kraken WebUI
        (https://docs.kraken.com/rest/#tag/User-Funding/operation/withdrawFunds).

        - https://docs.kraken.com/rest/#tag/User-Funding/operation/withdrawFunds

        :param asset: Asset to withdraw
        :type asset: str
        :param key: Withdrawal key name as set up in the account
        :type key: str
        :param amount: The amont to withdraw
        :type amount: str | int | float
        :return: The reference id of the withdraw
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.withdraw_funds(
            ...    asset="DOT",
            ...    key="MyPolkadotWallet"
            ...    amount=4
            ... )
            {"refid": "I7KGS6-UFMTTQ-AGBSO6T"}
        """
        return self._request(
            method="POST",
            uri="/private/Withdraw",
            params={"asset": asset, "key": str(key), "amount": str(amount)},
        )

    def get_recend_withdraw_status(
        self, asset: Union[str, None] = None, method: Union[str, None] = None
    ) -> List[dict[str, any]]:
        """
        Get information about the recend withdraw status, including withdraws of the
        past 90 days but at max 500 results.

        - https://docs.kraken.com/rest/#operation/getStatusRecentWithdrawals

        :param asset: Optional - Filter withdraws by asset
        :type asset: str | None
        :param method: Optional - Filter by withdraw method
        :type method: str | None

        :return:
        :rtype: List[dict[str, any]]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_recend_withdraw_status()
            [
                {
                    'method': 'Polkadot',
                    'aclass': 'currency',
                    'asset': 'DOT',
                    'refid': 'XXXXXX-XXXXXX-HLDRM5',
                    'txid': '0x51d9d13ade1c31a138dae81b845f091d1a6cf2e3c1c36d9cf4f7baf905c483e4',
                    'info': '16LrqRXyhjBCSfA6kKrdqxPKrZoMEUtmoW4nkx5ZhA374Bp3',
                    'amount': '94.39581164',
                    'fee': '0.05000000',
                    'time': 1677816733,
                    'status': 'Success'
                }, ...
            ]
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

        - https://docs.kraken.com/rest/#operation/cancelWithdrawal

        :param asset: Asset of the pending withdraw
        :type asset: str
        :param refid: The reference ID returned the withdraw was requested
        :type refid: str
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.cancel_withdraw(asset="DOT", refid="I7KGS6-UFMTTQ-AGBSO6T")
            { 'result': True }
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

        - https://docs.kraken.com/rest/#operation/walletTransfer

        :param asset: Asset to transfer
        :type asset: str
        :param from_: The wallet to withdraw from
        :type from_: str
        :param to_: The wallet to deposit to
        :type to_: str
        :param amount: The amont to transfer
        :type amount: str | int | float
        :return:
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.wallet_transfer(
            ...     asset="XBT",
            ...     from_="Spot Wallet",
            ...     to_="Futures Wallet",
            ...     amount=0.01
            ... )
            { 'refid': "ANS1EE5-SKACR4-PENGVP" }
        """
        return self._request(
            method="POST",
            uri="/private/WalletTransfer",
            params={"asset": asset, "from": from_, "to": to_, "amount": str(amount)},
        )
