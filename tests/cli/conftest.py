#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module implementing fixtures for testing"""

from __future__ import annotations

import os

import pytest
from click.testing import CliRunner


@pytest.fixture()
def cli_runner() -> CliRunner:
    """Provide a cli-runner for testing the CLI"""
    return CliRunner()


@pytest.fixture()
def _with_cli_env_vars() -> None:
    """Setup some environment variables for th CLI tests"""
    os.environ["KRAKEN_SPOT_API_KEY"] = os.getenv("SPOT_API_KEY", "")
    os.environ["KRAKEN_SPOT_SECRET_KEY"] = os.getenv("SPOT_SECRET_KEY", "")
    os.environ["KRAKEN_FUTURES_API_KEY"] = os.getenv("FUTURES_API_KEY", "")
    os.environ["KRAKEN_FUTURES_SECRET_KEY"] = os.getenv("FUTURES_SECRET_KEY", "")

    yield

    for var in (
        "KRAKEN_SPOT_API_KEY",
        "KRAKEN_SPOT_SECRET_KEY",
        "KRAKEN_FUTURES_API_KEY",
        "KRAKEN_FUTURES_SECRET_KEY",
    ):
        if os.getenv(var):
            del os.environ[var]
