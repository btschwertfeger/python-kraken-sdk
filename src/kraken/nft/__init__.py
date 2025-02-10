# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#
# pylint: disable=unused-import

"""This module provides the Kraken NFT clients"""

from kraken.nft.market import Market
from kraken.nft.trade import Trade

__all__ = [
    "Market",
    "Trade",
]
