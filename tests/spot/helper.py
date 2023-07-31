#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that implements the unit tests for the Kraken Spot Websocket API v1
client.
"""

from __future__ import annotations

import json
import logging
import os
from asyncio import sleep
from time import time
from typing import Any, Union

from kraken.spot import KrakenSpotWSClient, KrakenSpotWSClientV2, OrderbookClient

FIXTURE_DIR: str = os.path.join(os.path.dirname(__file__), "fixture")


def is_not_error(value: Any) -> bool:
    """Returns True if 'error' as key not in dict."""
    return isinstance(value, dict) and "error" not in value


async def async_wait(seconds: float = 1.0) -> None:
    """Function that waits for ``seconds`` - asynchron."""
    start: float = time()
    while time() - seconds < start:
        await sleep(0.2)
    return


class SpotWebsocketClientV1TestWrapper(KrakenSpotWSClient):
    """
    Class that creates an instance to test the KrakenSpotWSClient.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: SpotWebsocketClientV1TestWrapper,
        key: str = "",
        secret: str = "",
    ) -> None:
        super().__init__(key=key, secret=secret, callback=self.on_message)
        self.LOG.setLevel(logging.INFO)
        fh = logging.FileHandler("spot_ws_v1.log", mode="a")
        fh.setLevel(logging.INFO)
        self.LOG.addHandler(fh)

    async def on_message(
        self: SpotWebsocketClientV1TestWrapper,
        message: Union[list, dict],
    ) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.LOG.info(message)  # the log is read within the tests


class SpotWebsocketClientV2TestWrapper(KrakenSpotWSClientV2):
    """
    Class that creates an instance to test the KrakenSpotWSClientV2.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: SpotWebsocketClientV2TestWrapper,
        key: str = "",
        secret: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(key=key, secret=secret, callback=self.on_message, **kwargs)
        self.LOG.setLevel(logging.INFO)
        fh = logging.FileHandler("spot_ws_v2.log", mode="a")
        fh.setLevel(logging.INFO)
        self.LOG.addHandler(fh)

    async def on_message(self: SpotWebsocketClientV2TestWrapper, message: dict) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.LOG.info(json.dumps(message))  # the log is read within the tests


class OrderbookClientWrapper(OrderbookClient):
    """
    This class is used for testing the Spot Orderbook client.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(self: OrderbookClientWrapper) -> None:
        super().__init__()
        self.LOG.setLevel(logging.INFO)

    async def on_message(self: OrderbookClientWrapper, message: dict) -> None:
        self.ensure_log(message)
        await super().on_message(message=message)

    async def on_book_update(
        self: OrderbookClientWrapper,
        pair: str,
        message: dict,
    ) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.ensure_log((pair, message))

    @classmethod
    def ensure_log(cls, content: Any) -> None:
        """
        Ensures that the messages are logged.
        Into a file for debugging and general to the log
        to read the logs within the unit tests.
        """
        cls.LOG.info(json.dumps(content))

        log: str = ""
        try:
            with open("spot_orderbook.log", "r", encoding="utf-8") as logfile:
                log = logfile.read()
        except FileNotFoundError:
            pass

        with open("spot_orderbook.log", "w", encoding="utf-8") as logfile:
            logfile.write(f"{log}\n{json.dumps(content)}")
