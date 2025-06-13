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
# ruff: noqa:PLR0904

"""Module that implements the Kraken Futures market client"""

from __future__ import annotations

from functools import lru_cache
from typing import TypeVar

from kraken.base_api import FuturesClient, defined, ensure_string

Self = TypeVar("Self")


class Market(FuturesClient):
    """
    Class that implements the Kraken Futures market client

    If the sandbox environment is chosen, the keys must be generated from here:
    https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str, optional
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Futures Kraken API (default:
        https://futures.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional
    :param sandbox: If set to ``True`` the URL will be
        https://demo-futures.kraken.com (default: ``False``)
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Futures Market: Create the market client

        >>> from kraken.futures import Market
        >>> market = Market() # unauthenticated
        >>> market = Market(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Futures Market: Create the market client as context manager

        >>> from kraken.futures import Market
        >>> with Market() as market:
        ...     print(market.get_tick_types())
    """

    def __init__(  # nosec: B107
        self: Market,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
        *,
        sandbox: bool = False,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, proxy=proxy, sandbox=sandbox)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def get_ohlc(
        self: Market,
        tick_type: str,
        symbol: str,
        resolution: int,
        from_: int | None = None,
        to: int | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve the open, high, low, and close data for a specific symbol and
        resolution. It is also possible to filter by time.

        - https://docs.kraken.com/api/docs/futures-api/charts/candles

        :param tick_type: The kind of data, based on ``mark``, ``spot``, or
            ``trade``
        :type tick_type: str
        :param symbol: The asset pair to get the ohlc from
        :type symbol: str
        :param resolution: The tick resolution, one of ``1m``. ``5m``, ``15m``,
            ``1h``, ``4h``, ``12h``, ``1d``, ``1w``
        :type resolution: str
        :param from_: From date in epoch seconds
        :type from_: int, optional
        :param to: To date in epoch seconds (inclusive)
        :type to: int, optional
        :return: The current OHLC data for a specific asset pair
        :rtype: dict


        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the OHLC data

            >>> from kraken.futures import Market
            >>> Market().get_ohlc(tick_type="trade", symbol="PI_XBTUSD", resolution="1h")
            {
                'candles': [
                    {
                        'time': 1680624000000,
                        'open': '28050.0',
                        'high': '28150',
                        'low': '27983.0',
                        'close': '28126.0',
                        'volume': '1089794.00000000'
                    }
                ],
                'more_candles': True
            }
        """
        tick_types: tuple = ("spot", "mark", "trade")
        resolutions: tuple = ("1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d", "1w")
        if tick_type not in tick_types:
            raise ValueError(f"tick_type must be in {tick_types}")
        if resolution is not None and resolution not in resolutions:
            raise ValueError(f"resolution must be in {resolutions}")

        params: dict = {}
        if defined(from_):
            params["from"] = from_
        if defined(to):
            params["to"] = to
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri=f"/api/charts/v1/{tick_type}/{symbol}/{resolution}",
            query_params=params,
            auth=False,
            extra_params=extra_params,
        )

    @ensure_string("extra_params")
    @lru_cache
    def get_tick_types(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> list[str]:
        """
        Retrieve the available tick types that can be used for example to access
        the :func:`kraken.futures.Market.get_ohlc` endpoint.

        - https://docs.kraken.com/api/docs/futures-api/charts/tick-types

        This function uses caching. Run ``get_tick_types.cache_clear()`` to
        clear.

        :return: List of available tick types
        :rtype: list[str]

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the available tick types

            >>> from kraken.futures import Market
            >>> Market().get_tick_types()
            ['mark', 'spot', 'trade']
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/api/charts/v1/",
            auth=False,
            extra_params=extra_params,
        )

    @ensure_string("extra_params")
    @lru_cache
    def get_tradeable_products(
        self: Market,
        tick_type: str,
        *,
        extra_params: dict | None = None,
    ) -> list[str]:
        """
        Retrieve a list containing the tradeable assets on the futures market.

        - https://docs.kraken.com/api/docs/futures-api/charts/symbols

        This function uses caching. Run ``get_tradeable_products.cache_clear()``
        to clear.

        :param tick_type: The kind of data, based on ``mark``, ``spot``, or
            ``trade``
        :type tick_type: str
        :return: List of tradeable assets
        :type: list[str]

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the tradeable products

            >>> from kraken.futures import Market
            >>> Market().get_tradeable_products(tick_type="trade")
            ["PI_XBTUSD", "PF_XBTUSD", "PF_SOLUSD", ...]
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri=f"/api/charts/v1/{tick_type}",
            auth=False,
            extra_params=extra_params,
        )

    @ensure_string("extra_params")
    @lru_cache
    def get_resolutions(
        self: Market,
        tick_type: str,
        tradeable: str,
        *,
        extra_params: dict | None = None,
    ) -> list[str]:
        """
        Retrieve the list of available resolutions for a specific asset.

        - https://docs.kraken.com/api/docs/futures-api/charts/resolutions

        This function uses caching. Run ``get_resolutions.cache_clear()`` to
        clear.

        :param tick_type: The kind of data, based on ``mark``, ``spot``, or
            ``trade``
        :type tick_type: str
        :param tick_type: The asset of interest
        :type tick_type: str
        :return: List of resolutions
        :type: list[str]

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the available resolutions

            >>> from kraken.futures import Market
            >>> Market().get_resolutions(tick_type="mark", tradeable="PI_XBTUSD")
            ['1h', '12h', '1w', '15m', '1d', '5m', '30m', '4h', '1m']
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri=f"/api/charts/v1/{tick_type}/{tradeable}",
            auth=False,
            extra_params=extra_params,
        )

    @ensure_string("extra_params")
    @lru_cache
    def get_fee_schedules(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about the current fees

        - https://docs.kraken.com/api/docs/futures-api/trading/get-fee-schedules-v-3

        - https://www.kraken.com/features/fee-schedule

        This function uses caching. Run ``get_fee_schedules.cache_clear()`` to
        clear.

        :return: Dictionary containing information about the fees for wide range
            of tradeable assets
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the available fee schedules

            >>> from kraken.futures import Market
            >>> Market().get_fee_schedules()
            {
                'feeSchedules': [{
                    'uid': '5b755fea-c5b0-4307-a66e-b392cd5bd931',
                    'name': 'KF USD Multi-Collateral Fees',
                    'tiers': [
                        {'makerFee': 0.02, 'takerFee': 0.05, 'usdVolume': 0.0},
                        {'makerFee': 0.015, 'takerFee': 0.04, 'usdVolume': 100000.0},
                        {'makerFee': 0.0125, 'takerFee': 0.03, 'usdVolume': 1000000.0},
                        {'makerFee': 0.01, 'takerFee': 0.025, 'usdVolume': 5000000.0},
                        {'makerFee': 0.0075, 'takerFee': 0.02, 'usdVolume': 10000000.0},
                        {'makerFee': 0.005, 'takerFee': 0.015, 'usdVolume': 20000000.0},
                        {'makerFee': 0.0025, 'takerFee': 0.0125, 'usdVolume': 50000000.0},
                        {'makerFee': 0.0, 'takerFee': 0.01, 'usdVolume': 100000000.0}
                    ]}, ...
                ]
            }
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/feeschedules",
            auth=False,
            extra_params=extra_params,
        )

    def get_fee_schedules_vol(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the personal volumes per fee schedule

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-user-fee-schedule-volumes-v-3

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the personal fee schedule volumes

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.get_fee_schedules_vol()
            {
                'volumesByFeeSchedule': {
                    'ffb5403d-e82e-4ef0-8792-86a0471f526a': 0,
                    '5b755fea-c5b0-4307-a66e-b392cd5bd931': 0,
                    'eef90775-995b-4596-9257-0917f6134766': 0
                }
            }

        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/feeschedules/volumes",
            auth=True,
            extra_params=extra_params,
        )

    def get_orderbook(
        self: Market,
        symbol: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the orderbook of a specific asset/symbol. Even if the official
        kraken documentation states that the parameter ``symbol`` is not
        required, they will always respond with an error message, so it is
        recommended to use the ``symbol`` parameter until they don't fix this
        issue.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-orderbook

        :param symbol: The asset/symbol to get the orderbook from
        :type symbol: str, optional
        :return: The current orderbook for the futures contracts
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the assets orderbook

            >>> from kraken.futures import Market
            >>> Market().get_orderbook(symbol="PI_XBTUSD")
            {
                'result': 'success', 'orderBook': {
                    'bids': [
                        [27909, 3000], [27908.5, 1703], [27906, 1716],
                        [27905, 2900], [27904.5, 2900], [27904, 2900],
                        [27903.5, 8900], [27903, 3415], [27902.5, 2900],
                        [27902, 2900], [27901, 4200], [27900.5, 6000],
                        ...
                    ],
                    'asks': [
                        [27915, 4200], [27916, 1706], [27917.5, 2900],
                        [27918, 4619], [27918.5, 4200], [27919, 2900],
                        [27919.5, 78], [27920, 2900], [27920.5, 2900],
                        [27921, 6342], [27921.5, 4200], [27923, 27851],
                        ...
                    ]
                }
            }
        """
        params: dict = {}
        if defined(symbol):
            params["symbol"] = symbol

        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/orderbook",
            query_params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_tickers(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about the current tickers of all futures contracts.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-tickers

        :return: The current tickers
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the available tickers

            >>> from kraken.futures import Market
            >>> Market().get_tickers()
            {
                'tickers': [{
                    'tag': 'perpetual',
                    'pair': 'COMP:USD',
                    'symbol': 'pf_compusd',
                    'markPrice': 42.192,
                    'bid': 42.14,
                    'bidSize': 11.8,
                    'ask': 42.244,
                    'askSize': 80.7,
                    'vol24h': 96.8,
                    'volumeQuote': 4109.9678,
                    'openInterest': 451.3,
                    'open24h': 41.975,
                    'indexPrice': 42.193,
                    'last': 42.873,
                    'lastTime': '2023-04-04T00:07:33.690Z',
                    'lastSize': 13.9,
                    'suspended': False,
                    'fundingRate': 0.000220714078888884,
                    'fundingRatePrediction': 6.3914700437486e-05,
                    'postOnly': False
                }, ...]
            }
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/tickers",
            auth=False,
            extra_params=extra_params,
        )

    def get_instruments(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve more specific information about the tradeable assets on the
        Futures market

        - https://docs.kraken.com/api/docs/futures-api/trading/get-instruments

        :return: Dictionary containing information for all tradeable assets
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the available instruments/assets and information

            >>> from kraken.futures import Market
            >>> Market().get_instruments()
            {
              'instruments': [{
                    'symbol': 'pi_xbtusd',
                    'type': 'futures_inverse',
                    'underlying': 'rr_xbtusd',
                    'tickSize': 0.5,
                    'contractSize': 1,
                    'tradeable': True,
                    'impactMidSize': 1000.0,
                    'maxPositionSize': 75000000.0,
                    'openingDate': '2018-08-31T00:00:00.000Z',
                    'marginLevels': [{
                            'contracts': 0,
                            'initialMargin': 0.02,
                            'maintenanceMargin': 0.01
                        }, {
                            'contracts': 500000,
                            'initialMargin': 0.04,
                            'maintenanceMargin': 0.02
                        }, {
                            'contracts': 1000000,
                            'initialMargin': 0.06,
                            'maintenanceMargin': 0.03
                        }, {
                            'contracts': 3000000,
                            'initialMargin': 0.1,
                            'maintenanceMargin': 0.05
                        }, {
                            'contracts': 6000000,
                            'initialMargin': 0.15,
                            'maintenanceMargin': 0.075
                        }, {
                            'contracts': 12000000,
                            'initialMargin': 0.25,
                            'maintenanceMargin': 0.125
                        }, {
                            'contracts': 20000000,
                            'initialMargin': 0.3,
                            'maintenanceMargin': 0.15
                        }, {
                            'contracts': 50000000,
                            'initialMargin': 0.4,
                            'maintenanceMargin': 0.2
                        }
                    ],
                    'fundingRateCoefficient': 24,
                    'maxRelativeFundingRate': 0.0025,
                    'isin': 'GB00J62YGL67',
                    'contractValueTradePrecision': 0,
                    'postOnly': False,
                    'feeScheduleUid': 'eef90775-995b-4596-9257-0917f6134766',
                    'retailMarginLevels': [{
                        'contracts': 0,
                        'initialMargin': 0.5,
                        'maintenanceMargin': 0.25
                    }],
                    'category': '', 'tags': []
                }
            }

        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/instruments",
            auth=False,
            extra_params=extra_params,
        )

    def get_instruments_status(
        self: Market,
        instrument: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve status information of a specific or all futures contracts.

        - https://docs.kraken.com/api/docs/futures-api/trading/instrument-status

        :param instrument: Filter by asset
        :type instrument: str | None, optional
        :return: Status information about the asset(s)
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Retrieve information about a specific asset/contract/instrument

            >>> from kraken.futures import Market
            >>> Market().get_instruments_status(instrument="PI_XBTUSD")
            {
                'tradeable': 'PI_XBTUSD',
                'experiencingDislocation': False,
                'priceDislocationDirection': None,
                'experiencingExtremeVolatility': False,
                'extremeVolatilityInitialMarginMultiplier': 1
            }
        """
        if instrument:
            return self.request(  # type: ignore[return-value]
                method="GET",
                uri=f"/derivatives/api/v3/instruments/{instrument}/status",
                auth=False,
            )

        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/instruments/status",
            auth=False,
            extra_params=extra_params,
        )

    def get_trade_history(
        self: Market,
        symbol: str | None = None,
        lastTime: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve the trade history (max 100 entries), can be filtered using the
        parameters.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-history

        :param symbol: The asset to filter for
        :type symbol: str, optional
        :param lastTime: Filter by time
        :type lastTime: str, optional
        :return: Trade history
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the public trade history

            >>> from kraken.futures import Market
            >>> Market().get_trade_history(symbol="PI_XBTUSD")
            {
                'history': [{
                        'time': '2023-04-04T05:28:27.926Z',
                        'trade_id': 100,
                        'price': 27913,
                        'size': 2456,
                        'side': 'sell',
                        'type': 'fill',
                        'uid': 'de7a2eca-f2bc-4afb-860d-522a9dcc0b12'
                    }, {
                        'time': '2023-04-04T05:28:28.795Z',
                        'trade_id': 99, 'price': 27913.5,
                        'size': 3000, 'side': 'sell',
                        'type': 'fill',
                        'uid': 'c985c7ea-30a5-4456-b857-a4ec9156fb3b'
                    }, ...
                ]
        """
        params: dict = {}
        if defined(symbol):
            params["symbol"] = symbol
        if defined(lastTime):
            params["lastTime"] = lastTime

        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/history",
            query_params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_historical_funding_rates(
        self: Market,
        symbol: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about the historical funding rates for a specific
        asset.

        - https://docs.kraken.com/api/docs/futures-api/trading/historical-funding-rates

        :param symbol: The symbol/asset/futures contract
        :type symbol: str
        :return: Funding rates
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the historical funding rates

            >>> from kraken.futures import Market
            >>> Market().get_historical_funding_rates(symbol="PI_XBTUSD")
            {
                'rates': [{
                        'timestamp': '2018-08-31T16:00:00.000Z',
                        'fundingRate': 1.0327058177e-08,
                        'relativeFundingRate': 7.182407e-05
                    }, {
                        'timestamp': '2018-08-31T20:00:00.000Z',
                        'fundingRate': -1.2047162502e-08,
                        'relativeFundingRate': -8.4873103125e-05
                    }, {
                        'timestamp': '2018-09-01T00:00:00.000Z',
                        'fundingRate': -9.645113378e-09,
                        'relativeFundingRate': -6.76651e-05
                    }, ...
                ]
            }
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v4/historicalfundingrates",
            query_params={"symbol": symbol},
            auth=False,
            extra_params=extra_params,
        )

    def get_leverage_preference(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the current leverage preferences of the user.

        Requires at least the ``General API - Read Only`` permission in the API
        key settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-leverage-setting

        :return: The leverage preferences for all futures contracts
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the users leverage preferences

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.get_leverage_preference()
            {
                'leveragePreferences': [
                    {'symbol': 'PF_XBTUSD', 'maxLeverage': 5.0},
                    ...
                ]
            }
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/leveragepreferences",
            auth=True,
            extra_params=extra_params,
        )

    def set_leverage_preference(
        self: Market,
        symbol: str,
        maxLeverage: str | float | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Set a new leverage preference for a specific futures contract.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/set-leverage-setting

        :param symbol: The symbol to set the preference
        :type symbol: str, optional
        :param maxLeverage: The maximum allowed leverage for a futures contract
        :type maxLeverage: str | float, optional
        :return: Information about the success or fail
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Set the users leverage preferences

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.set_leverage_preference(symbol="PF_XBTUSD", maxLeverage=2)
            {'result': 'success', 'serverTime': '2023-04-04T05:59:49.576Z'}
        """
        params: dict = {"symbol": symbol}
        if defined(maxLeverage):
            params["maxLeverage"] = maxLeverage

        return self.request(  # type: ignore[return-value]
            method="PUT",
            uri="/derivatives/api/v3/leveragepreferences",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )

    def get_pnl_preference(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the current PNL (profit & loss) preferences. This can be used to
        define the currency in which the profits and losses are realized.

        Requires at least the ``General API - Read Only`` permission in the API
        key settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-pnl-currency-preference

        :return: The current NPL preferences
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the users profit/loss preferences

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.get_pnl_preference()
            {'result': 'success', 'serverTime': '2023-04-04T15:21:29.413Z', 'preferences': []}
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/pnlpreferences",
            auth=True,
            extra_params=extra_params,
        )

    def set_pnl_preference(
        self: Market,
        symbol: str,
        pnlPreference: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Modify or set the current PNL preference of the user. This can be used
        to define a specific currency that should be used to realize profits and
        losses. The default is the quote currency of the futures contract.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/set-pnl-currency-preference

        :param symbol: The asset pair or futures contract
        :type symbol: str
        :param pnlPreference: The currency to pay out the profits and losses
        :type str:
        :return: Success or failure of the request
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Set the users profit/loss preferences

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.set_pnl_preference(symbol="PF_XBTUSD", pnlPreference="USD")
            {'result': 'success', 'serverTime': '2023-04-04T15:24:18.406Z'}
        """
        return self.request(  # type: ignore[return-value]
            method="PUT",
            uri="/derivatives/api/v3/pnlpreferences",
            post_params={"symbol": symbol, "pnlPreference": pnlPreference},
            auth=True,
            extra_params=extra_params,
        )

    def _get_historical_events(
        self: Market,
        endpoint: str,
        before: int | None = None,
        continuation_token: str | None = None,
        since: int | None = None,
        sort: str | None = None,
        tradeable: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Method that uses as a gateway for the methods
        :func:`kraken.futures.Market.get_public_execution_events`,
        :func:`kraken.futures.Market.get_public_order_events`, and
        :func:`kraken.futures.Market.get_public_mark_price_events`.

        :param endpoint: The futures endpoint to access
        :type endpoint: str
        :param before: Filter by time
        :type before: int, optional
        :param continuation_token: Token that can be used to continue requesting
            historical events
        :type continuation_token: str, optional
        :param since: Filter by a specifying a start point
        :type since: int, optional
        :param sort: Sort the results
        :type sort: str, optional
        :param tradeable: The asset to filter for
        :type tradeable: str, optional
        :param auth: If the request is accessing a private endpoint (default:
            ``True``)
        :type auth: bool
        """
        params: dict = {}
        if defined(before):
            params["before"] = before
        if defined(continuation_token):
            params["continuation_token"] = continuation_token
        if defined(since):
            params["since"] = since
        if defined(sort):
            params["sort"] = sort
        if defined(tradeable):
            params["tradeable"] = tradeable

        return self.request(  # type: ignore[return-value]
            method="GET",
            uri=endpoint,
            post_params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_public_execution_events(
        self: Market,
        tradeable: str,
        before: int | None = None,
        continuation_token: str | None = None,
        since: int | None = None,
        sort: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about the public execution events. The returned
        ``continuation_token`` can be used to request more data.

        - https://docs.kraken.com/api/docs/futures-api/history/get-public-execution-events

        :param tradeable: The contract to filter for
        :type tradeable: str
        :param before: Filter by time
        :type before: int | None, optional
        :param continuation_token: Token that can be used to continue requesting
            historical events
        :type continuation_token: str | None, optional
        :param since: Filter by a specifying a start point
        :type since: int | None, optional
        :param sort: Sort the results
        :type sort: str | None, optional
        :return: The public execution events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the public execution events

            >>> from kraken.futures import Market
            >>> Market().get_public_execution_events(tradeable="PI_XBTUSD")
            {
                'elements': [
                    {
                        'uid': '9c74d4ba-a658-4208-891c-eee6e13bf910',
                        'timestamp': 1680874894684,
                        'event': {
                            'Execution': {
                                'execution': {
                                    'uid': '3df5cb59-d410-48f7-9c6f-ee9b849b9c91',
                                    'makerOrder': {
                                        'uid': 'a0d28216-54f8-4af0-9adc-0d0d4738936d',
                                        'tradeable': 'PI_XBTUSD',
                                        'direction': 'Buy',
                                        'quantity': '626',
                                        'timestamp': 1680874894675,
                                        'limitPrice': '27909.5',
                                        'orderType': 'Post',
                                        'reduceOnly': False,
                                        'lastUpdateTimestamp': 1680874894675
                                    },
                                    'takerOrder': {
                                        'uid': '09246639-9130-42fb-8d90-4ed39913456f',
                                        'tradeable': 'PI_XBTUSD',
                                        'direction': 'Sell',
                                        'quantity': '626',
                                        'timestamp': 1680874894684,
                                        'limitPrice': '27909.5000000000',
                                        'orderType': 'IoC',
                                        'reduceOnly': False,
                                        'lastUpdateTimestamp': 1680874894684
                                    },
                                    'timestamp': 1680874894684,
                                    'quantity': '626',
                                    'price': '27909.5',
                                    'markPrice': '27915.01610466227',
                                    'limitFilled': True,
                                    'usdValue': '626.00'
                                },
                                'takerReducedQuantity': ''
                            }
                        }
                    }, ...
                ],
                'len': 1000,
                'continuationToken': 'MTY4MDg2Nzg2ODkxOS85MDY0OTcwMTAxNA=='
            }
        """
        return self._get_historical_events(
            endpoint=f"/api/history/v2/market/{tradeable}/executions",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            extra_params=extra_params,
        )

    def get_public_order_events(
        self: Market,
        tradeable: str,
        before: int | None = None,
        continuation_token: str | None = None,
        since: int | None = None,
        sort: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about the public order events - filled, closed,
        opened, etc, for a specific contract.The returned ``continuation_token``
        can be used to request more data.

        - https://docs.kraken.com/api/docs/futures-api/history/get-public-order-events

        :param tradeable: The contract to filter for
        :type tradeable: str
        :param before: Filter by time
        :type before: int, optional
        :param continuation_token: Token that can be used to continue requesting
            historical events
        :type continuation_token: str, optional
        :param since: Filter by a specifying a start point
        :type since: int, optional
        :param sort: Sort the results
        :type sort: str, optional
        :return: The public order events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the public order events

            >>> from kraken.futures import Market
            >>> Market().get_public_order_events(tradeable="PI_XBTUSD")
            {
                'elements': [
                    {
                        'uid': '430782d7-7b6d-472a-9e92-67047289d742',
                        'timestamp': 1680875125649,
                        'event': {
                            'OrderPlaced': {
                                'order': {
                                    'uid': 'f9aaf471-95ba-4fde-ab68-251f12f96e47',
                                    'tradeable': 'PI_XBTUSD',
                                    'direction': 'Sell',
                                    'quantity': '652',
                                    'timestamp': 1680875125649,
                                    'limitPrice': '27927.5',
                                    'orderType': 'Post',
                                    'reduceOnly': False,
                                    'lastUpdateTimestamp': 1680875125649
                                },
                                'reason': 'new_user_order',
                                'reducedQuantity': ''
                            }
                        }
                    }, ...
                ],
                'len': 1000,
                'continuationToken': 'MTY4MDg3NTExMzc2OS85MDY2NDA1ODIyNw=='
            }
        """
        return self._get_historical_events(
            endpoint=f"/api/history/v2/market/{tradeable}/orders",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            extra_params=extra_params,
        )

    def get_public_mark_price_events(
        self: Market,
        tradeable: str,
        before: int | None = None,
        continuation_token: str | None = None,
        since: int | None = None,
        sort: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about public mark price events. The returned
        ``continuation_token`` can be used to request more data.

        - https://docs.kraken.com/api/docs/futures-api/history/get-public-price-events

        :param tradeable: The contract to filter for
        :type tradeable: str
        :param before: Filter by time
        :type before: int | None, optional
        :param continuation_token: Token that can be used to continue requesting
            historical events
        :type continuation_token: str | None, optional
        :param since: Filter by a specifying a start point
        :type since: int | None, optional
        :param sort: Sort the results
        :type sort: str | None, optional
        :return: The public order events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Market: Get the public mark price events

            >>> from kraken.futures import Market
            >>> Market().get_public_mark_price_events(tradeable="PI_XBTUSD")
            {
                'elements': [
                    {
                        'uid': '',
                        'timestamp': 1680875273372,
                        'event': {
                            'MarkPriceChanged': {
                                'price': '27900.67795901584'
                            }
                        }
                    }, {
                        'uid': '',
                        'timestamp': 1680875272263,
                        'event': {
                            'MarkPriceChanged': {
                                'price': '27900.09023205142'
                            }
                        }
                    }, ...
                ],
                'len': 1000,
                'continuationToken': 'MTY4MDg3NDEyNzg3OC85MDY2MjI3ODIzMA=='
            }
        """
        return self._get_historical_events(
            endpoint=f"/api/history/v2/market/{tradeable}/price",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            extra_params=extra_params,
        )


__all__ = ["Market"]
