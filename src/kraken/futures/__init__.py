# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#
# pylint: disable=unused-import

"""This module provides the Kraken Futures clients"""

from kraken.base_api import FuturesAsyncClient
from kraken.futures.funding import Funding
from kraken.futures.market import Market
from kraken.futures.trade import Trade
from kraken.futures.user import User
from kraken.futures.ws_client import FuturesWSClient

__all__ = [
    "Funding",
    "FuturesAsyncClient",
    "FuturesWSClient",
    "Market",
    "Trade",
    "User",
]
