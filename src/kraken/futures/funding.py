# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Module that implements the Kraken Futures Funding client"""

from __future__ import annotations

from typing import Self

from kraken.base_api import FuturesClient


class Funding(FuturesClient):
    """
    Class that implements the Kraken Futures Funding client

    If the sandbox environment is chosen, the keys must be generated from here:
    https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str, optional
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Futures Kraken API (default:
        https://futures.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional
    :param sandbox: If set to ``True`` the URL will be
        https://demo-futures.kraken.com (default: ``False``)
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Futures Funding: Create the funding client

        >>> from kraken.futures import Funding
        >>> funding = Funding() # unauthenticated
        >>> funding = Funding(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Futures Funding: Create the funding client as context manager

        >>> from kraken.futures import Funding
        >>> with Funding(key="api-key", secret="secret-key") as funding:
        ...     print(funding.get_historical_funding_rates(symbol="PI_XBTUSD"))
    """

    def __init__(  # nosec: B107
        self,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
        *,
        sandbox: bool = False,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, proxy=proxy, sandbox=sandbox)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def get_historical_funding_rates(
        self: Funding,
        symbol: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about the historical funding rates of a specific
        ``symbol``

        - https://docs.kraken.com/api/docs/futures-api/trading/historical-funding-rates

        :param symbol: The futures symbol to filter for
        :type symbol: str
        :return: The funding rates for a specific asset/contract
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Funding: Get the historical funding rates

            >>> from kraken.futures import Funding
            >>> Funding().get_historical_funding_rates(symbol="PI_XBTUSD")
            {
                'rates': [
                    {
                        'timestamp': '2019-02-27T16:00:00.000Z',
                        'fundingRate': 1.31656208775e-07,
                        'relativeFundingRate': 0.0005
                    }, {
                        'timestamp': '2019-02-27T20:00:00.000Z',
                        'fundingRate': 1.30695377827e-07,
                        'relativeFundingRate': 0.0005
                    }, ...
                ]
            }
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v4/historicalfundingrates",
            query_params={"symbol": symbol},
            auth=False,
            extra_params=extra_params,
        )

    def initiate_wallet_transfer(
        self: Funding,
        amount: str | float,
        fromAccount: str,
        toAccount: str,
        unit: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Submit a wallet transfer request to transfer funds between margin
        accounts.

        Requires the ``General API - Full Access`` and ``Withdrawal API - Full
        access`` permissions in the API key settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/transfer

        :param amount: The volume to transfer
        :type amount: str | float
        :param fromAccount: The account to withdraw from
        :type fromAccount: str
        :param fromAccount: The account to deposit to
        :type fromAccount: str
        :param unit: The currency or asset to transfer
        :type unit: str

        .. code-block:: python
            :linenos:
            :caption: Futures Funding: Transfer funds between wallets

            >>> from kraken.futures import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.initiate_wallet_transfer(
            ...     amount='100',
            ...     fromAccount='some cash or margin account',
            ...     toAccount='another cash or margin account',
            ...     unit='ADA'
            ... ))
            {
                'result': 'success',
                'serverTime': '2023-04-07T15:23:45.196Z"
            }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/transfer",
            post_params={
                "amount": str(amount),
                "fromAccount": fromAccount,
                "toAccount": toAccount,
                "unit": unit,
            },
            auth=True,
            extra_params=extra_params,
        )

    def initiate_subaccount_transfer(
        self: Funding,
        amount: str | float,
        fromAccount: str,
        fromUser: str,
        toAccount: str,
        toUser: str,
        unit: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Submit a request to transfer funds between the regular and subaccount.

        Requires the ``General API - Full Access`` and ``Withdrawal API - Full
        access`` permissions in the API key settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/sub-account-transfer

        :param amount: The volume to transfer
        :type amount: str | float
        :param fromAccount: The account to withdraw from
        :type fromAccount: str
        :param fromUser: The user account to transfer from
        :type fromUser: str
        :param toAccount: The account to deposit to
        :type toAccount: str
        :param unit: The asset to transfer
        :type unit: str

        .. code-block:: python
            :linenos:
            :caption: Futures Funding: Transfer funds between subaccounts

            >>> from kraken.futures import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.initiate_subaccount_transfer(
            ...     amount='2',
            ...     fromAccount='MyCashWallet',
            ...     fromUser='Subaccount1',
            ...     toAccount='MyCashWallet',
            ...     toUser='Subaccount2',
            ...     unit='XBT'
            ... ))
        """

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/transfer/subaccount",
            post_params={
                "amount": str(amount),
                "fromAccount": fromAccount,
                "fromUser": fromUser,
                "toAccount": toAccount,
                "toUser": toUser,
                "unit": unit,
            },
            auth=True,
            extra_params=extra_params,
        )

    def initiate_withdrawal_to_spot_wallet(
        self: Funding,
        amount: str | float,
        currency: str,
        sourceWallet: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Enables the transfer of funds between the futures and spot wallet.

        Requires the ``General API - Full Access`` and ``Withdrawal API - Full
        access`` permissions in the API key settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/withdrawal

        :param amount: The volume to transfer
        :type amount: str | float
        :param currency: The asset or currency to transfer
        :type currency: str
        :param sourceWallet: The wallet to withdraw from (default: ``cash``)
        :type sourceWallet: str, optional
        :raises ValueError: If this function is called within the sandbox/demo
            environment

        .. code-block:: python
            :linenos:
            :caption: Futures Funding: Transfer funds between Spot and Futures wallets

            >>> from kraken.futures import Funding
            >>> funding = Funding(key="api-key", secret="secret-key")
            >>> funding.initiate_withdrawal_to_spot_wallet(
            ...     amount=100,
            ...     currency='USDT',
            ...     sourceWallet='cash'
            ... ))
        """
        if self.sandbox:
            raise ValueError("This function is not available in sandbox mode.")
        params: dict = {
            "amount": str(amount),
            "currency": currency,
        }
        if sourceWallet is not None:
            params["sourceWallet"] = sourceWallet

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/withdrawal",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )


__all__ = ["Funding"]
