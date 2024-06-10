#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
# pylint: disable=unused-import,cyclic-import

"""Module that provides the Spot REST clients."""

from kraken.base_api import KrakenSpotAsyncClient as SpotAsyncClient
from kraken.spot.earn import Earn
from kraken.spot.funding import Funding
from kraken.spot.market import Market
from kraken.spot.orderbook_v1 import OrderbookClientV1
from kraken.spot.orderbook_v2 import OrderbookClientV2
from kraken.spot.staking import Staking
from kraken.spot.trade import Trade
from kraken.spot.user import User
from kraken.spot.websocket_v1 import KrakenSpotWSClientV1
from kraken.spot.websocket_v2 import KrakenSpotWSClientV2

__all__ = [
    "Earn",
    "Funding",
    "KrakenSpotWSClientV1",
    "KrakenSpotWSClientV2",
    "Market",
    "OrderbookClientV1",
    "OrderbookClientV2",
    "SpotAsyncClient",
    "Staking",
    "Trade",
    "User",
]
