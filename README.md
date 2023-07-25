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
[![release](https://img.shields.io/pypi/v/python-kraken-sdk)](https://pypi.org/project/python-kraken-sdk/)
[![DOI](https://zenodo.org/badge/510751854.svg)](https://zenodo.org/badge/latestdoi/510751854)
[![Documentation Status stable](https://readthedocs.org/projects/python-kraken-sdk/badge/?version=stable)](https://python-kraken-sdk.readthedocs.io/en/stable)

</div>

> ⚠️ This is an unofficial collection of REST and websocket clients for Spot and
> Futures trading on the Kraken cryptocurrency exchange using Python. Payward
> Ltd. and Kraken are in no way associated with the authors of this module and
> documentation.

---

## 📌 Disclaimer

There is no guarantee that this software will work flawlessly at this or later
times. Of course, no responsibility is taken for possible profits or losses.
This software probably has some errors in it, so use it at your own risk. Also
no one should be motivated or tempted to invest assets in speculative forms of
investment. By using this software you release the authors from any liability
regarding the use of this software.

---

## Features

Clients:

- Spot REST Clients
- Spot Websocket Clients (Websocket API v1 and v2)
- Spot Orderbook Client
- Futures REST Clients
- Futures Websocket Client

General:

- access both public and private, REST and websocket endpoints
- responsive error handling and custom exceptions
- extensive example scripts (see `/examples` and `/tests`)
- tested using the [pytest](https://docs.pytest.org/en/7.3.x/) framework
- releases are permanently archived at [Zenodo](https://zenodo.org/badge/latestdoi/510751854)

Documentation:

- Stable: [https://python-kraken-sdk.readthedocs.io/en/stable](https://python-kraken-sdk.readthedocs.io/en/stable)
- Latest: [https://python-kraken-sdk.readthedocs.io/en/latest](https://python-kraken-sdk.readthedocs.io/en/latest)

---

## ❗️ Attention

**ONLY** tagged releases are available at PyPI. So the content of the master may
not match with the content of the latest release. - Please have a look at the
release specific READMEs and changelogs.

---

## Table of Contents

- [ Installation and setup ](#installation)
- [ Spot Clients Example Usage ](#spotusage)
  - [REST API](#spotrest)
  - [Websockets (V2)](#spotws)
- [ Futures Clients Example Usage ](#futuresusage)
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
- Futures Trading: https://futures.kraken.com/trade/settings/api (see _[help](https://docs.futures.kraken.com/#introduction-generate-api-keys)_)
- Futures Sandbox: https://demo-futures.kraken.com/settings/api

### 3. Start using the provided example scripts

### 4. Error handling

If any unexpected behavior occurs, please check <b style="color: yellow">your
API permissions</b>, <b style="color: yellow">rate limits</b>, update the
python-kraken-sdk, see the [Troubleshooting](#trouble) section, and if the error
persists please open an issue.

---

<a name="spotusage"></a>

# 📍 Spot Clients Example Usage

A template for Spot trading using both websocket and REST clients can be
found in `/examples/spot_trading_bot_template_v2.py`.

For those who need a realtime order book - a script that demonstrates how to
maintain a valid order book can be found here: `/examples/spot_orderbook.py`.

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

    # ____MARKET____
    market = Market()
    print(market.get_ticker(pair="BTCUSD"))
    # ...

    # ____TRADE_________________________
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
    print(funding.cancel_withdraw(asset="DOT", refid="<some id>"))
    # ...

    # ____STAKING___________________________
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

## Websockets (V2)

Kraken offers two versions of their websocket API (V1 and V2). Since V2 is
offers more possibilities, is way faster and easier to use, only those examples
are shown below. For using the websocket API V1 please have a look into the
`examples` directory.

The documentation for both API versions can be found here:

- https://docs.kraken.com/websockets
- https://docs.kraken.com/websockets-v2

Note that authenticated Spot websocket clients can also un-/subscribe from/to
public feeds.

The following example can be found in `/examples/spot_ws_examples_v2.py`.

```python
import asyncio
import os
from kraken.spot import KrakenSpotWSClientV2

async def main():
    key = os.getenv("SPOT_API_KEY")
    secret = os.getenv("SPOT_SECRET_KEY")

    class Client(KrakenSpotWSClientV2):
        """Can be used to create a custom trading strategy"""

        async def on_message(self, message):
            """Receives the websocket messages"""
            if message.get("method") == "pong" \
                or message.get("channel") == "heartbeat":
                return

            print(message)
            # here we can access lots of methods, for example to create an order:
            # if self._is_auth:  # only if the client is authenticated …
            #     await self.send_message(
            #         message={
            #             "method": "add_order",
            #             "params": {
            #                 "limit_price": 1234.56,
            #                 "order_type": "limit",
            #                 "order_userref": 123456789,
            #                 "order_qty": 1.0,
            #                 "side": "buy",
            #                 "symbol": "BTC/USD",
            #                 "validate": True,
            #             },
            #         }
            #     )
            # ... it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient.
            # You can also un-/subscribe here using self.subscribe/self.unsubscribe.

    # Public/unauthenticated websocket client
    client = Client()  # only use this one if you don't need private feeds
    # print(client.public_channel_names)  # list public subscription names

    await client.subscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]}
    )
    await client.subscribe(
        params={"channel": "book", "depth": 25, "symbol": ["BTC/USD"]}
    )
    await client.subscribe(params={"channel": "ohlc", "symbol": ["BTC/USD"]})
    await client.subscribe(
        params={
            "channel": "ohlc",
            "interval": 15,
            "snapshot": False,
            "symbol": ["BTC/USD", "DOT/USD"],
        }
    )
    await client.subscribe(params={"channel": "trade", "symbol": ["BTC/USD"]})

    # wait because unsubscribing is faster than unsubscribing ... (just for that example)
    await asyncio.sleep(3)
    # print(client.active_public_subscriptions) # … to list active subscriptions
    await client.unsubscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]}
    )
    # ...

    # Per default, the authenticated client starts two websocket connections,
    # one for authenticated and one for public messages. If there is no need
    # for a public connection, it can be disabled using the ``no_public``
    # parameter.
    client_auth = Client(key=key, secret=secret, no_public=True)
    # print(client_auth.private_channel_names)  # … list private channel names
    # when using the authenticated client, you can also subscribe to public feeds
    await client_auth.subscribe(params={"channel": "executions"})

    await asyncio.sleep(5)
    await client_auth.unsubscribe(params={"channel": "executions"})

    while not client.exception_occur and not client_auth.exception_occur:
        await asyncio.sleep(6)
    return


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
        # The websocket client will send {'event': 'asyncio.CancelledError'}
        # via on_message so you can handle the behavior/next actions
        # individually within your strategy.
```

---

<a name="futuresusage"></a>

# 📍 Futures Clients Example Usage

Kraken provides a sandbox environment at https://demo-futures.kraken.com for
paper trading. When using this API keys you have to set the `sandbox` parameter
to `True` when instantiating the respective client.

A template for Futures trading using both websocket and REST clients can be
found in `/examples/futures_trading_bot_template.py`.

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

    # ____MARKET____
    market = Market()
    print(market.get_ohlc(tick_type="trade", symbol="PI_XBTUSD", resolution="5m"))

    priv_market = Market(key=key, secret=secret)
    print(priv_market.get_fee_schedules_vol())
    print(priv_market.get_execution_events())
    # ...

    # ____TRADE_________________________
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

    # ___Custom_Trading_Client________
    class Client(KrakenFuturesWSClient):

        async def on_message(self, event):
            print(event)
            # >> apply your trading strategy here <<
            # you can also combine this with the Futures REST clients

    # ___Public_Websocket_Feeds____
    client = Client()
    # print(client.get_available_public_subscription_feeds())

    products = ["PI_XBTUSD", "PF_ETHUSD"]

    # subscribe to a public websocket feed
    await client.subscribe(feed="ticker", products=products)
    # await client.subscribe(feed="book", products=products)
    # ...

    # unsubscribe from a public websocket feed
    # await client.unsubscribe(feed="ticker", products=products)

    # ___Authenticated_Websocket_________
    client_auth = Client(key=key, secret=secret)
    # print(client_auth.get_available_private_subscription_feeds())

    # subscribe to a private/authenticated websocket feed
    await client_auth.subscribe(feed="fills")
    await client_auth.subscribe(feed="open_positions")
    await client_auth.subscribe(feed="open_orders")
    # ...

    # unsubscribe from a private/authenticated websocket feed
    await client_auth.unsubscribe(feed="fills")

    while True:
        await asyncio.sleep(6)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # do some exception handling ...
        pass
```

Note: Authenticated Futures websocket clients can also un-/subscribe from/to public feeds.

---

<a name="contribution"></a>

# 🆕 Contributions

… are welcome! - Please have a look at [CONTRIBUTION.md](./CONTRIBUTING.md).

---

<a name="trouble"></a>

# 🚨 Troubleshooting

- Check if you downloaded and installed the **latest version** of the python-kraken-sdk.
- Check the **permissions of your API keys** and the required permissions on the respective endpoints.
- If you get some Cloudflare or **rate limit errors**, please check your Kraken Tier level and maybe apply for a higher rank if required.
- **Use different API keys for different algorithms**, because the nonce calculation is based on timestamps and a sent nonce must always be the highest nonce ever sent of that API key. Having multiple algorithms using the same keys will result in invalid nonce errors.

---

<a name="notes"></a>

# 📝 Notes

- The version scheme is `<Major>.<Minor>.<Service Level>` where:

  - **Major** will affect everything and there will be breaking changes
    in any case. This could be for example a change to Python 3.11+ only.

  - **Minor** introduces features and enhancements which may bring breaking
    changes in some cases. These breaking changes could be renaming or
    addition of parameters, change in order of parameters or even renaming
    a function.
  - **Service Level** includes bug fixes, documentation or CI related changes.

- Coding standards are not always followed to make arguments and function names
  as similar as possible to those of the Kraken API documentations.

<a name="references"></a>

# 🔭 References

- https://python-kraken-sdk.readthedocs.io/en/stable
- https://docs.kraken.com/rest
- https://docs.kraken.com/websockets
- https://docs.kraken.com/websockets-v2
- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

---
