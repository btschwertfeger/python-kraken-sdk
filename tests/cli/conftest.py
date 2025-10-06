# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module implementing fixtures for testing"""

from __future__ import annotations

import os
from typing import Generator

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a cli-runner for testing the CLI"""
    return CliRunner()


@pytest.fixture
def with_spot_secrets() -> Generator:
    """Setup some environment variables for th CLI tests"""

    if not all(
        (
            spot_api_key := os.getenv("SPOT_API_KEY"),
            spot_secret_key := os.getenv("SPOT_SECRET_KEY"),
        ),
    ):
        pytest.fail("No API keys provided for CLI tests!")

    os.environ["KRAKEN_SPOT_API_KEY"] = spot_api_key
    os.environ["KRAKEN_SPOT_SECRET_KEY"] = spot_secret_key

    yield

    for var in ("KRAKEN_SPOT_API_KEY", "KRAKEN_SPOT_SECRET_KEY"):
        if os.getenv(var):
            del os.environ[var]


@pytest.fixture
def with_futures_secrets() -> Generator:
    """Setup some environment variables for the CLI tests"""

    if not all(
        (
            futures_api_key := os.getenv("FUTURES_API_KEY"),
            futures_secret_key := os.getenv("FUTURES_SECRET_KEY"),
        ),
    ):
        pytest.fail("No API keys provided for CLI tests!")

    os.environ["KRAKEN_FUTURES_API_KEY"] = futures_api_key
    os.environ["KRAKEN_FUTURES_SECRET_KEY"] = futures_secret_key

    yield

    for var in (
        "KRAKEN_FUTURES_API_KEY",
        "KRAKEN_FUTURES_SECRET_KEY",
    ):
        if os.getenv(var):
            del os.environ[var]
