# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module implementing unit tests for the command-line interface"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kraken.cli import cli

if TYPE_CHECKING:
    from click.testing import CliRunner
import pytest


@pytest.mark.spot
def test_cli_version(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli, ["--version"], catch_exceptions=False)
    assert result.exit_code == 0


@pytest.mark.spot
@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            ["spot", "https://api.kraken.com/0/public/Time"],
            id="spot_public_full_url",
        ),
        pytest.param(
            ["spot", "/0/public/Time"],
            id="spot_public_path_only",
        ),
        pytest.param(
            ["spot", "-X", "GET", "/0/public/Time"],
            id="spot_public_X_path_only",
        ),
        pytest.param(
            ["spot", "https://api.kraken.com/0/public/Assets"],
            id="spot_public_assets",
        ),
        pytest.param(
            ["spot", "https://api.kraken.com/0/public/Assets?asset=XBT,ETH"],
            id="spot_public_assets_with_query",
        ),
        pytest.param(
            ["spot", "https://api.kraken.com/0/public/Ticker"],
            id="spot_public_ticker",
        ),
        pytest.param(
            ["spot", "https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=1440"],
            id="spot_public_ohlc_with_multiple_params",
        ),
        pytest.param(
            ["spot", "https://api.kraken.com:443/0/public/Time"],
            id="spot_public_with_port",
        ),
    ],
)
def test_cli_spot_public(cli_runner: CliRunner, args: list[str]) -> None:
    result = cli_runner.invoke(cli, args)
    assert result.exit_code == 0


@pytest.mark.usefixtures("_with_cli_env_vars")
@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            ["spot", "-X", "POST", "https://api.kraken.com/0/private/BalanceEx"],
            id="spot_private_balance_full_url",
        ),
        pytest.param(
            ["spot", "-X", "POST", "/0/private/BalanceEx"],
            id="spot_private_balance_path_only",
        ),
        pytest.param(
            [
                "spot",
                "-X",
                "POST",
                "https://api.kraken.com/0/private/TradeBalance",
                "-d",
                '{"asset": "DOT"}',
            ],
            id="spot_private_trade_balance_with_data_full_url",
        ),
        pytest.param(
            ["spot", "-X", "POST", "/0/private/TradeBalance", "-d", '{"asset": "DOT"}'],
            id="spot_private_trade_balance_with_data_path_only",
        ),
    ],
)
def test_cli_spot_private(cli_runner: CliRunner, args: list[str]) -> None:
    result = cli_runner.invoke(cli, args)
    assert result.exit_code == 0


@pytest.mark.futures
@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            ["futures", "https://futures.kraken.com/api/charts/v1/spot/PI_XBTUSD/1d"],
            id="futures_public_charts_full_url",
        ),
        pytest.param(
            ["futures", "/api/charts/v1/spot/PI_XBTUSD/1d"],
            id="futures_public_charts_path_only",
        ),
    ],
)
def test_cli_futures_public(cli_runner: CliRunner, args: list[str]) -> None:
    result = cli_runner.invoke(cli, args)
    assert result.exit_code == 0


@pytest.mark.usefixtures("_with_cli_env_vars")
@pytest.mark.futures
@pytest.mark.futures_auth
@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            ["futures", "https://futures.kraken.com/derivatives/api/v3/openpositions"],
            id="futures_public_openpositions_full_url",
        ),
        pytest.param(
            ["futures", "/derivatives/api/v3/openpositions"],
            id="futures_public_openpositions_path_only",
        ),
    ],
)
def test_cli_futures_private(cli_runner: CliRunner, args: list[str]) -> None:
    result = cli_runner.invoke(cli, args)
    assert result.exit_code == 0


