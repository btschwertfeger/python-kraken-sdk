#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger

"""Module that implements the Kraken Futures market client"""
from typing import Union

from kraken.base_api import KrakenBaseFuturesAPI


class Market(KrakenBaseFuturesAPI):

    """
    Class that implements the Kraken Futures market client

    If the sandbox environment is chosen, the keys must be generated from here:
        https://demo-futures.kraken.com/settings/api

    :param key: Optional - Futures API public key (default: ``""``)
    :type key: str
    :param secret: Optional - Futures API secret key (default: ``""``)
    :type secret: str
    :param url: Optional - The url to access the Futures Kraken API (default: https://futures.kraken.com)
    :type url: str
    :param sandbox: Optional - If set to ``True`` the url will be https://demo-futures.kraken.com (default: ``False``)
    :type sandbox: bool
    """

    def __init__(
        self, key: str = "", secret: str = "", url: str = "", sandbox: bool = False
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_ohlc(
        self,
        tick_type: str,
        symbol: str,
        resolution: int,
        from_: Union[int, None] = None,
        to: Union[int, None] = None,
    ) -> dict:
        """
        Retrieve the open, high, low, and close data for a specific symbol and resolution.
        It is also possible to filter by time.

        - https://docs.futures.kraken.com/#http-api-charts-ohlc-get-ohlc

        - https://support.kraken.com/hc/en-us/articles/4403284627220-OHLC

        :param tick_type: The kind of data, based on ``mark``, ``spot``, or ``trade``
        :type tick_type: str
        :param symbol: The asset pair to get the ohlc from
        :type symbol: str
        :param resolution: The tick resolution, one of ``1m``. ``5m``, ``15m``, ``1h``, ``4h``, ``12h``, ``1d``, ``1w``
        :type resolution: str
        :param from_: Optional - From date in epoch seconds
        :type from_: int | None
        :param to: Optional - To date in epoch seconds (inclusive)
        :type to: int | None
        """
        ttypes = ("spot", "mark", "trade")
        resolutions = ("1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d", "1w")
        if tick_type not in ttypes:
            raise ValueError(f"tick_type must be in {ttypes}")
        if resolution is not None and resolution not in resolutions:
            raise ValueError(f"resolution must be in {resolutions}")

        params = {}
        if from_ is not None:
            params["from"] = from_
        if to is not None:
            params["to"] = to
        return self._request(
            method="GET",
            uri=f"/api/charts/v1/{tick_type}/{symbol}/{resolution}",
            query_params=params,
            auth=False,
        )

    def get_tick_types(self) -> dict:
        """
        Retrieve the available tick types that can be used for example to access
        the :func:`kraken.futures.Market.get_ohlc` endpoint.

        - https://docs.futures.kraken.com/#http-api-charts-ohlc-get-tick-types

        :return: List of available tick types
        :rtype: List[str]
        """
        return self._request(method="GET", uri="/api/charts/v1/", auth=False)

    def get_tradeable_products(self, tick_type: str) -> dict:
        """
        Retrieve a list containing the tradeable assets on the futures market.

        - https://docs.futures.kraken.com/#http-api-charts-ohlc-get-tradeable-products

        :param tick_type: The kind of data, based on ``mark``, ``spot``, or ``trade``
        :type tick_type: str
        :return: List of tradeable assets
        :type: List[str]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> Market().get_tradeable_products(tick_type="trade")
            ["PI_XBTUSD", "PF_XBTUSD", "PF_SOLUSD", ...]
        """
        return self._request(
            method="GET", uri=f"/api/charts/v1/{tick_type}", auth=False
        )

    def get_resolutions(self, tick_type: str, tradeable: str) -> dict:
        """
        Retrieve the list of available resolutions for a specific asset.

        - https://docs.futures.kraken.com/#http-api-charts-ohlc-get-resolutions

        :param tick_type: The kind of data, based on ``mark``, ``spot``, or ``trade``
        :type tick_type: str
        :param tick_type: The asset of interest
        :type tick_type: str
        :return: List of resolutions
        :type: List[str]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> Market().get_resolutions(tick_type="mark", tradeable="PI_XBTUSD")
            ['1h', '12h', '1w', '15m', '1d', '5m', '30m', '4h', '1m']
        """
        return self._request(
            method="GET", uri=f"/api/charts/v1/{tick_type}/{tradeable}", auth=False
        )

    def get_fee_schedules(self) -> dict:
        """
        Retrieve information about the current fees

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-fee-schedules-get-fee-schedules

        - https://support.kraken.com/hc/en-us/articles/360049269572-Fee-Schedules

        :return: Dictionary containing information about the fees for wide range of tradeable assets
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET", uri="/derivatives/api/v3/feeschedules", auth=False
        )

    def get_fee_schedules_vol(self) -> dict:
        """

        Get the personal volumes per fee schedule

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-fee-schedules-get-fee-schedule-volumes

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET", uri="/derivatives/api/v3/feeschedules/volumes", auth=True
        )

    def get_orderbook(self, symbol: Union[str, None] = None) -> dict:
        """

        Get the orderboook of a specific asset/symbol. Even if the official kraken documentation
        states that the parameter ``symbol`` is not required, they will always respond with an error
        message, so it is recommanded to use the ``symbol`` parameter until they dont fix this issue.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-orderbook

        - https://support.kraken.com/hc/en-us/articles/360022839551-Order-Book

        :param symbol: Optional - The asset/symbol to get the orderbook from
        :type symbol: str | None
        :return: The current orderbook for the futures contracts
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        return self._request(
            method="GET",
            uri="/derivatives/api/v3/orderbook",
            query_params=params,
            auth=False,
        )

    def get_tickers(self) -> dict:
        """
        Retrieve information about the current tickers of all futures contracts

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-tickers

        - https://support.kraken.com/hc/en-us/articles/360022839531-Tickers

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET", uri="/derivatives/api/v3/tickers", auth=False
        )

    def get_instruments(self) -> dict:
        """

        Retrieve more specific information about the tradeable assets on the Futures market

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instruments

        - https://support.kraken.com/hc/en-us/articles/360022635672-Instruments

        :return: Dictionary containing information for all tradeable assets
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET", uri="/derivatives/api/v3/instruments", auth=False
        )

    def get_instruments_status(self, instrument: Union[str, None] = None) -> dict:
        """
        Retrieve status information of a specific or all futures contracts.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instrument-status-list

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instrument-status

        :param instrument: Optional - Filter by asset
        :type instrument: str | None
        :return: Status information about the asset(s)
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
            return self._request(
                method="GET",
                uri=f"/derivatives/api/v3/instruments/{instrument}/status",
                auth=False,
            )

        return self._request(
            method="GET", uri="/derivatives/api/v3/instruments/status", auth=False
        )

    def get_trade_history(
        self,
        symbol: Union[str, None] = None,
        lastTime: Union[str, None] = None,
        **kwargs,
    ) -> dict:
        """
        Retrieve the trade history (max 100 entries), can be filtered using the parameters.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-trade-history

        - https://support.kraken.com/hc/en-us/articles/360022839511-History

        :param symbol: Optional - The asset to filter for
        :type symbol: str | None
        :param lastTime: Optional - Filter by time
        :type lastTime: str | None
        :return: Trade history
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        if lastTime is not None:
            params["lastTime"] = lastTime
        params.update(kwargs)
        return self._request(
            method="GET",
            uri="/derivatives/api/v3/history",
            query_params=params,
            auth=False,
        )

    def get_historical_funding_rates(self, symbol: str) -> dict:
        """
        Retrieve information about the historical funding rates for a specific asset.

        - https://support.kraken.com/hc/en-us/articles/360061979852-Historical-Funding-Rates

        :param symbol: The symbol/asset/futures contract
        :type symbol: str
        :return: Funding rates
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET",
            uri="/derivatives/api/v4/historicalfundingrates",
            query_params={"symbol": symbol},
            auth=False,
        )

    def get_leverage_preference(self) -> dict:
        """
        Get the current leverage preferences of the user.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-get-the-leverage-setting-for-a-market

        :return: The leverage preferences for all futures contracts
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET", uri="/derivatives/api/v3/leveragepreferences", auth=True
        )

    def set_leverage_preference(
        self, symbol: Union[str, None], maxLeverage: Union[str, int, float, None] = None
    ) -> dict:
        """
        Set a new leverage preference for a specific futures contract.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-set-the-leverage-setting-for-a-market

        :param symbol: Optional - The symbol to set the preference
        :type symbol: str | None
        :param maxLeverage: Optional - The maximum allowd leverage for a futures contract
        :type maxLeverage: str | int | float | None
        :return: Information about the success or fail
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.set_leverage_preference(symbol="PF_XBTUSD", maxLeverage=2)
            {'result': 'success', 'serverTime': '2023-04-04T05:59:49.576Z'}
        """
        params = {"symbol": symbol}
        if maxLeverage is not None:
            params["maxLeverage"] = maxLeverage
        return self._request(
            method="PUT",
            uri="/derivatives/api/v3/leveragepreferences",
            query_params=params,
            auth=True,
        )

    def get_pnl_preference(self) -> dict:
        """
        Get the current pnl (profit & loss) preferences. This can be used to define the currency
        in which the profits and losses are realized.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-get-pnl-currency-preference-for-a-market

        :return: The current pnl preferences
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.get_pnl_preference()
            {'result': 'success', 'serverTime': '2023-04-04T15:21:29.413Z', 'preferences': []}
        """
        return self._request(
            method="GET", uri="/derivatives/api/v3/pnlpreferences", auth=True
        )

    def set_pnl_preference(self, symbol: str, pnlPreference: str) -> dict:
        """
        Modify or set the currenct pnl preference of the user. This can be used to define a
        specific currency that should be used to realize profits and losses. The default is
        the quote currency of the futures contract.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-set-pnl-currency-preference-for-a-market

        :param symbol: The asset pair or futures contract
        :type symbol: str
        :param pnlPreference: The currency to pay out the profits and losses
        :type str:
        :return: Success or failure of the request
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> market = Market(key="api-key", secret="secret-key")
            >>> market.set_pnl_preference(symbol="PF_XBTUSD", pnlPreference="USD")
            {'result': 'success', 'serverTime': '2023-04-04T15:24:18.406Z'}
        """
        return self._request(
            method="PUT",
            uri="/derivatives/api/v3/pnlpreferences",
            query_params={"symbol": symbol, "pnlPreference": pnlPreference},
            auth=True,
        )

    def _get_historical_events(
        self,
        endpoint: str,
        before: Union[int, None] = None,
        continuation_token: Union[str, None] = None,
        since: Union[int, None] = None,
        sort: Union[str, None] = None,
        tradeable: Union[str, None] = None,
        auth: bool = True,
        **kwargs,
    ) -> dict:
        """
        Method that uses as a gateway for the methods :func:`kraken.futures.Market.get_public_execution_events`,
        :func:`kraken.futures.Market.get_public_order_events`, and
        :func:`kraken.futures.Market.get_public_mark_price_events`.

        :param endpoint: The futures endpoint to access
        :type endpoint: str
        :param before: Optional - Filter by time
        :type before: int | None
        :param continuation_token: Optional - Token that can be used to continue requesting historical events
        :type token: str | None
        :param since: Optional - Filter by a specifying a start point
        :type since: int | None
        :param sort: Optional - Sort the results
        :type sort: str | None
        :param tradeable: Optional - The asset to filter for
        :type tradeable: str | None
        :param auth: Optional - If the request is accessing a private endpoint (default_ ``True``)
        :type auth: bool
        """
        params = {}
        if before is not None:
            params["before"] = before
        if continuation_token is not None:
            params["continuation_token"] = continuation_token
        if since is not None:
            params["since"] = since
        if sort is not None:
            params["sort"] = sort
        if tradeable is not None:
            params["tradeable"] = tradeable
        params.update(kwargs)
        return self._request(method="GET", uri=endpoint, post_params=params, auth=auth)

    def get_public_execution_events(
        self,
        tradeable: str,
        before: Union[int, None] = None,
        continuation_token: Union[str, None] = None,
        since: Union[int, None] = None,
        sort: Union[str, None] = None,
    ) -> dict:
        """
        Retrieve information about the public execition events. The returned ``continuation_token```
        can be used to request more data.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-public-execution-events

        - https://support.kraken.com/hc/en-us/articles/4401755685268-Market-History-Executions

        :param tradeable: The contract to filter for
        :type tradeable: str
        :param before: Filter by time
        :type before: int
        :param continuation_token: Optional - Token that can be used to continue requesting historical events
        :type token: str | None
        :param since: Optional - Filter by a specifying a start point
        :type since: int | None
        :param sort: Optional - Sort the results
        :type sort: str | None
        :param tradeable: Optional - The asset to filter for
        :type tradeable: str | None
        :return: The public execution events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> Market().get_public_execution_events()
        """
        return self._get_historical_events(
            endpoint=f"/api/history/v2/market/{tradeable}/executions",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            auth=False,
        )

    def get_public_order_events(
        self,
        tradeable: str,
        before: Union[int, None] = None,
        continuation_token: Union[str, None] = None,
        since: Union[int, None] = None,
        sort: Union[str, None] = None,
    ) -> dict:
        """
        Retrive information about the oublic order events - filled, closed, opened, etc, for
        a specific contract.The returned ``continuation_token``` can be used to request more data.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-public-order-events and

        - https://support.kraken.com/hc/en-us/articles/4401755906452-Market-History-Orders

        :param tradeable: The contract to filter for
        :type tradeable: str
        :param before: Filter by time
        :type before: int
        :param continuation_token: Optional - Token that can be used to continue requesting historical events
        :type token: str | None
        :param since: Optional - Filter by a specifying a start point
        :type since: int | None
        :param sort: Optional - Sort the results
        :type sort: str | None
        :param tradeable: Optional - The asset to filter for
        :type tradeable: str | None
        :return: The public order events
        :rtype: dict


        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> Market().get_public_order_events()
        """
        return self._get_historical_events(
            endpoint=f"/api/history/v2/market/{tradeable}/orders",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            auth=False,
        )

    def get_public_mark_price_events(
        self,
        tradeable: str,
        before: Union[int, None] = None,
        continuation_token: Union[str, None] = None,
        since: Union[int, None] = None,
        sort: Union[str, None] = None,
    ) -> dict:
        """
        Retrive information about public mark price events. The returned ``continuation_token```
        can be used to request more data.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-public-mark-price-events

        - https://support.kraken.com/hc/en-us/articles/4401748276116-Market-History-Mark-Price

        :param tradeable: The contract to filter for
        :type tradeable: str
        :param before: Filter by time
        :type before: int
        :param continuation_token: Optional - Token that can be used to continue requesting historical events
        :type token: str | None
        :param since: Optional - Filter by a specifying a start point
        :type since: int | None
        :param sort: Optional - Sort the results
        :type sort: str | None
        :param tradeable: Optional - The asset to filter for
        :type tradeable: str | None
        :return: The public order events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Market
            >>> Market().get_public_mark_price_events()
        """
        return self._get_historical_events(
            endpoint=f"/api/history/v2/market/{tradeable}/price",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            auth=False,
        )
