#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that checks the general Futures Base API class."""

from asyncio import run
from unittest import IsolatedAsyncioTestCase

import pytest
from proxy import TestCase

from kraken.base_api import FuturesAsyncClient, FuturesClient
from kraken.exceptions import KrakenRequiredArgumentMissingError
from kraken.futures import Funding, Market, Trade, User

from .helper import is_success


@pytest.mark.futures
def test_KrakenFuturesBaseAPI_without_exception() -> None:
    """
    Checks first if the expected error will be raised and than
    creates a new KrakenFuturesBaseAPI instance that do not raise
    the custom Kraken exceptions. This new instance than executes
    the same request and the returned response gets evaluated.
    """
    with pytest.raises(KrakenRequiredArgumentMissingError):
        FuturesClient(
            key="fake",
            secret="fake",
        ).request(method="POST", uri="/derivatives/api/v3/sendorder", auth=True)

    result: dict = (
        FuturesClient(key="fake", secret="fake", use_custom_exceptions=False)  # type: ignore[union-attr]
        .request(method="POST", uri="/derivatives/api/v3/sendorder", auth=True)
        .json()
    )

    assert result.get("result") == "error"
    assert result.get("error") == "requiredArgumentMissing"


@pytest.mark.futures
@pytest.mark.futures_auth
def test_futures_rest_contextmanager(
    futures_market: Market,
    futures_auth_funding: Funding,
    futures_demo_trade: Trade,
    futures_auth_user: User,
) -> None:
    """
    Checks if the clients can be used as context manager.
    """
    with futures_market as market:
        assert isinstance(market.get_tick_types(), list)

    with futures_auth_funding as funding:
        assert is_success(funding.get_historical_funding_rates(symbol="PF_SOLUSD"))

    with futures_auth_user as user:
        assert is_success(user.get_wallets())

    with futures_demo_trade as trade:
        assert is_success(trade.get_fills())


# ==============================================================================
# Futures async client


@pytest.mark.futures
def test_futures_async_rest_contextmanager() -> None:
    """
    Checks if the clients can be used as context manager.
    """

    async def check() -> None:
        async with FuturesAsyncClient() as client:
            assert isinstance(
                await client.request(
                    "GET",
                    "/api/charts/v1/spot/PI_XBTUSD/1h",
                    auth=False,
                    post_params={"from": "1668989233", "to": "1668999233"},
                ),
                dict,
            )

    run(check())


@pytest.mark.futures
@pytest.mark.futures_auth
def test_futures_rest_async_client_post(
    futures_api_key: str,
    futures_secret_key: str,
) -> None:
    """
    Check the instantiation as well as a simple request using the async client.
    """

    async def check() -> None:
        client = FuturesAsyncClient(futures_api_key, futures_secret_key)
        try:
            assert isinstance(
                await client.request(
                    "POST",
                    "/derivatives/api/v3/orders/status",
                    post_params={
                        "orderIds": [
                            "bcaaefce-27a3-44b4-b13a-19df21e3f087",
                            "685d5a1a-23eb-450c-bf17-1e4ab5c6fe8a",
                        ],
                    },
                ),
                dict,
            )
        finally:
            await client.async_close()

    run(check())


class TestProxyPyEmbedded(TestCase, IsolatedAsyncioTestCase):
    def get_proxy_str(self) -> str:
        return f"http://127.0.0.1:{self.PROXY.flags.port}"

    @pytest.mark.futures
    @pytest.mark.futures_market
    def test_futures_rest_proxies(self) -> None:
        """
        Checks if the clients can be used with a proxy.
        """
        client = FuturesClient(proxy=self.get_proxy_str())
        assert isinstance(
            client.request(
                "GET",
                "/api/charts/v1/spot/PI_XBTUSD/1h",
                auth=False,
                post_params={"from": "1668989233", "to": "1668999233"},
            ),
            dict,
        )

    @pytest.mark.asyncio
    @pytest.mark.futures
    @pytest.mark.futures_market
    async def test_futures_rest_proxies_async(self) -> None:
        """
        Checks if the async clients can be used with a proxy.
        """
        client = FuturesAsyncClient(proxy=self.get_proxy_str())
        res = await client.request(
            "GET",
            "/api/charts/v1/spot/PI_XBTUSD/1h",
            auth=False,
            post_params={"from": "1668989233", "to": "1668999233"},
        )
        assert isinstance(res, dict)
