#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements some example usage for the Kraken Futures REST clients."""

import logging
import os
import time
from pathlib import Path

from kraken.futures import Funding, Market, Trade, User

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

key = os.getenv("FUTURES_SANDBOX_KEY")
secret = os.getenv("FUTURES_SANDBOX_SECRET")

#  _   _  ___ _____ _____
# | \ | |/ _ \_   _| ____|_
# |  \| | | | || | |  _| (_)
# | |\  | |_| || | | |___ _
# |_| \_|\___/ |_| |_____(_)
# ----> More examples can be found in kraken/tests/*.py
#
# Examples may not be updated regularly


def market_examples() -> None:
    """Example market client usage"""
    # market = Market()
    # print(market.get_tick_types())
    # print(market.get_tradeable_products(tick_type='trade'))
    # print(market.get_resolutions(tick_type='trade', tradeable='PI_XBTUSD'))
    # print(market.get_ohlc(tick_type='trade', symbol='PI_XBTUSD', resolution='5m', from_='1668989233'))
    # print(market.get_fee_schedules())
    # # print(market.get_orderbook(symbol='fi_xbtusd_180615')) # this endpoint is broken
    # print(market.get_tickers())
    # print(market.get_instruments())
    # print(market.get_instruments_status())
    # print(market.get_instruments_status(instrument='PI_XBTUSD'))
    # print(market.get_trade_history(symbol='PI_XBTUSD'))
    # print(market.get_historical_funding_rates(symbol='PI_XBTUSD'))
    # time.sleep(2)

    priv_market = Market(key=key, secret=secret, sandbox=True)
    # print(priv_market.get_fee_schedules_vol())
    print(priv_market.get_leverage_preference())
    # print(priv_market.set_leverage_preference(symbol='PF_XBTUSD', maxLeverage=2)) # set max leverage
    # print(priv_market.set_leverage_preference(symbol='PF_XBTUSD')) # reset max leverage
    # print(priv_market.set_pnl_preference(symbol='PF_XBTUSD', pnlPreference='BTC'))

    # time.sleep(2)
    # print(priv_market.get_execution_events())
    # print(market.get_public_execution_events(tradeable='PI_XBTUSD'))
    # print(market.get_public_order_events(tradeable='PI_XBTUSD'))
    # print(market.get_public_mark_price_events(tradeable='PI_XBTUSD'))
    # print(priv_market.get_order_events())
    # print(priv_market.get_trigger_events())


def user_examples() -> None:
    """Example User client usage"""
    user = User(key=key, secret=secret, sandbox=True)
    print(user.get_wallets())

    print(user.get_subaccounts())
    print(user.get_unwind_queue())
    print(user.get_notifications())

    print(user.get_open_positions())
    print(user.get_open_orders())

    print(user.get_account_log(before="1604937694000"))
    print(user.get_account_log(info="futures liquidation"))
    time.sleep(2)
    response = user.get_account_log_csv()
    assert response.status_code in [200, "200"]
    with Path("account_log.csv").open("wb") as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)


def trade_examples() -> None:
    """Example Trade client usage"""
    raise ValueError(
        "Attention: Please check if you really want to test the trade endpoints!",
    )
    trade = Trade(key=key, secret=secret, sandbox=True)
    print(trade.get_fills())
    print(trade.get_fills(lastFillTime="2020-07-21T12:41:52.790Z"))
    print(
        trade.create_batch_order(
            batchorder_list=[
                {
                    "order": "send",
                    "order_tag": "1",
                    "orderType": "lmt",
                    "symbol": "PI_XBTUSD",
                    "side": "buy",
                    "size": 1,
                    "limitPrice": 1.00,
                },
                {
                    "order": "send",
                    "order_tag": "2",
                    "orderType": "stp",
                    "symbol": "PI_XBTUSD",
                    "side": "buy",
                    "size": 1,
                    "limitPrice": 2.00,
                    "stopPrice": 3.00,
                },
                {
                    "order": "cancel",
                    "order_id": "e35d61dd-8a30-4d5f-a574-b5593ef0c050",
                },
                {
                    "order": "cancel",
                    "cliOrdId": 123456789,
                },
            ],
        ),
    )
    print(trade.cancel_all_orders())
    print(trade.cancel_all_orders(symbol="pi_xbtusd"))
    print(trade.dead_mans_switch(timeout=60))
    print(trade.dead_mans_switch(timeout=0))  # to deactivate
    print(trade.cancel_order(order_id="some order id"))
    print(
        trade.edit_order(
            orderId="some order id",
            size=300,
            limitPrice=401,
            stopPrice=350,
        ),
    )
    print(trade.get_orders_status(orderIds=["orderid1", "orderid2"]))
    print(
        trade.create_order(
            orderType="lmt",
            side="buy",
            size=1,
            limitPrice=4,
            symbol="pf_bchusd",
        ),
    )
    print(
        trade.create_order(
            orderType="take_profit",
            side="buy",
            size=1,
            symbol="pf_bchusd",
            stopPrice=100,
            triggerSignal="mark",
        ),
    )


def funding_examples() -> None:
    """Example Funding client usage"""
    funding = Funding(key=key, secret=secret, sandbox=True)
    print(funding.get_historical_funding_rates(symbol="PF_SOLUSD"))


def main() -> None:
    user_examples()
    market_examples()
    trade_examples()
    funding_examples()


if __name__ == "__main__":
    main()
