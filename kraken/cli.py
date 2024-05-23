#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#
# pylint: disable=import-outside-toplevel

"""
Module implementing the command-line interface for the python-kraken-sdk.
"""

from __future__ import annotations

import logging
import sys
from re import sub as re_sub
from typing import Any

from cloup import (
    Choice,
    Context,
    HelpFormatter,
    HelpTheme,
    Style,
    argument,
    command,
    option,
)
from orjson import JSONDecodeError
from orjson import loads as orloads


def print_version(ctx: Context, param: Any, value: Any) -> None:
    """Prints the version of the package"""
    if not value or ctx.resilient_parsing:
        return
    from importlib.metadata import version

    print(version("python-kraken-sdk"))
    ctx.exit()


@command(
    context_settings={
        "auto_envvar_prefix": "KRAKEN",
        "help_option_names": ["-h", "--help"],
    },
    formatter_settings=HelpFormatter.settings(
        theme=HelpTheme(
            invoked_command=Style(fg="bright_yellow"),
            heading=Style(fg="bright_white", bold=True),
            constraint=Style(fg="magenta"),
            col1=Style(fg="bright_yellow"),
        ),
    ),
    no_args_is_help=True,
)
@option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@option(
    "-X",
    required=True,
    type=Choice(["GET", "POST", "PUT", "DELETE"]),
    default="GET",
    help="Request type",
)
@option(
    "-d",
    "--data",
    required=False,
    type=str,
    help="Payload as valid JSON string",
)
@option(
    "--timeout",
    required=False,
    type=int,
    default=10,
    help="Timeout in seconds",
)
@option(
    "-m",
    "--market",
    required=True,
    default="SPOT",
    type=Choice(["SPOT", "FUTURES", "NFT"]),
    help="Market to access",
)
@option(
    "--api-key",
    required=False,
    type=str,
    default="",
    help="Kraken Public API Key",
)
@option(
    "--secret-key",
    required=False,
    type=str,
    default="",
    help="Kraken Secret API Key",
)
@option(
    "-v",
    "--verbose",
    required=False,
    is_flag=True,
    help="Increase verbosity",
)
@argument("url", type=str, required=True)
def main(url: str, **kwargs: dict) -> None:
    """Command-line tool to access the Kraken Cryptocurrency Exchange API"""

    logging.basicConfig(
        format="%(asctime)s %(levelname)8s | %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        level=logging.INFO if not kwargs["verbose"] else logging.DEBUG,
    )

    if (market := kwargs["market"].lower()) == "spot":  # type: ignore[attr-defined]
        from kraken.base_api import KrakenSpotBaseAPI

        client = KrakenSpotBaseAPI
    elif market == "futures":
        from kraken.base_api import KrakenFuturesBaseAPI

        client = KrakenFuturesBaseAPI  # type: ignore[assignment]
    else:  # market == "nft":
        from kraken.base_api import KrakenNFTBaseAPI

        client = KrakenNFTBaseAPI

    logging.debug("Initializing Kraken Client")
    client = client(  # type: ignore[assignment]
        key=kwargs.get("api_key", None),  # type: ignore[arg-type]
        secret=kwargs.get("secret_key", None),  # type: ignore[arg-type]
    )

    try:

        response = client._request(  # type: ignore[call-arg] # pylint: disable=protected-access,no-value-for-parameter
            method=kwargs["x"],  # type: ignore[arg-type]
            uri=(uri := re_sub(r"https:/\/S+\.com", "", url)),
            params=orloads(kwargs.get("data") or "{}"),
            timeout=kwargs["timeout"],  # type: ignore[arg-type]
            auth="private" in uri.lower(),
        )
    except JSONDecodeError as exc:
        logging.error(f"Could not parse the passed data. {exc}")
    except Exception as exc:
        logging.error(f"Exception occurred: {exc}")
        sys.exit(1)
    else:
        print(response)
    sys.exit(0)
