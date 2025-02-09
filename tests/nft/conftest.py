# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module providing fixtures used for the unit tests regarding the Kraken NFT API.
"""

from __future__ import annotations

import os

import pytest

from kraken.nft import Market, Trade

SPOT_API_KEY: str = os.getenv("SPOT_API_KEY")
SPOT_SECRET_KEY: str = os.getenv("SPOT_SECRET_KEY")


@pytest.fixture
def spot_api_key() -> str:
    """Returns the Kraken Spot API Key for testing."""
    return SPOT_API_KEY


@pytest.fixture
def spot_secret_key() -> str:
    """Returns the Kraken Spot API secret for testing."""
    return SPOT_SECRET_KEY


@pytest.fixture
def nft_market() -> Market:
    """
    Fixture providing an authenticated NFT market client.
    """
    return Market()


@pytest.fixture
def nft_auth_trade() -> Trade:
    """
    Fixture providing an unauthenticated NFT trade client.
    """
    return Trade(key=SPOT_API_KEY, secret=SPOT_SECRET_KEY)
