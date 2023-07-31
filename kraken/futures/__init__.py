#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""This module provides the Kraken Futures clients"""

# pylint: disable=unused-import
from kraken.futures.funding import Funding
from kraken.futures.market import Market
from kraken.futures.trade import Trade
from kraken.futures.user import User
from kraken.futures.ws_client import KrakenFuturesWSClient

__all__ = ["Funding", "Market", "Trade", "User", "KrakenFuturesWSClient"]
