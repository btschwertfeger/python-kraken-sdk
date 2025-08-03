# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Module that implements the Kraken Spot Market client"""

from __future__ import annotations

from functools import lru_cache
from typing import Self

from kraken.base_api import SpotClient, defined, ensure_string


class Market(SpotClient):
    """
    Class that implements the Kraken Spot Market client. Can be used to access
    the Kraken Spot market data.

    :param key:  Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Kraken API (default:
        https://api.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional

    .. code-block:: python
        :linenos:
        :caption: Spot Market: Create the market client

        >>> from kraken.spot import Market
        >>> market = Market() # unauthenticated
        >>> auth_market = Market(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Spot Market: Create the market client as context manager

        >>> from kraken.spot import Market
        >>> with Market() as market:
        ...     print(market.get_assets())
    """

    def __init__(  # nosec: B107
        self: Market,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, proxy=proxy)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    @ensure_string("assets")
    @ensure_string("extra_params")
    @lru_cache
    def get_assets(
        self: Market,
        assets: str | list[str] | None = None,
        aclass: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about one or more assets. If ``assets`` is not
        specified, all assets will be returned.

        - https://docs.kraken.com/api/docs/rest-api/get-asset-info

        This function uses caching. Run ``get_assets.cache_clear()`` to clear.

        :param assets: Filter by asset(s)
        :type assets: str | list[str], optional
        :param aclass: Filter by asset class
        :type aclass: str, optional
        :return: Information about the requested assets
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get information about the available assets

            >>> from kraken.spot import Market
            >>> market = Market()
            >>> market.get_assets(assets="DOT")
            {
                'DOT': {
                    'aclass': 'currency',
                    'altname': 'DOT',
                    'decimals': 10,
                    'display_decimals': 8,
                    'collateral_value': 0.9,
                    'status': 'enabled'
                }
            }
            >>> market.get_assets(assets=["MATIC", "XBT"]) # same as market.get_assets(assets="MATIC,XBT"])
                'MATIC': {
                    'aclass': 'currency',
                    'altname': 'MATIC',
                    'decimals': 10,
                    'display_decimals': 5,
                    'collateral_value': 0.7,
                    'status': 'enabled'
                },
                'XXBT': {
                    'aclass': 'currency',
                    'altname': 'XBT',
                    'decimals': 10,
                    'display_decimals': 5,
                    'collateral_value': 1.0,
                    'status': 'enabled'
                }
            }
        """
        params: dict = {}
        if defined(assets):
            params["asset"] = assets
        if defined(aclass):
            params["aclass"] = aclass
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Assets",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    @ensure_string("pair")
    @ensure_string("extra_params")
    @lru_cache
    def get_asset_pairs(
        self: Market,
        pair: str | list[str] | None = None,
        info: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about a single or multiple asset/currency pair(s). If
        ``pair`` is left blank, all currency pairs will be returned.

        - https://docs.kraken.com/api/docs/rest-api/get-tradable-asset-pairs

        This function uses caching. Run ``get_asset_pairs.cache_clear()`` to
        clear.

        :param pair: Filter by asset pair(s)
        :type pair: str | list[str], optional
        :param info: Filter by info, can be one of: ``info`` (all info),
            ``leverage`` (leverage info), ``fees`` (fee info), and ``margin``
            (margin info)
        :type info: str, optional
        :return: Information about the asset pair
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get information about tradeable asset pairs

            >>> from kraken.spot import Market
            >>> Market().get_asset_pairs(pair="XBTUSD")
            {
                'XXBTZUSD': {
                    'altname': 'XBTUSD',
                    'wsname': 'XBT/USD',
                    'aclass_base': 'currency',
                    'base': 'XXBT',
                    'aclass_quote': 'currency',
                    'quote': 'ZUSD',
                    'lot': 'unit',
                    'cost_decimals': 5,
                    'pair_decimals': 1,
                    'lot_decimals': 8,
                    'lot_multiplier': 1,
                    'leverage_buy': [2, 3, 4, 5],
                    'leverage_sell': [2, 3, 4, 5],
                    'fees': [
                        [0, 0.26], [50000, 0.24], [100000, 0.22],
                        [250000, 0.2], [500000, 0.18], [1000000, 0.16],
                        [2500000, 0.14], [5000000, 0.12], [10000000, 0.1]
                    ],
                    'fees_maker': [
                        [0, 0.16], [50000, 0.14], [100000, 0.12],
                        [250000, 0.1], [500000, 0.08], [1000000, 0.06],
                        [2500000, 0.04], [5000000, 0.02], [10000000, 0.0]
                    ],
                    'fee_volume_currency': 'ZUSD',
                    'margin_call': 80,
                    'margin_stop': 40,
                    'ordermin': '0.0001',
                    'costmin': '0.5',
                    'tick_size': '0.1',
                    'status': 'online',
                    'long_position_limit': 270,
                    'short_position_limit': 180
                }
            }
        """
        params: dict = {}
        if defined(pair):
            params["pair"] = pair
        if defined(info):
            params["info"] = info
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/AssetPairs",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    @ensure_string("pair")
    def get_ticker(
        self: Market,
        pair: str | list[str] | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Returns all tickers if pair is not specified - else just the ticker of
        the ``pair``. Multiple pairs can be specified.

        - https://docs.kraken.com/api/docs/rest-api/get-ticker-information

        :param pair: Filter by pair(s)
        :type pair: str | list[str], optional
        :return: The ticker(s) including ask, bid, close, volume, vwap, high,
            low, todays open and more
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the ticker(s)

            >>> from kraken.spot import Market
            >>> Market().get_ticker(pair="XBTUSD")
            {
                'XXBTZUSD': {
                    'a': ['27948.00000', '3', '3.000'],      # ask
                    'b': ['27947.90000', '1', '1.000'],      # bid
                    'c': ['27947.90000', '0.00842808'],      # last trade close, lot volume
                    'v': ['3564.58017484', '4138.93906134'], # volume today and last 24h
                    'p': ['28351.31431', '28329.55480'],     # vwap today and last 24h
                    't': [33574, 43062],                     # number of trades today and last 24h
                    'l': ['27813.10000', '27813.10000'],     # low today and last 24h
                    'h': ['28792.30000', '28792.30000'],     # high today and last 24
                    'o': '28173.00000'                       # today's opening price
                }
            }
        """
        params: dict = {}
        if defined(pair):
            params["pair"] = pair
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Ticker",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_ohlc(
        self: Market,
        pair: str,
        interval: int | str = 1,
        since: int | str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the open, high, low, and close data for a specific trading pair.
        Returns at max 720 time steps per request.

        - https://docs.kraken.com/api/docs/rest-api/get-ohlc-data

        :param pair: The pair to get the ohlc from
        :type pair: str
        :param interval: the Interval in minutes (default: ``1``)
        :type interval: str | int, optional
        :param since: Timestamp to start from (default: ``None``)
        :type since: int | str, optional
        :return: The OHLC data of a given asset pair
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the OHLC data

            >>> from kraken.spot import Market
            >>> Market().get_ohlc(pair="XBTUSD")
            {
                "XXBTZUSD": [
                    [
                        1680671100,
                        "28488.9",
                        "28489.0",
                        "28488.8",
                        "28489.0",
                        "28488.9",
                        "1.03390376",
                        8
                    ], ...
                ]
            }
        """
        params: dict = {"pair": pair, "interval": interval}
        if defined(since):
            params["since"] = since
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/OHLC",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_order_book(
        self: Market,
        pair: str,
        count: int | None = 100,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the current orderbook of a specified trading pair.

        - https://docs.kraken.com/api/docs/rest-api/get-order-book

        :param pair: The pair to get the orderbook from
        :type pair: str
        :param count: Number of asks and bids, must be one of {1..500} (default:
            ``100``)
        :type count: int, optional

        :return:
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the orderbook

            >>> from kraken.spot import Market
            >>> Market().get_order_book(pair="XBTUSD", count=2)
            {
                'XXBTZUSD': {
                    'asks': [
                        ['28000.00000', '1.091', 1680714417],
                        ['28001.00000', '0.001', 1680714413]
                    ],
                    'bids': [
                        ['27999.90000', '2.240', 1680714419],
                        ['27999.50000', '0.090', 1680714418]
                    ]
                }
            }
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Depth",
            params={"pair": pair, "count": count},
            auth=False,
            extra_params=extra_params,
        )

    def get_recent_trades(
        self: Market,
        pair: str,
        since: str | int | None = None,
        count: int | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the latest trades for a specific trading pair (up to 1000).

        - https://docs.kraken.com/api/docs/rest-api/get-recent-trades

        :param pair: Pair to get the recent trades
        :type pair: str
        :param since: Filter trades since given timestamp (default: ``None``)
        :type since: str | int, optional
        :param count: The max number of results
        :type count: int, optional
        :return: The last public trades (up to 1000 results)
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the recent trades

            >>> from kraken.spot import Market
            >>> Market().get_recent_trades(pair="XBTUSD")
            {
                "XXBTZUSD": [
                    ["27980.90000", "0.00071054", 1680712703.2524643, "b", "l", "", 57811127],
                    ["27981.00000", "0.03180000", 1680712715.1806278, "b", "l", "", 57811128],
                    ["27980.90000", "0.00010000", 1680712715.469506, "s", "m", "", 57811129],
                    ...
                ]
            }

        """
        params: dict = {"pair": pair}
        if defined(since):
            params["since"] = since
        if defined(count):
            params["count"] = count
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Trades",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_recent_spreads(
        self: Market,
        pair: str,
        since: str | int | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the latest spreads for a specific trading pair.

        - https://docs.kraken.com/api/docs/rest-api/get-recent-spreads

        :param pair: Pair to get the recent spreads
        :type pair: str
        :param since: Filter trades since given timestamp (default: ``None``)
        :type since: str | int, optional
        :return: The last *n* spreads of the asset pair
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the recent spreads

            >>> from kraken.spot import Market
            >>> Market().get_recent_spreads(pair="XBTUSD")
            {
                "XXBTZUSD": [
                    [1680714601, "28015.00000", "28019.40000"],
                    [1680714601, "28015.00000", "28017.00000"],
                    [1680714601, "28015.00000", "28016.90000"],
                    ...
                ]
            }
        """
        params: dict = {"pair": pair}
        if defined(since):
            params["since"] = since
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Spread",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_system_status(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Returns the system status of the Kraken Spot API.

        - https://docs.kraken.com/api/docs/rest-api/get-system-status

        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the Kraken API system status

            >>> from kraken.spot import Market
            >>> Market().get_system_status()
            {'status': 'online', 'timestamp': '2023-04-05T17:12:31Z'}
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/SystemStatus",
            auth=False,
            extra_params=extra_params,
        )


__all__ = ["Market"]