@pytest.mark.spot
@pytest.mark.parametrize(
    ("url", "expected"),
    [
        pytest.param(
            "https://api.kraken.com/0/public/Time",
            "https://api.kraken.com",
            id="standard_spot_url",
        ),
        pytest.param(
            "https://api.vip.uat.lobster.kraken.com/0/private/BalanceEx",
            "https://api.vip.uat.lobster.kraken.com",
            id="custom_kraken_instance",
        ),
        pytest.param(
            "http://localhost:8080/api/v1/endpoint",
            "http://localhost:8080",
            id="http_localhost",
        ),
        pytest.param(
            "https://futures.kraken.com/derivatives/api/v3/openpositions",
            "https://futures.kraken.com",
            id="futures_url",
        ),
        pytest.param(
            "https://demo-futures.kraken.com/api/v3/accounts",
            "https://demo-futures.kraken.com",
            id="demo_sandbox_url",
        ),
        pytest.param(
            "/0/public/Time",
            "",
            id="path_only_no_scheme",
        ),
        pytest.param(
            "api/v1/endpoint",
            "",
            id="relative_path",
        ),
        pytest.param(
            "",
            "",
            id="empty_string",
        ),
        pytest.param(
            "https://api.kraken.com:443/0/public/Time",
            "https://api.kraken.com:443",
            id="url_with_port",
        ),
        pytest.param(
            "https://api.kraken.com/0/public/Assets?asset=XBT,ETH",
            "https://api.kraken.com",
            id="url_with_query_params",
        ),
    ],
)
def test_get_base_url(url: str, expected: str) -> None:
    """Test the get_base_url function extracts base URLs correctly"""
    from kraken.cli import _get_base_url  # noqa: PLC2701,PLC0415

    assert _get_base_url(url) == expected


@pytest.mark.spot
@pytest.mark.parametrize(
    ("url", "expected"),
    [
        pytest.param(
            "https://api.kraken.com/0/public/Time",
            "/0/public/Time",
            id="standard_spot_url",
        ),
        pytest.param(
            "https://api.vip.uat.lobster.kraken.com/0/private/BalanceEx",
            "/0/private/BalanceEx",
            id="custom_kraken_instance",
        ),
        pytest.param(
            "http://localhost:8080/0/private/Balance",
            "/0/private/Balance",
            id="http_localhost",
        ),
        pytest.param(
            "https://futures.kraken.com/derivatives/api/v3/openpositions",
            "/derivatives/api/v3/openpositions",
            id="futures_url",
        ),
        pytest.param(
            "https://demo-futures.kraken.com/api/v3/accounts",
            "/api/v3/accounts",
            id="demo_sandbox_url",
        ),
        pytest.param(
            "/0/public/Time",
            "/0/public/Time",
            id="path_only_no_scheme",
        ),
        pytest.param(
            "api/v1/endpoint",
            "api/v1/endpoint",
            id="relative_path",
        ),
        pytest.param(
            "",
            "",
            id="empty_string",
        ),
        pytest.param(
            "https://api.kraken.com:443/0/public/Time",
            "/0/public/Time",
            id="url_with_port",
        ),
        pytest.param(
            "https://api.kraken.com/0/public/Assets?asset=XBT,ETH",
            "/0/public/Assets?asset=XBT,ETH",
            id="url_with_query_params",
        ),
        pytest.param(
            "https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=1440",
            "/0/public/OHLC?pair=XBTUSD&interval=1440",
            id="url_with_multiple_query_params",
        ),
        pytest.param(
            "https://futures.kraken.com/api/charts/v1/spot/PI_XBTUSD/1d",
            "/api/charts/v1/spot/PI_XBTUSD/1d",
            id="futures_charts_url",
        ),
        pytest.param(
            "/derivatives/api/v3/openpositions",
            "/derivatives/api/v3/openpositions",
            id="derivatives_path_only",
        ),
    ],
)
def test_get_uri_path(url: str, expected: str) -> None:
    """Test the _get_uri_path function extracts URI paths correctly"""
    from kraken.cli import _get_uri_path  # noqa: PLC2701,PLC0415

    assert _get_uri_path(url) == expected
