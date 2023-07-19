#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
This module provides the Spot websocket client (Websocket API V2 as
documented in - https://docs.kraken.com/websockets-v2).
"""
from __future__ import annotations

# import asyncio
# import json
# import logging
# from copy import deepcopy
from typing import Callable, List, Optional

# from kraken.base_api import defined, ensure_string
# from kraken.exceptions import KrakenException
# from kraken.spot.trade import Trade
from kraken.spot.websocket import KrakenSpotWSClientBase


class KrakenSpotWSClientV2(KrakenSpotWSClientBase):
    """
    todo: write doc
    """

    def __init__(
        self: "KrakenSpotWSClientV2",
        key: str = "",
        secret: str = "",
        callback: Optional[Callable] = None,
        no_public: bool = False,
        beta: bool = False,
    ):
        super().__init__(
            key=key,
            secret=secret,
            callback=callback,
            no_public=no_public,
            beta=beta,
            api_version="v2",
        )

    async def send_message(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2,
    ) -> None:
        """
        todo: implement this
        """

    async def subscribe(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2,
    ) -> None:
        """
        todo: implement this
        """

    async def unsubscribe(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2,
    ) -> None:
        """
        todo: implement this
        """

    @property
    def private_sub_names(self: KrakenSpotWSClientV2) -> List[str]:
        """
        todo: implement this
        :return: _description_
        :rtype: list[str]
        """
        return []

    @property
    def public_sub_names(self: KrakenSpotWSClientV2) -> List[str]:
        """
        todo: implement this

        :return: _description_
        :rtype: list[str]
        """
        return []
