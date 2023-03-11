#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Spot market client"""
from kraken.base_api.base_api import KrakenBaseSpotAPI


class MarketClient(KrakenBaseSpotAPI):
    """Class that implements the Kraken Spot market client"""

    def get_assets(self, assets=None, aclass: str = None) -> dict:
        """https://docs.kraken.com/rest/#operation/getAssetInfo"""
        params = {}
        if assets is not None:
            params["asset"] = self._to_str_list(assets)
        if aclass is not None:
            params["aclass"] = aclass
        return self._request(
            method="GET", uri="/public/Assets", params=params, auth=False
        )

    def get_tradable_asset_pair(self, pair: str, info=None) -> dict:
        """https://docs.kraken.com/rest/#operation/getTradableAssetPairs"""
        params = {}
        params["pair"] = self._to_str_list(pair)
        if info is not None:
            params["info"] = info

        return self._request(
            method="GET", uri="/public/AssetPairs", params=params, auth=False
        )

    def get_ticker(self, pair: str = None) -> dict:
        """https://docs.kraken.com/rest/#operation/getTickerInformation"""
        params = {}
        if pair is not None:
            params["pair"] = self._to_str_list(pair)
        return self._request(
            method="GET", uri="/public/Ticker", params=params, auth=False
        )

    def get_ohlc(self, pair: str, interval: int = None, since: int = None) -> dict:
        """https://docs.kraken.com/rest/#operation/getOHLCData"""
        params = {"pair": pair}
        if interval is not None:
            params["interval"] = interval
        if since is not None:
            params["since"] = since
        return self._request(
            method="GET", uri="/public/OHLC", params=params, auth=False
        )

    def get_order_book(self, pair: str, count=None) -> dict:
        """https://docs.kraken.com/rest/#operation/getOrderBook"""
        params = {"pair": pair}
        if count is not None:
            params["count"] = count
        return self._request(
            method="GET", uri="/public/Depth", params=params, auth=False
        )

    def get_recent_trades(self, pair: str, since=None) -> dict:
        """https://docs.kraken.com/rest/#operation/getRecentTrades"""
        params = {"pair": pair}
        if since is not None:
            params["since"] = None
        return self._request(
            method="GET", uri="/public/Trades", params=params, auth=False
        )

    def get_recend_spreads(self, pair: str, since=None) -> dict:
        """https://docs.kraken.com/rest/#operation/getRecentSpreads"""
        params = {"pair": pair}
        if since is not None:
            params["since"] = since
        return self._request(
            method="GET", uri="/public/Spread", params=params, auth=False
        )

    def get_system_status(self) -> dict:
        """Returns the system status of the Kraken API"""
        return self._request(method="GET", uri="/public/SystemStatus", auth=False)
