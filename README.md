<h1 align="center">Futures and Spot Websocket and REST API Python SDK for the Kraken Cryptocurrency Exchange 🐙</h1>

<div align="center">

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/btschwertfeger/python-kraken-sdk)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-orange.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Generic badge](https://img.shields.io/badge/python-3.7_|_3.8_|_3.9_|_3.10_|_3.11-blue.svg)](https://shields.io/)
[![Downloads](https://static.pepy.tech/personalized-badge/python-kraken-sdk?period=total&units=abbreviation&left_color=grey&right_color=orange&left_text=downloads)](https://pepy.tech/project/python-kraken-sdk)

[![Typing](https://img.shields.io/badge/typing-mypy-informational)](https://mypy-lang.org/)
[![CodeQL](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/codeql.yaml/badge.svg?branch=master)](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/codeql.yaml)
[![CI/CD](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/cicd.yaml/badge.svg?branch=master)](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/btschwertfeger/python-kraken-sdk/branch/master/badge.svg)](https://app.codecov.io/gh/btschwertfeger/python-kraken-sdk)

![release](https://shields.io/github/release-date/btschwertfeger/python-kraken-sdk)
![release](https://shields.io/github/v/release/btschwertfeger/python-kraken-sdk?display_name=tag)
[![DOI](https://zenodo.org/badge/510751854.svg)](https://zenodo.org/badge/latestdoi/510751854)
[![Documentation Status stable](https://readthedocs.org/projects/python-kraken-sdk/badge/?version=stable)](https://python-kraken-sdk.readthedocs.io/en/stable)

</div>

> ⚠️ This is an unofficial collection of REST and websocket clients for Spot and Futures trading on the Kraken cryptocurrency exchange using Python. Payward Ltd. and Kraken are in no way associated with the authors of this module and documentation.

---

## 📌 Disclaimer

There is no guarantee that this software will work flawlessly at this or later times. Of course, no responsibility is taken for possible profits or losses. This software probably has some errors in it, so use it at your own risk. Also no one should be motivated or tempted to invest assets in speculative forms of investment. By using this software you release the authors from any liability regarding the use of this software.

---

## Features

Clients:

- Spot REST Clients
- Spot Websocket Client
- Futures REST Clients
- Futures Websocket Client

General:

- access both public and private endpoints
- responsive error handling and custom exceptions
- extensive example scripts (see `/examples` and `/tests`)
- tested using the pytest framework
- releases are permanently archived at [Zenodo](https://zenodo.org/badge/latestdoi/510751854)

Documentation:

- Stable: [https://python-kraken-sdk.readthedocs.io/en/stable](https://python-kraken-sdk.readthedocs.io/en/stable)
- Latest: [https://python-kraken-sdk.readthedocs.io/en/latest](https://python-kraken-sdk.readthedocs.io/en/latest)

---

## ❗️ Attention

**ONLY** tagged releases are available at PyPI. So the content of the master may not match with the content of the latest release. - Please have a look at the release specific READMEs and changelogs.

---

## Table of Contents

- [ Installation and setup ](#installation)
- [ Spot Client Example Usage ](#spotusage)
  - [REST API](#spotrest)
  - [Websockets](#spotws)
- [ Futures Client Example Usage ](#futuresusage)
  - [REST API](#futuresrest)
  - [Websockets](#futuresws)
- [ Troubleshooting ](#trouble)
- [ Contributions ](#contribution)
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

If any unexpected behaviour occurs, please check <b style="color: yellow">your API permissions</b>, <b style="color: yellow">rate limits</b>, update the python-kraken-sdk, see the [Troubleshooting](#trouble) section, and if the error persists please open an issue.

---

<a name="spotusage"></a>

# 📍 Spot Client Example Usage

A template Spot trading bot using both websocket and REST clients can be found in `/examples/spot_trading_bot_template.py`.

<a name="spotrest"></a>

## Spot REST API

... can be found in `/examples/spot_examples.py`

```python
from kraken.spot import User, Market, Trade, Funding, Staking

def main():
    key = "kraken-public-key"
    secret = "kraken-secret-key"

    # ____USER________________________
    user = User(key=key, secret=secret)
    print(user.get_account_balance())
    print(user.get_open_orders())
    # ...

    # ____MARKET_____
    market = Market()
    print(market.get_ticker(pair="BTCUSD"))
    # ...

    # ____TRADE__________________________
    trade = Trade(key=key, secret=secret)
    print(trade.create_order(
         ordertype="limit",
         side="buy",
         volume=1,
         pair="BTC/EUR",
         price=20000
    ))
    # ...

    # ____FUNDING___________________________
    funding = Funding(key=key, secret=secret)
    print(
        funding.withdraw_funds(
            asset="DOT", key="MyPolkadotWallet", amount=200
        )
    )
    print(funding.cancel_widthdraw(asset="DOT", refid="<some id>"))
    # ...

    # ____STAKING______
    staking = Staking(key=key, secret=secret)
    print(staking.list_stakeable_assets())
    print(
        staking.stake_asset(
            asset="DOT", amount=20, method="polkadot-staked"
        )
    )
    # ...

if __name__ == "__main__":
    main()
```

<a name="spotws"></a>

## Websockets

... can be found in `/examples/spot_ws_examples.py`

```python
import time
import asyncio
from kraken.spot import KrakenSpotWSClient

async def main() -> None:

    key = "kraken-public-key"
    secret = "kraken-secret-key"

    class Bot(KrakenSpotWSClient):
        async def on_message(self, msg):
            if isinstance(msg, dict) and "event" in msg:
                if msg["event"] in ("pong", "heartbeat"):
                    return

            print(msg)
            # if condition:
            #     await self.create_order(
            #         ordertype="limit",
            #         side="buy",
            #         pair="BTC/EUR",
            #         price=20000,
            #         volume=1
            #     )
            # ... it is also possible to call regular Spot REST endpoints
            # but using the WsClient's functions is more efficient
            # because the requests will be sent via the ws connection

    # ___Public_Websocket_Feeds_______
    bot = Bot() # only use the unauthenticated client if you don't need private feeds
    print(bot.public_sub_names) # list public subscription names

    await bot.subscribe(subscription={ "name": "ticker" }, pair=["XBT/EUR", "DOT/EUR"])
    await bot.subscribe(subscription={ "name": "spread" }, pair=["XBT/EUR", "DOT/EUR"])
    # await bot.subscribe(subscription={ "name": "book" }, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "book", "depth": 25}, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "ohlc" }, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "ohlc", "interval": 15}, pair=["XBT/EUR", "DOT/EUR"])
    # await bot.subscribe(subscription={ "name": "trade" }, pair=["BTC/EUR"])
    # await bot.subscribe(subscription={ "name": "*" } , pair=["BTC/EUR"])

    time.sleep(2) # wait because unsubscribing is faster than subscribing ...
    await bot.unsubscribe(subscription={ "name": "ticker" }, pair=["XBT/EUR","DOT/EUR"])
    await bot.unsubscribe(subscription={ "name": "spread" }, pair=["XBT/EUR"])
    await bot.unsubscribe(subscription={ "name": "spread" }, pair=["DOT/EUR"])
    # ....

    # ___Authenticated_Websocket_____
    # when using the authenticated client, you can also subscribe to public feeds
    auth_bot = Bot(key=key, secret=secret)
    print(auth_bot.private_sub_names) # list private subscription names
    await auth_bot.subscribe(subscription={ "name": "ownTrades" })
    await auth_bot.subscribe(subscription={ "name": "openOrders" })

    time.sleep(2)
    await auth_bot.unsubscribe(subscription={ "name": "ownTrades" })
    await auth_bot.unsubscribe(subscription={ "name": "openOrders" })

    while True:
        await asyncio.sleep(6)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        loop.close()
```

Note: Authenticated Spot websocket clients can also un/subscribe from/to public feeds.

---

<a name="futuresusage"></a>

# 📍 Futures Client Example Usage

Kraken provides a sandbox environment at https://demo-futures.kraken.com for paper trading. When using this API keys you have to set the `sandbox` parameter to `True` when instantiating the respective client.

A template Futures trading bot using both websocket and REST clients can be found in `/examples/futures_trading_bot_template.py`.

<a name="futuresrest"></a>

## Futures REST API

The following example can be found in `/examples/futures_examples.py`.

```python
from kraken.futures import Market, User, Trade, Funding

def main():

    key = "futures-api-key"
    secret = "futures-secret-key"

    # ____USER________________________
    user = User(key=key, secret=secret) # optional: sandbox=True
    print(user.get_wallets())
    print(user.get_open_orders())
    print(user.get_open_positions())
    print(user.get_subaccounts())
    # ...

    # ____MARKET_____
    market = Market()
    print(market.get_ohlc(tick_type="trade", symbol="PI_XBTUSD", resolution="5m"))

    priv_market = Market(key=key, secret=secret)
    print(priv_market.get_fee_schedules_vol())
    print(priv_market.get_execution_events())
    # ...

    # ____TRADE__________________________
    trade = Trade(key=key, secret=secret)
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
            "cliOrdId": "some-client-id"
        }, {
            "order": "send",
            "order_tag": "2",
            "orderType": "stp",
            "symbol": "PI_XBTUSD",
            "side": "buy",
            "size": 1,
            "limitPrice": 10000,
            "stopPrice": 11000,
        }, {
            "order": "cancel",
            "order_id": "e35dsdfsdfsddd-8a30-4d5f-a574-b5593esdf0",
        }, {
            "order": "cancel",
            "cliOrdId": "another-client-id",
        }],
    ))
    print(trade.cancel_all_orders())
    print(
        trade.create_order(
            orderType="lmt",
            side="buy",
            size=1,
            limitPrice=4,
            symbol="pf_bchusd"
        )
    )
    # ...

    # ____FUNDING___________________________
    funding = Funding(key=key, secret=secret)
    # ...

if __name__ == "__main__":
    main()
```

<a name="futuresws"></a>

## Futures Websocket Client

The following example can be found in `/examples/futures_ws_examples.py`.

```python
import asyncio
from kraken.futures import KrakenFuturesWSClient

async def main():

    key = "futures-api-key"
    secret = "futures-secret-key"

    # ___Custom_Trading_Bot__________
    class Bot(KrakenFuturesWSClient):

        async def on_message(self, event):
            print(event)
            # >> apply your trading strategy here <<
            # you can also combine this with the Futures REST clients

    # ___Public_Websocket_Feeds____:
    bot = Bot()
    # print(bot.get_available_public_subscription_feeds())

    products = ["PI_XBTUSD", "PF_ETHUSD"]

    # subscribe to a public websocket feed
    await bot.subscribe(feed="ticker", products=products)
    # await bot.subscribe(feed="book", products=products)
    # ...

    # unsubscribe from a public websocket feed
    # await bot.unsubscribe(feed="ticker", products=products)

    # ___Authenticated_Websocket_________
    auth_bot = Bot(key=key, secret=secret)
    # print(auth_bot.get_available_private_subscription_feeds())

    # subscribe to a private/authenticated websocket feed
    await auth_bot.subscribe(feed="fills")
    await auth_bot.subscribe(feed="open_positions")
    await auth_bot.subscribe(feed="open_orders")
    # ...

    # unsubscribe from a private/authenticaed websocket feed
    await auth_bot.unsubscribe(feed="fills")

    while True:
        await asyncio.sleep(6)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        loop.close()

```

Note: Authenticated Futures websocket clients can also un-/subscribe from/to public feeds.

---

<a name="contribution"></a>

# 🆕 Contributions

... are welcome! - Please have a look at [CONTRIBUTION.md](./CONTRIBUTING.md).

---

<a name="trouble"></a>

# 🚨 Troubleshooting

- Check if you downloaded and installed the **latest version** of the python-kraken-sdk.
- Check the **permissions of your API keys** and the required permissions on the respective endpoints.
- If you get some cloudflare or **rate limit errors**, please check your Kraken Tier level and maybe apply for a higher rank if required.
- **Use different API keys for different algorithms**, because the nonce calculation is based on timestamps and a sent nonce must always be the highest nonce ever sent of that API key. Having multiple algorithms using the same keys will result in invalid nonce errors.

---

<a name="notes"></a>

# 📝 Notes:

- Coding standards are not always followed to make arguments and function names as similar as possible to those in the Kraken API documentations.

<a name="references"></a>

# 🔭 References

- https://python-kraken-sdk.readthedocs.io/en/stable
- https://docs.kraken.com/rest
- https://docs.kraken.com/websockets
- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

---
