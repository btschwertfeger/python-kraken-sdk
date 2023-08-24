#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Spot Staking client"""

from __future__ import annotations

from typing import List, Optional, TypeVar, Union

from kraken.base_api import KrakenBaseSpotAPI, defined

Self = TypeVar("Self")


class Staking(KrakenBaseSpotAPI):
    """
    Class that implements the Kraken Spot Staking client. Currently there
    are no staking endpoints that could be accesses without authentication.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Kraken API (default: https://api.kraken.com)
    :type url: str, optional
    :param sandbox: Use the sandbox (not supported for Spot trading so far, default: ``False``)
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Spot Staking: Create the staking client

        >>> from kraken.spot import Staking
        >>> staking = Staking() # unauthenticated
        >>> auth_staking = Staking(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Spot Staking: Create the staking client as context manager

        >>> from kraken.spot import Staking
        >>> with Staking(key="api-key", secret="secret-key") as staking:
        ...     print(staking.stake_asset(asset="XLM", amount=200, method="Lumen Staked"))
    """

    def __init__(
        self,
        key: str = "",
        secret: str = "",
        url: str = "",
    ) -> None:
        super().__init__(key=key, secret=secret, url=url)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def stake_asset(
        self: Staking,
        asset: str,
        amount: Union[str, float],
        method: str,
    ) -> dict:
        """
        Stake the specified asset from the Spot wallet.

        Requires the ``Withdraw funds`` permission in the API key settings.

        Have a look at :func:`kraken.spot.Staking.list_stakeable_assets` to get
        information about the stakeable assets and methods.

        - https://docs.kraken.com/rest/#operation/stake

        :param asset: The asset to stake
        :type asset: str
        :param amount: The amount to stake
        :type amount: str | float
        :param method: The staking method
        :type method: str
        :return: The reference id of the staking transaction
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Staking: Stake an asset

            >>> from kraken.spot import Staking
            >>> staking = Staking(key="api-key", secret="secret-key")
            >>> staking.stake_asset(
            ...     asset="DOT",
            ...     amount=2000,
            ...     method="polkadot-staked"
            ... )
            { 'refid': 'BOG5AE5-KSCNR4-VPNPEV' }
        """
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/Stake",
            params={"asset": asset, "amount": amount, "method": method},
            auth=True,
        )

    def unstake_asset(
        self: Staking,
        asset: str,
        amount: Union[str, float],
        method: Optional[str] = None,
    ) -> dict:
        """
        Unstake an asset and transfer the amount to the Spot wallet.

        Requires the ``Withdraw funds`` permission in the API key settings.

        Have a look at :func:`kraken.spot.Staking.list_stakeable_assets` to get
        information about the stakeable assets and methods.

        - https://docs.kraken.com/rest/#operation/unstake

        :param asset: The asset to stake
        :type asset: str
        :param amount: The amount to stake
        :type amount: str | float
        :param method: Filter by staking method (default: ``None``)
        :type method: str, optional
        :return: The reference id of the unstaking transaction
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Staking: Unstake a staked asset

            >>> from kraken.spot import Staking
            >>> staking = Staking(key="api-key", secret="secret-key")
            >>> staking.unstake_asset(
            ...     asset="DOT",
            ...     amount=2000,
            ...     method="polkadot-staked"
            ... )
            { 'refid': 'BOG5AE5-KSCNR4-VPNPEV' }
        """
        params: dict = {"asset": asset, "amount": amount}
        if defined(method):
            params["method"] = method

        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/Unstake",
            params=params,
            auth=True,
        )

    def list_stakeable_assets(self: Staking) -> List[dict]:
        """
        Get a list of stakeable assets. Only assets that the user is able to stake
        will be shown.

        Requires the ``Withdraw funds`` and ``Query funds`` API key permissions.

        https://docs.kraken.com/rest/#operation/getStakingAssetInfo

        :return: Information for all assets that can be staked on Kraken
        :rtype: List[dict]

        .. code-block:: python
            :linenos:
            :caption: Spot Staking: List the stakeable assets

            >>> from kraken.spot import Staking
            >>> staking = Staking(key="api-key", secret="secret-key")
            >>> staking.list_stakeable_assets()
            [
                {
                    "method": "polkadot-staked",
                    "asset": "DOT",
                    "staking_asset": "DOT.S",
                    "rewards": {
                        "type": "percentage",
                        "reward": "7-11"
                    },
                    "on_chain": True,
                    "can_stake": True,
                    "can_unstake": True,
                    "minimum_amount": {
                        "staking": "0.0000000100",
                        "unstaking": "0.0000000100"
                    }
                }, {
                    "method": "polygon-staked",
                    "asset": "MATIC",
                    "staking_asset": "MATIC.S",
                    "rewards": {
                        "type": "percentage",
                        "reward": "1-2"
                    },
                    "on_chain": True,
                    "can_stake": True,
                    "can_unstake": True,
                    "minimum_amount": {
                        "staking": "0.0000000000",
                        "unstaking": "0.0000000000"
                    }
                }, ...
            ]
        """
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/Staking/Assets",
            auth=True,
        )

    def get_pending_staking_transactions(self: Staking) -> List[dict]:
        """
        Get the list of pending staking transactions of the user.

        Requires the ``Withdraw funds`` and ``Query funds`` API key permissions.

        - https://docs.kraken.com/rest/#operation/getStakingPendingDeposits

        :return: List of pending staking transactions
        :rtype: List[dict]

        .. code-block:: python
            :linenos:
            :caption: Spot Staking: Get the pending staking transactions

            >>> from kraken.spot import Staking
            >>> staking = Staking(key="api-key", secret="secret-key")
            >>> staking.get_pending_staking_transactions()
            [
                {
                    'method': 'polkadot-staked',
                    'aclass': 'currency',
                    'asset': 'DOT.S',
                    'refid': 'BOG5AE5-KSCNR4-VPNPEV',
                    'amount': '1982.17316',
                    'fee': '0.00000000',
                    'time': 1623653613,
                    'status': 'Initial',
                    'type': 'bonding'
                }, ...
            ]
        """
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/Staking/Pending",
            auth=True,
        )

    def list_staking_transactions(self: Staking) -> List[dict]:
        """
        List the last 1000 staking transactions of the past 90 days.

        Requires the ``Query funds`` API key permission.

        - https://docs.kraken.com/rest/#operation/getStakingTransactions

        :return: List of historical staking transactions
        :rtype: List[dict]

        .. code-block:: python
            :linenos:
            :caption: Spot Staking: List the historical staking transactions

            >>> from kraken.spot import Staking
            >>> staking = Staking(key="api-key", secret="secret-key")
            >>> staking.list_staking_transactions()
            [
                {
                    'method': 'polkadot-staked',
                    'aclass': 'currency',
                    'asset': 'DOT.S',
                    'refid': 'POLZN7T-RWBL2YD-3HAPL1',
                    'amount': '121.1',
                    'fee': '1.0000000000',
                    'time': 1622971496,
                    'status': 'Success'.
                    'type': 'bonding',
                    'bond_start': 1623234684,
                    'bond_end': 1632345316
                }, ...
            ]

        """
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/Staking/Transactions",
            auth=True,
        )


__all__ = ["Staking"]
