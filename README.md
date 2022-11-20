# Welcome to the Python SDK for the Kraken Cryptocurrency Exchange! 🦑

<div align="center">

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/btschwertfeger/python-kraken-sdk)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-orange.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Generic badge](https://img.shields.io/badge/python-3.7+-blue.svg)](https://shields.io/)
[![Downloads](https://static.pepy.tech/personalized-badge/python-kraken-sdk?period=total&units=abbreviation&left_color=grey&right_color=orange&left_text=downloads)](https://pepy.tech/project/python-kraken-sdk)

<!-- [![PyPI download month](https://img.shields.io/pypi/dm/python-kraken-sdk.svg)](https://pypi.python.org/pypi/python-kraken-sdk) -->

</div>

This is an unofficial collection of REST and websocket clients to interact with the Kraken exchange API in Python.

There is no guarantee that this software will work flawlessly at this or later times. Everyone has to look at the underlying source code themselves and consider whether this is appropriate for their own use.

Of course, no responsibility is taken for possible profits or losses. No one should be motivated or tempted to invest assets in speculative forms of investment.

---

## Table of Contents

- [ Installation ](#installation)
- [ Spot Clients Example Usage ](#spotusage)
  - [REST API](#spotrest)
  - [Websockets](#spotws)
- [ Futures Clients Example Usage ](#futuresusage)
  - [REST API](#futuresrest)
  - [Websockets](#futuresws)
- [ Spot Clients Documentation ](#spotdocu)
  - [ User ](#spotuser)
  - [ Trade ](#spottrade)
  - [ Market ](#spotmarket)
  - [ Funding ](#spotfunding)
  - [ Staking ](#spotstaking)
  - [ WsClient ](#spotwsclient)
- [ Futures Clients Documentation ](#futuresdocu)
  - [ User ](#futuresuser)
  - [ Trade ](#futurestrade)
  - [ Market ](#futuresmarket)
  - [ Funding ](#futuresfunding)
- [ Notes ](#notes)
- [ References ](#references)

---

<a name="installation"></a>

## Installation

```bash
python3 -m pip install python-kraken-sdk
```

---

<a name="spotusage"></a>

## Spot Clients Example Usage

<a name="spotrest"></a>

### REST API

... can be found in `/examples/examples.py`

```python
from kraken.spot.client import User, Market, Trade, Funding, Staking

def main() -> None:
    key = 'Kraken pub key'
    secret = 'Kraken secret key'

    # ____USER________
    user = User(key=key, secret=secret)
    print(user.get_account_balance())
    print(user.get_open_orders())

    # ____MARKET_______
    market = Market(key=key, secret=secret)
    print(market.get_ticker(pair='BTCUSD'))

    # ____TRADE________
    trade = Trade(key=key, secret=secret)
    print(trade.create_order(
         ordertype='limit',
         side='buy',
         volume=1,
         pair='BTC/EUR',
         price=20000
    ))

    # ____FUNDING______
    funding = Funding(key=key, secret=secret)
    print(funding.withdraw_funds(asset='DOT', key='MyPolkadotWallet', amount=200))
    print(funding.cancel_widthdraw(asset='DOT', refid='<some id>'))

    # ____STAKING______
    staking = Staking(key=key, secret=secret)
    print(staking.list_stakeable_assets())
    print(staking.stake_asset(asset='DOT', amount=20, method='polkadot-staked'))

if __name__ == '__main__':
    main()
```

<a name="spotws"></a>

### Websockets

... can be found in `/examples/ws_examples.py`

```python
import asyncio
from kraken.spot.client import WsClient
from kraken.spot.websocket.websocket import KrakenSpotWSClient

async def main() -> None:

    key = 'kraken public key'
    secret = 'kraken secret key'

    class Bot(KrakenSpotWSClient):
        async def on_message(self, msg) -> None:
            if 'event' in msg:
                if msg['event'] in ['pong', 'heartbeat']: return

            print(msg)
            # await self._client.create_order(
            #     ordertype='limit',
            #     side='buy',
            #     pair='BTC/EUR',
            #     price=20000,
            #     volume=1
            # )
            # ... it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient

    bot = Bot(WsClient(key=key, secret=secret))
    await bot.subscribe(pair=['BTC/EUR'], subscription={ 'name': 'ticker' }, private=False)
    await bot.subscribe(subscription={ 'name': 'ownTrades' }, private=True)

    while True: await asyncio.sleep(6)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

---

<a name="futuresusage"></a>

## Futures Clients Example Usage

<a name="futuresrest"></a>

### REST API

... can be found in `/examples/futures_examples.py`

```python
from kraken.futures.client import Market, User, Trade, Funding

def main() -> None:

    demo: bool = False
    key = 'Kraken futures public key'
    secret = 'Kraken futures secret key'

    # ____USER__________
    user = User(key=key,secret=secret, sandbox=demo)
    print(user.get_wallets())
    print(user.get_open_orders())
    print(user.get_open_positions())
    print(user.get_subaccounts())
    # ....

    # ____MARKET_________
    market = Market()
    print(market.get_ohlc(tick_type='trade', symbol='PI_XBTUSD', resolution='5m'))

    priv_market = Market(key=key,secret=secret, sandbox=demo)
    print(priv_market.get_fee_schedules_vol())
    print(priv_market.get_execution_events())
    # ....

    # ____TRADE_________
    trade = Trade(key=key, secret=secret, sandbox=demo)
    print(trade.get_fills())
    print(trade.create_batch_order(
        batchorder_list = [{
            "order": "send",
            "order_tag": "1",
            "orderType": "lmt",
            "symbol": "PI_XBTUSD",
            "side": "buy",
            "size": 1,
            "limitPrice": 12000,
            "cliOrdId": "another-client-id"
        }, {
            "order": "send",
            "order_tag": "2",
            "orderType": "stp",
            "symbol": "PI_XBTUSD",
            "side": "buy",
            "size": 1,
            "limitPrice": 10000,
            "stopPrice": 110000,
        }, {
            "order": "cancel",
            "order_id": "e35dsdfsdfsddd-8a30-4d5f-a574-b5593esdf0",
        }, {
            "order": "cancel",
            "cliOrdId": "some-client-id",
        }],
    ))
    print(trade.cancel_all_orders())
    print(trade.create_order(
        orderType='lmt', side='buy', size=1, limitPrice=4, symbol='pf_bchusd'
    ))
    # ....

    # ____FUNDING_______
    funding = Funding(key=key, secret=secret, sandbox=demo)
    # ....

if __name__ == '__main__':
    main()
```

<a name="futuresws"></a>

### Websockets

... not implemented so far

```python

```

---

<a name="spotdocu"></a>

## Sport Clients Documentation

<a name="spotuser"></a>

### User

| Method                     | Documentation                                             |
| -------------------------- | --------------------------------------------------------- |
| `get_account_balance`      | https://docs.kraken.com/rest/#operation/getAccountBalance |
| `get_balances`             |
| `get_trade_balance`        | https://docs.kraken.com/rest/#operation/getTradeBalance   |
| `get_open_orders`          | https://docs.kraken.com/rest/#operation/getOpenOrders     |
| `get_closed_orders`        | https://docs.kraken.com/rest/#operation/getClosedOrders   |
| `get_orders_info`          | https://docs.kraken.com/rest/#operation/getOrdersInfo     |
| `get_trades_history`       | https://docs.kraken.com/rest/#operation/getTradeHistory   |
| `get_trades_info`          | https://docs.kraken.com/rest/#operation/getTradesInfo     |
| `get_open_positions`       | https://docs.kraken.com/rest/#operation/getOpenPositions  |
| `get_ledgers_info`         | https://docs.kraken.com/rest/#operation/getLedgers        |
| `get_ledgers`              | https://docs.kraken.com/rest/#operation/getLedgersInfo    |
| `get_trade_volume`         | https://docs.kraken.com/rest/#operation/getTradeVolume    |
| `request_export_report`    | https://docs.kraken.com/rest/#operation/addExport         |
| `get_export_report_status` | https://docs.kraken.com/rest/#operation/exportStatus      |
| `retrieve_export`          | https://docs.kraken.com/rest/#operation/retrieveExport    |
| `delete_export_report`     | https://docs.kraken.com/rest/#operation/removeExport      |

<a name="spottrade"></a>

### Trade

| Method                      | Documentation                                                |
| --------------------------- | ------------------------------------------------------------ |
| `create_order`              | https://docs.kraken.com/rest/#operation/addOrder             |
| `create_order_batch`        | https://docs.kraken.com/rest/#operation/addOrderBatch        |
| `edit_order`                | https://docs.kraken.com/rest/#operation/editOrder            |
| `cancel_order`              | https://docs.kraken.com/rest/#operation/cancelOrder          |
| `cancel_all_orders`         | https://docs.kraken.com/rest/#operation/cancelAllOrders      |
| `cancel_all_orders_after_x` | https://docs.kraken.com/rest/#operation/cancelAllOrdersAfter |
| `cancel_order_batch`        | https://docs.kraken.com/rest/#operation/cancelOrderBatch     |

<a name="spotmarket"></a>

### Market

| Method                    | Documentation                                                 |
| ------------------------- | ------------------------------------------------------------- |
| `get_assets`              | https://docs.kraken.com/rest/#operation/getAssetInfo          |
| `get_tradable_asset_pair` | https://docs.kraken.com/rest/#operation/getTradableAssetPairs |
| `get_ticker`              | https://docs.kraken.com/rest/#operation/getTickerInformation  |
| `get_ohlc`                | https://docs.kraken.com/rest/#operation/getOHLCData           |
| `get_order_book`          | https://docs.kraken.com/rest/#operation/getOrderBook          |
| `get_recent_trades`       | https://docs.kraken.com/rest/#operation/getRecentTrades       |
| `get_recend_spreads`      | https://docs.kraken.com/rest/#operation/getRecentSpreads      |
| `get_system_status`       |                                                               |

<a name="spotfunding"></a>

### Funding

| Method                       | Documentation                                                      |
| ---------------------------- | ------------------------------------------------------------------ |
| `get_deposit_methods`        | https://docs.kraken.com/rest/#operation/getDepositMethods          |
| `get_deposit_address`        | https://docs.kraken.com/rest/#operation/getDepositAddresses        |
| `get_recend_deposits_status` | https://docs.kraken.com/rest/#operation/getStatusRecentDeposits    |
| `get_withdrawal_info`        | https://docs.kraken.com/rest/#operation/getWithdrawalInformation   |
| `withdraw_funds`             | https://docs.kraken.com/rest/#operation/withdrawFund               |
| `get_recend_withdraw_status` | https://docs.kraken.com/rest/#operation/getStatusRecentWithdrawals |
| `cancel_withdraw`            | https://docs.kraken.com/rest/#operation/cancelWithdrawal           |
| `wallet_transfer`            | https://docs.kraken.com/rest/#operation/walletTransfer             |

<a name="spotstaking"></a>

### Staking

| Method                             | Documentation                                                     |
| ---------------------------------- | ----------------------------------------------------------------- |
| `stake_asset`                      | https://docs.kraken.com/rest/#operation/stake                     |
| `unstake_asset`                    | https://docs.kraken.com/rest/#operation/unstake                   |
| `list_stakeable_assets`            | https://docs.kraken.com/rest/#operation/getStakingAssetInfo       |
| `get_pending_staking_transactions` | https://docs.kraken.com/rest/#operation/getStakingPendingDeposits |
| `list_staking_transactions`        | https://docs.kraken.com/rest/#operation/getStakingTransactions    |

<a name="spotwsclient"></a>

### WsClient

| Method                        | Documentation                                                    |
| ----------------------------- | ---------------------------------------------------------------- |
| `get_ws_token`                | https://docs.kraken.com/rest/#tag/Websockets-Authentication      |
| `create_order`                | https://docs.kraken.com/websockets/#message-addOrder             |
| `edit_order`                  | https://docs.kraken.com/websockets/#message-editOrder            |
| `cancel_order`                | https://docs.kraken.com/websockets/#message-cancelOrder          |
| `cancel_all_orders`           | https://docs.kraken.com/websockets/#message-cancelAll            |
| `cancel_all_orders_after`     | https://docs.kraken.com/websockets/#message-cancelAllOrdersAfter |
| `subscribe`                   |                                                                  |
| `unsubscribe`                 |                                                                  |
| `get_available_subscriptions` |                                                                  |

---

<a name="futuresdocu"></a>

## Futures Client Documentation

<a name="futuresuser"></a>

### User

| Method                | Documentation                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `get_wallets`         | https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-wallets                             |
| `get_open_orders`     | https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-orders                         |
| `get_open_positions`  | https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-positions                      |
| `get_subaccounts`     | https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-subaccounts                         |
| `get_unwindqueue`     | https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-position-percentile-of-unwind-queue |
| `get_notificatios`    | https://docs.futures.kraken.com/#http-api-trading-v3-api-general-get-notifications                                   |
| `get_account_log`     | https://docs.futures.kraken.com/#http-api-history-account-log                                                        |
| `get_account_log_csv` | https://docs.futures.kraken.com/#http-api-history-account-log-get-recent-account-log-csv                             |

<a name="futurestrade"></a>

### Trade

| Method               | Documentation                                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `get_fills`          | https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-data-get-your-fills                              |
| `create_batch_order` | https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-batch-order-management                     |
| `cancel_all_orders`  | https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-all-orders                          |
| `dead_mans_switch`   | https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-dead-man-39-s-switch                       |
| `cancel_order`       | https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-order                               |
| `edit_order`         | https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-edit-order                                 |
| `get_orders_status`  | https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-get-the-current-status-for-specific-orders |
| `create_order`       | https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order                                 |

<a name="futuresmarket"></a>

### Market

| Method                         | Documentation                                                                                                                                                                                               |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_ohlc`                     | https://docs.futures.kraken.com/#http-api-charts-ohlc-get-ohlc                                                                                                                                              |
| `get_tick_types`               | https://docs.futures.kraken.com/#http-api-charts-ohlc-get-tick-types                                                                                                                                        |
| `get_tradeable_products`       | https://docs.futures.kraken.com/#http-api-charts-ohlc-get-tradeable-products                                                                                                                                |
| `get_resolutions`              | https://docs.futures.kraken.com/#http-api-charts-ohlc-get-resolutions                                                                                                                                       |
| `get_fee_schedules`            | https://docs.futures.kraken.com/#http-api-trading-v3-api-fee-schedules-get-fee-schedules                                                                                                                    |
| `get_fee_schedules_vol`        | https://docs.futures.kraken.com/#http-api-trading-v3-api-fee-schedules-get-fee-schedule-volumes                                                                                                             |
| `get_orderbook`                | https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-orderbook                                                                                                                          |
| `get_tickers`                  | https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-tickers                                                                                                                            |
| `get_instruments`              | https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instruments                                                                                                                 |
| `get_instruments_status`       | https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instrument-status-list and https://docs.futures.kraken.com#http-api-trading-v3-api-instrument-details-get-instrument-status |
| `get_trade_history`            | https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-trade-history                                                                                                                      |
| `get_historical_funding_rates` | https://support.kraken.com/hc/en-us/articles/360061979852-Historical-Funding-Rates                                                                                                                          |
| `get_leverage_preference`      | https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-get-the-leverage-setting-for-a-market                                                                                             |
| `set_leverage_preference`      | https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-set-the-leverage-setting-for-a-market                                                                                             |
| `get_pnl_preference`           | https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-get-pnl-currency-preference-for-a-market                                                                                          |
| `set_pnl_preference`           | https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-set-pnl-currency-preference-for-a-market                                                                                          |
| `get_execution_events`         | https://docs.futures.kraken.com/#http-api-history-market-history-get-execution-events                                                                                                                       |
| `get_public_execution_events`  | https://docs.futures.kraken.com/#http-api-history-market-history-get-public-execution-events and https://support.kraken.com/hc/en-us/articles/4401755685268-Market-History-Executions                       |
| `get_public_order_events`      | https://docs.futures.kraken.com/#http-api-history-market-history-get-public-order-events and https://support.kraken.com/hc/en-us/articles/4401755906452-Market-History-Orders                               |
| `get_public_mark_price_events` | https://docs.futures.kraken.com/#http-api-history-market-history-get-public-mark-price-events and https://support.kraken.com/hc/en-us/articles/4401748276116-Market-History-Mark-Price                      |
| `get_order_events`             | https://docs.futures.kraken.com/#http-api-history-market-history-get-order-events                                                                                                                           |
| `get_trigger_events`           | https://docs.futures.kraken.com/#http-api-history-market-history-get-trigger-events                                                                                                                         |

<a name="futuresfunding"></a>

### Funding

| Method                               | Documentation                                                                                            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `get_historical_funding_rates`       | https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-funding-rates-historicalfundingrates |
| `initiate_wallet_transfer`           | https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-wallet-transfer              |
| `initiate_subccount_transfer`        | https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-sub-account-transfer         |
| `initiate_withdrawal_to_spot_wallet` | https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-withdrawal-to-spot-wallet    |

---

<a name="notes"></a>

## Notes:

- Pull requests will be ignored until the owner finished the core idea
<!-- - Triggers: stop-loss, stop-loss-limit, take-profit and take-profit-limit orders. -->

---

<a name="references"></a>

## References

- https://docs.kraken.com/websockets
- https://docs.kraken.com/rest/
- https://docs.futures.kraken.com/
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

---
