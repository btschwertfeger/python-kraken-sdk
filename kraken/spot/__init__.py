#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
# pylint: disable=unused-import,cyclic-import

"""Module that provides the Spot REST clients."""

from kraken.base_api import SpotAsyncClient, SpotClient
from kraken.spot.earn import Earn
from kraken.spot.funding import Funding
from kraken.spot.market import Market
from kraken.spot.orderbook import SpotOrderBookClient
from kraken.spot.trade import Trade
from kraken.spot.user import User
from kraken.spot.ws_client import SpotWSClient

__all__ = [
    "Earn",
    "Funding",
    "SpotWSClient",
    "Market",
    "SpotOrderBookClient",
    "SpotClient",
    "SpotAsyncClient",
    "Trade",
    "User",
]
