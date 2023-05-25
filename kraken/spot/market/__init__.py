#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Spot market client"""

from binascii import crc32
from collections import OrderedDict
from functools import lru_cache
from typing import Dict, List, Optional, Union

from ...base_api import KrakenBaseSpotAPI, defined, ensure_string
from ..websocket import KrakenSpotWSClient


class Market(KrakenBaseSpotAPI):
    """
    Class that implements the Kraken Spot Market client. Can be used to access
    the Kraken Spot market data.

    :param key:  Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Kraken API (default: https://api.kraken.com)
    :type url: str, optional
    :param sandbox: Use the sandbox (not supported for Spot trading so far, default: ``False``)
    :type sandbox: bool, optional

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

    def __init__(
        self: "Market",
        key: str = "",
        secret: str = "",
        url: str = "",
    ) -> None:
        super().__init__(key=key, secret=secret, url=url)

    def __enter__(self: "Market") -> "Market":
        super().__enter__()
        return self

    @ensure_string("assets")
    @lru_cache()
    def get_assets(
        self: "Market",
        assets: Optional[Union[str, List[str]]] = None,
        aclass: Optional[str] = None,
    ) -> dict:
        """
        Get information about one or more assets.
        If ``assets`` is not specified, all assets will be returned.

        - https://docs.kraken.com/rest/#operation/getAssetInfo

        This function uses caching. Run ``get_assets.cache_clear()`` to clear.

        :param assets: Filter by asset(s)
        :type assets: str | List[str], optional
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
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/public/Assets", params=params, auth=False
        )

    @ensure_string("pair")
    @lru_cache()
    def get_asset_pairs(
        self: "Market",
        pair: Optional[Union[str, List[str]]] = None,
        info: Optional[str] = None,
    ) -> dict:
        """
        Get information about a single or multiple asset/currency pair(s).
        If ``pair`` is left blank, all currency pairs will be returned.

        - https://docs.kraken.com/rest/#operation/getTradableAssetPairs

        This function uses caching. Run ``get_asset_pairs.cache_clear()`` to clear.

        :param pair: Filter by asset pair(s)
        :type pair: str | List[str], optional
        :param info: Filter by info, can be one of: ``info`` (all info), ``leverage``
            (leverage info), ``fees`` (fee info), and ``margin`` (margin info)
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
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/public/AssetPairs", params=params, auth=False
        )

    @ensure_string("pair")
    def get_ticker(
        self: "Market", pair: Optional[Union[str, List[str]]] = None
    ) -> dict:
        """
        Returns all tickers if pair is not specified - else just
        the ticker of the ``pair``. Multiple pairs can be specified.

        https://docs.kraken.com/rest/#operation/getTickerInformation

        :param pair: Filter by pair(s)
        :type pair: str | List[str], optional
        :return: The ticker(s) including ask, bid, close, volume, vwap, high, low, todays open and more
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
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/public/Ticker", params=params, auth=False
        )

    def get_ohlc(
        self: "Market",
        pair: str,
        interval: Union[int, str] = 1,
        since: Optional[Union[int, str]] = None,
    ) -> dict:
        """
        Get the open, high, low, and close data for a specific trading pair.
        Returns at max 720 time stamps per request.

        - https://docs.kraken.com/rest/#operation/getOHLCData

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
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/public/OHLC", params=params, auth=False
        )

    def get_order_book(self: "Market", pair: str, count: Optional[int] = 100) -> dict:
        """
        Get the current orderbook of a specified trading pair.

        - https://docs.kraken.com/rest/#operation/getOrderBook

        :param pair: The pair to get the orderbook from
        :type pair: str
        :param count: Number of asks and bids, must be one of {1..500} (default: ``100``)
        :type count: int, optional

        :return:
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the order book

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
        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/public/Depth",
            params={"pair": pair, "count": count},
            auth=False,
        )

    def get_recent_trades(
        self: "Market", pair: str, since: Optional[Union[str, int]] = None
    ) -> dict:
        """
        Get the latest trades for a specific trading pair (up to 1000).

        - https://docs.kraken.com/rest/#operation/getRecentTrades

        :param pair: Pair to get the recent trades
        :type pair: str
        :param since: Filter trades since given timestamp (default: ``None``)
        :type since: str | int, optional
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
            params["since"] = None
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/public/Trades", params=params, auth=False
        )

    def get_recent_spreads(
        self: "Market", pair: str, since: Optional[Union[str, int]] = None
    ) -> dict:
        """
        Get the latest spreads for a specific trading pair.

        - https://docs.kraken.com/rest/#operation/getRecentSpreads

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
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/public/Spread", params=params, auth=False
        )

    def get_system_status(self: "Market") -> dict:
        """
        Returns the system status of the Kraken Spot API.

        - https://docs.kraken.com/rest/#section/General-Usage/Requests-Responses-and-Errors

        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Market: Get the Kraken API system status

            >>> from kraken.spot import Market
            >>> Market().get_system_status()
            {'status': 'online', 'timestamp': '2023-04-05T17:12:31Z'}
        """
        return self._request(  # type: ignore[return-value]
            method="GET", uri="/public/SystemStatus", auth=False
        )


