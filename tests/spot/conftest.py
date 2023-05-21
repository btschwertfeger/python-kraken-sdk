#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module providing fixtures used for the unit tests regarding the Kraken Spot API."""

import os

import pytest

from kraken.spot import Funding, Market, Staking, Trade, User


@pytest.fixture
def spot_auth_user() -> User:
    """
    Fixture providing an authenticated Spot user client.
    """
    return User(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_market() -> Market:
    """
    Fixture providing an unauthenticated Spot market client.
    """
    return Market()


@pytest.fixture
def spot_auth_market() -> Market:
    """
    Fixture providing an authenticated Spot market client.
    """
    return Market(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_trade() -> Trade:
    """
    Fixture providing an unauthenticated Spot trade client.
    """
    return Trade()


@pytest.fixture
def spot_auth_trade() -> Trade:
    """
    Fixture providing an authenticated Spot trade client.
    """
    return Trade(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_auth_funding() -> Funding:
    """
    Fixture providing an authenticated Spot funding client.
    """
    return Funding(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_auth_staking() -> Staking:
    """
    Fixture providing an authenticated Spot staking client.
    """
    return Staking(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))
