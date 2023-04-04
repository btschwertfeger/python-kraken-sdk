#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Spot market client"""
from typing import List, Union

from kraken.base_api import KrakenBaseSpotAPI


class Market(KrakenBaseSpotAPI):
    """
    Class that implements the Kraken Spot Market client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: ``False``)
    :type sandbox: bool
    """

    def get_assets(
        self,
        assets: Union[str, List[str], None] = None,
        aclass: Union[str, None] = None,
    ) -> dict:
        """
        Get information about all available assets for trading, staking, deposit,
        and withdraw.

        (see: https://docs.kraken.com/rest/#operation/getAssetInfo)

        :param asset: Optional - Filter by asset
        :type asset: str | List[str] | None
        :param aclass: Optional - Filter by asset class
        :type aclass: str | None
        """
        params = {}
        if assets is not None:
            params["asset"] = self._to_str_list(assets)
        if aclass is not None:
            params["aclass"] = aclass
        return self._request(
            method="GET", uri="/public/Assets", params=params, auth=False
        )

    def get_tradable_asset_pair(
        self, pair: Union[str, List[str]], info: Union[str, None] = None
    ) -> dict:
        """
        Get information about the tradable asset pairs.

        (see: https://docs.kraken.com/rest/#operation/getTradableAssetPairs)

        :param asset: Filter by asset pair(s)
        :type asset: str | List[str]
        :param info: Optional - Filter by info, can be one of: `info` (all info), `leverage` (leverage info), `fees` (fee info), and `margin` (margin info)
        :type info: str | None
        """
        params = {}
        params["pair"] = self._to_str_list(pair)
        if info is not None:
            params["info"] = info

        return self._request(
            method="GET", uri="/public/AssetPairs", params=params, auth=False
        )

    def get_ticker(self, pair: Union[str, None] = None) -> dict:
        """
        Returns all ticker if pair is specified.

        (see: https://docs.kraken.com/rest/#operation/getTickerInformation)

        :param pair: Optional - Filter by pair
        :type pair: str | None
        """
        params = {}
        if pair is not None:
            params["pair"] = self._to_str_list(pair)
        return self._request(
            method="GET", uri="/public/Ticker", params=params, auth=False
        )

    def get_ohlc(
        self,
        pair: str,
        interval: Union[int, str] = 1,
        since: Union[int, str, None] = None,
    ) -> dict:
        """
        Get the open, high, low, and close data for a specific trading pair.
        Returns at max 720 time stamps per request.

        (see: https://docs.kraken.com/rest/#operation/getOHLCData)

        :param pair: The pair to get the ohlc from
        :type pair: str
        :param interval: Optional - the Interval in minutes (default: 1)
        :type interval: str | int
        :param since: Timestamp to start from
        :type since: int | str | None
        """
        params = {"pair": pair, "interval": interval}
        if since is not None:
            params["since"] = since
        return self._request(
            method="GET", uri="/public/OHLC", params=params, auth=False
        )

    def get_order_book(self, pair: str, count: int = 100) -> dict:
        """
        Get the current orderbook of a specified trading pair.

        (see: https://docs.kraken.com/rest/#operation/getOrderBook)

        :param pair: The pair to get the orderbook
        :type pair: str
        :param count: Number of asks and bids, must be one of {1...500} (default: 100)
        :type count: int
        """
        return self._request(
            method="GET",
            uri="/public/Depth",
            params={"pair": pair, "count": count},
            auth=False,
        )

    def get_recent_trades(self, pair: str, since: Union[str, int, None] = None) -> dict:
        """
        Get the latest trades for a specific trading pair (up to 1000).

        (see: https://docs.kraken.com/rest/#operation/getRecentTrades)

        :param pair: Pair to get the recend trades
        :type pair: str
        :param since: Filter trades since given timestamp (default: None)
        :type str | int | None
        """
        params = {"pair": pair}
        if since is not None:
            params["since"] = None
        return self._request(
            method="GET", uri="/public/Trades", params=params, auth=False
        )

    def get_recend_spreads(
        self, pair: str, since: Union[str, int, None] = None
    ) -> dict:
        """
        Get the latest spreads for a specific trading pair.

        (see: https://docs.kraken.com/rest/#operation/getRecentSpreads)

        :param pair: Pair to get the recend spreads
        :type pair: str
        :param since: Filter trades since given timestamp (default: None)
        :type str | int | None
        """
        params = {"pair": pair}
        if since is not None:
            params["since"] = since
        return self._request(
            method="GET", uri="/public/Spread", params=params, auth=False
        )

    def get_system_status(self) -> dict:
        """
        Returns the system status of the Kraken Spot API

        (see: https://docs.kraken.com/rest/#section/General-Usage/Requests-Responses-and-Errors)
        """
        return self._request(method="GET", uri="/public/SystemStatus", auth=False)
