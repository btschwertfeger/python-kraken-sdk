# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures user client."""

import random
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

import pytest

from kraken.futures import User

from .helper import is_success

if TYPE_CHECKING:
    import requests


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
class TestFuturesUser:
    """Test class for Futures User client functionality."""

    TRADEABLE = "PF_SOLUSD"
    SINCE = 1668989233
    BEFORE = 1668999999
    SORT_ASC = "asc"
    SUBACCOUNT_UID = "778387bh61b-f990-4128-16a7-f819abc8"

    def _assert_successful_response(self: Self, result: Any) -> None:
        """Helper method to assert a successful response."""
        assert is_success(result)

    def _assert_elements_in_result(self: Self, result: dict) -> None:
        """Helper method to assert 'elements' key is in result."""
        assert isinstance(result, dict)
        assert "elements" in result

    def test_get_wallets(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_wallets`` endpoint.
        """
        self._assert_successful_response(futures_auth_user.get_wallets())

    def test_get_subaccounts(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_subaccounts`` endpoint.
        """
        self._assert_successful_response(futures_auth_user.get_subaccounts())

    def test_get_unwindqueue(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_unwindqueue`` endpoint.
        """
        self._assert_successful_response(futures_auth_user.get_unwind_queue())

    def test_get_notifications(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_notifications`` endpoint.
        """
        self._assert_successful_response(futures_auth_user.get_notifications())

    def test_get_account_log(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_account_log`` endpoint.
        """
        assert isinstance(futures_auth_user.get_account_log(), dict)
        assert isinstance(
            futures_auth_user.get_account_log(info="futures liquidation"),
            dict,
        )

    def test_get_account_log_csv(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_account_log_csv`` endpoint.
        """
        response: requests.Response = futures_auth_user.get_account_log_csv()
        assert response.status_code in {200, "200"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path: Path = (
                Path(tmp_dir) / f"account_log-{random.randint(0, 10000)}.csv"
            )

            with file_path.open("wb") as file:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        file.write(chunk)

    def test_get_execution_events(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_execution_events`` endpoint.
        """
        result: dict = futures_auth_user.get_execution_events(
            tradeable=self.TRADEABLE,
            since=self.SINCE,
            before=self.BEFORE,
            sort=self.SORT_ASC,
        )
        self._assert_elements_in_result(result)

    def test_get_order_events(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_order_events`` endpoint.
        """
        result: dict = futures_auth_user.get_order_events(
            tradeable=self.TRADEABLE,
            since=self.SINCE,
            before=self.BEFORE,
            sort=self.SORT_ASC,
        )
        self._assert_elements_in_result(result)

    def test_get_open_orders(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_open_orders`` endpoint.
        """
        self._assert_successful_response(futures_auth_user.get_open_orders())

    def test_get_open_positions(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_open_positions`` endpoint.
        """
        self._assert_successful_response(futures_auth_user.get_open_positions())

    def test_get_trigger_events(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``get_trigger_events`` endpoint.
        """
        result = futures_auth_user.get_trigger_events(
            tradeable=self.TRADEABLE,
            since=self.SINCE,
            before=self.BEFORE,
            sort=self.SORT_ASC,
        )
        self._assert_elements_in_result(result)

    @pytest.mark.skip("Subaccount actions are only available for institutional clients")
    def test_check_trading_enabled_on_subaccount(
        self: Self,
        futures_auth_user: User,
    ) -> None:
        """
        Checks the ``check_trading_enabled_on_subaccount`` function.

        Until now, subaccounts are only available for institutional clients, so this
        execution raises an error. This test will work correctly (hopefully) when
        Kraken enables subaccounts for pro trader.
        """
        assert futures_auth_user.check_trading_enabled_on_subaccount(
            subaccountUid=self.SUBACCOUNT_UID,
        ) == {"tradingEnabled": False}

    @pytest.mark.skip("Subaccount actions are only available for institutional clients")
    def test_set_trading_on_subaccount(self: Self, futures_auth_user: User) -> None:
        """
        Checks the ``set_trading_on_subaccount`` function.

        Until now, subaccounts are only available for institutional clients, so this
        execution raises an error. This test will work correctly (hopefully) when
        Kraken enables subaccounts for pro trader.
        """
        assert futures_auth_user.set_trading_on_subaccount(
            subaccountUid=self.SUBACCOUNT_UID,
            trading_enabled=True,
        ) == {"tradingEnabled": True}
