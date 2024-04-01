#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the Spot Funding client"""

from __future__ import annotations

from typing import TypeVar

from kraken.base_api import KrakenSpotBaseAPI, defined

Self = TypeVar("Self")


class Funding(KrakenSpotBaseAPI):
    """
    Class that implements the Spot Funding client. Currently there are no
    funding endpoints that could be accesses without authentication.

    - https://docs.kraken.com/rest/#tag/Funding

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Kraken API (default:
        https://api.kraken.com)
    :type url: str, optional

    .. code-block:: python
        :linenos:
        :caption: Spot Funding: Create the funding client

        >>> from kraken.spot import Funding
        >>> funding = Funding() # unauthenticated
        >>> auth_funding = Funding(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Spot Funding: Create the funding client as context manager

        >>> from kraken.spot import Funding
        >>> with Funding(key="api-key", secret="secret-key") as funding:
        ...     print(funding.get_deposit_methods(asset="XLM"))
    """

    def __init__(
        self: Funding,
        key: str = "",
        secret: str = "",
        url: str = "",
    ) -> None:
        super().__init__(key=key, secret=secret, url=url)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def get_deposit_methods(
        self: Funding,
        asset: str,
        *,
        extra_params: dict | None = None,
    ) -> list[dict]:
        """
        Get the available deposit methods for a specific asset.

        - https://docs.kraken.com/rest/#operation/getDepositMethods

        :param asset: Asset being deposited
        :type asset: str
        :return: List of available deposit methods of the asset
        :rtype: list[dict]

        .. code-block:: python
            :linenos:
            :caption: Spot Funding: Get the available deposit methods

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_deposit_methods(asset="XLM")
            [
                {
                    'method': 'Stellar XLM',
                    'limit': False,
                    'gen-address': True
                }, {
                    'method': 'Stellar XLM Multi',
                    'limit': False,
                    'gen-address': True
                }
            ]
        """
        return self._request(
            method="POST",
            uri="/0/private/DepositMethods",
            params={"asset": asset},  # type: ignore[return-value]
            extra_params=extra_params,
        )

    def get_deposit_address(
        self: Funding,
        asset: str,
        method: str,
        *,
        new: bool | None = False,
        extra_params: dict | None = None,
    ) -> list[dict]:
        """
        Get the deposit addresses for a specific asset. New deposit addresses
        can be generated.

        Requires the ``Deposit funds`` API key permission.

        - https://docs.kraken.com/rest/#operation/getDepositAddresses

        :param asset: Asset being deposited
        :type asset: str
        :param method: Deposit method name
        :type method: str
        :param new: Generate a new deposit address (default: ``False``)
        :type new: bool, optional
        :return: The user and asset specific deposit addresses
        :rtype: list[dict]

        .. code-block:: python
            :linenos:
            :caption: Spot Funding: Get the available deposit addresses

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
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/DepositAddresses",
            params={"asset": asset, "method": method, "new": new},
            extra_params=extra_params,
        )

    def get_recent_deposits_status(
        self: Funding,
        asset: str | None = None,
        method: str | None = None,
        start: str | None = None,
        end: str | None = None,
        cursor: bool | str = False,  # noqa: FBT001, FBT002
        *,
        extra_params: dict | None = None,
    ) -> list[dict] | dict:
        """
        Get information about the recent deposit status. The look back period is
        90 days and only the last 25 deposits will be returned.

        Requires the ``Query funds`` and ``Deposit funds`` API key permissions.

        - https://docs.kraken.com/rest/#operation/getStatusRecentDeposits

        :param asset: Filter by asset
        :type asset: str, optional
        :param method: Filter by deposit method
        :type method: str, optional
        :param start: Start timestamp
        :type start: str, optional
        :param end: End timestamp
        :type end: str, optional
        :param cursor: If bool: dis-/enable paginated responses; if str: cursor
            for next page
        :type cursor: bool | str, default: ``False``
        :return: The user specific deposit history
        :rtype: list[dict] | dict

        .. code-block:: python
            :linenos:
            :caption: Spot Funding: Get the recent deposit status

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_recent_deposits_status()
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
        params: dict = {"cursor": cursor}
        if defined(asset):
            params["asset"] = asset
        if defined(method):
            params["method"] = method
        if defined(start):
            params["start"] = start
        if defined(end):
            params["end"] = end

        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/DepositStatus",
            params=params,
            extra_params=extra_params,
        )

    def get_withdrawal_info(
        self: Funding,
        asset: str,
        key: str,
        amount: str | float,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about a possible withdraw, including fee and limit
        information. The ``key`` must be the name of the key defined in the
        account. You can add a new key for any asset listed on Kraken here:
        https://www.kraken.com/u/funding/withdraw.

        Requires the ``Query funds`` and ``Withdraw funds`` API key permissions.

        - https://docs.kraken.com/rest/#operation/getWithdrawalInformation

        :param asset: Asset to withdraw
        :type asset: str
        :param key: Withdrawal key name as set up in the user account
        :type key: str
        :param amount: The amount to withdraw
        :type amount: str | float
        :return: Information about a possible withdraw including the fee and
            amount.
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Funding: Get withdrawal information

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
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/WithdrawInfo",
            params={"asset": asset, "key": str(key), "amount": str(amount)},
            extra_params=extra_params,
        )

    def withdraw_funds(
        self: Funding,
        asset: str,
        key: str,
        amount: str | float,
        max_fee: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Create a new withdraw. The key must be the name of the withdraw key
        defined in the withdraw section of the Kraken WebUI.

        Requires the ``Withdraw funds`` API key permissions.

        - https://docs.kraken.com/rest/#tag/User-Funding/operation/withdrawFunds

        :param asset: Asset to withdraw
        :type asset: str
        :param key: Withdrawal key name as set up in the account
        :type key: str
        :param amount: The amount to withdraw
        :type amount: str | float
        :param max_fee: Fail withdraw if the fee will be higher than the
            specified max_fee.
        :type max_fee: str
        :return: The reference id of the withdraw
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Funding: Withdraw Funds

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.withdraw_funds(
            ...    asset="DOT",
            ...    key="MyPolkadotWallet"
            ...    amount=4
            ... )
            { 'refid': 'I7KGS6-UFMTTQ-AGBSO6T'}
        """
        params: dict = {"asset": asset, "key": str(key), "amount": str(amount)}
        if defined(max_fee):
            params["max_fee"] = max_fee

        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Withdraw",
            params=params,
            extra_params=extra_params,
        )

    def get_recent_withdraw_status(
        self: Funding,
        asset: str | None = None,
        method: str | None = None,
        start: str | None = None,
        end: str | None = None,
        cursor: str | bool | None = None,  # noqa: FBT001
        *,
        extra_params: dict | None = None,
    ) -> list[dict]:
        """
        Get information about the recent withdraw status, including withdraws of
        the past 90 days but at max 500 results.

        - https://docs.kraken.com/rest/#operation/getStatusRecentWithdrawals

        :param asset: Filter withdraws by asset (default: ``None``)
        :type asset: str, optional
        :param method: Filter by withdraw method (default: ``None``)
        :type method: str, optional
        :param start: Filter by start timestamp
        :type start: str, optional
        :param end: Filter by end timestamp
        :type end: str, optional
        :param cursor: en-/disable paginated responses via ``True``/``False`` or
            define the page as str.
        :type cursor: str | bool, optional
        :return: Withdrawal information
        :rtype: list[dict]

        .. code-block:: python
            :linenos:
            :caption: Get the recent withdraw status

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.get_recent_withdraw_status()
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
        params: dict = {}
        if defined(asset):
            params["asset"] = asset
        if defined(method):
            params["method"] = method
        if defined(start):
            params["start"] = start
        if defined(end):
            params["end"] = end
        if defined(cursor):
            params["cursor"] = cursor
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/WithdrawStatus",
            params=params,
            extra_params=extra_params,
        )

    def cancel_withdraw(
        self: Funding,
        asset: str,
        refid: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Cancel a requested withdraw. This will only be successful if the
        withdraw is not being processed so far.

        Requires the ``Withdraw funds`` API key permissions.

        - https://docs.kraken.com/rest/#operation/cancelWithdrawal

        :param asset: Asset of the pending withdraw
        :type asset: str
        :param refid: The reference ID returned the withdraw was requested
        :type refid: str
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Funding: Cancel Withdraw

            >>> from kraken.spot import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.cancel_withdraw(asset="DOT", refid="I7KGS6-UFMTTQ-AGBSO6T")
            { 'result': True }
        """
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/WithdrawCancel",
            params={"asset": asset, "refid": str(refid)},
            extra_params=extra_params,
        )

    def wallet_transfer(
        self: Funding,
        asset: str,
        from_: str,
        to_: str,
        amount: str | float,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Transfer assets between the Spot and Futures wallet.

        Requires the ``Withdraw funds`` API key permissions.

        - https://docs.kraken.com/rest/#operation/walletTransfer

        :param asset: Asset to transfer
        :type asset: str
        :param from_: The wallet to withdraw from
        :type from_: str
        :param to_: The wallet to deposit to
        :type to_: str
        :param amount: The amount to transfer
        :type amount: str | float
        :return: The reference id
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Funding: Wallet Transfer

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
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/WalletTransfer",
            params={"asset": asset, "from": from_, "to": to_, "amount": str(amount)},
            extra_params=extra_params,
        )

    def withdraw_methods(
        self: Funding,
        asset: str | None = None,
        aclass: str | None = None,
        network: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Returns the list of available withdraw methods for that user.

        Requires the ``Funds permissions - Query`` and ``Funds permissions -
        Withdraw`` API key permissions.

        :param asset: Filter by asset
        :type asset: Optional[str]
        :param aclass: Filter by asset class (default: ``currency``)
        :type aclass: Optional[str]
        :param network: Filter by network
        :type network: Optional[str]
        :return: List of available withdraw methods
        :rtype: list[dict]
        """
        params: dict = {}
        if defined(asset):
            params["asset"] = asset
        if defined(aclass):
            params["network"] = aclass
        if defined(network):
            params["network"] = network
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/WithdrawMethods",
            params=params,
            extra_params=extra_params,
        )

    def withdraw_addresses(
        self: Funding,
        asset: str | None = None,
        aclass: str | None = None,
        method: str | None = None,
        key: str | None = None,
        verified: bool | None = None,  # noqa: FBT001
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Returns the list of available withdrawal addresses for that user.

        Requires the ``Funds permissions - Query`` and ``Funds permissions -
        Withdraw`` API key permissions.

        :param asset: Filter by asset
        :type asset: Optional[str]
        :param aclass: Filter by asset class (default: ``currency``)
        :type aclass: Optional[str]
        :param method: Filter by method
        :type method: Optional[str]
        :param key: Filter by key
        :type key: Optional[str]
        :param verified: List only addresses which are confirmed via E-Mail
        :type verified: Optional[str]
        :return: List of available addresses for withdrawal
        :rtype: list[dict]
        """
        params: dict = {}
        if defined(asset):
            params["asset"] = asset
        if defined(aclass):
            params["network"] = aclass
        if defined(method):
            params["method"] = method
        if defined(key):
            params["key"] = key
        if defined(verified):
            params["verified"] = verified
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/WithdrawMethods",
            params=params,
            extra_params=extra_params,
        )


__all__ = ["Funding"]
