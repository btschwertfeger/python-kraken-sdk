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

import asyncio
import json

# import logging
# from copy import deepcopy
from typing import Any, Callable, List, Optional

from kraken.base_api import defined  # , ensure_string
from kraken.exceptions import KrakenException

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
        message: dict,
        raw: bool = False,
    ) -> None:
        """
        todo: document this

        """
        if not message.get("method", False):
            raise ValueError(
                """
                The ``message`` must contain the 'method' key with a proper value.
            """
            )
        private: bool = message["method"] in self.private_methods
        print(message)

        if private and not self._is_auth:
            raise KrakenException.KrakenAuthenticationError()

        retries: int = 0
        socket: Any = self._get_socket(private=private)
        while not socket and retries < 12:
            retries += 1
            socket = self._get_socket(private=private)
            await asyncio.sleep(0.4)

        if retries == 12 and not socket:
            raise TimeoutError("Could not get the desired websocket connection!")

        if raw:
            await socket.send(json.dumps(message))
            return

        if private:
            message["params"]["token"] = self._priv_conn.ws_conn_details["token"]

        await socket.send(json.dumps(message))

    async def subscribe(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2, params: dict, req_id: Optional[int] = None
    ) -> None:
        """
        todo: implement this

        - https://docs.kraken.com/websockets-v2/#subscribe
        """

        payload: dict = {"method": "subscribe"}
        if defined(req_id):
            payload["req_id"] = req_id

        payload["params"] = params

        await self.send_message(message=payload)

    async def unsubscribe(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2, params: dict, req_id: Optional[int] = None
    ) -> None:
        """
        todo: implement this

        - https://docs.kraken.com/websockets-v2/#unsubscribe
        """
        payload: dict = {"method": "unsubscribe"}
        if defined(req_id):
            payload["req_id"] = req_id

        payload["params"] = params

        await self.send_message(message=payload)

    @property
    def public_channel_names(self: KrakenSpotWSClientV2) -> List[str]:
        """
        Returns the list of valid values for ``channel`` when un-/subscribing
        from/to public feeds without authentication.

        :return: List of available public channel names
        :rtype: list[str]
        """
        return ["book", "instrument", "ohlc", "ticker", "trade", "ping"]

    @property
    def private_channel_names(self: KrakenSpotWSClientV2) -> List[str]:
        """
        Returns the list of valid values for ``channel`` when un-/subscribing
        from/to private feeds that need authentication.

        :return: List of available private channel names
        :rtype: list[str]
        """
        return ["executions"]

    @property
    def private_methods(self: KrakenSpotWSClientV2) -> List[str]:
        """
        Returns the list of available methods - similar to the REST API Trade
        methods.

        :return: List of available methods
        :rtype: List[str]
        """
        return [
            "add_order",
            "batch_add",
            "batch_cancel",
            "cancel_all",
            "cancel_all_orders_after",
            "cancel_order",
            "edit_order",
        ]
