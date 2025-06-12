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

"""Module that implements the Kraken Spot Earn client"""

from __future__ import annotations

from typing import TypeVar

from kraken.base_api import SpotClient, defined

Self = TypeVar("Self")


class Earn(SpotClient):
    """

    Class that implements the Kraken Spot Earn client. Currently there are no
    earn endpoints that could be accesses without authentication.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Kraken API (default:
        https://api.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional

    .. code-block:: python
        :linenos:
        :caption: Spot Earn: Create the Earn client

        >>> from kraken.spot import Earn
        >>> earn = Earn() # unauthenticated
        >>> auth_earn = Earn(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Spot Earn: Create the earn client as context manager

        >>> from kraken.spot import Earn
        >>> with Earn(key="api-key", secret="secret-key") as earn:
        ...     print(earn.stake_asset(asset="XLM", amount=200, method="Lumen Staked"))
    """

    def __init__(  # nosec: B107
        self,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, proxy=proxy)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def allocate_earn_funds(
        self: Earn,
        amount: str | float,
        strategy_id: str,
        *,
        extra_params: dict | None = None,
    ) -> bool:
        """
        Allocate funds according to the defined strategy.

        Requires the ``Earn Funds`` API key permission

        - https://docs.kraken.com/api/docs/rest-api/allocate-strategy

        :param amount: The amount to allocate
        :type amount: str | float
        :param strategy_id: Identifier of th chosen earn strategy (see
            :func:`kraken.spot.Earn.list_earn_strategies`)
        :type strategy_id: str

        .. code-block:: python
            :linenos:
            :caption: Spot Earn: Allocate funds

            >>> from kraken.earn import Earn
            >>> earn = Earn(key="api-key", secret="secret-key")
            >>> earn.allocate_earn_funds(
            ...     amount=2000,
            ...     strategy_id="ESRFUO3-Q62XD-WIOIL7"
            ... )
            True

        """

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/Allocate",
            params={"amount": amount, "strategy_id": strategy_id},
            auth=True,
            extra_params=extra_params,
        )

    def deallocate_earn_funds(
        self: Earn,
        amount: str | float,
        strategy_id: str,
        *,
        extra_params: dict | None = None,
    ) -> bool:
        """
        Deallocate funds according to the defined strategy.

        Requires the ``Earn Funds`` API key permission

        - https://docs.kraken.com/api/docs/rest-api/deallocate-strategy

        :param amount: The amount to deallocate
        :type amount: str | float
        :param strategy_id: Identifier of th chosen earn strategy (see
            :func:`kraken.spot.Earn.list_earn_strategies`)
        :type strategy_id: str

        .. code-block:: python
            :linenos:
            :caption: Spot Earn: Deallocate funds

            >>> from kraken.earn import Earn
            >>> earn = Earn(key="api-key", secret="secret-key")
            >>> earn.deallocate_earn_funds(
            ...     amount=2000,
            ...     strategy_id="ESRFUO3-Q62XD-WIOIL7"
            ... )
            True

        """

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/Deallocate",
            params={"amount": amount, "strategy_id": strategy_id},
            auth=True,
            extra_params=extra_params,
        )

    def get_allocation_status(
        self: Earn,
        strategy_id: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve the status of the last allocation request.

        Requires the ``Earn Funds`` or ``Query Funds`` API key permission.

        - https://docs.kraken.com/api/docs/rest-api/get-allocate-strategy-status

        :param strategy_id: Identifier of th chosen earn strategy (see
            :func:`kraken.spot.Earn.list_earn_strategies`)
        :type strategy_id: str

        .. code-block:: python
            :linenos:
            :caption: Spot Earn: Allocation Status

            >>> from kraken.earn import Earn
            >>> earn = Earn(key="api-key", secret="secret-key")
            >>> earn.get_allocation_status(
            ...     strategy_id="ESRFUO3-Q62XD-WIOIL7"
            ... )
            {'pending': False}
        """

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/AllocateStatus",
            params={"strategy_id": strategy_id},
            auth=True,
            extra_params=extra_params,
        )

    def get_deallocation_status(
        self: Earn,
        strategy_id: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve the status of the last deallocation request.

        Requires the ``Earn Funds`` or ``Query Funds`` API key permission.

        - https://docs.kraken.com/api/docs/rest-api/get-deallocate-strategy-status

        :param strategy_id: Identifier of th chosen earn strategy (see
            :func:`kraken.spot.Earn.list_earn_strategies`)
        :type strategy_id: str

        .. code-block:: python
            :linenos:
            :caption: Spot Earn: Deallocation Status

            >>> from kraken.earn import Earn
            >>> earn = Earn(key="api-key", secret="secret-key")
            >>> earn.get_deallocation_status(
            ...     strategy_id="ESRFUO3-Q62XD-WIOIL7"
            ... )
            {'pending': False}
        """

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/DeallocateStatus",
            params={"strategy_id": strategy_id},
            auth=True,
            extra_params=extra_params,
        )

    def list_earn_strategies(
        self: Earn,
        asset: str | None = None,
        limit: int | None = None,
        lock_type: list[str] | None = None,
        cursor: bool | None = None,  # noqa: FBT001
        ascending: bool | None = None,  # noqa: FBT001
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        List the available earn strategies as well as additional information.

        Requires an API key but no special permission set.

        - https://docs.kraken.com/api/docs/rest-api/list-strategies

        (March 9, 2024): The endpoint is not fully implemented on the side of
        Kraken. Some errors may happen.

        :param asset: Asset to filter for, defaults to None
        :type asset: Optional[str], optional
        :param limit: Items per page, defaults to None
        :type limit: Optional[int], optional
        :param lock_type: Filter strategies by lock type (``flex``, ``bounded``,
            ``timed``, ``instant``), defaults to None
        :type lock_type: Optional[list[str]], optional
        :param cursor: Page ID, defaults to None
        :type cursor: Optional[bool], optional
        :param ascending: Sort ascending, defaults to False
        :type ascending: bool, optional

        .. code-block:: python
            :linenos:
            :caption: Spot Earn: List Earn Strategies

            >>> from kraken.earn import Earn
            >>> earn = Earn(key="api-key", secret="secret-key")
            >>> earn.list_earn_strategies(asset="DOT")
            {
                "next_cursor": None,
                "items": [
                    {
                        "id": "ESMWVX6-JAPVY-23L3CV",
                        "asset": "DOT",
                        "lock_type": {
                            "type": "bonded",
                            "payout_frequency": 604800,
                            "bonding_period": 0,
                            "bonding_period_variable": False,
                            "bonding_rewards": False,
                            "unbonding_period": 2419200,
                            "unbonding_period_variable": False,
                            "unbonding_rewards": False,
                            "exit_queue_period": 0,
                        },
                        "apr_estimate": {"low": "15.0000", "high": "21.0000"},
                        "user_min_allocation": "0.01",
                        "allocation_fee": "0.0000",
                        "deallocation_fee": "0.0000",
                        "auto_compound": {"type": "enabled"},
                        "yield_source": {"type": "staking"},
                        "can_allocate": True,
                        "can_deallocate": True,
                        "allocation_restriction_info": [],
                    },
                    {
                        "id": "ESRFUO3-Q62XD-WIOIL7",
                        "asset": "DOT",
                        "lock_type": {"type": "instant", "payout_frequency": 604800},
                        "apr_estimate": {"low": "7.0000", "high": "11.0000"},
                        "user_min_allocation": "0.01",
                        "allocation_fee": "0.0000",
                        "deallocation_fee": "0.0000",
                        "auto_compound": {"type": "enabled"},
                        "yield_source": {"type": "staking"},
                        "can_allocate": True,
                        "can_deallocate": True,
                        "allocation_restriction_info": [],
                    },
                ],
            }
        """
        params: dict = {}
        if defined(ascending):
            params["ascending"] = ascending
        if defined(asset):
            params["asset"] = asset
        if defined(limit):
            params["limit"] = limit
        if defined(lock_type):
            params["lock_type"] = lock_type
        if defined(cursor):
            params["cursor"] = cursor

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/Strategies",
            params=params,
            auth=True,
            extra_params=extra_params,
        )

    def list_earn_allocations(
        self: Earn,
        ascending: str | None = None,
        hide_zero_allocations: str | None = None,
        converted_asset: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        List the user's allocations.

        Requires the ``Query Funds`` API key permission.

        - https://docs.kraken.com/api/docs/rest-api/list-allocations

        (March 9, 2024): The endpoint is not fully implemented on the side of
        Kraken. Some errors may happen.

        :param ascending: Sort ascending, defaults to False
        :type ascending: bool, optional
        :param hide_zero_allocations: Hide past allocations without balance,
            defaults to False
        :type hide_zero_allocations: bool, optional
        :param coverted_asset: Currency to express the value of the allocated
            asset, defaults to None
        :type coverted_asset: str, optional

        .. code-block:: python
            :linenos:
            :caption: Spot Earn: List Earn Allocations

            >>> from kraken.earn import Earn
            >>> earn = Earn(key="api-key", secret="secret-key")
            >>> earn.list_earn_allocations(asset="DOT")
            {
            "converted_asset": "USD",
                "total_allocated": "49.2398",
                "total_rewarded": "0.0675",
                "next_cursor": "2",
                "items": [{
                    "strategy_id": "ESDQCOL-WTZEU-NU55QF",
                    "native_asset": "ETH",
                    "amount_allocated": {},
                    "total_rewarded": {}
                }]
            }
        """
        params: dict = {}
        if defined(ascending):
            params["ascending"] = ascending
        if defined(hide_zero_allocations):
            params["hide_zero_allocations"] = hide_zero_allocations
        if defined(converted_asset):
            params["converted_asset"] = converted_asset

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/Allocations",
            params=params,
            auth=True,
            extra_params=extra_params,
        )
