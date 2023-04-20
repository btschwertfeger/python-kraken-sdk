#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

import os

import pytest

from kraken.futures import Funding, Market, Trade, User


@pytest.fixture
def futures_market() -> None:
    return Market()


@pytest.fixture
def futures_auth_market() -> None:
    return Market(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_market() -> None:
    return Market(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )


@pytest.fixture
def futures_user() -> None:
    return User()


@pytest.fixture
def futures_auth_user() -> None:
    return User(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_user() -> None:
    return User(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )


@pytest.fixture
def futures_trade() -> None:
    return Trade()


@pytest.fixture
def futures_auth_trade() -> None:
    return Trade(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_trade() -> None:
    return Trade(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )


@pytest.fixture
def futures_funding() -> None:
    return Funding()


@pytest.fixture
def futures_auth_funding() -> None:
    return Funding(
        key=os.getenv("FUTURES_API_KEY"), secret=os.getenv("FUTURES_SECRET_KEY")
    )


@pytest.fixture
def futures_demo_funding() -> None:
    return Funding(
        key=os.getenv("FUTURES_SANDBOX_KEY"),
        secret=os.getenv("FUTURES_SANDBOX_SECRET"),
        sandbox=True,
    )
