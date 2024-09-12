#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
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
