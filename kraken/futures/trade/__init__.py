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
    :type key: str, optional
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Futures Kraken API (default: https://futures.kraken.com)
    :type url: str, optional
    :param sandbox: If set to ``True`` the URL will be https://demo-futures.kraken.com
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Futures Trade: Create the trade client

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

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-data-get-your-fills

        :param lastFillTime: Filter by last filled timestamp
        :type lastFillTime: str | None, optional
        :return: Fills
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Get the recend fills

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.get_fills()
            {
                'result': 'success',
                'fills': [{
                    'fill_id': '15dae264-01e9-4d4c-8962-2f49b98c46f6',
                    'symbol': 'pi_ethusd',
                    'side': 'buy',
                    'order_id': '267372ec-272f-4ca7-9b8c-99a0dc8f781c',
                    'size': 5,
                    'price': 1859.075,
                    'fillTime': '2023-04-07T15:07:46.540Z',
                    'fillType': 'taker'
                }, ...],
                'serverTime': '2023-04-07T15:23:48.705Z'
            }
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

        Requires the ``General API - Full Access`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-batch-order-management

        :param batchorder_list: List of order instructions (see example below - or the linked official Kraken documentation)
        :type batchorder_list: List[dict]
        :return: Information about the submitted request
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Create a batch order

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_batch_order(
            ...     batchorder_list=[
            ...         {
            ...             "order": "send",
            ...             "order_tag": "1",
            ...             "orderType": "lmt",
            ...             "symbol": "PI_XBTUSD",
            ...             "side": "buy",
            ...             "size": 5,
            ...             "limitPrice": 1.00,
            ...             "cliOrdId": "my_another_client_id",
            ...         },
            ...         {
            ...             "order": "send",
            ...             "order_tag": "2",
            ...             "orderType": "stp",
            ...             "symbol": "PI_XBTUSD",
            ...             "side": "buy",
            ...             "size": 1,
            ...             "limitPrice": 2.00,
            ...             "stopPrice": 3.00,
            ...         },
            ...         {
            ...             "order": "cancel",
            ...             "order_id": "e35d61dd-8a30-4d5f-a574-b5593ef0c050",
            ...         },
            ...         {
            ...             "order": "cancel",
            ...             "cliOrdId": "my_client_id",
            ...         },
            ...     ],
            ... )
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

        Requires the ``General API - Full Access`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-all-orders

        :param symbol: Filter by symbol
        :type symbol: str | None, optional
        :return: Information about the success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Cancell all open orders

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

        Requires the ``General API - Full Access`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-dead-man-39-s-switch

        :param timeout: The timeout in seconds
        :type timeout: int | None, optional
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Setup the Death man's Switch

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

        Requires the ``General API - Full Access`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-order

        :param order_id: The order_id to cancel
        :type order_id: str | None, optional
        :param cliOrdId: The client defined order id
        :type cliOrdId: str | None, optional
        :raises ValueError: If both ``order_id`` and ``cliOrdId`` are not set
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Cancel an order

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

        Requires the ``General API - Full Access`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-edit-order

        :param orderId: The order id to cancel
        :type orderId: str | None, optional
        :param cliOrdId: The client defined order id
        :type cliOrdId: str | None, optional
        :param limitPrice: The new limitprice
        :type limitPrice: str | int | float None
        :param size: The new size of the position
        :type size: str | int | float | None, optional
        :param stopPrice: The stop price
        :type stopPrice: str | int | float | None, optional
        :raises ValueError: If both ``orderId`` and ``cliOrdId`` are not set
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Edit an open order

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

        Requires at least the ``General API - Read Only`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-get-the-current-status-for-specific-orders

        :param orderIds: The order ids to cancel
        :type orderIds: str | List[str] | None, optional
        :param cliOrdId: The client defined order ids
        :type cliOrdId: str | List[str] | None, optional
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Get the order status

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

        return self._request(
            method="POST",
            uri="/derivatives/api/v3/orders/status",
            post_params=params,
            auth=True,
        )

    def get_open_positions(self) -> dict:
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
        return self._request(
            method="GET", uri="/derivatives/api/v3/openpositions", auth=True
        )

    def get_open_orders(self) -> dict:
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
        return self._request(
            method="GET", uri="/derivatives/api/v3/openorders", auth=True
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

        Requires the ``General API - Full Access`` permission in the API key settings.

        - https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order

        :param orderType: The order type, one of ``lmt``, ``post``, ``ioc``, ``mkt``, ``stp``, ``take_profit``, ``trailing_stop``
        :type orderType: str
        :param size: The volume of the position
        :type size: str | int | float
        :param symbol: The symbol to trade
        :type symbol: str
        :param side: Long or Short, i.e.,: ``buy`` or ``sell``
        :type side: str
        :param cliOrdId: A user defined order id
        :type cliOrdId: str | None, optional
        :param limitPrice: Define a custom limit price
        :type limitPrice: str | int | float
        :param reduceOnly: Reduces existing positions if set to ``True``
        :type reduceOnly: bool | None, optional
        :param stopPrice: Define a price when to exit the order. Required for specific ordertypes
        :type stopPrice: str | None, optional
        :param triggerSignal: Define a trigger for specific orders (must be one of ``mark``, ``index``, ``last``)
        :type triggerSignal: str | None, optional
        :param trailingStopDeviationUnit: See referenced Kraken documentation
        :type trailingStopDeviationUnit: str | None, optional
        :param trailingStopMaxDeviation: See referenced Kraken documentation
        :type trailingStopMaxDeviation: str | None, optional
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Create and submit a new order

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_order(
            ...     orderType="lmt",
            ...     size=1000,
            ...     symbol="PF_ETHUSD",
            ...     side="buy",
            ...     limitPrice=1200.0,
            ... )
            {
                'result': 'success',
                'sendStatus': {
                    'order_id': '2ce038ae-c144-4de7-a0f1-82f7f4fca864',
                    'status': 'placed',
                    'receivedTime': '2023-04-07T15:18:04.699Z',
                    'orderEvents': [
                        {
                            'order': {
                                'orderId': '2ce038ae-c144-4de7-a0f1-82f7f4fca864',
                                'cliOrdId': None,
                                'type': 'lmt',
                                'symbol': 'pi_ethusd',
                                'side': 'buy',
                                'quantity': 100,
                                'filled': 0,
                                'limitPrice': 1200.0,
                                'reduceOnly': False,
                                'timestamp': '2023-04-07T15:18:04.699Z',
                                'lastUpdateTimestamp': '2023-04-07T15:18:04.699Z'
                            },
                            'reducedQuantity': None,
                            'type': 'PLACE'
                        }
                    ]
                },
                'serverTime': '2023-04-07T15:18:04.700Z'
            }
            >>> trade.create_order(
            ...     orderType="mkt",
            ...     size=5,
            ...     side="buy",
            ...     symbol="PI_ETHUSD",
            ... )
            {
                'result': 'success',
                'sendStatus': {
                    'order_id': '267372ec-272f-4ca7-9b8c-99a0dc8f781c',
                    'status': 'placed',
                    'receivedTime': '2023-04-07T15:07:46.540Z',
                    'orderEvents': [
                        {
                            'executionId': '15dae264-01e9-4d4c-8962-2f49b98c46f6',
                            'price': 1859.075,
                            'amount': 5,
                            'orderPriorEdit': None,
                            'orderPriorExecution': {
                                'orderId': '267372ec-272f-4ca7-9b8c-99a0dc8f781c',
                                'cliOrdId': None,
                                'type': 'ioc',
                                'symbol': 'pi_ethusd',
                                'side': 'buy',
                                'quantity': 5,
                                'filled': 0,
                                'limitPrice': 1877.65,
                                'reduceOnly': False,
                                'timestamp': '2023-04-07T15:07:46.540Z',
                                'lastUpdateTimestamp': '2023-04-07T15:07:46.540Z'
                            },
                            'takerReducedQuantity': None,
                            'type': 'EXECUTION'
                        }
                    ]
                },
                'serverTime': '2023-04-07T15:07:46.541Z'
            }
            >>> trade.create_order(
            ...     orderType="take_profit",
            ...     size=10,
            ...     side="buy",
            ...     symbol="PI_ETHUSD",
            ...     limitPrice="1860.0",
            ...     triggerSignal="last",
            ...     stopPrice=1880.4,
            ... )
            {
                'result': 'success',
                'sendStatus': {
                    'order_id': 'e58ed100-1fb8-4e6c-a5ea-1cf85b0f0654',
                    'status': 'placed',
                    'receivedTime': '2023-04-07T15:12:08.131Z',
                    'orderEvents': [
                        {
                            'orderTrigger': {
                                'uid': 'e58ed100-1fb8-4e6c-a5ea-1cf85b0f0654',
                                'clientId': None,
                                'type': 'lmt',
                                'symbol': 'pi_ethusd',
                                'side': 'buy',
                                'quantity': 10,
                                'limitPrice': 1860.0,
                                'triggerPrice': 1880.4,
                                'triggerSide': 'trigger_below',
                                'triggerSignal': 'last_price',
                                'reduceOnly': False,
                                'timestamp': '2023-04-07T15:12:08.131Z',
                                'lastUpdateTimestamp': '2023-04-07T15:12:08.131Z',
                                'startTime': None
                            },
                            'type': 'PLACE'
                        }
                    ]
                },
                'serverTime': '2023-04-07T15:12:08.131Z'
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
