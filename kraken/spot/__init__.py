#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger


"""Module that provides the Spot REST clients"""
# pylint: disable=unused-import
from kraken.spot.funding import Funding
from kraken.spot.market import Market
from kraken.spot.staking import Staking
from kraken.spot.trade import Trade
from kraken.spot.user import User
from kraken.spot.websocket import KrakenSpotWSClient
