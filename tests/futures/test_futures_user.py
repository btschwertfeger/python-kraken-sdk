#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

import os
import random
import tempfile

import pytest

from .helper import is_success


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_wallets(futures_auth_user) -> None:
    """
    Checks the ``get_wallets`` endpoint.
    """
    assert is_success(futures_auth_user.get_wallets())


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_subaccounts(futures_auth_user) -> None:
    """
    Checks the ``get_subaccounts`` endpoint.
    """
    assert is_success(futures_auth_user.get_subaccounts())


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_unwindqueue(futures_auth_user) -> None:
    """
    Checks the ``get_unwindqueue`` endpoint.
    """
    assert is_success(futures_auth_user.get_unwindqueue())


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_notifications(futures_auth_user) -> None:
    """
    Checks the ``get_notifications`` endpoint.
    """
    assert is_success(futures_auth_user.get_notifications())


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_account_log(futures_auth_user) -> None:
    """
    Checks the ``get_account_log`` endpoint.
    """
    assert isinstance(futures_auth_user.get_account_log(), dict)
    assert isinstance(
        futures_auth_user.get_account_log(info="futures liquidation"), dict
    )


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_account_log_csv(futures_auth_user) -> None:
    """
    Checks the ``get_account_log_csv`` endpoint.
    """
    response = futures_auth_user.get_account_log_csv()
    assert response.status_code in (200, "200")

    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(
            os.path.join(tmp_dir, f"account_log-{random.randint(0, 10000)}.csv"), "wb"
        ) as file:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    file.write(chunk)


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_execution_events(futures_auth_user) -> None:
    """
    Checks the ``get_execution_events`` endpoint.
    """
    result = futures_auth_user.get_execution_events(
        tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc"
    )

    assert isinstance(result, dict)
    assert "elements" in result.keys()


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_order_events(futures_auth_user) -> None:
    """
    Checks the ``get_order_events`` endpoint.
    """
    result = futures_auth_user.get_order_events(
        tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc"
    )
    assert isinstance(result, dict)
    assert "elements" in result.keys()


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_open_orders(futures_auth_user) -> None:
    """
    Checks the ``get_open_orders`` endpoint.
    """
    assert is_success(futures_auth_user.get_open_orders())


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_open_positions(futures_auth_user) -> None:
    """
    Checks the ``get_open_positions`` endpoint.
    """
    assert is_success(futures_auth_user.get_open_positions())


@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.futures_user
def test_get_trigger_events(futures_auth_user) -> None:
    """
    Checks the ``get_trigger_events`` endpoint.
    """
    result = futures_auth_user.get_trigger_events(
        tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc"
    )
    assert isinstance(result, dict)
    assert "elements" in result.keys()
