.. -*- mode: rst; coding: utf-8 -*-
..
.. Copyright (C) 2024 Benjamin Thomas Schwertfeger
.. All rights reserved.
.. https://github.com/btschwertfeger
..

.. _section-command-line-interface-examples:

Command-line Interface
----------------------

The python-kraken-sdk provides a command-line interface to access the Kraken API
using basic instructions while performing authentication tasks in the
background. The Spot and Futures APIs are accessible and follow the pattern
``kraken {spot,futures} [OPTIONS] URL``. All endpoints of the Kraken Spot and
Futurs API can be accessed like that. See examples below.

.. code-block:: bash
    :linenos:
    :caption: Command-line Interface Examples

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

.. click:: kraken.cli:cli
   :prog: kraken
   :nested: full
