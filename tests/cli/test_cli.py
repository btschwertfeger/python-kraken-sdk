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
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0, result.exception


@pytest.mark.spot
def test_cli_spot_public(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli, ["spot", "https://api.kraken.com/0/public/Time"])
    assert result.exit_code == 0, result.exception

    result = cli_runner.invoke(cli, ["spot", "/0/public/Time"])
    assert result.exit_code == 0, result.exception


@pytest.mark.usefixtures("_with_cli_env_vars")
@pytest.mark.spot
@pytest.mark.spot_auth
def test_cli_spot_private(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        cli,
        ["spot", "-X", "POST", "https://api.kraken.com/0/private/Balance"],
    )
    assert result.exit_code == 0, result.exception

    result = cli_runner.invoke(
        cli,
        ["spot", "-X", "POST", "/0/private/Balance", "-d", '\'{"asset": "DOT"}\''],
    )
    assert result.exit_code == 0, result.exception


@pytest.mark.futures
def test_cli_futures_public(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(
        cli,
        ["futures", "https://futures.kraken.com/api/charts/v1/spot/PI_XBTUSD/1d"],
    )
    assert result.exit_code == 0, result.exception

    result = cli_runner.invoke(cli, ["futures", "/api/charts/v1/spot/PI_XBTUSD/1d"])
    assert result.exit_code == 0, result.exception


@pytest.mark.usefixtures("_with_cli_env_vars")
@pytest.mark.futures
@pytest.mark.futures_auth
def test_cli_futures_private(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        cli,
        ["futures", "https://futures.kraken.com/derivatives/api/v3/openpositions"],
    )
    assert result.exit_code == 0, result.exception


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
            "https://api.kraken.com/0/public/Ticker#section",
            "/0/public/Ticker#section",
            id="url_with_fragment",
        ),
        pytest.param(
            "https://api.kraken.com/0/public/Ticker?pair=XBTUSD#section",
            "/0/public/Ticker?pair=XBTUSD#section",
            id="url_with_query_and_fragment",
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
