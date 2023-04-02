<h1 align="center">Futures and Spot Websocket and REST API Python SDK for the Kraken Cryptocurrency Exchange 🐙</h1>

<div align="center">

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/btschwertfeger/python-kraken-sdk)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-orange.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Generic badge](https://img.shields.io/badge/python-3.7_|_3.8_|_3.9_|_3.10_|_3.11-blue.svg)](https://shields.io/)
[![Downloads](https://static.pepy.tech/personalized-badge/python-kraken-sdk?period=total&units=abbreviation&left_color=grey&right_color=orange&left_text=downloads)](https://pepy.tech/project/python-kraken-sdk)

[![CodeQL](https://github.com/btschwertfeger/Python-Kraken-SDK/actions/workflows/codeql.yml/badge.svg?branch=master)](https://github.com/btschwertfeger/Python-Kraken-SDK/actions/workflows/codeql.yml)
[![CI/CD](https://github.com/btschwertfeger/Python-Kraken-SDK/actions/workflows/cicd.yml/badge.svg?branch=master)](https://github.com/btschwertfeger/Python-Kraken-SDK/actions/workflows/cicd.yml)
![codecov](https://codecov.io/gh/btschwertfeger/Python-Kraken-SDK/branch/master/badge.svg)

![release](https://shields.io/github/release-date/btschwertfeger/python-kraken-sdk)
![release](https://shields.io/github/v/release/btschwertfeger/python-kraken-sdk?display_name=tag)
[![DOI](https://zenodo.org/badge/510751854.svg)](https://zenodo.org/badge/latestdoi/510751854)

</div>

<h3>
This is an unofficial collection of REST and websocket clients for Spot and Futures trading on the Kraken cryptocurrency exchange using Python.
</h3>

---

## 📌 Disclaimer

There is no guarantee that this software will work flawlessly at this or later times. Of course, no responsibility is taken for possible profits or losses. This software probably has some errors in it, so use it at your own risk. Also no one should be motivated or tempted to invest assets in speculative forms of investment. By using this software you release the author(s) from any liability regarding the use of this software.

---

## Features

Clients:

- Spot REST Clients
- Spot Websocket Client
- Futures REST Clients
- Futures Websocket Client

General:

- access both public and private endpoints
- responsive error handling, custom exceptions and logging
- extensive example scripts (see `/examples`)

---

## ❗️ Attention

**ONLY** tagged releases are availabe at PyPI. So the content of the master may not match with the content of the latest release. So please have a look at the release specifc READMEs and changelogs.

---

## Table of Contents

- [ Installation and setup ](#installation)
- [ Spot Client Example Usage ](#spotusage)
  - [REST API](#spotrest)
  - [Websockets](#spotws)
- [ Futures Client Example Usage ](#futuresusage)
  - [REST API](#futuresrest)
  - [Websockets](#futuresws)
- [ Spot Client Documentation ](#spotdocu)
  - [ User ](#spotuser)
  - [ Trade ](#spottrade)
  - [ Market ](#spotmarket)
  - [ Funding ](#spotfunding)
  - [ Staking ](#spotstaking)
  - [ KrakenSpotWSClient ](#spotwsclient)
- [ Futures Client Documentation ](#futuresdocu)
  - [ User ](#futuresuser)
  - [ Trade ](#futurestrade)
  - [ Market ](#futuresmarket)
  - [ Funding ](#futuresfunding)
  - [ KrakenFuturesWSClient ](#futureswsclient)
- [ Troubleshooting ](#trouble)
- [ Notes ](#notes)
- [ References ](#references)

---

<a name="installation"></a>

# 🛠 Installation and setup

### 1. Install the Python module:

```bash
python3 -m pip install python-kraken-sdk
```

### 2. Register at Kraken and generate API Keys:

- Spot Trading: https://www.kraken.com/u/security/api
- Futures Trading: https://futures.kraken.com/trade/settings/api
- Futures Sandbox: https://demo-futures.kraken.com/settings/api

### 3. Start using the provided example scripts

### 4. Error handling

If any unexpected behaviour occurs, please check <b style="color: yellow">your API permissions</b>, <b style="color: yellow">rate limits</b>, update the python-kraken-sdk, see the [Troubleshooting](#trouble) section, and if the error persits please open an issue.

---

<a name="spotusage"></a>

# 📍 Spot Client Example Usage

A template Spot trading bot using both websocket and REST clients can be found in `/examples/spot_trading_bot_template.py`.

<a name="spotrest"></a>

## Spot REST API

... can be found in `/examples/spot_examples.py`

```python
from kraken.spot import User, Market, Trade, Funding, Staking

def main() -> None:
    key = 'Kraken-public-key'
    secret = 'Kraken-secret-key'

    # ____USER________
    user = User(key=key, secret=secret)
    print(user.get_account_balance())
    print(user.get_open_orders())

    # ____MARKET_______
    market = Market()
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

if __name__ == '__main__': main()
```

<a name="spotws"></a>

## Websockets

... can be found in `/examples/spot_ws_examples.py`

```python
import asyncio, time
from kraken.spot import KrakenSpotWSClient

async def main() -> None:

    key = 'Kraken-public-key'
    secret = 'Kraken-secret-key'

    class Bot(KrakenSpotWSClient):
        async def on_message(self, msg) -> None:
            if 'event' in msg:
                if msg['event'] in ['pong', 'heartbeat']: return

            print(msg)
            # if condition:
            #     await self.create_order(
            #         ordertype='limit',
            #         side='buy',
            #         pair='BTC/EUR',
            #         price=20000,
            #         volume=1
            #     )
            # ... it is also possible to call regular Spot REST endpoints
            # but using the WsClient's functions is more efficient
            # because the requests will be sent via the ws connection

    # ___Public_Websocket_Feeds_______
    bot = Bot() # only use this one if you dont need private feeds
    print(bot.public_sub_names) # list public subscription names

    await bot.subscribe(subscription={ 'name': 'ticker' }, pair=['XBT/EUR', 'DOT/EUR'])
    await bot.subscribe(subscription={ 'name': 'spread' }, pair=['XBT/EUR', 'DOT/EUR'])
    # await bot.subscribe(subscription={ 'name': 'book' }, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': 'book', 'depth': 25}, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': 'ohlc' }, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': 'ohlc', 'interval': 15}, pair=['XBT/EUR', 'DOT/EUR'])
    # await bot.subscribe(subscription={ 'name': 'trade' }, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': '*' } , pair=['BTC/EUR'])

    time.sleep(2) # wait because unsubscribing is faster than subscribing ...
    await bot.unsubscribe(subscription={ 'name': 'ticker' }, pair=['XBT/EUR','DOT/EUR'])
    await bot.unsubscribe(subscription={ 'name': 'spread' }, pair=['XBT/EUR'])
    await bot.unsubscribe(subscription={ 'name': 'spread' }, pair=['DOT/EUR'])
    # ....

    # ___Authenticated_Websocket_____
    # when using the authenticated bot, you can also subscribe to public feeds
    auth_bot = Bot(key=key, secret=secret)
    print(auth_bot.private_sub_names) # list private subscription names
    await auth_bot.subscribe(subscription={ 'name': 'ownTrades' })
    await auth_bot.subscribe(subscription={ 'name': 'openOrders' })

    time.sleep(2)
    await auth_bot.unsubscribe(subscription={ 'name': 'ownTrades' })
    await auth_bot.unsubscribe(subscription={ 'name': 'openOrders' })

    while True: await asyncio.sleep(6)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: asyncio.run(main())
    except KeyboardInterrupt: loop.close()
```

Note: Authenticated Spot websocket clients can also un/subscribe from/to public feeds.

---

<a name="futuresusage"></a>

# 📍 Futures Client Example Usage

Kraken provides a sandbox environment at https://demo-futures.kraken.com for paper trading. When using this API keys you have to set the `sandbox` parameter to `True` when instantiating the respecitve client.

A template Futures trading bot using both websocket and REST clients can be found in `/examples/futures_trading_bot_template.py`.

<a name="futuresrest"></a>

## Futures REST API

The following example can be found in `/examples/futures_examples.py`.

```python
from kraken.futures import Market, User, Trade, Funding

def main() -> None:

    key = 'futures-api-key'
    secret = 'futures-secret-key'

    # ____USER__________
    user = User(key=key, secret=secret) # optional: sandbox=True
    print(user.get_wallets())
    print(user.get_open_orders())
    print(user.get_open_positions())
    print(user.get_subaccounts())
    # ....

    # ____MARKET_________
    market = Market()
    print(market.get_ohlc(tick_type='trade', symbol='PI_XBTUSD', resolution='5m'))

    priv_market = Market(key=key, secret=secret)
    print(priv_market.get_fee_schedules_vol())
    print(priv_market.get_execution_events())
    # ....

    # ____TRADE_________
    trade = Trade(key=key, secret=secret)
    print(trade.get_fills())
    print(trade.create_batch_order(
        batchorder_list = [{
            'order': 'send',
            'order_tag': '1',
            'orderType': 'lmt',
            'symbol': 'PI_XBTUSD',
            'side': 'buy',
            'size': 1,
            'limitPrice': 12000,
            'cliOrdId': 'some-client-id'
        }, {
            'order': 'send',
            'order_tag': '2',
            'orderType': 'stp',
            'symbol': 'PI_XBTUSD',
            'side': 'buy',
            'size': 1,
            'limitPrice': 10000,
            'stopPrice': 11000,
        }, {
            'order': 'cancel',
            'order_id': 'e35dsdfsdfsddd-8a30-4d5f-a574-b5593esdf0',
        }, {
            'order': 'cancel',
            'cliOrdId': 'another-client-id',
        }],
    ))
    print(trade.cancel_all_orders())
    print(trade.create_order(orderType='lmt', side='buy', size=1, limitPrice=4, symbol='pf_bchusd'))
    # ....

    # ____FUNDING_______
    funding = Funding(key=key, secret=secret)
    # ....

if __name__ == '__main__': main()
```

<a name="futuresws"></a>

## Futures Websocket Client

The following example can be found in `/examples/futures_ws_examples.py`.

```python
import asyncio
from kraken.futures import KrakenFuturesWSClient

async def main() -> None:

    key = 'futures-api-key'
    secret = 'futures-secret-key'

    # ___Custom_Trading_Bot__________
    class Bot(KrakenFuturesWSClient):

        async def on_message(self, event) -> None:
            print(event)
            # >> apply your trading strategy here <<
            # you can also combine this with the Futures REST clients

    # _____Public_Websocket_Feeds___________________
    bot = Bot()
    # print(bot.get_available_public_subscription_feeds())

    products = ['PI_XBTUSD', 'PF_ETHUSD']

    # subscribe to a public websocket feed
    await bot.subscribe(feed='ticker', products=products)
    # await bot.subscribe(feed='book', products=products)
    # ...

    # unsubscribe from a public websocket feed
    # await bot.unsubscribe(feed='ticker', products=products)

    # _____Authenticated_Websocket__________________
    auth_bot = Bot(key=key, secret=secret)
    # print(auth_bot.get_available_private_subscription_feeds())

    # subscribe to a private/authenticated websocket feed
    await auth_bot.subscribe(feed='fills')
    await auth_bot.subscribe(feed='open_positions')
    await auth_bot.subscribe(feed='open_orders')
    # ...

    # unsubscribe from a private/authenticaed websocket feed
    await auth_bot.unsubscribe(feed='fills')

    while True: await asyncio.sleep(6)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: asyncio.run(main())
    except KeyboardInterrupt: loop.close()

```

Note: Authenticated Futures websocket clients can also un/subscribe from/to public feeds.

---

<a name="spotdocu"></a>

# 📖 Spot Client Documentation

<a name="spotuser"></a>

## User

`kraken.spot.User`

| Method                     | Documentation                                                                 |
| -------------------------- | ----------------------------------------------------------------------------- |
| `get_account_balance`      | https://docs.kraken.com/rest/#operation/getAccountBalance                     |
| `get_balances`             | returns the overall and available balance of a given currency                 |
| `get_trade_balance`        | https://docs.kraken.com/rest/#operation/getTradeBalance                       |
| `get_open_orders`          | https://docs.kraken.com/rest/#operation/getOpenOrders                         |
| `get_closed_orders`        | https://docs.kraken.com/rest/#operation/getClosedOrders                       |
| `get_orders_info`          | https://docs.kraken.com/rest/#operation/getOrdersInfo                         |
| `get_trades_history`       | https://docs.kraken.com/rest/#operation/getTradeHistory                       |
| `get_trades_info`          | https://docs.kraken.com/rest/#operation/getTradesInfo                         |
| `get_open_positions`       | https://docs.kraken.com/rest/#operation/getOpenPositions                      |
| `get_ledgers_info`         | https://docs.kraken.com/rest/#operation/getLedgers                            |
| `get_ledgers`              | https://docs.kraken.com/rest/#operation/getLedgersInfo                        |
| `get_trade_volume`         | https://docs.kraken.com/rest/#operation/getTradeVolume                        |
| `request_export_report`    | https://docs.kraken.com/rest/#operation/addExport                             |
| `get_export_report_status` | https://docs.kraken.com/rest/#operation/exportStatus                          |
| `retrieve_export`          | https://docs.kraken.com/rest/#operation/retrieveExport                        |
| `delete_export_report`     | https://docs.kraken.com/rest/#operation/removeExport                          |
| `create_subaccount`        | https://docs.kraken.com/rest/#tag/User-Subaccounts/operation/createSubaccount |

<a name="spottrade"></a>

## Trade

`kraken.spot.Trade`

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

## Market

`kraken.spot.Market`

| Method                    | Documentation                                                 |
| ------------------------- | ------------------------------------------------------------- |
| `get_assets`              | https://docs.kraken.com/rest/#operation/getAssetInfo          |
| `get_tradable_asset_pair` | https://docs.kraken.com/rest/#operation/getTradableAssetPairs |
| `get_ticker`              | https://docs.kraken.com/rest/#operation/getTickerInformation  |
| `get_ohlc`                | https://docs.kraken.com/rest/#operation/getOHLCData           |
| `get_order_book`          | https://docs.kraken.com/rest/#operation/getOrderBook          |
| `get_recent_trades`       | https://docs.kraken.com/rest/#operation/getRecentTrades       |
| `get_recend_spreads`      | https://docs.kraken.com/rest/#operation/getRecentSpreads      |
| `get_system_status`       | checks if Kraken is online                                    |

<a name="spotfunding"></a>

## Funding

`kraken.spot.Funding`

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

## Staking

`kraken.spot.Staking`

| Method                             | Documentation                                                     |
| ---------------------------------- | ----------------------------------------------------------------- |
| `stake_asset`                      | https://docs.kraken.com/rest/#operation/stake                     |
| `unstake_asset`                    | https://docs.kraken.com/rest/#operation/unstake                   |
| `list_stakeable_assets`            | https://docs.kraken.com/rest/#operation/getStakingAssetInfo       |
| `get_pending_staking_transactions` | https://docs.kraken.com/rest/#operation/getStakingPendingDeposits |
| `list_staking_transactions`        | https://docs.kraken.com/rest/#operation/getStakingTransactions    |

<a name="spotwsclient"></a>

## KrakenSpotWSClient

`kraken.spot.KrakenSpotWSClient`

| Method                         | Documentation                                                             |
| ------------------------------ | ------------------------------------------------------------------------- |
| `get_ws_token`                 | https://docs.kraken.com/rest/#tag/Websockets-Authentication               |
| `create_order`                 | https://docs.kraken.com/websockets/#message-addOrder                      |
| `edit_order`                   | https://docs.kraken.com/websockets/#message-editOrder                     |
| `cancel_order`                 | https://docs.kraken.com/websockets/#message-cancelOrder                   |
| `cancel_all_orders`            | https://docs.kraken.com/websockets/#message-cancelAll                     |
| `cancel_all_orders_after`      | https://docs.kraken.com/websockets/#message-cancelAllOrdersAfter          |
| `subscribe`                    | https://docs.kraken.com/websockets/#message-subscribe                     |
| `unsubscribe`                  | https://docs.kraken.com/websockets/#message-unsubscribe                   |
| `private_sub_names`            | get private subscription names                                            |
| `public_sub_names`             | get public subscription names                                             |
| `active_private_subscriptions` | get active private subscriptions                                          |
| `active_public_subscriptions`  | get active public subscriptions                                           |
| `on_message`                   | function which should be overloaded or will execute the callback function |

---

<a name="futuresdocu"></a>

# 📖 Futures Client Documentation

<a name="futuresuser"></a>

## User

`kraken.futures.User`

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

## Trade

`kraken.futures.Trade`

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

## Market

`kraken.futures.Market`

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

## Funding

`kraken.futures.Funding`

| Method                               | Documentation                                                                                            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `get_historical_funding_rates`       | https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-funding-rates-historicalfundingrates |
| `initiate_wallet_transfer`           | https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-wallet-transfer              |
| `initiate_subccount_transfer`        | https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-sub-account-transfer         |
| `initiate_withdrawal_to_spot_wallet` | https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-withdrawal-to-spot-wallet    |

<a name="futureswsclient"></a>

## KrakenFuturesWSClient

`kraken.futures.KrakenFuturesWSClient`

| Method                                     | Documentation                                |
| ------------------------------------------ | -------------------------------------------- |
| `subscribe`                                | subscribe to a feed                          |
| `unsubscribe`                              | unsubscribe from a feed                      |
| `get_available_public_subscription_feeds`  | returns all available public feeds           |
| `get_available_private_subscription_feeds` | returns all available private feeds          |
| `on_message`                               | callback function which should be overloaded |

---

<a name="trouble"></a>

# 🚨 Troubleshooting

- Check if your version of <b>python-kraken-sdk version</b> is the newest.
- Check the <b>permissions of your API keys</b> and the required permissions on the respective endpoints.
- If you get some cloudflare or <b>rate limit errors</b>, please check your Kraken Tier level and maybe apply for a higher rank if required.
- <b>Use different API keys for different algorithms</b>, because the nonce calculation is based on timestamps and a sent nonce must always be the highest nonce ever sent of that API key. Having multiple algorithms using the same keys will result in invalid nonce errors.

---

<a name="notes"></a>

# 📝 Notes:

- Pull requests will be ignored until the owner finished the core idea
<!-- - Triggers: stop-loss, stop-loss-limit, take-profit and take-profit-limit orders. -->

- Coding standards are not always followed to make arguments and function names as similar as possible to those in the Kraken API documentations.

<a name="references"></a>

# 🔭 References

- https://docs.kraken.com/rest
- https://docs.kraken.com/websockets
- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

---
