#!/bin/bash

kraken spot https://api.kraken.com/0/public/Time
kraken spot /0/public/Time

kraken spot -X POST https://api.kraken.com/0/private/Balance
kraken spot -X POST https://api.kraken.com/0/private/TradeBalance -d '{"asset": "DOT"}'

kraken futures https://futures.kraken.com/api/charts/v1/spot/PI_XBTUSD/1d
kraken futures /api/charts/v1/spot/PI_XBTUSD/1d

kraken futures https://futures.kraken.com/derivatives/api/v3/openpositions
# kraken futures -X POST https://futures.kraken.com/derivatives/api/v3/editorder -d '{"cliOrdID": "12345", "limitPrice": 10}'
