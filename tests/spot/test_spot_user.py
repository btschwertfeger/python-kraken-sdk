#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot user client."""

import os
import random
import tempfile
from time import sleep, time

import pytest

from kraken.exceptions import KrakenException
from kraken.spot import User

from .helper import is_not_error


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_account_balance(spot_auth_user: User) -> None:
    """
    Checks the ``get_account_balance`` function by validating that
    the response do not contain the error key.
    """
    assert is_not_error(spot_auth_user.get_account_balance())


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_balances(spot_auth_user):
    """
    Checks the ``get_balances`` function by validating that
    the response do not contain the error key.
    """
    assert is_not_error(spot_auth_user.get_balances(currency="USD"))


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_trade_balance(spot_auth_user: User) -> None:
    """
    Checks the ``get_trade_balances`` function by validating that
    the response do not contain the error key.

    (sleep since we dont want API rate limit error...)
    """
    sleep(3)
    assert is_not_error(spot_auth_user.get_trade_balance())
    assert is_not_error(spot_auth_user.get_trade_balance(asset="EUR"))


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_open_orders(spot_auth_user: User) -> None:
    """
    Checks the ``get_open_orders`` function by validating that
    the response do not contain the error key.
    """
    assert is_not_error(spot_auth_user.get_open_orders(trades=True))
    assert is_not_error(spot_auth_user.get_open_orders(trades=False, userref="1234567"))


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_closed_orders(spot_auth_user: User) -> None:
    """
    Checks the ``get_closed_orders`` function by validating that
    the responses do not contain the error key.
    """
    assert is_not_error(spot_auth_user.get_closed_orders())
    assert is_not_error(spot_auth_user.get_closed_orders(trades=True, userref="1234"))
    assert is_not_error(
        spot_auth_user.get_closed_orders(trades=True, start="1668431675.4778206")
    )
    assert is_not_error(
        spot_auth_user.get_closed_orders(
            trades=True, start="1668431675.4778206", end="1668455555.4778206", ofs=2
        )
    )
    assert is_not_error(
        spot_auth_user.get_closed_orders(
            trades=True,
            start="1668431675.4778206",
            end="1668455555.4778206",
            ofs=1,
            closetime="open",
        )
    )


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_trades_info(spot_auth_user: User) -> None:
    """
    Checks the ``get_trades_info`` function by validating that
    the responses do not contain the error key.
    """
    for params, method in zip(
        (
            {"txid": "OXBBSK-EUGDR-TDNIEQ"},
            {"txid": "OXBBSK-EUGDR-TDNIEQ", "trades": True},
            {"txid": "OQQYNL-FXCFA-FBFVD7"},
            {"txid": ["OE3B4A-NSIEQ-5L6HW3", "O23GOI-WZDVD-XWGC3R"]},
        ),
        (
            spot_auth_user.get_trades_info,
            spot_auth_user.get_trades_info,
            spot_auth_user.get_trades_info,
            spot_auth_user.get_trades_info,
        ),
    ):
        try:
            assert is_not_error(method(**params))
        except KrakenException.KrakenInvalidOrderError:
            pass
        finally:
            sleep(2)


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_orders_info(spot_auth_user: User) -> None:
    """
    Checks the ``get_orders_info`` function by validating that
    the responses do not contain the error key.
    """
    for params, method in zip(
        (
            {"txid": "OXBBSK-EUGDR-TDNIEQ"},
            {"txid": "OXBBSK-EUGDR-TDNIEQ", "trades": True},
            {"txid": "OQQYNL-FXCFA-FBFVD7", "consolidate_taker": True},
            {"txid": ["OE3B4A-NSIEQ-5L6HW3", "O23GOI-WZDVD-XWGC3R"]},
        ),
        (
            spot_auth_user.get_orders_info,
            spot_auth_user.get_orders_info,
            spot_auth_user.get_orders_info,
            spot_auth_user.get_orders_info,
        ),
    ):
        try:
            assert is_not_error(method(**params))
        except KrakenException.KrakenInvalidOrderError:
            pass
        finally:
            sleep(2)


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_trades_history(spot_auth_user: User) -> None:
    """
    Checks the ``get_trades_history`` function by validating that
    the responses do not contain the error key.
    """
    sleep(3)
    assert is_not_error(spot_auth_user.get_trades_history(type_="all", trades=True))
    assert is_not_error(
        spot_auth_user.get_trades_history(
            type_="closed position",
            start="1677717104",
            end="1677817104",
            ofs="1",
        )
    )


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_open_positions(spot_auth_user: User) -> None:
    """
    Checks the ``get_open_positions`` function by validating that
    the responses do not contain the error key.
    """
    assert isinstance(spot_auth_user.get_open_positions(), list)
    assert isinstance(
        spot_auth_user.get_open_positions(txid="OQQYNL-FXCFA-FBFVD7"), list
    )
    assert isinstance(
        spot_auth_user.get_open_positions(txid="OQQYNL-FXCFA-FBFVD7", docalcs=True),
        list,
    )


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_ledgers_info(spot_auth_user: User) -> None:
    """
    Checks the ``get_ledgers_info`` function by validating that
    the responses do not contain the error key.
    """
    assert is_not_error(spot_auth_user.get_ledgers_info())
    assert is_not_error(spot_auth_user.get_ledgers_info(type_="deposit"))
    assert is_not_error(
        spot_auth_user.get_ledgers_info(
            asset="EUR", start="1668431675.4778206", end="1668455555.4778206", ofs=2
        )
    )
    assert is_not_error(
        spot_auth_user.get_ledgers_info(
            asset=["EUR", "USD"],
        )
    )
    assert is_not_error(
        spot_auth_user.get_ledgers_info(
            asset="EUR,USD",
        )
    )


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_ledgers(spot_auth_user: User) -> None:
    """
    Checks the ``get_ledgers`` function by validating that
    the responses do not contain the error key.
    """
    assert is_not_error(spot_auth_user.get_ledgers(id_="LNYQGU-SUR5U-UXTOWM"))
    assert is_not_error(
        spot_auth_user.get_ledgers(
            id_=["LNYQGU-SUR5U-UXTOWM", "LTCMN2-5DZHX-6CPRC4"], trades=True
        )
    )


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_get_trade_volume(spot_auth_user: User) -> None:
    """
    Checks the ``get_trade_volume`` function by validating that
    the responses do not contain the error key.
    """
    assert is_not_error(spot_auth_user.get_trade_volume())
    assert is_not_error(spot_auth_user.get_trade_volume(pair="DOT/EUR", fee_info=False))


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_request_save_export_report(spot_auth_user: User) -> None:
    """
    Checks the ``save_export_report`` function by requesting an
    report and saving them.
    """
    with pytest.raises(ValueError):
        # invalid report type
        spot_auth_user.request_export_report(
            report="invalid", description="this is an invalid report type"
        )

    for report in ("trades", "ledgers"):
        if report == "trades":
            fields = [
                "ordertxid",
                "time",
                "ordertype",
                "price",
                "cost",
                "fee",
                "vol",
                "margin",
                "misc",
                "ledgers",
            ]
        else:
            fields = [
                "refid",
                "time",
                "type",
                "aclass",
                "asset",
                "amount",
                "fee",
                "balance",
            ]

        export_descr = f"{report}-export-{random.randint(0, 10000)}"
        response = spot_auth_user.request_export_report(
            report=report,
            description=export_descr,
            fields=fields,
            format_="CSV",
            starttm="1662100592",
            endtm=int(1000 * time()),
        )
        assert is_not_error(response) and "id" in response
        sleep(2)

        status = spot_auth_user.get_export_report_status(report=report)
        assert isinstance(status, list)
        sleep(5)

        result = spot_auth_user.retrieve_export(id_=response["id"])
        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, f"{export_descr}.zip"), "wb") as file:
                for chunk in result.iter_content(chunk_size=512):
                    if chunk:
                        file.write(chunk)

        status = spot_auth_user.get_export_report_status(report=report)
        assert isinstance(status, list)
        for response in status:
            assert "id" in response
            try:
                assert isinstance(
                    spot_auth_user.delete_export_report(
                        id_=response["id"], type_="delete"
                    ),
                    dict,
                )
            except (
                Exception
            ):  # '200 - {"error":["WDatabase:No change"],"result":{"delete":true}}'
                pass
            sleep(2)


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_export_report_status_invalid(spot_auth_user: User) -> None:
    """
    Checks the ``export_report_status`` function by passing an invalid
    report type.
    """
    try:
        spot_auth_user.get_export_report_status(report="invalid")
    except ValueError:
        pass


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_user
def test_create_subaccount(spot_auth_user: User) -> None:
    """
    Checks the ``create_subaccount`` function by creating one.

    Creating subaccounts is only available for institutional clients (May 2023),
    so a KrakenException.KrakenPermissionDeniedError will be raised.
    """
    with pytest.raises(KrakenException.KrakenPermissionDeniedError):
        spot_auth_user.create_subaccount(email="abc@welt.de", username="tomtucker")
