#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Checks the internals
"""

from __future__ import annotations

from asyncio import run as asyncio_run
from typing import Any

import pytest

from kraken.spot.websocket import KrakenSpotWSClientBase

from .helper import async_wait


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_ws_base_client_invalid_api_v() -> None:
    """
    Checks that the KrakenSpotWSClientBase raises an error when an invalid API
    version was specified.
    """
    with pytest.raises(ValueError):
        client = KrakenSpotWSClientBase(api_version="10")


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_ws_base_client_context_manager() -> None:
    """
    Checks that the KrakenSpotWSClientBase can be instantiated as context
    manager.
    """

    async def check_it() -> None:
        class TestClient(KrakenSpotWSClientBase):
            async def on_message(self: TestClient, message: dict) -> None:
                if message == {"error": "yes"}:
                    raise ValueError

        with TestClient(api_version="v2", no_public=True) as client:
            with pytest.raises(ValueError):
                await client.on_message(message={"error": "yes"})
            await async_wait(seconds=5)

    asyncio_run(check_it())


@pytest.mark.spot
@pytest.mark.spot_websocket
def test_ws_base_client_on_message_no_callback(caplog: Any) -> None:
    """
    Checks that the KrakenSpotWSClientBase logs a message when no callback
    was defined.
    """
    client = KrakenSpotWSClientBase(api_version="v2", no_public=True)
    asyncio_run(client.on_message({"event": "testing"}))
    assert "Received message but no callback is defined!" in caplog.text
