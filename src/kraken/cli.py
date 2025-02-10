# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#
# pylint: disable=import-outside-toplevel

"""
Module implementing the command-line interface for the python-kraken-sdk.
"""

from __future__ import annotations

import logging
import sys
from re import sub as re_sub
from typing import TYPE_CHECKING, Any

from click import echo
from cloup import (
    Choice,
    HelpFormatter,
    HelpTheme,
    Style,
    argument,
    group,
    option,
    pass_context,
)
from orjson import JSONDecodeError
from orjson import loads as orloads

if TYPE_CHECKING:
    from cloup import Context

LOG: logging.Logger = logging.getLogger(__name__)


def print_version(ctx: Context, param: Any, value: Any) -> None:  # noqa: ANN401, ARG001
    """Prints the version of the package"""
    if not value or ctx.resilient_parsing:
        return
    from importlib.metadata import version  # noqa: PLC0415

    echo(version("python-kraken-sdk"))
    ctx.exit()


@group(
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
    "-v",
    "--verbose",
    required=False,
    is_flag=True,
    help="Increase verbosity",
)
@pass_context
def cli(ctx: Context, **kwargs: dict) -> None:
    """Command-line tool to access the Kraken Cryptocurrency Exchange API"""
    ctx.obj = kwargs

    logging.basicConfig(
        format="%(asctime)s %(levelname)8s | %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        level=logging.INFO if not kwargs["verbose"] else logging.DEBUG,
    )


@cli.command()
@option(
    "-X",
    required=True,
    type=Choice(["GET", "POST", "PUT", "DELETE"]),
    default="GET",
    help="Request method",
    show_default="GET",
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
@argument("url", type=str, required=True)
@pass_context
def spot(ctx: Context, url: str, **kwargs: dict) -> None:  # noqa: ARG001
    """Access the Kraken Spot REST API"""
    from kraken.base_api import SpotClient  # noqa: PLC0415

    LOG.debug("Initialize the Kraken client")
    client = SpotClient(
        key=kwargs["api_key"],  # type: ignore[arg-type]
        secret=kwargs["secret_key"],  # type: ignore[arg-type]
    )

    try:
        response = (
            client.request(  # pylint: disable=protected-access,no-value-for-parameter
                method=kwargs["x"],  # type: ignore[arg-type]
                uri=(uri := re_sub(r"https://.*.com", "", url)),
                params=orloads(kwargs.get("data") or "{}"),
                timeout=kwargs["timeout"],  # type: ignore[arg-type]
                auth="private" in uri.lower(),
            )
        )
    except JSONDecodeError as exc:
        LOG.error(f"Could not parse the passed data. {exc}")  # noqa: G004
    except Exception as exc:  # noqa: BLE001
        LOG.error(f"Exception occurred: {exc}")  # noqa: G004
        sys.exit(1)
    else:
        echo(response)
    sys.exit(0)


@cli.command()
@option(
    "-X",
    required=True,
    type=Choice(["GET", "POST", "PUT", "DELETE"]),
    default="GET",
    help="Request method",
    show_default="GET",
)
@option(
    "-d",
    "--data",
    required=False,
    type=str,
    help="POST parameters as valid JSON string",
)
@option(
    "-q",
    "--query",
    required=False,
    type=str,
    help="Query parameters as valid JSON string",
)
@option(
    "--timeout",
    required=False,
    type=int,
    default=10,
    help="Timeout in seconds",
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
@argument("url", type=str, required=True)
@pass_context
def futures(ctx: Context, url: str, **kwargs: dict) -> None:  # noqa: ARG001
    """Access the Kraken Futures REST API"""
    from kraken.base_api import FuturesClient  # noqa: PLC0415

    LOG.debug("Initialize the Kraken client")
    client = FuturesClient(
        key=kwargs["api_key"],  # type: ignore[arg-type]
        secret=kwargs["secret_key"],  # type: ignore[arg-type]
    )

    try:
        response = (
            client.request(  # pylint: disable=protected-access,no-value-for-parameter
                method=kwargs["x"],  # type: ignore[arg-type]
                uri=(uri := re_sub(r"https://.*.com", "", url)),
                post_params=orloads(kwargs.get("data") or "{}"),
                query_params=orloads(kwargs.get("query") or "{}"),
                timeout=kwargs["timeout"],  # type: ignore[arg-type]
                auth="derivatives" in uri.lower(),
            )
        )
    except JSONDecodeError as exc:
        LOG.error(f"Could not parse the passed data. {exc}")  # noqa: G004
    except Exception as exc:  # noqa: BLE001
        LOG.error(f"Exception occurred: {exc}")  # noqa: G004
        sys.exit(1)
    else:
        echo(response)
    sys.exit(0)
