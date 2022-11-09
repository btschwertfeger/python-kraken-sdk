# Welcome to the Python Kraken SDK! 🦑

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

## Installation

```bash
python3 -m pip install python-kraken-sdk
```

## Usage

#### REST

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

#### Websockets

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

## What else?

#### Logging

Logging messages are enabled, so you can configure your own logger to track every event. One example can be found in `/examples/examples.py`.

## References

- https://docs.kraken.com/websockets
- https://docs.kraken.com/rest/
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

## Notes:

- Pull requests will be ignored until the owner finished the core idea
<!-- - Triggers: stop-loss, stop-loss-limit, take-profit and take-profit-limit orders. -->
