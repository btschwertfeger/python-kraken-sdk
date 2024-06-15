#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Checks the internals."""

from __future__ import annotations

from asyncio import run as asyncio_run
from asyncio import sleep as async_sleep

import pytest

from kraken.spot.websocket import SpotWSClientBase


@pytest.mark.spot()
@pytest.mark.spot_websocket()
def test_ws_base_client_context_manager() -> None:
    """
    Checks that the KrakenSpotWSClientBase can be instantiated as context
    manager.
    """

    async def check_it() -> None:
        class TestClient(SpotWSClientBase):
            async def on_message(self: TestClient, message: dict) -> None:
                if message == {"error": "yes"}:
                    raise ValueError("Test Error")

        with TestClient(no_public=True) as client:
            with pytest.raises(ValueError, match=r"Test Error"):
                await client.on_message(message={"error": "yes"})
            await async_sleep(5)

    asyncio_run(check_it())


@pytest.mark.spot()
@pytest.mark.spot_websocket()
def test_ws_base_client_on_message_no_callback(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Checks that the KrakenSpotWSClientBase logs a message when no callback
    was defined.
    """
    client = SpotWSClientBase(no_public=True)
    asyncio_run(client.on_message({"event": "testing"}))
    assert "Received message but no callback is defined!" in caplog.text
