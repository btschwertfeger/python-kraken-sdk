# !/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module that implements *some* examples for the Kraken Spot REST clients usage
with focus on xStocks.

NOTE: The xStocks feature is not available globally. Please checkout Kraken's
      documentation to get to know the availability zones.
"""

import logging
import os

from kraken.spot import SpotClient, Trade

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


key = os.getenv("SPOT_API_KEY")
secret = os.getenv("SPOT_SECRET_KEY")

CLIENT = SpotClient(key=key, secret=secret)


def list_all_xstocks() -> None:
    """List all available xStocks on Kraken."""
    print(
        CLIENT.request(
            "GET",
            "/0/public/AssetPairs",
            params={"aclass_base": "tokenized_asset"},
            auth=False,
        ),
    )


def create_xstock_order() -> None:
    """Create a test order for an xStock (validate mode, not placing actual order)."""
    print(
        CLIENT.request(
            "POST",
            "/0/private/AddOrder",
            params={
                "type": "buy",
                "volume": "1",
                "ordertype": "limit",
                "pair": "AAPLxUSD",
                "price": "100.0",
                "validate": True,
                "asset_class": "tokenized_asset",
            },
        ),
    )


def create_xstock_order_alternative() -> None:
    """Create a test order for an xStock (validate mode, not placing actual order)."""
    trade = Trade(key=key, secret=secret)

    print(
        trade.create_order(
            pair="AAPLxUSD",
            side="buy",
            ordertype="limit",
            volume="1",
            price="100.0",
            validate=True,
            extra_params={"asset_class": "tokenized_asset"},
        ),
    )


def main() -> None:
    """Uncomment the examples you want to run:"""
    # NOTE: These are only examples that show how to use the clients, there are
    #       many other functions available in the clients.
    list_all_xstocks()
    # create_xstock_order()
    # create_xstock_order_alternative()


if __name__ == "__main__":
    main()
