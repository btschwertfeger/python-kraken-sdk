#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

import os

import pytest

from kraken.futures import Funding, Market, Trade, User

FUTURES_API_KEY: str = os.getenv("FUTURES_API_KEY")
FUTURES_SECRET_KEY: str = os.getenv("FUTURES_SECRET_KEY")
FUTURES_SANDBOX_KEY: str = os.getenv("FUTURES_SANDBOX_KEY")
FUTURES_SANDBOX_SECRET_KEY: str = os.getenv("FUTURES_SANDBOX_SECRET")


@pytest.fixture()
def futures_api_key() -> str:
    """Returns the Futures API key"""
    return FUTURES_API_KEY


@pytest.fixture()
def futures_secret_key() -> str:
    """Returns the Futures API secret key"""
    return FUTURES_SECRET_KEY


@pytest.fixture()
def futures_market() -> Market:
    """
    Fixture providing an unauthenticated Futures Market client
    """
    return Market()


@pytest.fixture()
def futures_auth_market() -> Market:
    """
    Fixture providing an authenticated Futures Market client.
    """
    return Market(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)


@pytest.fixture()
def futures_demo_market() -> Market:
    """
    Fixture providing an authenticated Futures Market client that
    uses the demo/sandbox environment.
    """
    return Market(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )


@pytest.fixture()
def futures_user() -> User:
    """
    Fixture providing an unauthenticated Futures User client.
    """
    user: User = User()
    user.TIMEOUT = 30
    return user


@pytest.fixture()
def futures_auth_user() -> User:
    """
    Fixture providing an authenticated Futures User client.
    """
    user: User = User(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)
    User.TIMEOUT = 30
    return user


@pytest.fixture()
def futures_demo_user() -> User:
    """
    Fixture providing an authenticated Futures User client that
    uses the demo/sandbox environment.
    """
    return User(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )


@pytest.fixture()
def futures_trade() -> Trade:
    """
    Fixture providing an unauthenticated Futures Trade client.
    """
    return Trade()


@pytest.fixture()
def futures_auth_trade() -> Trade:
    """
    Fixture providing an authenticated Futures Trade client.
    """
    return Trade(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)


@pytest.fixture()
def futures_demo_trade() -> Trade:
    """
    Fixture providing an authenticated Futures Trade client that
    uses the demo/sandbox environment.
    """
    return Trade(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )


@pytest.fixture()
def futures_funding() -> Funding:
    """
    Fixture providing an unauthenticated Futures Funding client.
    """
    return Funding()


@pytest.fixture()
def futures_auth_funding() -> Funding:
    """
    Fixture providing an authenticated Futures Funding client.
    """
    return Funding(key=FUTURES_API_KEY, secret=FUTURES_SECRET_KEY)


@pytest.fixture()
def futures_demo_funding() -> Funding:
    """
    Fixture providing an authenticated Futures Funding client that
    uses the demo/sandbox environment.
    """
    return Funding(
        key=FUTURES_SANDBOX_KEY,
        secret=FUTURES_SANDBOX_SECRET_KEY,
        sandbox=True,
    )
