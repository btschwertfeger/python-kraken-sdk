#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that provides the Spot REST clients and utility functions."""

# pylint: disable=unused-import
from .funding import Funding
from .market import Market, SpotOrderBookClient
from .staking import Staking
from .trade import Trade
from .user import User
from .websocket import KrakenSpotWSClient
