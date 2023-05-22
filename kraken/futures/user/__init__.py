#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Futures user client"""

from typing import Optional, Union

import requests

from ...base_api import KrakenBaseFuturesAPI, defined


class User(KrakenBaseFuturesAPI):
    """
    Class that implements the Kraken Futures user client

    If the sandbox environment is chosen, the keys must be generated from here:
    https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str, optional
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Futures Kraken API (default: https://futures.kraken.com)
    :type url: str, optional
    :param sandbox: If set to ``True`` the URL will be https://demo-futures.kraken.com
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Futures User: Create the user client

        >>> from kraken.futures import User
        >>> user = User() # unauthenticated
        >>> user = User(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Futures User: Create the user client as context manager

        >>> from kraken.futures import User
        >>> with User(key="api-key", secret="secret-key") as user:
        ...     print(user.get_wallets())
    """

    def __init__(
        self: "User",
        key: str = "",
        secret: str = "",
        url: str = "",
        sandbox: bool = False,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def __enter__(self: "User") -> "User":
        super().__enter__()
        return self

    def get_wallets(self: "User") -> dict:
        """
        Lists the current wallet balances of the user.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-wallets

        :return: Information about the current balances of the user
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the user's wallets

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_wallets()
            {
                'result': 'success',
                'accounts': {
                    'fi_xbtusd': {
                        'auxiliary': {
                            'usd': 0,
                            'pv': 0.0,
                            'pnl': 0.0,
                            'af': 0.0,
                            'funding': 0.0
                        },
                        'marginRequirements': {
                            'im': 0.0,
                            'mm': 0.0,
                            'lt': 0.0,
                            'tt': 0.0
                        },
                        'triggerEstimates': {
                            'im': 0,
                            'mm': 0,
                            'lt': 0,
                            'tt': 0
                        },
                        'balances': {
                            'xbt': 0.0
                        },
                        'currency': 'xbt',
                        'type': 'marginAccount'
                    },
                    'cash': {
                        'balances': {
                            'eur': 4567.7117591172,
                            'gbp': 4002.4975584765,
                            'bch': 39.3081761006,
                            'usd': 5000.0,
                            'xrp': 10055.1019587339,
                            'eth': 2.6868286287,
                            'usdt': 4999.3200924674,
                            'usdc': 4999.8300057798,
                            'ltc': 53.9199827456,
                            'xbt': 0.1785169809
                        },
                        'type': 'cashAccount'
                    },
                    'flex': {
                        'currencies': {},
                        'initialMargin': 0.0,
                        'initialMarginWithOrders': 0.0,
                        'maintenanceMargin': 0.0,
                        'balanceValue': 0.0,
                        'portfolioValue': 0.0,
                        'collateralValue': 0.0,
                        'pnl': 0.0,
                        'unrealizedFunding': 0.0,
                        'totalUnrealized': 0.0,
                        'totalUnrealizedAsMargin': 0.0,
                        'availableMargin': 0.0,
                        'marginEquity': 0.0,
                        'type': 'multiCollateralMarginAccount'
                    }
                },
                'serverTime': '2023-04-04T17:56:49.027Z'
            }
        """
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/derivatives/api/v3/accounts", auth=True
        )

    def get_subaccounts(self: "User") -> dict:
        """
        List the subaccounts of the user.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-subaccounts

        :return: Information about the user owned subaccounts
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the user's subaccounts

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_subaccounts()
            {
                'result': 'success',
                'serverTime': '2023-04-04T18:03:33.696Z',
                'masterAccountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                'subaccounts': []
            }
        """
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/derivatives/api/v3/subaccounts", auth=True
        )

    def get_unwindqueue(self: "User") -> dict:
        """
        Retrieve information about the percentile of the open position in case of unwinding.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-position-percentile-of-unwind-queue

        :return: Information about unwind queue
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the user's unwind queue

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_unwindqueue()
            {
                'result': 'success',
                'serverTime': '2023-04-04T18:05:01.328Z',
                'queue': [
                    { 'symbol': 'PF_UNIUSD', 'percentile': 20 }
                ]
            }
        """
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/derivatives/api/v3/unwindqueue", auth=True
        )

    def get_notifications(self: "User") -> dict:
        """
        Retrieve the latest notifications from the Kraken Futures API

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-general-get-notifications

        :return: Notifications
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the latest notifications

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_notifications()
            {
               'result': 'success',
                'notifications': [{
                    'type': 'general',
                    'priority': 'high',
                    'note': 'Market in post only mode until 4pm.'
                }],
                'serverTime': '2023-04-04T18:01:39.729Z'
            }
        """
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/derivatives/api/v3/notifications", auth=True
        )

    def get_account_log(
        self: "User",
        before: Optional[Union[str, int]] = None,
        count: Optional[Union[str, int]] = None,
        from_: Optional[Union[str, int]] = None,
        info: Optional[str] = None,
        since: Optional[Union[str, int]] = None,
        sort: Optional[str] = None,
        to: Optional[str] = None,
    ) -> dict:
        """
        Get the historical events of the user's account. This is not available in the
        Kraken demo/sandbox environment.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-history-account-history-get-account-log

        :param before: Filter to only return results before a specific timestamp or date
        :type before: str | int, optional
        :param count: Defines the maximum number of results (max: ``500``)
        :type count: str | int, optional
        :param from_: Defines the first id to start with
        :type from_: str | int, optional
        :param info: Filter by info (e.g.,: ``futures liquidation``)
        :type info: str, optional
        :param since: Defines the first entry to begin with by item
        :type since: str | int, optional
        :param sort: Sort the results
        :type sort: str, optional
        :param to: Id of the last entry
        :type to: str, optional
        :return: The account log
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the user's account log

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_account_log(before="2023-04-04T16:10:46.260Z", count=1)
            {
                'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                'logs': [
                    {
                        'asset': 'eth',
                        'contract': None,
                        'booking_uid': 'be3d0e19-887a-4a8e-b8f6-32b9ef7f04ab',
                        'collateral': None,
                        'date': '2023-04-04T16:10:46.260Z',
                        'execution': None,
                        'fee': None,
                        'funding_rate': None,
                        'id': 10,
                        'info': 'admin transfer',
                        'margin_account': 'ETH',
                        'mark_price': None,
                        'new_average_entry_price': None,
                        'new_balance': 2.6868286287,
                        'old_average_entry_price': None,
                        'old_balance': 0.0,
                        'realized_funding': None,
                        'realized_pnl': None,
                        'trade_price': None,
                        'conversion_spread_percentage': None
                    }
                ], ...
            }
        """

        params: dict = {}
        if defined(before):
            params["before"] = before
        if defined(count):
            params["count"] = count
        if defined(from_):
            params["from"] = from_
        if defined(info):
            params["info"] = info
        if defined(since):
            params["since"] = since
        if defined(sort):
            params["sort"] = sort
        if defined(to):
            params["to"] = to
        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/api/history/v2/account-log",
            query_params=params,
            auth=True,
        )

    def get_account_log_csv(self: "User") -> requests.Response:
        """
        Return the account log as csv, for example to export it. This is not available in the
        Kraken demo/sandbox environment.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-history-account-log-get-recent-account-log-csv

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the account log and export as CSV

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> response = user.get_account_log_csv()
            >>> with open(f"account_log.csv", "wb") as file:
            ...     for chunk in response.iter_content(chunk_size=512):
            ...         if chunk:
            ...             file.write(chunk)
        """

        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/api/history/v2/accountlogcsv",
            auth=True,
            return_raw=True,
        )

    def _get_historical_events(
        self: "User",
        endpoint: str,
        before: Optional[int] = None,
        continuation_token: Optional[str] = None,
        since: Optional[int] = None,
        sort: Optional[str] = None,
        tradeable: Optional[str] = None,
        **kwargs: dict,
    ) -> dict:
        """
        Method that uses as a gateway for the methods :func:`kraken.futures.User.get_execution_events`,
        :func:`kraken.futures.User.get_order_events`, and
        :func:`kraken.futures.User.get_trigger_events`

        :param endpoint: The futures endpoint to access
        :type endpoint: str
        :param before: Filter by time
        :type before: int, optional
        :param continuation_token: Token that can be used to continue requesting historical events
        :type continuation_token: str, optional
        :param since: Filter by a specifying a start point
        :type since: int, optional
        :param sort: Sort the results
        :type sort: str, optional
        :param tradeable: The asset to filter for
        :type tradeable: str, optional
        :param auth: If the request is accessing a private endpoint (default: ``True``)
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
        params.update(kwargs)
        return self._request(  # type: ignore[return-value]
            method="GET", uri=endpoint, query_params=params, auth=True
        )

    def get_execution_events(
        self: "User",
        before: Optional[int] = None,
        continuation_token: Optional[str] = None,
        since: Optional[int] = None,
        sort: Optional[str] = None,
        tradeable: Optional[str] = None,
    ) -> dict:
        """
        Retrieve the order/position execution events of this user. The returned ``continuation_token``
        can be used to request more data.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-history-account-history-get-execution-events

        :param before: Filter by time
        :type before: int, optional
        :param continuation_token: Token that can be used to continue requesting historical events
        :type continuation_token: str, optional
        :param since: Filter by a specifying a start point
        :type since: int, optional
        :param sort: Sort the results
        :type sort: str, optional
        :param tradeable: The asset to filter for
        :type tradeable: str, optional
        :return: The user-specific execution events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the user's historical execution events

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_execution_events(
            ...    tradeable="PF_SOLUSD",
            ...    since=1668989233,
            ...    before=1668999999,
            ...    sort="asc"
            ... )
            {
                'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                'continuationToken': 'alp81a',
                'elements': [{
                    'event': {
                        'execution': {
                            'execution': {
                                'limitFilled': false,
                                'makerOrder': {
                                    'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                                    'direction': 'Buy',
                                    'filled': '2332.12239',
                                    'lastUpdateTimestamp': 1605126171852,
                                    'limitPrice': '1234.56789',
                                    'orderType': 'lmt',
                                    'quantity': '1234.56789',
                                    'reduceOnly': false,
                                    'timestamp': 1605126171852,
                                    'tradeable': 'pi_xbtusd',
                                    'uid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0'
                                },
                                'makerOrderData': {
                                    'fee': '12.56789',
                                    'positionSize': '2332.12239'
                                },
                                'markPrice': '27001.56',
                                'oldTakerOrder': {
                                    'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                                    'direction': 'Buy',
                                    'filled': '2332.12239',
                                    'lastUpdateTimestamp': 1605126171852,
                                    'limitPrice': '27002.56789',
                                    'orderType': 'string',
                                    'quantity': '0.156789',
                                    'reduceOnly': false,
                                    'timestamp': 1605126171852,
                                    'tradeable': 'pi_xbtusd',
                                    'uid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0'
                                },
                                'price': '2701.8163',
                                'quantity': '0.156121',
                                'takerOrder': {
                                    'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                                    'direction': 'Buy',
                                    'filled': '0.156121',
                                    'lastUpdateTimestamp': 1605126171852,
                                    'limitPrice': '2702.91',
                                    'orderType': 'lmt',
                                    'quantity': '0.156121',
                                    'reduceOnly': false,
                                    'timestamp': 1605126171852,
                                    'tradeable': 'pi_xbtusd',
                                    'uid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0'
                                },
                                'takerOrderData': {
                                    'fee': '12.83671',
                                    'positionSize': '27012.91'
                                },
                                'timestamp': 1605126171852,
                                'uid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                                'usdValue': '2301.56789'
                            },
                            }
                        },
                    'timestamp': 1605126171852,
                    'uid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0'
                }, ...
            ],
            'len': 0,
            'serverTime': '2023-04-06T21:11:31.677Z'
        }
        """
        return self._get_historical_events(
            endpoint="/api/history/v2/executions",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
        )

    def get_order_events(
        self: "User",
        before: Optional[int] = None,
        continuation_token: Optional[str] = None,
        since: Optional[int] = None,
        sort: Optional[str] = None,
        tradeable: Optional[str] = None,
    ) -> dict:
        """
        Retriev information about the user-specific order events including opened, closed, filled, etc.
        The returned ``continuation_token`` can be used to request more data.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-order-events

        :param before: Filter by time
        :type before: int, optional
        :param continuation_token: Token that can be used to continue requesting historical events
        :type continuation_token: str, optional
        :param since: Filter by a specifying a start point
        :type since: int, optional
        :param sort: Sort the results
        :type sort: str, optional
        :param tradeable: The asset to filter for
        :type tradeable: str, optional
        :return: The user-specific order events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the user's historical order events

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_order_events(tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc")
            {
                'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                'continuationToken': 'simb178',
                'elements': [{
                    'event': {
                        'OrderPlaced': {
                            'order': {
                                'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0',
                                'direction': 'Sell',
                                'filled': '12.011',
                                'lastUpdateTimestamp': 1605126171852,
                                'limitPrice': '28900.0',
                                'orderType': 'string',
                                'quantity': '13.12',
                                'reduceOnly': false,
                                'timestamp': 1605126171852,
                                'tradeable': 'pi_xbtusd',
                                'uid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0'
                            },
                            'reason': 'string',
                            'reducedQuantity': 'string'
                        }
                    },
                    'timestamp': 1605126171852,
                    'uid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0'
                }, ...
            ],
            'len': 10,
            'serverTime': '2023-04-05T12:31:42.677Z'
        }
        """
        return self._get_historical_events(
            endpoint="/api/history/v2/orders",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
        )

    def get_trigger_events(
        self: "User",
        before: Optional[int] = None,
        continuation_token: Optional[str] = None,
        since: Optional[int] = None,
        sort: Optional[str] = None,
        tradeable: Optional[str] = None,
    ) -> dict:
        """
        Retrieve information about trigger events.

        The returned ``continuation_token`` can be used to request more data.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-trigger-events

        :param before: Filter by time
        :type before: int, optional
        :param continuation_token: Token that can be used to continue requesting historical events
        :type continuation_token: str, optional
        :param since: Filter by a specifying a start point
        :type since: int, optional
        :param sort: Sort the results
        :type sort: str, optional
        :param tradeable: The asset to filter for
        :type tradeable: str, optional
        :return: The user-specific trigger events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures User: Get the user's historical trigger events

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_trigger_events(tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc")
            {
                "accountUid": "f7d5571c-6d10-4cf1-944a-048d25682ed0",
                "continuationToken": "c3RyaW5n",
                "elements": [{
                    "event": {
                        "OrderTriggerPlaced": {
                            "order": {
                                "accountId": 0.0,
                                "accountUid": "f7d5571c-6d10-4cf1-944a-048d25682ed0",
                                "direction": "Buy",
                                "lastUpdateTimestamp": 1605126171852,
                                "limitPrice": "29000.0",
                                "orderType": "lmt",
                                "quantity": "1.0",
                                "reduceOnly": false,
                                "timestamp": 1605126171852,
                                "tradeable": "pi_xbtusd",
                                "triggerOptions": {
                                    "trailingStopOptions": {
                                        "maxDeviation": "0.1",
                                        "unit": "Percent"
                                    },
                                    "triggerPrice": "29200.0",
                                    "triggerSide": "Sell",
                                    "triggerSignal": "trade"
                                },
                                "uid": "f7d5571c-6d10-4cf1-944a-048d25682ed0"
                            },
                            "reason": "maxDeviation triggered"
                        }
                    },
                    "timestamp": 1605126171852,
                    "uid": "f7d5571c-6d10-4cf1-944a-048d25682ed0"
                }, ...
            ],
            "len": 10,
            "serverTime": "2022-03-31T20:38:53.677Z"
        }
        """
        return self._get_historical_events(
            endpoint="/api/history/v2/triggers",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
        )

    def get_open_positions(self: "User") -> dict:
        """
        List the open positions of the user.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-positions

        :return: Information about the open positions
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Get the user's open positions

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.get_open_positions()
            {
                'result': 'success',
                'openPositions': [
                    {
                        'side': 'short',
                        'symbol': 'pi_xbtusd',
                        'price': 27523.749993345933,
                        'fillTime': '2023-04-05T12:31:21.410Z',
                        'size': 8000,
                        'unrealizedFunding': 0.00005879463852989987
                    },
                ],
                'serverTime': '2023-04-06T16:12:15.410Z'
            }
        """
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/derivatives/api/v3/openpositions", auth=True
        )

    def get_open_orders(self: "User") -> dict:
        """
        Retrieve the open orders.

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-get-open-orders

        :return: The open futures positions/orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Get open orders

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.get_open_orders()
            {
                'result': 'success',
                'openOrders': [{
                    'order_id': '2ce038ae-c144-4de7-a0f1-82f7f4fca864',
                    'symbol': 'pi_ethusd',
                    'side': 'buy',
                    'orderType': 'lmt',
                    'limitPrice': 1200,
                    'unfilledSize': 100,
                    'receivedTime': '2023-04-07T15:18:04.699Z',
                    'status': 'untouched',
                    'filledSize': 0,
                    'reduceOnly': False,
                    'lastUpdateTime': '2023-04-07T15:18:04.699Z'
                }, {
                    'order_id': 'c8135f52-2a86-4e26-b629-43cc37da9dbf',
                    'symbol': 'pi_ethusd',
                    'side': 'buy',
                    'orderType': 'take_profit',
                    'limitPrice': 1860,
                    'stopPrice': 1880.4,
                    'unfilledSize': 10,
                    'receivedTime': '2023-04-07T15:14:25.995Z',
                    'status': 'untouched',
                    'filledSize': 0,
                    'reduceOnly': False,
                    'triggerSignal': 'last',
                    'lastUpdateTime': '2023-04-07T15:14:25.995Z'
                }, {
                    'order_id': 'e58ed100-1fb8-4e6c-a5ea-1cf85b0f0654',
                    'symbol': 'pi_ethusd',
                    'side': 'buy',
                    'orderType': 'take_profit',
                    'limitPrice': 1860,
                    'stopPrice': 1880.4,
                    'unfilledSize': 10,
                    'receivedTime': '2023-04-07T15:12:08.131Z',
                    'status': 'untouched',
                    'filledSize': 0,
                    'reduceOnly': False,
                    'triggerSignal': 'last',
                    'lastUpdateTime': '2023-04-07T15:12:08.131Z'
                }, {
                    'order_id': 'c8776f6e-c29e-4c6a-83ee-2d3cc6781cda',
                    'symbol': 'pf_ethusd',
                    'side': 'buy',
                    'orderType': 'take_profit',
                    'limitPrice': 1860,
                    'stopPrice': 5,
                    'unfilledSize': 0.5,
                    'receivedTime': '2023-04-07T14:57:37.849Z',
                    'status': 'untouched',
                    'filledSize': 0,
                    'reduceOnly': True,
                    'triggerSignal': 'last',
                    'lastUpdateTime': '2023-04-07T14:57:37.849Z'
                }, ...],
                'serverTime': '2023-04-07T15:30:29.911Z'
            }
        """
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/derivatives/api/v3/openorders", auth=True
        )

    def check_trading_enabled_on_subaccount(self: "User", subaccountUid: str) -> dict:
        """
        Checks if trading is enabled or disabled on the specified subaccount.

        Requires the ``General API - Full Access`` permission in the API key settings.

        This endpoint is only available for institutional clients and is not tested so far and
        results in ``KrakenAuthenticationError``.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-other-check-if-a-subaccount-has-trading-enabled-or-disabled

        :return: The open futures positions/orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Check if trading is enabled on a subaccount

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.set_trading_on_subaccount(
            ...    subaccountUid="778387bh61b-f990-4128-16a7-f4ab669a9b",
            ... )
            {
               "tradingEnabled": False
            }
        """
        return self._request(  # type: ignore[return-value]
            method="GET",
            uri=f"/derivatives/api/v3/subaccount/{subaccountUid}/trading-enabled",
            auth=True,
        )

    def set_trading_on_subaccount(
        self: "User", subaccountUid: str, trading_enabled: bool
    ) -> dict:
        """
        Enable or disable trading on a subaccount.

        Requires the ``General API - Full Access`` permission in the API key settings.

        This endpoint is only available for institutional clients and is not tested so far and
        always results in ``INTERNAL_SERVER_ERROR``.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-other-enable-or-disable-trading-on-a-subaccount

        :return: The open futures positions/orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Dis-/Enable trading on a subaccount

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.set_trading_on_subaccount(
            ...    subaccountUid="778387bh61b-f990-4128-16a7-f4ab669a9b",
            ...    trading_enabled=True
            ... )
            {
                "tradingEnabled": True
            }
        """
        return self._request(  # type: ignore[return-value]
            method="PUT",
            uri=f"/derivatives/api/v3/subaccount/{subaccountUid}/trading-enabled",
            post_params={"tradingEnabled": trading_enabled},
            auth=True,
        )
