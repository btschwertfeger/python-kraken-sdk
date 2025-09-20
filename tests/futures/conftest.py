# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

import os

import pytest

from kraken.futures import Funding, Market, Trade, User

FUTURES_API_KEY: str = os.getenv("FUTURES_API_KEY")
FUTURES_SECRET_KEY: str = os.getenv("FUTURES_SECRET_KEY")
FUTURES_SANDBOX_KEY: str = os.getenv("FUTURES_SANDBOX_KEY")
FUTURES_SANDBOX_SECRET_KEY: str = os.getenv("FUTURES_SANDBOX_SECRET")
FUTURES_EXTENDED_TIMEOUT: int = 30


@pytest.fixture(scope="session")
def futures_api_key() -> str:
    """Returns the Futures API key"""
    return FUTURES_API_KEY


@pytest.fixture(scope="session")
def futures_secret_key() -> str:
    """Returns the Futures API secret key"""
    return FUTURES_SECRET_KEY


@pytest.fixture(scope="session")
def futures_market() -> Market:
    """
    Fixture providing an unauthenticated Futures Market client
    """
    market: Market = Market()
    market.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return market


@pytest.fixture(scope="session")
def futures_auth_market() -> Market:
    """
    Fixture providing an authenticated Futures Market client.
    """
    market: Market = Market(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)
    market.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return market


@pytest.fixture(scope="session")
def futures_demo_market() -> Market:
    """
    Fixture providing an authenticated Futures Market client that
    uses the demo/sandbox environment.
    """
    market: Market = Market(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )
    market.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return market


@pytest.fixture(scope="session")
def futures_user() -> User:
    """
    Fixture providing an unauthenticated Futures User client.
    """
    user: User = User()
    user.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return user


@pytest.fixture(scope="session")
def futures_auth_user() -> User:
    """
    Fixture providing an authenticated Futures User client.
    """
    user: User = User(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)
    User.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return user


@pytest.fixture(scope="session")
def futures_demo_user() -> User:
    """
    Fixture providing an authenticated Futures User client that
    uses the demo/sandbox environment.
    """
    user: User = User(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )
    User.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return user


@pytest.fixture(scope="session")
def futures_trade() -> Trade:
    """
    Fixture providing an unauthenticated Futures Trade client.
    """
    trade: Trade = Trade()
    trade.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return trade


@pytest.fixture(scope="session")
def futures_auth_trade() -> Trade:
    """
    Fixture providing an authenticated Futures Trade client.
    """
    trade: Trade = Trade(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)
    trade.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return trade


@pytest.fixture(scope="session")
def futures_demo_trade() -> Trade:
    """
    Fixture providing an authenticated Futures Trade client that
    uses the demo/sandbox environment.
    """
    trade: Trade = Trade(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )
    trade.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return trade


@pytest.fixture(scope="session")
def futures_funding() -> Funding:
    """
    Fixture providing an unauthenticated Futures Funding client.
    """
    funding: Funding = Funding()
    funding.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return funding


@pytest.fixture(scope="session")
def futures_auth_funding() -> Funding:
    """
    Fixture providing an authenticated Futures Funding client.
    """
    funding: Funding = Funding(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)
    funding.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return funding


@pytest.fixture(scope="session")
def futures_demo_funding() -> Funding:
    """
    Fixture providing an authenticated Futures Funding client that
    uses the demo/sandbox environment.
    """
    funding: Funding = Funding(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )
    funding.TIMEOUT = FUTURES_EXTENDED_TIMEOUT
    return funding
