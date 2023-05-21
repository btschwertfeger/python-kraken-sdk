#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

import os

import pytest

from kraken.futures import Funding, Market, Trade, User


@pytest.fixture
def futures_market() -> Market:
    return Market()


@pytest.fixture
def futures_auth_market() -> Market:
    return Market(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_market() -> Market:
    return Market(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )


@pytest.fixture
def futures_user() -> User:
    return User()


@pytest.fixture
def futures_auth_user() -> User:
    return User(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_user() -> User:
    return User(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )


@pytest.fixture
def futures_trade() -> Trade:
    return Trade()


@pytest.fixture
def futures_auth_trade() -> Trade:
    return Trade(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_trade() -> Trade:
    return Trade(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )


@pytest.fixture
def futures_funding() -> Funding:
    return Funding()


@pytest.fixture
def futures_auth_funding() -> Funding:
    return Funding(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_funding() -> Funding:
    return Funding(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )
