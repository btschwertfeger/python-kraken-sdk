#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger


"""Module that provides the Spot REST clients"""
from kraken.spot.funding import FundingClient
from kraken.spot.market import MarketClient
from kraken.spot.staking import StakingClient
from kraken.spot.trade import TradeClient
from kraken.spot.user import UserClient
from kraken.spot.websocket import KrakenSpotWSClientCl


class User(UserClient):
    """
    Class that is used as a client to access the user-related
    Kraken Futures endpoints.
    """


class Trade(TradeClient):
    """
    Class that is used as a client to access the trade-related
    Kraken Futures endpoints.
    """


class Market(MarketClient):
    """
    Class that is used as a client to access the market-related
    Kraken Futures endpoints.
    """


class Funding(FundingClient):
    """
    Class that is used as a client to access the funding-related
    Kraken Futures endpoints.
    """


class Staking(StakingClient):
    """
    Class that is used as a client to access the staking-related
    Kraken Futures endpoints.
    """


class KrakenSpotWSClient(KrakenSpotWSClientCl):
    """
    Class that is used as a client to create a websocket connection
    and handle un/subscribing, reconnecting, ...
    """
