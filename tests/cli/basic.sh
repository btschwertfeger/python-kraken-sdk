#!/bin/bash
# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#
# Test basic CLI functionality

set -e

run_test() {
    local description="$1"
    shift
    if "$@" > /dev/null 2>&1; then
        echo "${description}:: SUCCESS"
    else
        echo "${description}:: FAILED"
        return 1
    fi
}

run_test "spot_public_full_url" kraken spot https://api.kraken.com/0/public/Time
run_test "spot_public_path_only" kraken spot /0/public/Time

run_test "spot_private_balance_full_url" kraken spot -X POST https://api.kraken.com/0/private/Balance
run_test "spot_private_balance_path_only" kraken spot -X POST /0/private/Balance

run_test "spot_private_trade_balance_with_data_full_url" kraken spot -X POST https://api.kraken.com/0/private/TradeBalance -d '{"asset": "DOT"}'
run_test "spot_private_trade_balance_with_data_path_only" kraken spot -X POST /0/private/TradeBalance -d '{"asset": "DOT"}'

run_test "futures_public_charts_full_url" kraken futures https://futures.kraken.com/api/charts/v1/spot/PI_XBTUSD/1d
run_test "futures_public_charts_path_only" kraken futures /api/charts/v1/spot/PI_XBTUSD/1d

run_test "futures_private_openpositions" kraken futures https://futures.kraken.com/derivatives/api/v3/openpositions
# run_test "futures_private_editorder" kraken futures -X POST https://futures.kraken.com/derivatives/api/v3/editorder -d '{"cliOrdID": "12345", "limitPrice": 10}'
