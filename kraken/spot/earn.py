#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger


"""Module that implements the Kraken Spot Earn client"""

from __future__ import annotations

from typing import Optional, TypeVar

from kraken.base_api import KrakenSpotBaseAPI, defined

Self = TypeVar("Self")


class Earn(KrakenSpotBaseAPI):
    """

    Class that implements the Kraken Spot Earn client. Currently there are no
    earn endpoints that could be accesses without authentication.

    - https://docs.kraken.com/rest/#tag/Earn

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Kraken API (default:
        https://api.kraken.com)
    :type url: str, optional

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

    def allocate_earn_funds(
        self: Earn,
        amount: str | float,
        strategy_id: str,
        *,
        extra_params: Optional[dict] = None,
    ) -> bool:
        """
        Allocate funds according to the defined strategy.

        Requires the ``Earn Funds`` API key permission

        - https://docs.kraken.com/rest/#tag/Earn/operation/allocateStrategy

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

        return self._request(  # type: ignore[return-value]
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
        extra_params: Optional[dict] = None,
    ) -> bool:
        """
        Deallocate funds according to the defined strategy.

        Requires the ``Earn Funds`` API key permission

        - https://docs.kraken.com/rest/#tag/Earn/operation/deallocateStrategy

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

        return self._request(  # type: ignore[return-value]
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
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Retrieve the status of the last allocation request.

        Requires the ``Earn Funds`` or ``Query Funds`` API key permission.

        - https://docs.kraken.com/rest/#tag/Earn/operation/getAllocateStrategyStatus

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

        return self._request(  # type: ignore[return-value]
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
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Retrieve the status of the last deallocation request.

        Requires the ``Earn Funds`` or ``Query Funds`` API key permission.

        - https://docs.kraken.com/rest/#tag/Earn/operation/getDeallocateStrategyStatus

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

        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/DeallocateStatus",
            params={"strategy_id": strategy_id},
            auth=True,
            extra_params=extra_params,
        )

    def list_earn_strategies(
        self: Earn,
        asset: Optional[str] = None,
        limit: Optional[int] = None,
        lock_type: Optional[list[str]] = None,
        cursor: Optional[bool] = None,
        ascending: bool = False,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        List the available earn strategies as well as additional information.

        Requires an API key but no special permission set.

        - https://docs.kraken.com/rest/#tag/Earn/operation/listStrategies

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

        """
        params: dict = {"ascending": ascending}
        if defined(asset):
            params["asset"] = asset
        if defined(limit):
            params["limit"] = limit
        if defined(lock_type):
            params["lock_type"] = lock_type
        if defined(cursor):
            params["cursor"] = cursor

        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/Strategies",
            params=params,
            auth=True,
            extra_params=extra_params,
        )

    def list_earn_allocations(
        self: Earn,
        ascending: bool = False,
        hide_zero_allocations: bool = False,
        converted_asset: Optional[str] = None,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        List the user's allocations.

        Requires the ``Query Funds`` API key permission.

        - https://docs.kraken.com/rest/#tag/Earn/operation/listAllocations

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

        """
        params = {
                "ascending": ascending,
                "hide_zero_allocations": hide_zero_allocations,
            }
        if defined(converted_asset):
            params["converted_asset"]= converted_asset
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Earn/Allocations",
            params=params,
            auth=True,
            extra_params=extra_params,
        )
