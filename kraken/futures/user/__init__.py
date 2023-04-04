#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Futures user client"""
from typing import Union

from kraken.base_api import KrakenBaseFuturesAPI


class User(KrakenBaseFuturesAPI):
    """
    Class that implements the Kraken Futures user client

    If the sandbox environment is chosen, the keys must be generated from here:
        https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str
    :param url: The url to access the Futures Kraken API (default: https://futures.kraken.com)
    :type url: str
    :param sandbox: If set to ``True`` the url will be https://demo-futures.kraken.com
    :type sandbox: bool

    .. code-block:: python
        :linenos:
        :caption: Example

        >>> from kraken.futures import User
        >>> user = User() # unauthenticated
        >>> user = User(key="api-key", secret="secret-key") # authenticated
    """

    def __init__(
        self, key: str = "", secret: str = "", url: str = "", sandbox: bool = False
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_wallets(self) -> dict:
        """
        Lists the current wallet balances of the user.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-wallets

        :return: Information about the current balances of the user
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_wallets()
            {
                "result": "success",
                "accounts": {
                    "fi_xbtusd": {
                    "auxiliary": {
                        "usd": 0,
                        "pv": 0.0,
                        "pnl": 0.0,
                        "af": 0.0,
                        "funding": 0.0
                    },
                    "marginRequirements": { "im": 0.0, "mm": 0.0, "lt": 0.0, "tt": 0.0 },
                    "triggerEstimates": { "im": 0, "mm": 0, "lt": 0, "tt": 0 },
                    "balances": { "xbt": 0.0 },
                    "currency": "xbt",
                    "type": "marginAccount"
                    },
                    "cash": {
                    "balances": {
                        "eur": 4567.7117591172,
                        "gbp": 4002.4975584765,
                        "bch": 39.3081761006,
                        "usd": 5000.0,
                        "xrp": 10055.1019587339,
                        "eth": 2.6868286287,
                        "usdt": 4999.3200924674,
                        "usdc": 4999.8300057798,
                        "ltc": 53.9199827456,
                        "xbt": 0.1785169809
                    },
                    "type": "cashAccount"
                    },
                    "flex": {
                    "currencies": {},
                    "initialMargin": 0.0,
                    "initialMarginWithOrders": 0.0,
                    "maintenanceMargin": 0.0,
                    "balanceValue": 0.0,
                    "portfolioValue": 0.0,
                    "collateralValue": 0.0,
                    "pnl": 0.0,
                    "unrealizedFunding": 0.0,
                    "totalUnrealized": 0.0,
                    "totalUnrealizedAsMargin": 0.0,
                    "availableMargin": 0.0,
                    "marginEquity": 0.0,
                    "type": "multiCollateralMarginAccount"
                    }
                },
                "serverTime": "2023-04-04T17:56:49.027Z"
            }
        """
        return self._request(
            method="GET", uri="/derivatives/api/v3/accounts", auth=True
        )

    def get_open_orders(self) -> dict:
        """
        List the open orders of the user.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-orders

        :return: Information about the open orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_open_orders()
            {'result': 'success', 'openOrders': [], 'serverTime': '2023-04-04T18:01:39.729Z'}
        """
        return self._request(
            method="GET", uri="/derivatives/api/v3/openorders", auth=True
        )

    def get_open_positions(self) -> dict:
        """
        List the open positions of the user.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-positions

        :return: Information about the open positions
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_open_positions()
            'result': 'success', 'openPositions': [], 'serverTime': '2023-04-04T18:02:44.132Z'}
        """

        return self._request(
            method="GET", uri="/derivatives/api/v3/openpositions", auth=True
        )

    def get_subaccounts(self) -> dict:
        """
        List the subaccounts of the user.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-subaccounts

        :return: Information about the user owned subaccounts
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET", uri="/derivatives/api/v3/subaccounts", auth=True
        )

    def get_unwindqueue(self) -> dict:
        """
        Retrieve information about the percentile of the open position in case of unwinding.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-position-percentile-of-unwind-queue

        :return: Information about unwindqueue
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        return self._request(
            method="GET", uri="/derivatives/api/v3/unwindqueue", auth=True
        )

    def get_notificatios(self) -> dict:
        """
        Retrieve the latest notifications from the Kraken Futures API

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-general-get-notifications

        :return: Notifications
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_notificatios()
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
        return self._request(
            method="GET", uri="/derivatives/api/v3/notifications", auth=True
        )

    def get_account_log(
        self,
        before: Union[str, int, None] = None,
        count: Union[str, int, None] = None,
        from_: Union[str, int, None] = None,
        info: Union[str, None] = None,
        since: Union[str, int, None] = None,
        sort: Union[str, None] = None,
        to: Union[str, None] = None,
    ) -> dict:
        """

        - https://docs.futures.kraken.com/#http-api-history-account-history-get-account-log

        :param before: Optional - Filter to only return results before a specific timestamp or date
        :type before: str | int | None
        :param count: Optional - Define the maximum number of results (max: ``500``)
        :type count: str | int | None
        :param from_: Optional - Define the first id to start with
        :type from_: str | int | None
        :param info: Optional - Filter by info (e.g.,: ``futures liquidation``)
        :type info: str | None
        :param since: Optinoal - Define the first entry to begin with by item
        :type since: str | int | None
        :param sort: Optional - Sort the results
        :type sort: str | None
        :param to: Optional - Id of the last entry
        :type to: str | None
        :return: The account log
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        params = {}
        if before is not None:
            params["before"] = before
        if count is not None:
            params["count"] = count
        if from_ is not None:
            params["from"] = from_
        if info is not None:
            params["info"] = info
        if since is not None:
            params["since"] = since
        if sort is not None:
            params["sort"] = sort
        if to is not None:
            params["to"] = to
        return self._request(
            method="GET",
            uri="/api/history/v2/account-log",
            query_params=params,
            auth=True,
        )

    def get_account_log_csv(self):
        """
        Return the account log as csv, for example to export it.

        - https://docs.futures.kraken.com/#http-api-history-account-log-get-recent-account-log-csv

        :return: raw chunked response

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> response = user.get_account_log_csv()
            >>> with open(f"account_log.csv", "wb") as file:
            ...     for chunk in response.iter_content(chunk_size=512):
            ...         if chunk:
            ...             file.write(chunk)
        """

        return self._request(
            method="GET",
            uri="/api/history/v2/accountlogcsv",
            auth=True,
            return_raw=True,
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
        Method that uses as a gateway for the methods :func:`kraken.futures.User.get_execution_events`,
        :func:`kraken.futures.User.get_order_events`, and
        :func:`kraken.futures.User.get_trigger_events`

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
        return self._request(method="GET", uri=endpoint, query_params=params, auth=auth)

    def get_execution_events(
        self,
        before: Union[int, None] = None,
        continuation_token: Union[str, None] = None,
        since: Union[int, None] = None,
        sort: Union[str, None] = None,
        tradeable: Union[str, None] = None,
    ) -> dict:
        """
        Retrieve the order/position execution events of this user. The returned ``continuation_token```
        can be used to request more data.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-execution-events

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
        :return: The user-specific execution events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_execution_events(
            ...    tradeable="PF_SOLUSD",
            ...    since=1668989233,
            ...    before=1668999999,
            ...    sort="asc"
            ... )
            {'elements': [], 'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0', 'len': 0}
        """

        return self._get_historical_events(
            endpoint="/api/history/v2/executions",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
            auth=True,
        )

    def get_order_events(
        self,
        before: Union[int, None] = None,
        continuation_token: Union[str, None] = None,
        since: Union[int, None] = None,
        sort: Union[str, None] = None,
        tradeable: Union[str, None] = None,
    ) -> dict:
        """
        Retriev information about the user-specific order events including opened, closed, filled, etc.
        The returned ``continuation_token``` can be used to request more data.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-order-events

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
        :return: The user-specific order events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_order_events(tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc")
            {'elements': [], 'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0', 'len': 0}

        """
        return self._get_historical_events(
            endpoint="/api/history/v2/orders",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
            auth=True,
        )

    def get_trigger_events(
        self,
        before: Union[int, None] = None,
        continuation_token: Union[str, None] = None,
        since: Union[int, None] = None,
        sort: Union[str, None] = None,
        tradeable: Union[str, None] = None,
    ) -> dict:
        """
        Retrieve information about trigger events.

        The returned ``continuation_token``` can be used to request more data.

        - https://docs.futures.kraken.com/#http-api-history-market-history-get-trigger-events

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
        :return: The user-specific trigger events
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_trigger_events(tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc")
            {'elements': [], 'accountUid': 'f7d5571c-6d10-4cf1-944a-048d25682ed0', 'len': 0}
        """
        return self._get_historical_events(
            endpoint="/api/history/v2/triggers",
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
            auth=True,
        )
