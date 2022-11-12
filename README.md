# Welcome to the Python SDK for the Kraken Cryptocurrency Exchange! 🦑

<div style="text-align: center">

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

## Installation

```bash
python3 -m pip install python-kraken-sdk
```

---

## Usage

### REST API

... can be found in `/examples/examples.py`

```python
from kraken.spot.client import User, Market, Trade, Funding, Staking

def main() -> None:
    key = 'kraken pub key'
    secret = 'kraken secret key'

    user = User(key=key, secret=secret)
    print(user.get_account_balance())
    print(user.get_open_orders())

    market = Market(key=key, secret=secret)
    print(market.get_ticker(pair='BTCUSD'))

    trade = Trade(key=key, secret=secret)
    print(trade.create_order(
         ordertype='limit',
         side='buy',
         volume=1,
         pair='BTC/EUR',
         price=20000
    ))

    funding = Funding(key=key, secret=secret)
    print(funding.withdraw_funds(asset='DOT', key='MyPolkadotWallet', amount=200))
    print(funding.cancel_widthdraw(asset='DOT', refid='<some id>'))

    staking = Staking(key=key, secret=secret)
    print(staking.list_stakeable_assets())
    print(staking.stake_asset(asset='DOT', amount=20, method='polkadot-staked'))

if __name__ == '__main__':
    main()
```

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

## Sport Client Methods

## User

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

## Funding

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

## Staking

| Method                             | Documentation                                                     |
| ---------------------------------- | ----------------------------------------------------------------- |
| `stake_asset`                      | https://docs.kraken.com/rest/#operation/stake                     |
| `unstake_asset`                    | https://docs.kraken.com/rest/#operation/unstake                   |
| `list_stakeable_assets`            | https://docs.kraken.com/rest/#operation/getStakingAssetInfo       |
| `get_pending_staking_transactions` | https://docs.kraken.com/rest/#operation/getStakingPendingDeposits |
| `list_staking_transactions`        | https://docs.kraken.com/rest/#operation/getStakingTransactions    |

---

## Futures Client Methods (untested)

## Market

| Method                          | Documentation                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| `get_ohlc`                      | https://support.kraken.com/hc/en-us/articles/4403284627220-OHLC                      |
| `get_fee_schedules`             | https://support.kraken.com/hc/en-us/articles/360049269572-Fee-Schedules              |
| `get_orderbook`                 | https://support.kraken.com/hc/en-us/articles/360022839551-Order-Book                 |
| `get_tickers`                   | https://support.kraken.com/hc/en-us/articles/360022839531-Tickers                    |
| `get_instruments`               | https://support.kraken.com/hc/en-us/articles/360022635672-Instruments                |
| `get_history`                   | https://support.kraken.com/hc/en-us/articles/360022839511-History                    |
| `get_historical_funding_rates`  | https://support.kraken.com/hc/en-us/articles/360061979852-Historical-Funding-Rates   |
| `get_market_history_execution`  | https://support.kraken.com/hc/en-us/articles/4401755685268-Market-History-Executions |
| `get_market_history_mark_price` | https://support.kraken.com/hc/en-us/articles/4401748276116-Market-History-Mark-Price |
| `get_market_history_orders`     | https://support.kraken.com/hc/en-us/articles/4401755906452-Market-History-Orders     |

---

## References

- https://docs.kraken.com/websockets
- https://docs.kraken.com/rest/
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

---

## Notes:

- Pull requests will be ignored until the owner finished the core idea
<!-- - Triggers: stop-loss, stop-loss-limit, take-profit and take-profit-limit orders. -->
