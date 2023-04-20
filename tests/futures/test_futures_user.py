#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

import random

from .helper import is_success


def test_get_wallets(futures_auth_user) -> None:
    assert is_success(futures_auth_user.get_wallets())


def test_get_subaccounts(futures_auth_user) -> None:
    assert is_success(futures_auth_user.get_subaccounts())


def test_get_unwindqueue(futures_auth_user) -> None:
    assert is_success(futures_auth_user.get_unwindqueue())


def test_get_notifications(futures_auth_user) -> None:
    assert is_success(futures_auth_user.get_notifications())


def test_get_account_log(futures_auth_user) -> None:
    assert isinstance(futures_auth_user.get_account_log(), dict)
    assert isinstance(
        futures_auth_user.get_account_log(info="futures liquidation"), dict
    )


def test_get_account_log_csv(futures_auth_user) -> None:
    response = futures_auth_user.get_account_log_csv()
    assert response.status_code in (200, "200")
    with open(f"account_log-{random.randint(0, 10000)}.csv", "wb") as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)


def test_get_execution_events(futures_auth_user) -> None:
    result = futures_auth_user.get_execution_events(
        tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc"
    )

    assert isinstance(result, dict)
    assert "elements" in result.keys()


def test_get_order_events(futures_auth_user) -> None:
    result = futures_auth_user.get_order_events(
        tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc"
    )
    assert isinstance(result, dict)
    assert "elements" in result.keys()


def test_get_open_orders(futures_auth_user) -> None:
    assert is_success(futures_auth_user.get_open_orders())


def test_get_open_positions(futures_auth_user) -> None:
    assert is_success(futures_auth_user.get_open_positions())


def test_get_trigger_events(futures_auth_user) -> None:
    result = futures_auth_user.get_trigger_events(
        tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc"
    )
    assert isinstance(result, dict)
    assert "elements" in result.keys()
