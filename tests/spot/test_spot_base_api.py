#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that checks the general Spot Base API class as well as the Async Client."""

from __future__ import annotations

import random
import tempfile
from asyncio import run
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING
from unittest import IsolatedAsyncioTestCase

import pytest
from proxy import TestCase

from kraken.exceptions import KrakenInvalidAPIKeyError, KrakenPermissionDeniedError
from kraken.spot import SpotAsyncClient, SpotClient

if TYPE_CHECKING:
    from kraken.spot import Funding, Market, Trade, User
from .helper import is_not_error


@pytest.mark.spot
def test_KrakenSpotBaseAPI_without_exception() -> None:
    """
    Checks first if the expected error will be raised and than creates a new
    KrakenSpotBaseAPI instance that do not raise the custom Kraken exceptions.
    This new instance than executes the same request and the returned response
    gets evaluated.
    """
    with pytest.raises(KrakenInvalidAPIKeyError):
        SpotClient(
            key="fake",
            secret="fake",
        ).request(method="POST", uri="/0/private/AddOrder", auth=True)

    assert SpotClient(
        key="fake",
        secret="fake",
        use_custom_exceptions=False,
    ).request(method="POST", uri="/0/private/AddOrder", auth=True).json() == {
        "error": ["EAPI:Invalid key"],
    }


@pytest.mark.spot
@pytest.mark.spot_auth
def test_spot_rest_contextmanager(
    spot_market: Market,
    spot_auth_funding: Funding,
    spot_auth_trade: Trade,
    spot_auth_user: User,
) -> None:
    """
    Checks if the clients can be used as context manager.
    """
    with spot_market as market:
        result = market.get_assets()
        assert is_not_error(result), result

    with spot_auth_funding as funding:
        assert isinstance(funding.get_deposit_methods(asset="XBT"), list)

    with spot_auth_user as user:
        assert is_not_error(user.get_account_balance())

    with spot_auth_trade as trade, pytest.raises(KrakenPermissionDeniedError):
        trade.cancel_order(txid="OB6JJR-7NZ5P-N5SKCB")


# ==============================================================================
# Spot async client


@pytest.mark.spot
def test_spot_rest_async_client_get() -> None:
    """
    Check the instantiation as well as a simple request using the async client.
    """

    async def check() -> None:
        client = SpotAsyncClient()
        try:
            assert is_not_error(
                await client.request(
                    "GET",
                    "/0/public/OHLC",
                    params={"pair": "XBTUSD"},
                    auth=False,
                ),
            )
        finally:
            await client.async_close()

    run(check())


@pytest.mark.spot
def test_spot_async_rest_contextmanager(
    spot_api_key: str,
    spot_secret_key: str,
) -> None:
    """
    Checks if the clients can be used as context manager.
    """

    async def check() -> None:
        async with SpotAsyncClient(spot_api_key, spot_secret_key) as client:
            result = await client.request("GET", "/0/public/Time", auth=False)
            assert is_not_error(result), result

    run(check())


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.timeout(120)
def test_spot_rest_async_client_post_report(
    spot_api_key: str,
    spot_secret_key: str,
) -> None:
    """
    Check the authenticated async client using multiple request to retrieve a
    the user-specific order report.
    """

    async def check() -> None:
        client = SpotAsyncClient(spot_api_key, spot_secret_key)

        first_of_current_month = int(datetime.now().replace(day=1).timestamp())
        try:
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
                response = await client.request(
                    "POST",
                    "/0/private/AddExport",
                    params={
                        "format": "CSV",
                        "fields": fields,
                        "report": report,
                        "description": export_descr,
                        "endtm": first_of_current_month + 100 * 100,
                    },
                    timeout=30,
                )
                assert is_not_error(response)
                assert "id" in response
                sleep(2)

                status = await client.request(
                    "POST",
                    "/0/private/ExportStatus",
                    params={"report": report},
                )
                assert isinstance(status, list)
                sleep(5)

                result = await client.request(
                    "POST",
                    "/0/private/RetrieveExport",
                    params={"id": response["id"]},
                    timeout=30,
                    return_raw=True,
                )

                with tempfile.TemporaryDirectory() as tmp_dir:
                    file_path = Path(tmp_dir) / f"{export_descr}.zip"

                    with file_path.open("wb") as file:
                        async for chunk in result.content.iter_chunked(1024):
                            file.write(chunk)

                status = await client.request(
                    "POST",
                    "/0/private/ExportStatus",
                    params={"report": report},
                )
                assert isinstance(status, list)
                for response in status:
                    assert "id" in response
                    with suppress(Exception):
                        assert isinstance(
                            await client.request(
                                "POST",
                                "/0/private/RemoveExport",
                                params={
                                    "id": response["id"],
                                    "type": "delete",
                                },
                            ),
                            dict,
                        )
                    sleep(2)
        finally:
            await client.async_close()

    run(check())


class TestProxyPyEmbedded(TestCase, IsolatedAsyncioTestCase):
    def get_proxy_str(self) -> str:
        return f"http://127.0.0.1:{self.PROXY.flags.port}"

    @pytest.mark.spot
    @pytest.mark.spot_market
    def test_spot_rest_proxies(self) -> None:
        """
        Checks if the clients can be used with a proxy.
        """
        client = SpotClient(proxy=self.get_proxy_str())
        assert is_not_error(
            client.request(
                "GET",
                "/0/public/OHLC",
                params={"pair": "XBTUSD"},
                auth=False,
            ),
        )

    @pytest.mark.spot
    @pytest.mark.spot_market
    @pytest.mark.asyncio
    async def test_spot_rest_proxies_async(self) -> None:
        """
        Checks if the async clients can be used with a proxy.
        """
        client = SpotAsyncClient(proxy=self.get_proxy_str())
        res = await client.request(
            "GET",
            "/0/public/OHLC",
            params={"pair": "XBTUSD"},
            auth=False,
        )
        assert is_not_error(res)
