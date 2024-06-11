<h1 align="center">Futures, Spot and NFT - REST and Websocket API Python SDK for the Kraken Cryptocurrency Exchange 🐙</h1>

<div align="center">

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/btschwertfeger/python-kraken-sdk)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Generic badge](https://img.shields.io/badge/python-3.11+-blue.svg)](https://shields.io/)
[![Downloads](https://static.pepy.tech/personalized-badge/python-kraken-sdk?period=total&units=abbreviation&left_color=grey&right_color=orange&left_text=downloads)](https://pepy.tech/project/python-kraken-sdk)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typing](https://img.shields.io/badge/typing-mypy-informational)](https://mypy-lang.org/)
[![CI/CD](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/cicd.yaml/badge.svg?branch=master)](https://github.com/btschwertfeger/python-kraken-sdk/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/btschwertfeger/python-kraken-sdk/branch/master/badge.svg)](https://app.codecov.io/gh/btschwertfeger/python-kraken-sdk)

[![OpenSSF ScoreCard](https://img.shields.io/ossf-scorecard/github.com/btschwertfeger/python-kraken-sdk?label=openssf%20scorecard&style=flat)](https://securityscorecards.dev/viewer/?uri=github.com/btschwertfeger/python-kraken-sdk)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8673/badge)](https://www.bestpractices.dev/projects/8673)

[![release](https://shields.io/github/release-date/btschwertfeger/python-kraken-sdk)](https://github.com/btschwertfeger/python-kraken-sdk/releases)
[![release](https://img.shields.io/pypi/v/python-kraken-sdk)](https://pypi.org/project/python-kraken-sdk/)
[![DOI](https://zenodo.org/badge/510751854.svg)](https://zenodo.org/badge/latestdoi/510751854)
[![Documentation Status Stable](https://readthedocs.org/projects/python-kraken-sdk/badge/?version=stable)](https://python-kraken-sdk.readthedocs.io/en/stable)

</div>

> ⚠️ This is an unofficial collection of REST and websocket clients for Spot and
> Futures trading on the Kraken cryptocurrency exchange using Python. Payward
> Ltd. and Kraken are in no way associated with the authors of this package and
> documentation.
>
> Please note that this project is independent and not endorsed by Kraken or
> Payward Ltd. Users should be aware that they are using third-party software,
> and the authors of this project are not responsible for any issues, losses, or
> risks associated with its usage.

## 📌 Disclaimer

There is no guarantee that this software will work flawlessly at this or later
times. Of course, no responsibility is taken for possible profits or losses.
This software probably has some errors in it, so use it at your own risk. Also
no one should be motivated or tempted to invest assets in speculative forms of
investment. By using this software you release the author(s) from any liability
regarding the use of this software.

---

## Features

General:

- command-line interface
- access both public and private, REST and websocket endpoints
- responsive error handling and custom exceptions
- extensive example scripts (see `/examples` and `/tests`)
- tested using the [pytest](https://docs.pytest.org/en/7.3.x/) framework
- releases are permanently archived at [Zenodo](https://zenodo.org/badge/latestdoi/510751854)

Available Clients:

- Spot REST Clients (sync and async; including access to NFT trading)
- Spot Websocket Clients (Websocket API v1 and v2)
- Spot Orderbook Clients (Websocket API v1 and v2)
- Futures REST Clients (sync and async)
- Futures Websocket Client

Documentation:

- [https://python-kraken-sdk.readthedocs.io/en/stable](https://python-kraken-sdk.readthedocs.io/en/stable)
- [https://python-kraken-sdk.readthedocs.io/en/latest](https://python-kraken-sdk.readthedocs.io/en/latest)

---

## ❗️ Attention

**ONLY** tagged releases are available at PyPI. So the content of the master may
not match with the content of the latest release. - Please have a look at the
release specific READMEs and changelogs.

It is also recommended to _pin the used version_ to avoid unexpected behavior on
new releases.

**Changes since v3.0.0**: The tool aims to be fast, easy to use and maintain. In
the past, lots of clients were implemented, that provided functions for "all"
available endpoints of the Kraken API. The effort to maintain this collection
grew to a level where it was not possible to check various changelogs to apply
new updates on a regular basis. **Instead, it was decided to concentrate on the
`request` functions of the `SpotClient`, `SpotAsyncClient`, `FuturesClient` and
the `FuturesAsyncClient` (as well as their websocket client implementations).
All those clients named "User", "Trade", "Market", "Funding" and so on will no
longer be extended, but maintained to a certain degree.**

---

## Table of Contents

- [ Installation and setup ](#installation)
- [ Command-line interface ](#cliusage)
- [ Spot Clients ](#spotusage)
  - [REST API](#spotrest)
  - [Websocket API V2](#spotws)
- [ Futures Clients ](#futuresusage)
  - [REST API](#futuresrest)
  - [Websocket API](#futuresws)
- [ Troubleshooting ](#trouble)
- [ Contributions ](#contribution)
- [ Notes ](#notes)
- [ References ](#references)

<a name="installation"></a>

# 🛠 Installation and setup

### 1. Install the package into the desired environment

```bash
python3 -m pip install python-kraken-sdk
```

### 2. Register at [Kraken](https://www.kraken.com) and generate API keys

- Spot Trading: https://www.kraken.com/u/security/api
- Futures Trading: https://futures.kraken.com/trade/settings/api (see _[help](https://docs.futures.kraken.com/#introduction-generate-api-keys)_)
- Futures Sandbox: https://demo-futures.kraken.com/settings/api

### 3. Start using the provided example scripts

### 4. Error handling

If any unexpected behavior occurs, please check <b style="color: yellow">your
API permissions</b>, <b style="color: yellow">rate limits</b>, update the
python-kraken-sdk, see the [Troubleshooting](#trouble) section, and if the error
persists please open an issue.

<a name="cliusage"></a>

# 📍 Command-line interface

The python-kraken-sdk provides a command-line interface to access the Kraken API
using basic instructions while performing authentication tasks in the
background. The Spot, NFT and Futures API are accessible and follow the pattern
`kraken {spot,futures} [OPTIONS] URL`. See examples below.

```bash
# get server time
kraken spot https://api.kraken.com/0/public/Time
{'unixtime': 1716707589, 'rfc1123': 'Sun, 26 May 24 07:13:09 +0000'}

# get user's balances
kraken spot --api-key=<api-key> --secret-key=<secret-key> -X POST https://api.kraken.com/0/private/Balance
{'ATOM': '17.28229999', 'BCH': '0.0000077100', 'ZUSD': '1000.0000'}

# get user's trade balances
kraken spot --api-key=<api-key> --secret-key=<secret-key> -X POST https://api.kraken.com/0/private/TradeBalance --data '{"asset": "DOT"}'
{'eb': '2.8987347115', 'tb': '1.1694303513', 'm': '0.0000000000', 'uv': '0', 'n': '0.0000000000', 'c': '0.0000000000', 'v': '0.0000000000', 'e': '1.1694303513', 'mf': '1.1694303513'}

# get 1D candles for a futures instrument
kraken futures https://futures.kraken.com/api/charts/v1/spot/PI_XBTUSD/1d
{'candles': [{'time': 1625616000000, 'open': '34557.84000000000', 'high': '34803.20000000000', 'low': '33816.32000000000', 'close': '33880.22000000000', 'volume': '0' ...

# get user's open futures positions
kraken futures --api-key=<api-key> --secret-key=<secret-key> https://futures.kraken.com/derivatives/api/v3/openpositions
{'result': 'success', 'openPositions': [], 'serverTime': '2024-05-26T07:15:38.91Z'}
```

... All endpoints of the Kraken Spot and Futurs API can be accessed like that.

<a name="spotusage"></a>

# 📍 Spot Clients

The python-kraken-sdk provides lots of functions to easily access most of the
REST and websocket endpoints of the Kraken Cryptocurrency Exchange API. Since
these endpoints and their parameters may change, all implemented endpoints are
tested on a regular basis.

The Kraken Spot API can be accessed by executing requests to the endpoints
directly using the `request` method provided by any client. This is demonstrated
below.

### `SpotClient`

```python
from kraken.spot import SpotClient

client = SpotClient(key="<your-api-key>", secret="<your-secret-key>")
print(client.request("POST", "/0/private/Balance"))
```

### `SpotAsyncClient`

```python
import asyncio
from kraken.spot import SpotAsyncClient

async def main():
    client = SpotAsyncClient(key="<your-api-key>", secret="<your-secret-key>")
    try:
        response = await client.request("POST", "/0/private/Balance")
        print(response)
    finally:
        await client.async_close()

asyncio.run(main())
```

```python
import asyncio
from kraken.spot import SpotAsyncClient

async def main():
    async with SpotAsyncClient(key="<your-api-key>", secret="<your-secret-key>")as client:
        response = await client.request("POST", "/0/private/Balance")
        print(response)

asyncio.run(main())
```

<a name="spotws"></a>

### Spot Websocket API V2

Kraken offers two versions of their websocket API (V1 and V2). Since V2 is
offers more possibilities, is way faster and easier to use, only those examples
are shown below. For using the websocket API V1 please have a look into the
`examples/spot_ws_examples_v1.py`.

The documentation for both API versions can be found here:

- https://docs.kraken.com/websockets
- https://docs.kraken.com/websockets-v2

Note that authenticated Spot websocket clients can also un-/subscribe from/to
public feeds.

The example below can be found in an extended way in
`examples/spot_ws_examples_v2.py`.

```python
import asyncio
from kraken.spot import SpotWSClientV2


async def main():
    class Client(SpotWSClientV2):
        """Can be used to create a custom trading strategy"""

        async def on_message(self, message):
            """Receives the websocket messages"""
            if message.get("method") == "pong" \
                or message.get("channel") == "heartbeat":
                return

            print(message)
            # Here we can access lots of methods, for example to create an order:
            # if self.is_auth:  # only if the client is authenticated …
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
            # … it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient.
            # You can also un-/subscribe here using self.subscribe/self.unsubscribe.

    # Public/unauthenticated websocket client
    client = Client()  # only use this one if you don't need private feeds

    await client.subscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]}
    )
    await client.subscribe(
        params={"channel": "book", "depth": 25, "symbol": ["BTC/USD"]}
    )
    # wait because unsubscribing is faster than unsubscribing … (just for that example)
    await asyncio.sleep(3)
    # print(client.active_public_subscriptions) # to list active subscriptions
    await client.unsubscribe(
        params={"channel": "ticker", "symbol": ["BTC/USD", "DOT/USD"]}
    )
    # …

    # Per default, the authenticated client starts two websocket connections,
    # one for authenticated and one for public messages. If there is no need
    # for a public connection, it can be disabled using the ``no_public``
    # parameter.
    client_auth = Client(key="api-key", secret="secret-key", no_public=True)
    await client_auth.subscribe(params={"channel": "balances"})

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

<a name="futuresusage"></a>

# Futures Clients

The Kraken Spot API can be accessed by executing requests to the endpoints
directly using the `request` method provided by any client. This is demonstrated
below.

### `FuturesClient`

```python
from kraken.futures import FuturesClient

client = FuturesClient(key="<your-api-key>", secret="<your-secret-key>")
print(client.request("GET", "/derivatives/api/v3/accounts"))
```

### `FuturesAsyncClient`

```python
import asyncio
from kraken.futures import FuturesAsyncClient

async def main():
    client = FuturesAsyncClient(key="<your-api-key>", secret="<your-secret-key>")
    try:
        response = await client.request("GET", "/derivatives/api/v3/accounts")
        print(response)
    finally:
        await client.async_close()

asyncio.run(main())
```

```python
import asyncio
from kraken.futures import FuturesAsyncClient


async def main():
    async with FuturesAsyncClient(key="<your-api-key>", secret="<your-secret-key>") as client:
        response = await client.request("GET", "/derivatives/api/v3/accounts")
        print(response)

asyncio.run(main())
```

<a name="futuresws"></a>

### Futures Websocket API

Not only REST, also the websocket API for Kraken Futures is available. Examples
are shown below and demonstrated in `examples/futures_ws_examples.py`.

- https://docs.futures.kraken.com/#websocket-api

Note: Authenticated Futures websocket clients can also un-/subscribe from/to
public feeds.

```python
import asyncio
from kraken.futures import FuturesWSClient

async def main():
    class Client(FuturesWSClient):

        async def on_message(self, event):
            print(event)

    # Public/unauthenticated websocket connection
    client = Client()

    products = ["PI_XBTUSD", "PF_ETHUSD"]

    # subscribe to a public websocket feed
    await client.subscribe(feed="ticker", products=products)
    # await client.subscribe(feed="book", products=products)
    # …

    # unsubscribe from a public websocket feed
    # await client.unsubscribe(feed="ticker", products=products)

    # Private/authenticated websocket connection (+public)
    client_auth = Client(key="key-key", secret="secret-key")
    # print(client_auth.get_available_private_subscription_feeds())

    # subscribe to a private/authenticated websocket feed
    await client_auth.subscribe(feed="fills")
    await client_auth.subscribe(feed="open_positions")
    await client_auth.subscribe(feed="open_orders")
    # …

    # unsubscribe from a private/authenticated websocket feed
    await client_auth.unsubscribe(feed="fills")

    while True:
        await asyncio.sleep(6)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # do some exception handling …
        pass
```

---

<a name="contribution"></a>

# 🆕 Contributions

… are welcome - but:

- First check if there is an existing issue or PR that addresses your
  problem/solution. If not - create one first - before creating a PR.
- Typo fixes, project configuration, CI, documentation or style/formatting PRs
  will be rejected. Please create an issue for that.
- PRs must provide a reasonable, easy to understand and maintain solution for an
  existing problem. You may want to propose a solution when creating the issue
  to discuss the approach before creating a PR.
- Please have a look at [CONTRIBUTION.md](./CONTRIBUTING.md).

---

<a name="trouble"></a>

# 🚨 Troubleshooting

- Check if you downloaded and installed the **latest version** of the
  python-kraken-sdk.
- Check the **permissions of your API keys** and the required permissions on the
  respective endpoints.
- If you get some Cloudflare or **rate limit errors**, please check your Kraken
  Tier level and maybe apply for a higher rank if required.
- **Use different API keys for different algorithms**, because the nonce
  calculation is based on timestamps and a sent nonce must always be the highest
  nonce ever sent of that API key. Having multiple algorithms using the same
  keys will result in invalid nonce errors.

---

<a name="notes"></a>

# 📝 Notes

The versioning scheme follows the pattern `v<Major>.<Minor>.<Patch>`. Here's what each part signifies:

- **Major**: This denotes significant changes that may introduce new features or
  modify existing ones. It's possible for these changes to be breaking, meaning
  backward compatibility is not guaranteed. To avoid unexpected behavior, it's
  advisable to specify at least the major version when pinning dependencies.
- **Minor**: This level indicates additions of new features or extensions to
  existing ones. Typically, these changes do not break existing implementations.
- **Patch**: Here, you'll find bug fixes, documentation updates, and changes
  related to continuous integration (CI). These updates are intended to enhance
  stability and reliability without altering existing functionality.

Coding standards are not always followed to make arguments and function names as
similar as possible to those of the Kraken API documentations.

<a name="references"></a>

# 🔭 References

- https://python-kraken-sdk.readthedocs.io/en/stable
- https://docs.kraken.com/rest
- https://docs.kraken.com/websockets
- https://docs.kraken.com/websockets-v2
- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API

---
