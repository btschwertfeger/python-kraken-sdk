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

    :param key: Futures API public key (default: "")
    :type key: str
    :param secret: Futures API secret key (default: "")
    :type secret: str
    :param url: The url to access the Futures Kraken API (default: https://futures.kraken.com)
    :type url: str
    :param sandbox: If set to true the url will be https://demo-futures.kraken.com
    :type sandbox: bool
    """

    def __init__(
        self, key: str = "", secret: str = "", url: str = "", sandbox: bool = False
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_wallets(self) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-wallets)"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/accounts", auth=True
        )

    def get_open_orders(self) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-orders)"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/openorders", auth=True
        )

    def get_open_positions(self) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-positions)"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/openpositions", auth=True
        )

    def get_subaccounts(self) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-subaccounts)"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/subaccounts", auth=True
        )

    def get_unwindqueue(self) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-position-percentile-of-unwind-queue)"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/unwindqueue", auth=True
        )

    def get_notificatios(self) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-general-get-notifications)"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/notifications", auth=True
        )

    def get_account_log(
        self,
        before: int = None,
        count: str = None,
        from_: str = None,
        info: str = None,
        since: str = None,
        sort: str = None,
        to: str = None,
    ) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-history-account-log)"""
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

    def get_account_log_csv(self) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-history-account-log-get-recent-account-log-csv)"""

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
            >>> user.get_execution_events(tradeable="PF_SOLUSD", since=1668989233, before=1668999999, sort="asc")
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
