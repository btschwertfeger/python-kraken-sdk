# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot Earn client."""

from typing import Any, Self

import pytest

from kraken.spot import Earn

from .helper import is_not_error


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_earn
@pytest.mark.skip(reason="Tests do not have earn permission")
class TestSpotEarn:
    """Test class for Spot Earn client functionality."""

    TEST_AMOUNT = "1"
    TEST_STRATEGY_ID = "ESRFUO3-Q62XD-WIOIL7"
    TEST_ASSET = "DOT"

    def _assert_successful_operation(self: Self, result: Any) -> None:  # noqa: ANN401
        """Helper method to assert successful operations for allocation/deallocation."""
        assert isinstance(result, bool)

    def _assert_successful_query(self: Self, result: Any) -> None:  # noqa: ANN401
        """Helper method to assert successful query operations."""
        assert is_not_error(result)

    def test_allocate_earn_funds(self: Self, spot_auth_earn: Earn) -> None:
        """
        Checks if the response of the ``allocate_earn_funds`` is of
        type bool which mean that the request was successful.
        """
        result = spot_auth_earn.allocate_earn_funds(
            amount=self.TEST_AMOUNT,
            strategy_id=self.TEST_STRATEGY_ID,
        )
        self._assert_successful_operation(result)

    def test_deallocate_earn_funds(self: Self, spot_auth_earn: Earn) -> None:
        """
        Checks if the response of the ``deallocate_earn_funds`` is of
        type bool which mean that the request was successful.
        """
        result = spot_auth_earn.deallocate_earn_funds(
            amount=self.TEST_AMOUNT,
            strategy_id=self.TEST_STRATEGY_ID,
        )
        self._assert_successful_operation(result)

    def test_get_allocation_status(self: Self, spot_auth_earn: Earn) -> None:
        """
        Checks if the response of the ``get_allocation_status`` does not contain a
        named error which mean that the request was successful.
        """
        result = spot_auth_earn.get_allocation_status(
            strategy_id=self.TEST_STRATEGY_ID,
        )
        self._assert_successful_query(result)

    def test_get_deallocation_status(self: Self, spot_auth_earn: Earn) -> None:
        """
        Checks if the response of the ``get_deallocation_status`` does not contain a
        named error which mean that the request was successful.
        """
        result = spot_auth_earn.get_deallocation_status(
            strategy_id=self.TEST_STRATEGY_ID,
        )
        self._assert_successful_query(result)

    def test_list_earn_strategies(self: Self, spot_auth_earn: Earn) -> None:
        """
        Checks if the response of the ``list_earn_strategies`` does not contain a
        named error which mean that the request was successful.
        """
        result = spot_auth_earn.list_earn_strategies(asset=self.TEST_ASSET)
        self._assert_successful_query(result)

    def test_list_earn_allocations(self: Self, spot_auth_earn: Earn) -> None:
        """
        Checks if the response of the ``list_earn_allocations`` does not contain a
        named error which mean that the request was successful.
        """
        result = spot_auth_earn.list_earn_allocations(asset=self.TEST_ASSET)
        self._assert_successful_query(result)
