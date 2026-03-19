# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

from __future__ import annotations

import contextlib
import logging
from pathlib import Path

from kraken.futures import FuturesWSClient

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


class FuturesWebsocketClientTestWrapper(FuturesWSClient):
    """
    Class that creates an instance to test the FuturesWSClient.

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
        with contextlib.suppress(FileNotFoundError):
            log = Path(CACHE_DIR / "futures_ws.log").read_text(  # noqa: ASYNC240
                encoding="utf-8",
            )

        Path(CACHE_DIR / "futures_ws.log").write_text(  # noqa: ASYNC240
            f"{log}\n{message}",
            encoding="utf-8",
        )