class SpotOrderBookClient(KrakenSpotWSClient):
    """
    The SpotOrderBookClient class inherit the subscribe function from the
    KrakenSpotWSClient class. The subscribe function must be used to
    subscribe to one or multiple order books. The feed will initially
    send the current order book and then send updates when anything
    changes.

    NOTE: This class has a fixed depth.

    References

    - https://support.kraken.com/hc/en-us/articles/360027821131-WebSocket-API-v1-How-to-maintain-a-valid-order-book

    - https://docs.kraken.com/websockets/#book-checksum
    """

    def __init__(self: "SpotOrderBookClient", depth: int = 10) -> None:
        super().__init__()
        self.__book: Dict[str, dict] = {}
        self.__depth: int = depth

    async def on_message(self: "SpotOrderBookClient", msg: Union[list, dict]) -> None:
        """
        The on_message function is implemented in the KrakenSpotWSClient
        class and used as callback to receive all messages sent by the
        Kraken API.
        """
        if "errorMessage" in msg:
            self.LOG.warning(msg)

        if "event" in msg and isinstance(msg, dict):
            # ignore heartbeat / ping - pong messages / any event message
            # ignore errors since they are handled by the parent class
            # just handle the removal of an order book
            if (
                msg["event"] == "subscriptionStatus"
                and "status" in msg
                and "pair" in msg
                and msg["status"] == "unsubscribed"
                and msg["pair"] in self.__book
            ):
                del self.__book[msg["pair"]]
                return

        if not isinstance(msg, list):
            # The order book feed only sends messages with type list,
            # so we can ignore anything else.
            return

        pair: str = msg[-1]
        if pair not in self.__book:
            self.__book[pair] = {
                "bid": {},
                "ask": {},
                "valid": True,
            }

        if "as" in msg[1]:
            # This will be triggered initially when the
            # first message comes in that provides the initial snapshot
            # of the current order book.
            self.__update_book(pair=pair, side="ask", snapshot=msg[1]["as"])
            self.__update_book(pair=pair, side="bid", snapshot=msg[1]["bs"])
        else:
            checksum: Optional[str] = None
            # This is executed every time a new update comes in.
            for data in msg[1 : len(msg) - 2]:
                if "a" in data:
                    self.__update_book(pair=pair, side="ask", snapshot=data["a"])
                elif "b" in data:
                    self.__update_book(pair=pair, side="bid", snapshot=data["b"])
                if "c" in data:
                    checksum = data["c"]

            self.__validate_checksum(pair=pair, checksum=checksum)

        await self.on_book_update(pair=pair, message=msg)

    async def on_book_update(
        self: "SpotOrderBookClient", pair: str, message: list
    ) -> None:
        """
        This function will be called every time the order book gets updated.
        It needs to be overloaded.

        :param pair: The currency pair of the order book that has
            been updated.
        :type pair: str
        """
        print(
            "Please overload this function to receive the information"
            " about updated entries within the order book."
        )

    async def add_book(self: "SpotOrderBookClient", pairs: List[str]) -> None:
        """
        Add an order book to this client. The feed will be subscribed
        and updates will be published to the :func:`on_book_update` function.

        :param pairs: The pair(s) to subscribe to
        :type pairs: List[str]
        :param depth: The book depth
        :type depth: int
        """
        await self.subscribe(
            subscription={"name": "book", "depth": self.__depth}, pair=pairs
        )

    async def remove_book(self: "SpotOrderBookClient", pairs: List[str]) -> None:
        """
        Unsubscribe from a subscribed order book.

        :param pairs: The pair(s) to unsubscribe from
        :type pairs: List[str]
        :param depth: The book depth
        :type depth: int
        """
        await self.unsubscribe(
            subscription={"name": "book", "depth": self.__depth}, pair=pairs
        )

    @property
    def depth(self: "SpotOrderBookClient") -> int:
        """
        Return the fixed depth of this order book client.
        """
        return self.__depth

    def get(self: "SpotOrderBookClient", pair: str) -> Optional[dict]:
        """
        Returns the order book for a specific ``pair``.

        :param pair: The pair to get the order book from
        :type pair: str
        :return: The order book of that ``pair``.
        :rtype: dict
        """
        return self.__book.get(pair)

    def __update_book(
        self: "SpotOrderBookClient", pair: str, side: str, snapshot: list
    ) -> None:
        """
        This functions updates the local order book based on the
        information provided in ``data`` and assigns/update the
        asks and bids in book.

        The ``data`` here looks like:
        [
            ['25026.00000', '2.77183035', '1684658128.013525'],
            ['25028.50000', '0.04725650', '1684658121.180535'],
            ['25030.20000', '0.29527502', '1684658128.018182'],
            ['25030.40000', '2.77134976', '1684658131.751539'],
            ['25032.20000', '0.13978808', '1684658131.751577']
        ]
        ... where the first value is the ask or bid price, the second
            represents the volume and the last one is the time stamp.

        :param side: The side to assign the data to,
            either ``ask`` or ``bid``
        :type side: str
        :param data: The data that needs to be assigned.
        :type data: list
        """
        for entry in snapshot:
            price: str = entry[0]
            volume: str = entry[1]

            if float(volume) > 0.0:
                # Price level exist or is new
                self.__book[pair][side][price] = volume
            else:
                # Price level moved out of range
                self.__book[pair][side].pop(price)

            if side == "ask":
                self.__book[pair]["ask"] = OrderedDict(
                    sorted(self.__book[pair]["ask"].items(), key=self.get_first)[
                        : self.__depth
                    ]
                )

            elif side == "bid":
                self.__book[pair]["bid"] = OrderedDict(
                    sorted(
                        self.__book[pair]["bid"].items(),
                        key=self.get_first,
                        reverse=True,
                    )[: self.__depth]
                )

    def __validate_checksum(
        self: "SpotOrderBookClient", pair: str, checksum: str
    ) -> None:
        """
        Function that validates the checksum of the order book as described here
        https://docs.kraken.com/websockets/#book-checksum.

        :param pair: The pair that's order book checksum should be validated.
        :type pair: str
        :param checksum: The checksum sent by the Kraken API
        :type checksum: str
        """
        book: dict = self.__book[pair]

        # sort ask (desc) and bid (asc)
        ask: List[tuple] = sorted(book["ask"].items(), key=self.get_first)
        bid: List[tuple] = sorted(
            book["bid"].items(),
            key=self.get_first,
            reverse=True,
        )

        local_checksum: str = ""
        for price_level, volume in ask[:10]:
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".", ""
            ).lstrip("0")

        for price_level, volume in bid[:10]:
            local_checksum += price_level.replace(".", "").lstrip("0") + volume.replace(
                ".", ""
            ).lstrip("0")

        self.__book[pair]["valid"] = checksum == str(crc32(local_checksum.encode()))
        # assert self.__book[pair]["valid"]

    @staticmethod
    def get_first(values: tuple) -> float:
        """
        This function is used as callback for the ``sorted`` method
        to sort a tuple/list by its first value and while ensuring
        that the values are floats and comparable.

        :param values: A tuple of string values
        :type values: tuple
        :return: The first value of ``values`` as float.
        :rtype: float
        """
        return float(values[0])
