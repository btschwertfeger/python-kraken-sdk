#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Futures trade client"""
from typing import List, Union

from kraken.base_api import KrakenBaseFuturesAPI


class Trade(KrakenBaseFuturesAPI):
    """
    Class that implements the Kraken Futures trade client

    If the sandbox environment is chosen, the keys must be generated from here:
    https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str
    :param url: The url to access the Futures Kraken API (default: https://futures.kraken.com)
    :type url: str
    :param sandbox: If set to true the url will be https://demo-futures.kraken.com
    :type sandbox: bool

    .. code-block:: python
        :linenos:
        :caption: Example

        >>> from kraken.futures import Trade
        >>> trade = Trade() # unauthenticated
        >>> trade = Trade(key="api-key", secret="secret-key") # authenticated
    """

    def __init__(
        self, key: str = "", secret: str = "", url: str = "", sandbox: bool = False
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_fills(self, lastFillTime: Union[str, None] = None) -> dict:
        """
        Return the current fills of the user.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-data-get-your-fills

        :param lastFillTime: Optional - Filter by last filled timestamp
        :type lastFillTime: str | None
        :return: Fills
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.get_fills()
            {'result': 'success', 'fills': [], 'serverTime': '2023-04-04T16:55:47.534Z'}
        """
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
        """
        Create multiple orders at once using the batch order endpoit.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-batch-order-management

        :param batchorder_list: List of order instructions (see example below - or the linked official Kraken documentation)
        :type batchorder_list: List[dict]
        :return: Information about the submitted request
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade..create_batch_order(
                    batchorder_list=[
                        {
                            "order": "send",
                            "order_tag": "1",
                            "orderType": "lmt",
                            "symbol": "PI_XBTUSD",
                            "side": "buy",
                            "size": 5,
                            "limitPrice": 1.00,
                            "cliOrdId": "my_another_client_id",
                        },
                        {
                            "order": "send",
                            "order_tag": "2",
                            "orderType": "stp",
                            "symbol": "PI_XBTUSD",
                            "side": "buy",
                            "size": 1,
                            "limitPrice": 2.00,
                            "stopPrice": 3.00,
                        },
                        {
                            "order": "cancel",
                            "order_id": "e35d61dd-8a30-4d5f-a574-b5593ef0c050",
                        },
                        {
                            "order": "cancel",
                            "cliOrdId": "my_client_id",
                        },
                    ],
                )
            {
                'result': 'success',
                'serverTime': '2023-04-04T17:03:36.100Z',
                'batchStatus': [
                    {
                        'status': 'insufficientAvailableFunds',
                        'order_tag': '1',
                        'orderEvents': []
                    }, {
                        'status': 'placed',
                        'order_tag': '2',
                        'order_id':
                        'fc589be9-5095-48f0-b6f1-a2dfad6d9677',
                        'dateTimeReceived': '2023-04-04T17:03:36.053Z',
                        'orderEvents': [
                            {
                                'orderTrigger': {
                                    'uid': 'fc589be9-5095-48f0-b6f1-a2dfad6d9677',
                                    'clientId': None,
                                    'type': 'lmt',
                                    'symbol': 'pi_xbtusd',
                                    'side': 'buy',
                                    'quantity': 1,
                                    'limitPrice': 2.0,
                                    'triggerPrice': 3.0,
                                    'triggerSide': 'trigger_above',
                                    'triggerSignal':
                                    'last_price',
                                    'reduceOnly': False,
                                    'timestamp': '2023-04-04T17:03:36.053Z',
                                    'lastUpdateTimestamp': '2023-04-04T17:03:36.053Z',
                                    'startTime': None
                                },
                                'type': 'PLACE'
                            }
                        ]
                    }, {
                        'status': 'notFound',
                        'order_id': 'e35d61dd-8a30-4d5f-a574-b5593ef0c050',
                        'orderEvents': []
                    }, {
                        'status': 'notFound',
                        'cliOrdId': 'my_client_id',
                        'orderEvents': []
                    }
                ]
            }
        """
        batchorder = {"batchOrder": batchorder_list}
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/batchorder",
            post_params={"json": f"{batchorder}"},
            auth=True,
        )

    def cancel_all_orders(self, symbol: Union[str, None] = None) -> dict:
        """
        Cancels all open orders, can be filtered by symbol.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-all-orders

        :param symbol: Optional - Filter by symbol
        :type symbol: str | None
        :return: Information about the success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.cancel_all_orders()
            {
                'result': 'success',
                'cancelStatus': {
                    'receivedTime': '2023-04-04T17:09:09.986Z',
                    'cancelOnly': 'all',
                    'status': 'cancelled',
                    'cancelledOrders': [
                        {
                            'order_id': 'fc589be9-5095-48f0-b6f1-a2dfad6d9677'
                        }, {
                            'order_id': '0365942e-4850-4e41-90c3-a10f96f7baaf'
                        }
                    ],
                    'orderEvents': []
                },
                'serverTime': '2023-04-04T17:09:09.987Z'
            }
        """
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/cancelallorders",
            post_params=params,
            auth=True,
        )

    def dead_mans_switch(self, timeout: Union[int, None] = 0) -> dict:
        """
        The Death Man's Switch can be used to cancel all orders after a specific timeout.
        If the timeout is set to 60, all orders will be cancelled after 60 seconds. The timeout
        can be pushed back by accessing this endpoint over and over again. Set the timeout to zero
        to reset.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-dead-man-39-s-switch

        :param timeout: The timeout in seconds
        :type timeout: int | None
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.dead_mans_switch(timeout=60)
            {
                'result': 'success',
                'serverTime': '2023-04-04T17:14:34.113Z',
                'status': {
                    'currentTime': '2023-04-04T17:14:34.076Z',
                    'triggerTime': '0'
                }
            }
        """
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/cancelallordersafter",
            post_params={"timeout": timeout},
        )

    def cancel_order(
        self, order_id: Union[str, None] = None, cliOrdId: Union[str, None] = None
    ) -> dict:
        """
        This endpoint can be used to cancel a specific order by ``order_id`` or ``cliOrdId``.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-order

        :param order_id: Optional - The order_id to cancel
        :type order_id: str | None
        :param cliOrdId: Optional the client defined order id
        :type cliOrdId: str | None
        :raises ValueError: If both ``order_id`` and ``cliOrdId`` are not set
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.cancel_order(order_id="fc589be9-5095-48f0-b6f1-a2dfad6d9677")
            {
                'result': 'success',
                'cancelStatus': {
                    'status': 'notFound',
                    'receivedTime': '2023-04-04T17:18:11.628Z'
                },
                'serverTime': '2023-04-04T17:18:11.628Z'
            }
        """

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
        orderId: Union[str, None] = None,
        cliOrdId: Union[str, None] = None,
        limitPrice: Union[str, int, float, None] = None,
        size: Union[str, int, float, None] = None,
        stopPrice: Union[str, int, float, None] = None,
    ) -> dict:
        """
        Edit an open order.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-edit-order

        :param order_id: Optional - The order_id to cancel
        :type order_id: str | None
        :param cliOrdId: Optional the client defined order id
        :type cliOrdId: str | None
        :param limitPrice: Optional - The new limitprice
        :type limitPrice: str | int | float None
        :param size: Optional - The new size of the position
        :type size: str | int | float | None
        :param stopPrice: Optional - The stop price
        :type stopPrice: str | int | float | None
        :raises ValueError:  If both ``order_id`` and ``cliOrdId`` are not set
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.edit_order(orderId="fc589be9-5095-48f0-b6f1-a2dfad6d9677", size=100)
            {
                'result': 'success',
                'serverTime': '2023-04-04T17:24:53.233Z',
                'editStatus': {
                    'status': 'orderForEditNotFound',
                    'orderId': 'fc589be9-5095-48f0-b6f1-a2dfad6d9677',
                    'receivedTime':
                    '2023-04-04T17:24:53.233Z',
                    'orderEvents': []
                }
            }
        """
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
        self,
        orderIds: Union[str, List[str], None] = None,
        cliOrdIds: Union[str, List[str], None] = None,
    ) -> dict:
        """
        Get the status of multiple orders.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-get-the-current-status-for-specific-orders

        :param order_id: Optional - The order ids to cancel
        :type order_id: str | List[str] | None
        :param cliOrdId: Optional the client defined order ids
        :type cliOrdId: str | List[str] | None
        :raises ValueError:  If both ``order_id`` and ``cliOrdId`` are not set
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.get_orders_status(orderIds=["fc589be9-5095-48f0-b6f1-a2dfad6d9677","some-other-order"])
            {'result': 'success', 'serverTime': '2023-04-04T17:27:29.667Z', 'orders': []}
        """
        params = {}
        if orderIds is not None:
            params["orderIds"] = orderIds
        elif cliOrdIds is not None:
            params["cliOrdIds"] = cliOrdIds
        else:
            raise ValueError("Either orderIds or cliOrdIds must be specified!")
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/orders/status",
            post_params=params,
            auth=True,
        )

    def create_order(
        self,
        orderType: str,
        size: Union[str, int, float],
        symbol: str,
        side: str,
        cliOrdId: Union[str, None] = None,
        limitPrice: Union[str, int, float, None] = None,
        reduceOnly: Union[bool, None] = None,
        stopPrice: Union[str, int, float, None] = None,
        triggerSignal: Union[str, None] = None,
        trailingStopDeviationUnit: Union[str, None] = None,
        trailingStopMaxDeviation: Union[str, None] = None,
    ) -> dict:
        """
        Create and place an order on the futures market.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order

        :param orderType: The order type, one of ``lmt``, ``post``, ``ioc``, ``mkt``, ``stp``, ``take_profit``, ``trailing_stop``
        :type orderType: str
        :param size: The volume of the position
        :type size: str | int | float
        :param symbol: The symbol to trade
        :type symbol: str
        :param side: Long or Short, i.e.,: ``buy`` or ``sell``
        :type side: str
        :param cliOrdId: Optinoal - A user defined order id
        :type cliOrdId: str | None
        :param limitPrice: Optional - Define a custom limit price
        :type limitPrice: str | int | float
        :param reduceOnly: Reduces existing positions if set to ``True``
        :type reduceOnly: bool | None
        :param stopPrice: Optional - define a price when to exit the order. Required for specific ordertypes
        :type stopPrice: str | None
        :param triggerSignal: Optional - Define a trigger for specific orders (must be one of ``mark``, ``index``, ``last``)
        :type triggerSignal: str | None
        :param trailingStopDeviationUnit: Optional - See referenced Kraken documentation
        :type trailingStopDeviationUnit: str | None
        :param trailingStopMaxDeviation: Optional - See referenced Kraken documentation
        :type trailingStopMaxDeviation: str | None
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_order(
                    orderType="lmt",
                    size=1,
                    symbol="PF_SOLUSD",
                    side="buy",
                    limitPrice=1,
                    stopPrice=10
                )
            {
                'result': 'success',
                'sendStatus': {
                    'status': 'insufficientAvailableFunds'
                },
                'serverTime': '2023-04-04T17:31:52.089Z'
            }
        """

        sides = ("buy", "sell")
        if side not in sides:
            raise ValueError(f"Invalid side. One of [{sides}] is required!")

        params = {"orderType": orderType, "side": side, "size": size, "symbol": symbol}
        if cliOrdId is not None:
            params["cliOrdId"] = cliOrdId
        if limitPrice is not None:
            params["limitPrice"] = limitPrice
        if reduceOnly is not None:
            params["reduceOnly"] = reduceOnly
        if stopPrice is not None:
            params["stopPrice"] = stopPrice
        if triggerSignal is not None:
            trigger_signals = ("mark", "spot", "last")
            if triggerSignal not in trigger_signals:
                raise ValueError(f"Trigger signal must be in [{trigger_signals}]!")
            params["triggerSignal"] = triggerSignal
        if trailingStopDeviationUnit is not None:
            params["trailingStopDeviationUnit"] = trailingStopDeviationUnit
        if trailingStopMaxDeviation is not None:
            params["trailingStopMaxDeviation"] = trailingStopMaxDeviation

        return self._request(
            method="POST",
            uri="/derivatives/api/v3/sendorder",
            post_params=params,
            auth=True,
        )
