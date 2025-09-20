# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module providing fixtures used for the unit tests regarding the Kraken Spot API.
"""

import os

import pytest

from kraken.spot import Earn, Funding, Market, Trade, User

SPOT_API_KEY: str = os.getenv("SPOT_API_KEY")
SPOT_SECRET_KEY: str = os.getenv("SPOT_SECRET_KEY")


@pytest.fixture(scope="session")
def spot_api_key() -> str:
    """Returns the Kraken Spot API Key for testing."""
    return SPOT_API_KEY


@pytest.fixture(scope="session")
def spot_secret_key() -> str:
    """Returns the Kraken Spot API secret for testing."""
    return SPOT_SECRET_KEY


@pytest.fixture(scope="session")
def spot_auth_user() -> User:
    """
    Fixture providing an authenticated Spot user client.
    """
    return User(key=SPOT_API_KEY, secret=SPOT_SECRET_KEY)


@pytest.fixture(scope="session")
def spot_market() -> Market:
    """
    Fixture providing an unauthenticated Spot market client.
    """
    return Market()


@pytest.fixture(scope="session")
def spot_auth_market() -> Market:
    """
    Fixture providing an authenticated Spot market client.
    """
    return Market(key=SPOT_API_KEY, secret=SPOT_SECRET_KEY)


@pytest.fixture(scope="session")
def spot_trade() -> Trade:
    """
    Fixture providing an unauthenticated Spot trade client.
    """
    return Trade()


@pytest.fixture(scope="session")
def spot_auth_trade() -> Trade:
    """
    Fixture providing an authenticated Spot trade client.
    """
    return Trade(key=SPOT_API_KEY, secret=SPOT_SECRET_KEY)


@pytest.fixture(scope="session")
def spot_earn() -> Earn:
    """
    Fixture providing an unauthenticated Spot earn client.
    """
    return Earn()


@pytest.fixture(scope="session")
def spot_auth_earn() -> Earn:
    """
    Fixture providing an authenticated Spot earn client.
    """
    raise ValueError("Do not use the authenticated Spot earn client for testing!")


@pytest.fixture(scope="session")
def spot_auth_funding() -> Funding:
    """
    Fixture providing an authenticated Spot funding client.
    """
    return Funding(key=SPOT_API_KEY, secret=SPOT_SECRET_KEY)
