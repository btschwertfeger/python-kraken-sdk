#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

import os

import pytest

from kraken.spot import Funding, Market, Staking, Trade, User


@pytest.fixture
def spot_auth_user() -> Market:
    return User(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_auth_market() -> Market:
    return Market(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_auth_trade() -> Trade:
    return Trade(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_auth_funding() -> Funding:
    return Funding(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))


@pytest.fixture
def spot_auth_staking() -> Staking:
    return Staking(key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY"))
