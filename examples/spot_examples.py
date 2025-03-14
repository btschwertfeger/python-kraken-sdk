# -*- mode: python; coding: utf-8 -*-
# !/usr/bin/env python3
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Module that implements some samples for the Kraken Spot REST clients.

This module may not be maintained on a regular basis, so please refer to the
unit tests of this package as they provide a much deeper dive into the usage.
"""

import logging
import logging.config
import os
import time
from pathlib import Path

from kraken.spot import Earn, Funding, Market, Trade, User

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


key = os.getenv("API_KEY")
secret = os.getenv("SECRET_KEY")


def user_examples() -> None:
    """Example usage of the User client"""
    user = User(key=key, secret=secret)

    print(user.get_account_balance())
    print(user.get_trade_balance())  # asset='BTC'
    print(user.get_open_orders())
    print(user.get_closed_orders())
    print(
        user.get_orders_info(txid="OBQFM7-JNVKS-H3ULEH"),
    )  # or txid='id1,id2,id3' or txid=['id1','id2']
    print(user.get_trades_history())
    time.sleep(3)
    print(user.get_trades_info(txid="TCNTTR-QBEVO-E5H5UK"))
    print(user.get_open_positions())  # txid='someid'
    print(
        user.get_ledgers_info(),
    )  # asset='BTC' or asset='BTC,EUR' or asset=['BTC','EUR']
    print(user.get_ledgers(id_="LIORGR-33NXH-LBUS5Z"))
    print(user.get_trade_volume())  # pair='BTC/EUR'

    # ____export_report____
    response = user.request_export_report(
        report="ledgers",
        description="myLedgers1",
        format_="CSV",
    )  # report='trades'
    print(user.get_export_report_status(report="ledgers"))

    # save report to file
    response_data = user.retrieve_export(id_=response["id"])
    with Path("myExport.zip").open("wb") as file:
        for chunk in response_data.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)

    print(
        user.delete_export_report(id_=response["id"], type_="delete"),
    )  # alternative: type_=cancel


def market_examples() -> None:
    """Example usage of the Market client"""
    market = Market()

    print(market.get_assets(assets=["XBT"]))
    print(market.get_asset_pairs(pair=["DOTEUR"]))
    print(market.get_ticker(pair="XBTUSD"))
    print(market.get_ohlc(pair="XBTUSD", interval=5))
    print(market.get_order_book(pair="XBTUSD", count=10))
    print(market.get_recent_trades(pair="XBTUSD"))
    print(market.get_recent_spreads(pair="XBTUSD"))
    print(market.get_system_status())
    time.sleep(2)


def trade_examples() -> None:
    """Example usage of the Trade client"""
    raise ValueError(
        "Attention: Please check if you really want to execute trade functions.",
    )
    trade = Trade(key=key, secret=secret)

    if False:
        print(
            trade.create_order(
                ordertype="limit",
                side="buy",
                volume=1,
                pair="BTC/EUR",
                price=0.01,
            ),
        )
        print(
            trade.create_order_batch(
                orders=[
                    {
                        "close": {
                            "ordertype": "stop-loss-limit",
                            "price": 120,
                            "price2": 110,
                        },
                        "ordertype": "limit",
                        "price": 140,
                        "price2": 130,
                        "timeinforce": "GTC",
                        "type": "buy",
                        "userref": "345dsdfddfgdsgdfgsfdsfsdf",
                        "volume": 1000,
                    },
                    {
                        "ordertype": "limit",
                        "price": 150,
                        "timeinforce": "GTC",
                        "type": "sell",
                        "userref": "1dfgesggwe5t3",
                        "volume": 123,
                    },
                ],
                pair="BTC/USD",
                validate=True,
            ),
        )

        print(
            trade.edit_order(txid="sometxid", pair="BTC/EUR", volume=4.2, price=17000),
        )
        time.sleep(2)

        print(trade.cancel_order(txid="O2JLFP-VYFIW-35ZAAE"))
        print(trade.cancel_all_orders())
        print(trade.cancel_all_orders_after_x(timeout=6))

    print(
        trade.cancel_order_batch(
            orders=[
                "O2JLFP-VYFIW-35ZAAE",
                "O523KJ-DO4M2-KAT243",
                "OCDIAL-YC66C-DOF7HS",
                "OVFPZ2-DA2GV-VBFVVI",
            ],
        ),
    )


def funding_examples() -> None:
    """Example usage of the Funding client"""
    funding = Funding(key=key, secret=secret)
    print(funding.get_deposit_methods(asset="DOT"))
    # print(funding.get_deposit_address(asset='DOT', method='Polkadot'))
    # print(funding.get_recent_deposits_status(asset='DOT'))
    print(
        funding.get_withdrawal_info(asset="DOT", key="MyPolkadotWallet", amount="200"),
    )

    raise ValueError(
        "Attention: Please check if you really want to execute funding functions.",
    )
    if False:
        time.sleep(2)
        print(funding.withdraw_funds(asset="DOT", key="MyPolkadotWallet", amount=200))
        print(funding.get_recent_withdraw_status(asset="DOT"))
        print(funding.cancel_widthdraw(asset="DOT", refid="12345"))
        print(
            funding.wallet_transfer(
                asset="ETH",
                amount=0.100,
                from_="Spot Wallet",
                to_="Futures Wallet",
            ),
        )


def earn_examples() -> None:
    """
    Example usage of the Funding client; not shown, since special API key
    permissions must be set.
    """
    earn = Earn(key=key, secret=secret)  # noqa: F841
    # ...
    # see tests/spot/test_spot_earn.py for examples.


def main() -> None:
    user_examples()
    market_examples()
    trade_examples()
    funding_examples()
    earn_examples()


if __name__ == "__main__":
    main()
