#!/usr/bin/env python
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
from asyncio import sleep
from pathlib import Path
from time import time

from kraken.spot import (
    OrderbookClientV1,
    OrderbookClientV2,
    SpotWSClientV1,
    SpotWSClientV2,
)

FIXTURE_DIR: Path = Path(__file__).resolve().parent / "fixture"
CACHE_DIR: Path = Path(__file__).resolve().parent.parent.parent / ".cache" / "tests"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def is_not_error(
    value: object | dict | set | tuple | list | str | float | None,
) -> bool:
    """Returns True if 'error' as key not in dict."""
    return isinstance(value, dict) and "error" not in value


async def async_wait(seconds: float = 1.0) -> None:
    """Function that waits for ``seconds`` - asynchronous."""
    start: float = time()
    while time() - seconds < start:
        await sleep(0.2)


class SpotWebsocketClientV1TestWrapper(SpotWSClientV1):
    """
    Class that creates an instance to test the SpotWSClientV1.

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
        fh = logging.FileHandler(filename=CACHE_DIR / "spot_ws-v1.log", mode="a")
        fh.setLevel(logging.INFO)
        self.LOG.addHandler(fh)

    async def on_message(
        self: SpotWebsocketClientV1TestWrapper,
        message: list | dict,
    ) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.LOG.info(message)  # the log is read within the tests


class SpotWebsocketClientV2TestWrapper(SpotWSClientV2):
    """
    Class that creates an instance to test the SpotWSClientV2.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: SpotWebsocketClientV2TestWrapper,
        key: str = "",
        secret: str = "",
        **kwargs: dict | str | float | bool | None,
    ) -> None:
        super().__init__(key=key, secret=secret, callback=self.on_message, **kwargs)
        self.LOG.setLevel(logging.INFO)
        fh = logging.FileHandler(filename=CACHE_DIR / "spot_ws-v2.log", mode="a")
        fh.setLevel(logging.INFO)
        self.LOG.addHandler(fh)

    async def on_message(self: SpotWebsocketClientV2TestWrapper, message: dict) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.LOG.info(json.dumps(message))  # the log is read within the tests


class OrderbookClientV1Wrapper(OrderbookClientV1):
    """
    This class is used for testing the Spot OrderbookClientV1.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(self: OrderbookClientV1Wrapper) -> None:
        super().__init__()
        self.LOG.setLevel(logging.INFO)

    async def on_message(
        self: OrderbookClientV1Wrapper,
        message: list | dict,
    ) -> None:
        self.ensure_log(message)
        await super().on_message(message=message)

    async def on_book_update(
        self: OrderbookClientV1Wrapper,
        pair: str,
        message: list,
    ) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.ensure_log((pair, message))

    @classmethod
    def ensure_log(cls, content: dict | list | str) -> None:
        """
        Ensures that the messages are logged.
        Into a file for debugging and general to the log
        to read the logs within the unit tests.
        """
        cls.LOG.info(content)

        log: str = ""
        try:
            with Path(CACHE_DIR / "spot_orderbook-v1.log").open(
                mode="r",
                encoding="utf-8",
            ) as logfile:
                log = logfile.read()
        except FileNotFoundError:
            pass

        with Path(CACHE_DIR / "spot_orderbook.log").open(
            mode="w",
            encoding="utf-8",
        ) as logfile:
            logfile.write(f"{log}\n{content}")


class OrderbookClientV2Wrapper(OrderbookClientV2):
    """
    This class is used for testing the Spot OrderbookClientV2.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(self: OrderbookClientV2Wrapper) -> None:
        super().__init__()
        self.LOG.setLevel(logging.INFO)

    async def on_message(self: OrderbookClientV2Wrapper, message: dict) -> None:
        self.ensure_log(message)
        await super().on_message(message=message)

    async def on_book_update(
        self: OrderbookClientV2Wrapper,
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
            mode="w",
            encoding="utf-8",
        ) as logfile:
            logfile.write(f"{log}\n{json.dumps(content)}")
