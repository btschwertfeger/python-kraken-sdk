# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2026 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module implementing unit tests for the MCP server tool wiring"""

from __future__ import annotations

from unittest import mock

import pytest
from mcp.server.mcpserver.exceptions import ToolError

from kraken import mcp


@pytest.mark.unit
@pytest.mark.mcp
def test_spot_request_wiring() -> None:
    """spot_request forwards its arguments to SpotClient.request and
    returns the result serialized as JSON"""
    with mock.patch.object(
        mcp._spot,
        "request",
        return_value={"unixtime": 0},
    ) as request:
        result = mcp.spot_request("GET", "/0/public/Time")

    request.assert_called_once_with(
        "GET",
        "/0/public/Time",
        params=None,
        auth=False,
        do_json=False,
    )
    assert result == {"unixtime": 0}


@pytest.mark.unit
@pytest.mark.mcp
def test_spot_request_wraps_exceptions() -> None:
    """spot_request re-raises SDK exceptions as ToolError so the model
    sees the actual error message instead of a generic one"""
    with (
        mock.patch.object(mcp._spot, "request", side_effect=ValueError("boom")),
        pytest.raises(ToolError, match="boom"),
    ):
        mcp.spot_request("GET", "/0/private/Balance", auth=True)


@pytest.mark.unit
@pytest.mark.mcp
def test_futures_request_wiring() -> None:
    """futures_request forwards its arguments to FuturesClient.request and
    returns the result serialized as JSON"""
    with mock.patch.object(
        mcp._futures,
        "request",
        return_value={"result": "success"},
    ) as request:
        result = mcp.futures_request("GET", "/api/v3/openpositions")

    request.assert_called_once_with(
        "GET",
        "/api/v3/openpositions",
        post_params=None,
        query_params=None,
        auth=False,
    )
    assert result == {"result": "success"}


@pytest.mark.unit
@pytest.mark.mcp
def test_futures_request_wraps_exceptions() -> None:
    """futures_request re-raises SDK exceptions as ToolError so the model
    sees the actual error message instead of a generic one"""
    with (
        mock.patch.object(mcp._futures, "request", side_effect=ValueError("boom")),
        pytest.raises(ToolError, match="boom"),
    ):
        mcp.futures_request("GET", "/api/v3/accounts", auth=True)
