#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that implements the unit tests for the Kraken Spot Websocket API v2
client.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from kraken.spot import SpotOrderBookClient, SpotWSClient

FIXTURE_DIR: Path = Path(__file__).resolve().parent / "fixture"
CACHE_DIR: Path = Path(__file__).resolve().parent.parent.parent / ".cache" / "tests"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def is_not_error(
    value: object | dict | set | tuple | list | str | float | None,
) -> bool:
    """Returns True if 'error' as key not in dict."""
    return isinstance(value, dict) and "error" not in value


class SpotWebsocketClientTestWrapper(SpotWSClient):
    """
    Class that creates an instance to test the SpotWSClient.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: SpotWebsocketClientTestWrapper,
        key: str = "",
        secret: str = "",
        **kwargs: dict | str | float | bool | None,
    ) -> None:
        super().__init__(key=key, secret=secret, callback=self.on_message, **kwargs)
        self.LOG.setLevel(logging.INFO)
        fh = logging.FileHandler(filename=CACHE_DIR / "spot_ws-v2.log", mode="a")
        fh.setLevel(logging.INFO)
        self.LOG.addHandler(fh)

    async def on_message(self: SpotWebsocketClientTestWrapper, message: dict) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.LOG.info(json.dumps(message))  # the log is read within the tests


class SpotOrderBookClientWrapper(SpotOrderBookClient):
    """
    This class is used for testing the Spot SpotOrderBookClient.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(self: SpotOrderBookClientWrapper) -> None:
        super().__init__()
        self.LOG.setLevel(logging.INFO)

    async def on_message(self: SpotOrderBookClientWrapper, message: dict) -> None:
        self.ensure_log(message)
        await super().on_message(message=message)

    async def on_book_update(
        self: SpotOrderBookClientWrapper,
        pair: str,
        message: dict,
    ) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.ensure_log((pair, message))

    @classmethod
    def ensure_log(cls, content: dict | list) -> None:
        """
        Ensures that the messages are logged.
        Into a file for debugging and general to the log
        to read the logs within the unit tests.
        """
        cls.LOG.info(json.dumps(content))

        log: str = ""
        try:
            with Path(CACHE_DIR / "spot_orderbook-2.log").open(
                mode="r",
                encoding="utf-8",
            ) as logfile:
                log = logfile.read()
        except FileNotFoundError:
            pass

        with Path(CACHE_DIR / "spot_orderbook.log").open(
            mode="a",
            encoding="utf-8",
        ) as logfile:
            logfile.write(f"{log}\n{json.dumps(content)}")
