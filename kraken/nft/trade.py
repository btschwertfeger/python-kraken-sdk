#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module implementing the NFT Trade client"""

from __future__ import annotations

from kraken.base_api import KrakenNFTBaseAPI


class Trade(KrakenNFTBaseAPI):
    """
    Class that implements the Kraken NFT Trade client. Can be used to access
    the Kraken NFT market data.

    Please note that these API endpoints are new and still under development at
    Kraken. So the behavior and parameters may change unexpectedly. Please open
    an issue at https://github.com/btschwertfeger/python-kraken-sdk for any
    issues that can be addressed within this package.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional

    .. code-block:: python
        :linenos:
        :caption: NFT Trade: Create the Trade client

        >>> from kraken.nft import Trade
        >>> trade = Trade() # unauthenticated
        >>> auth_trade = Trade(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: NFT Trade:

        >>> from kraken.nft import Market
        >>> with Trade(key="api-key", secret="secret-key") as trade:
        ...     print(trade.)
    """
