#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfegerr
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Futures user client"""
from kraken.base_api.base_api import KrakenBaseFuturesAPI


class UserClient(KrakenBaseFuturesAPI):
    """Class that implements the Kraken Futures user client"""

    def __init__(
        self, key: str = "", secret: str = "", url: str = "", sandbox: bool = False
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_wallets(self) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-wallets"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/accounts", auth=True
        )

    def get_open_orders(self) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-orders"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/openorders", auth=True
        )

    def get_open_positions(self) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-positions"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/openpositions", auth=True
        )

    def get_subaccounts(self) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-subaccounts"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/subaccounts", auth=True
        )

    def get_unwindqueue(self) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-position-percentile-of-unwind-queue"""
        return self._request(
            method="GET", uri="/derivatives/api/v3/unwindqueue", auth=True
        )

    def get_notificatios(self) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-general-get-notifications"""
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
        """https://docs.futures.kraken.com/#http-api-history-account-log"""
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
        """https://docs.futures.kraken.com/#http-api-history-account-log-get-recent-account-log-csv"""
        return self._request(
            method="GET",
            uri="/api/history/v2/accountlogcsv",
            auth=True,
            return_raw=True,
        )
