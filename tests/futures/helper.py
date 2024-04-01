#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

from __future__ import annotations

import logging
from asyncio import sleep
from pathlib import Path
from time import time

from kraken.futures import KrakenFuturesWSClient

CACHE_DIR: Path = Path(__file__).resolve().parent.parent.parent / ".cache" / "tests"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def is_success(value: object | dict | set | tuple | list | str | float | None) -> bool:
    """
    Returns true if result is success, even if the order may not exist - but kraken received the correct request.
    """
    return (
        isinstance(value, dict) and "result" in value and value["result"] == "success"
    )


def is_not_error(
    value: object | dict | set | tuple | list | str | float | None,
) -> bool:
    """Returns true if result is not error"""
    return isinstance(value, dict) and "error" not in value


async def async_wait(seconds: float = 1.0) -> None:
    """Function that realizes the wait for ``seconds``."""
    start: float = time()
    while time() - seconds < start:
        await sleep(0.2)


class FuturesWebsocketClientTestWrapper(KrakenFuturesWSClient):
    """
    Class that creates an instance to test the KrakenFuturesWSClient.

    It writes the messages to the log and a file. The log is used
    within the tests, the log file is for local debugging.
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: FuturesWebsocketClientTestWrapper,
        key: str = "",
        secret: str = "",
    ) -> None:
        super().__init__(key=key, secret=secret, callback=self.on_message)
        self.LOG.setLevel(logging.INFO)

    async def on_message(
        self: FuturesWebsocketClientTestWrapper,
        message: list | dict,
    ) -> None:
        """
        This is the callback function that must be implemented
        to handle custom websocket messages.
        """
        self.LOG.info(message)  # the log is read within the tests

        log: str = ""
        try:
            with Path(CACHE_DIR / "futures_ws.log").open(
                mode="r",
                encoding="utf-8",
            ) as logfile:
                log = logfile.read()
        except FileNotFoundError:
            pass

        with Path(CACHE_DIR / "futures_ws.log").open(
            mode="w",
            encoding="utf-8",
        ) as logfile:
            logfile.write(f"{log}\n{message}")
