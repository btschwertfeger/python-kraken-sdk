#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""This module provides the Kraken Futures clients"""

# pylint: disable=unused-import
from .funding import Funding
from .market import Market
from .trade import Trade
from .user import User
from .ws_client import KrakenFuturesWSClient
