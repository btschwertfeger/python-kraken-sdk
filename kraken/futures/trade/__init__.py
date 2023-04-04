#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Futures trade client"""
from typing import List

from kraken.base_api import KrakenBaseFuturesAPI


class Trade(KrakenBaseFuturesAPI):
    """
    Class that implements the Kraken Futures trade client

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

    def get_fills(self, lastFillTime: str = None) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-data-get-your-fills)"""
        query_params = {}
        if lastFillTime:
            query_params["lastFillTime"] = lastFillTime
        return self._request(
            method="GET",
            uri="/derivatives/api/v3/fills",
            query_params=query_params,
            auth=True,
        )

    def create_batch_order(self, batchorder_list: List[dict]) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-batch-order-management)"""
        batchorder = {"batchOrder": batchorder_list}
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/batchorder",
            post_params={"json": f"{batchorder}"},
            auth=True,
        )

    def cancel_all_orders(self, symbol: str = None) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-all-orders)"""
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/cancelallorders",
            post_params=params,
            auth=True,
        )

    def dead_mans_switch(self, timeout: int = 60) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-dead-man-39-s-switch)"""
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/cancelallordersafter",
            post_params={"timeout": timeout},
        )

    def cancel_order(self, order_id: str = "", cliOrdId: str = "") -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-order)"""

        params = {}
        if order_id != "":
            params["order_id"] = order_id
        elif cliOrdId != "":
            params["cliOrdId"] = cliOrdId
        else:
            raise ValueError("Either order_id or cliOrdId must be set!")

        return self._request(
            method="POST",
            uri="/derivatives/api/v3/cancelorder",
            post_params=params,
            auth=True,
        )

    def edit_order(
        self,
        orderId: str = None,
        cliOrdId: str = None,
        limitPrice: float = None,
        size: float = None,
        stopPrice: float = None,
    ) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-edit-order)"""
        if orderId == "" and cliOrdId == "":
            raise ValueError("Either orderId or cliOrdId must be set!")

        params = {}
        if orderId != "":
            params["orderId"] = orderId
        elif cliOrdId != "":
            params["cliOrdId"] = cliOrdId
        if limitPrice is not None:
            params["limitPrice"] = limitPrice
        if size is not None:
            params["size"] = size
        if stopPrice is not None:
            params["stopPrice"] = stopPrice
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/editorder",
            post_params=params,
            auth=True,
        )

    def get_orders_status(
        self, orderIds: List[str] = None, cliOrdIds: List[str] = None
    ) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-get-the-current-status-for-specific-orders)"""
        if orderIds is None and cliOrdIds is None:
            raise ValueError("Either orderIds or cliOrdIds must be specified!")

        params = {}
        if orderIds is not None:
            params["orderIds"] = orderIds
        elif cliOrdIds is not None:
            params["cliOrdIds"] = cliOrdIds
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/orders/status",
            post_params=params,
            auth=True,
        )

    def create_order(
        self,
        orderType: str,
        size: float,
        symbol: str,
        side: str,
        cliOrdId: str = None,
        limitPrice: float = None,
        reduceOnly: bool = None,
        stopPrice: float = None,
        triggerSignal: str = None,
    ) -> dict:
        """(see: https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order)"""

        order_types = ("lmt", "post", "ioc", "mkt", "stp", "take_profit")
        if orderType not in order_types:
            raise ValueError(f"Invalid orderType. One of [{order_types}] is required!")
        sides = ("buy", "sell")
        if side not in sides:
            raise ValueError(f"Invalid side. One of [{sides}] is required!")

        params = {"orderType": orderType, "side": side, "size": size, "symbol": symbol}
        if cliOrdId is not None:
            params["cliOrdId"] = cliOrdId
        if reduceOnly is not None:
            params["reduceOnly"] = reduceOnly
        if orderType in ["post", "lmt"]:
            if limitPrice is None:
                raise ValueError(
                    f"No limitPrice specified for order of type {orderType}!"
                )
            params["limitPrice"] = limitPrice
        elif orderType in ["stp", "take_profit"]:
            if stopPrice is None:
                raise ValueError(
                    f"Parammeter stopPrice must be set if orderType {orderType}!"
                )
            if triggerSignal is None:
                raise ValueError(
                    f"Parammeter triggerSignal must be set if orderType {orderType}!"
                )
        if stopPrice is not None:
            params["stopPrice"] = stopPrice
        if triggerSignal is not None:
            trigger_signals = ("mark", "spot", "last")
            if triggerSignal not in trigger_signals:
                raise ValueError(f"Trigger signal must be in [{trigger_signals}]!")
            params["triggerSignal"] = triggerSignal

        return self._request(
            method="POST",
            uri="/derivatives/api/v3/sendorder",
            post_params=params,
            auth=True,
        )
