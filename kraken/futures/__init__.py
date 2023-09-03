#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
# pylint: disable=unused-import

"""This module provides the Kraken Futures clients"""

from kraken.futures.funding import Funding
from kraken.futures.market import Market
from kraken.futures.trade import Trade
from kraken.futures.user import User
from kraken.futures.ws_client import KrakenFuturesWSClient

__all__ = ["Funding", "Market", "Trade", "User", "KrakenFuturesWSClient"]
