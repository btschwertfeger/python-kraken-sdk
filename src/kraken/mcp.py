# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2026 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""MCP server exposing the Kraken Spot and Futures ``request`` methods"""

from __future__ import annotations

import os
import threading
from typing import Any, cast

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from kraken.base_api import FuturesClient, SpotClient

mcp: MCPServer = MCPServer("kraken")

_spot = SpotClient(
    key=os.getenv("KRAKEN_SPOT_API_KEY", ""),
    secret=os.getenv("KRAKEN_SPOT_SECRET_KEY", ""),
)
_futures = FuturesClient(
    key=os.getenv("KRAKEN_FUTURES_API_KEY", ""),
    secret=os.getenv("KRAKEN_FUTURES_SECRET_KEY", ""),
    sandbox=os.getenv("KRAKEN_FUTURES_SANDBOX", "").lower() in {"1", "true"},
)

# The MCP SDK dispatches concurrent tool calls onto separate worker threads
# (only "initialize" is handled inline); these clients' nonce generation and
# session-renewal are not thread-safe, so serialize calls per client.
_spot_lock = threading.Lock()
_futures_lock = threading.Lock()


@mcp.tool()
def spot_request(
    method: str,
    uri: str,
    params: dict | None = None,
    *,
    auth: bool = False,
    do_json: bool = False,
) -> dict[str, Any] | list[str] | list[dict[str, Any]]:
    """
    Send a request against the Kraken Spot REST API (also covers xStocks —
    pass ``"asset_class": "tokenized_asset"`` inside ``params`` where the
    Kraken API docs require it).

    :param method: The request method, e.g., ``GET``, ``POST``, ``PUT``
    :param uri: The endpoint to send the request to, e.g. ``/0/public/Time``
    :param params: The request parameters (default: ``None``)
    :param auth: If the request requires authentication (default: ``False``)
    :param do_json: If the params should be sent as JSON body instead of
        form-urlencoded (default: ``False``)
    :return: The parsed response
    """
    try:
        with _spot_lock:
            result = _spot.request(
                method,
                uri,
                params=params,
                auth=auth,
                do_json=do_json,
            )
    except Exception as exc:
        raise ToolError(str(exc)) from exc
    # return_raw is never passed, so result is never a requests.Response
    return cast("dict[str, Any] | list[str] | list[dict[str, Any]]", result)


@mcp.tool()
def futures_request(
    method: str,
    uri: str,
    post_params: dict | None = None,
    query_params: dict | None = None,
    *,
    auth: bool = False,
) -> dict[str, Any] | list[Any]:
    """
    Send a request against the Kraken Futures REST API.

    :param method: The request method, e.g., ``GET``, ``POST``, ``PUT``
    :param uri: The endpoint to send the request to
    :param post_params: The request's POST parameters (default: ``None``)
    :param query_params: The request's query parameters (default: ``None``)
    :param auth: If the request requires authentication (default: ``False``)
    :return: The parsed response
    """
    try:
        with _futures_lock:
            result = _futures.request(
                method,
                uri,
                post_params=post_params,
                query_params=query_params,
                auth=auth,
            )
    except Exception as exc:
        raise ToolError(str(exc)) from exc
    # return_raw is never passed, so result is never a requests.Response
    return cast("dict[str, Any] | list[Any]", result)


def main() -> None:
    """Run the MCP server using the stdio transport"""
    mcp.run()


if __name__ == "__main__":
    main()
