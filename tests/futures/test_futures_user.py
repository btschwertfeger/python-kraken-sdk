#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Futures user client."""

import random
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from kraken.futures import User

from .helper import is_success

if TYPE_CHECKING:
    import requests


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_wallets(futures_auth_user: User) -> None:
    """
    Checks the ``get_wallets`` endpoint.
    """
    assert is_success(futures_auth_user.get_wallets())


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_subaccounts(futures_auth_user: User) -> None:
    """
    Checks the ``get_subaccounts`` endpoint.
    """
    assert is_success(futures_auth_user.get_subaccounts())


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_unwindqueue(futures_auth_user: User) -> None:
    """
    Checks the ``get_unwindqueue`` endpoint.
    """
    assert is_success(futures_auth_user.get_unwind_queue())


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_notifications(futures_auth_user: User) -> None:
    """
    Checks the ``get_notifications`` endpoint.
    """
    assert is_success(futures_auth_user.get_notifications())


@pytest.mark.flaky()
@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_account_log(futures_auth_user: User) -> None:
    """
    Checks the ``get_account_log`` endpoint.
    """
    assert isinstance(futures_auth_user.get_account_log(), dict)
    assert isinstance(
        futures_auth_user.get_account_log(info="futures liquidation"),
        dict,
    )


# FIXME: They often encounter 500 status_codes - maybe an error in Kraken's API
@pytest.mark.flaky()
@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_account_log_csv(futures_auth_user: User) -> None:
    """
    Checks the ``get_account_log_csv`` endpoint.
    """
    response: requests.Response = futures_auth_user.get_account_log_csv()
    assert response.status_code in {200, "200"}

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path: Path = Path(tmp_dir) / f"account_log-{random.randint(0, 10000)}.csv"

        with file_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    file.write(chunk)


# FIXME: They often encounter 500 status_codes - maybe an error in Kraken's API
@pytest.mark.flaky()
@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_execution_events(futures_auth_user: User) -> None:
    """
    Checks the ``get_execution_events`` endpoint.
    """
    result: dict = futures_auth_user.get_execution_events(
        tradeable="PF_SOLUSD",
        since=1668989233,
        before=1668999999,
        sort="asc",
    )

    assert isinstance(result, dict)
    assert "elements" in result


# FIXME: They often encounter 500 status_codes - maybe an error in Kraken's API
@pytest.mark.flaky()
@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_order_events(futures_auth_user: User) -> None:
    """
    Checks the ``get_order_events`` endpoint.
    """
    result: dict = futures_auth_user.get_order_events(
        tradeable="PF_SOLUSD",
        since=1668989233,
        before=1668999999,
        sort="asc",
    )
    assert isinstance(result, dict)
    assert "elements" in result


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_open_orders(futures_auth_user: User) -> None:
    """
    Checks the ``get_open_orders`` endpoint.
    """
    assert is_success(futures_auth_user.get_open_orders())


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_open_positions(futures_auth_user: User) -> None:
    """
    Checks the ``get_open_positions`` endpoint.
    """
    assert is_success(futures_auth_user.get_open_positions())


# FIXME: They often encounter 500 status_codes - maybe an error in Kraken's API
@pytest.mark.flaky()
@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
def test_get_trigger_events(futures_auth_user: User) -> None:
    """
    Checks the ``get_trigger_events`` endpoint.
    """
    result = futures_auth_user.get_trigger_events(
        tradeable="PF_SOLUSD",
        since=1668989233,
        before=1668999999,
        sort="asc",
    )
    assert isinstance(result, dict)
    assert "elements" in result


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
@pytest.mark.skip("Subaccount actions are only available for insitutional clients")
def test_check_trading_enabled_on_subaccount(futures_auth_user: User) -> None:
    """
    Checks the ``check_trading_enabled_on_subaccount`` function.

    Until now, subaccounts are only available for institutional clients, so this
    execution raises an error. This test will work correctly (hopefully) when
    Kraken enables subaccounts for pro trader.
    """
    assert futures_auth_user.check_trading_enabled_on_subaccount(
        subaccountUid="778387bh61b-f990-4128-16a7-f819abc8",
    ) == {"tradingEnabled": False}


@pytest.mark.futures()
@pytest.mark.futures_auth()
@pytest.mark.futures_user()
@pytest.mark.skip("Subaccount actions are only available for insitutional clients")
def test_set_trading_on_subaccount(futures_auth_user: User) -> None:
    """
    Checks the ``set_trading_on_subaccount`` function.

    Until now, subaccounts are only available for institutional clients, so this
    execution raises an error. This test will work correctly (hopefully) when
    Kraken enables subaccounts for pro trader.
    """
    assert futures_auth_user.set_trading_on_subaccount(
        subaccountUid="778387bh61b-f990-4128-16a7-f819abc8",
        trading_enabled=True,
    ) == {"tradingEnabled": True}
