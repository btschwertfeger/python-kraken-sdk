# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Module that implements the Kraken Futures trade client"""

from __future__ import annotations

from typing import TypeVar

from kraken.base_api import FuturesClient, defined

Self = TypeVar("Self")


class Trade(FuturesClient):
    """
    Class that implements the Kraken Futures trade client

    If the sandbox environment is chosen, the keys must be generated from here:
    https://demo-futures.kraken.com/settings/api

    :param key: Futures API public key (default: ``""``)
    :type key: str, optional
    :param secret: Futures API secret key (default: ``""``)
    :type secret: str, optional
    :param url: Alternative URL to access the Futures Kraken API (default:
        https://futures.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional
    :param sandbox: If set to ``True`` the URL will be
        https://demo-futures.kraken.com (default: ``False``)
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Futures Trade: Create the trade client

        >>> from kraken.futures import Trade
        >>> trade = Trade() # unauthenticated
        >>> trade = Trade(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Futures Trade: Create the trade client as context manager

        >>> from kraken.futures import Trade
        >>> with Trade(key="api-key", secret="secret-key") as trade:
        ...     print(trade.get_fills())
    """

    def __init__(  # nosec: B107
        self: Trade,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
        *,
        sandbox: bool = False,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, proxy=proxy, sandbox=sandbox)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def get_fills(
        self: Trade,
        lastFillTime: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Return the current fills of the user.

        Requires at least the ``General API - Read Only`` permission in the API
        key settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-fills

        :param lastFillTime: Filter by last filled timestamp
        :type lastFillTime: str, optional
        :return: Fills
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Get the recent fills

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
        query_params: dict = {}
        if defined(lastFillTime):
            query_params["lastFillTime"] = lastFillTime
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/derivatives/api/v3/fills",
            query_params=query_params,
            auth=True,
            extra_params=extra_params,
        )

    def create_batch_order(
        self: Trade,
        batchorder_list: list[dict],
        processBefore: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Create multiple orders at once using the batch order endpoint.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/send-batch-order

        :param batchorder_list: List of order instructions (see example below -
            or the linked official Kraken documentation)
        :type batchorder_list: list[dict]
        :param processBefore: Process before timestamp otherwise reject
        :type processBefore: str, optional
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
        batchorder: dict = {"batchOrder": batchorder_list}
        params = {"json": f"{batchorder}"}
        if processBefore:
            params["processBefore"] = processBefore

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/batchorder",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )

    def cancel_all_orders(
        self: Trade,
        symbol: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Cancels all open orders, can be filtered by symbol.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/cancel-all-orders

        :param symbol: Filter by symbol
        :type symbol: str, optional
        :return: Information about the success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Cancel all open orders

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
        params: dict = {}
        if defined(symbol):
            params["symbol"] = symbol
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/cancelallorders",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )

    def dead_mans_switch(
        self: Trade,
        timeout: int | None = 0,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        The Death Man's Switch can be used to cancel all orders after a specific
        timeout. If the timeout is set to 60, all orders will be cancelled after
        60 seconds. The timeout can be pushed back by accessing this endpoint
        over and over again. Set the timeout to zero to reset.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/cancel-all-orders-after

        :param timeout: The timeout in seconds
        :type timeout: int, optional
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
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/cancelallordersafter",
            post_params={"timeout": timeout},
            extra_params=extra_params,
        )

    def cancel_order(
        self: Trade,
        order_id: str | None = None,
        cliOrdId: str | None = None,
        processBefore: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        This endpoint can be used to cancel a specific order by ``order_id`` or
        ``cliOrdId``.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/cancel-order

        :param order_id: The order_id to cancel
        :type order_id: str, optional
        :param cliOrdId: The client defined order id
        :type cliOrdId: str, optional
        :param processBefore: Process before timestamp otherwise reject
        :type processBefore: str, optional
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

        params: dict = {}
        if defined(order_id):
            params["order_id"] = order_id
        elif defined(cliOrdId):
            params["cliOrdId"] = cliOrdId
        elif defined(processBefore):
            params["processBefore"] = processBefore
        else:
            raise ValueError("Either order_id or cliOrdId must be set!")

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/cancelorder",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )

    def edit_order(
        self: Trade,
        orderId: str | None = None,
        cliOrdId: str | None = None,
        limitPrice: str | float | None = None,
        size: str | float | None = None,
        stopPrice: str | float | None = None,
        processBefore: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Edit an open order.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/edit-order-spring

        :param orderId: The order id to cancel
        :type orderId: str, optional
        :param cliOrdId: The client defined order id
        :type cliOrdId: str, optional
        :param limitPrice: The new limit price
        :type limitPrice: str | float None
        :param size: The new size of the position
        :type size: str | float, optional
        :param stopPrice: The stop price
        :type stopPrice: str | float, optional
        :param processBefore: Process before timestamp otherwise reject
        :type processBefore: str, optional
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
        params: dict = {}
        if defined(orderId):
            params["orderId"] = orderId
        elif defined(cliOrdId):
            params["cliOrdId"] = cliOrdId
        else:
            raise ValueError("Either orderId or cliOrdId must be set!")

        if defined(limitPrice):
            params["limitPrice"] = limitPrice
        if defined(size):
            params["size"] = size
        if defined(stopPrice):
            params["stopPrice"] = stopPrice
        if defined(processBefore):
            params["processBefore"] = processBefore

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/editorder",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )

    def get_orders_status(
        self: Trade,
        orderIds: str | list[str] | None = None,
        cliOrdIds: str | list[str] | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the status of multiple orders.

        Requires at least the ``General API - Read Only`` permission in the API
        key settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/get-order-status

        :param orderIds: The order ids to cancel
        :type orderIds: str | list[str], optional
        :param cliOrdId: The client defined order ids
        :type cliOrdId: str | list[str], optional
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Get the order status

            >>> from kraken.futures import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.get_orders_status(
            ...     orderIds=[
            ...         "2c611222-bfe6-42d1-9f55-77bddc01a313",
            ...         "5f204f95-4354-4610-bb3b-c902ad333012"
            ... ])
            {'result': 'success', 'serverTime': '2023-04-04T17:27:29.667Z', 'orders': []}
        """
        params = {}
        if defined(orderIds):
            params["orderIds"] = orderIds
        elif defined(cliOrdIds):
            params["cliOrdIds"] = cliOrdIds

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/orders/status",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )

    def create_order(  # pylint: disable=too-many-arguments # noqa: PLR0913,PLR0917,C901
        self: Trade,
        orderType: str,
        size: str | float,
        symbol: str,
        side: str,
        cliOrdId: str | None = None,
        limitPrice: str | float | None = None,
        reduceOnly: bool | None = None,  # noqa: FBT001
        stopPrice: str | float | None = None,
        triggerSignal: str | None = None,
        trailingStopDeviationUnit: str | None = None,
        trailingStopMaxDeviation: str | None = None,
        processBefore: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Create and place an order on the futures market.

        Requires the ``General API - Full Access`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/futures-api/trading/send-order

        :param orderType: The order type, one of ``lmt``, ``post``, ``ioc``,
            ``mkt``, ``stp``, ``take_profit``, ``trailing_stop``
            (https://support.kraken.com/hc/en-us/sections/200577136-Order-types)
        :type orderType: str
        :param size: The volume of the position
        :type size: str | float
        :param symbol: The symbol to trade
        :type symbol: str
        :param side: Long or Short, i.e.,: ``buy`` or ``sell``
        :type side: str
        :param cliOrdId: A user defined order id
        :type cliOrdId: str, optional
        :param limitPrice: Define a custom limit price
        :type limitPrice: str | float, optional
        :param reduceOnly: Reduces existing positions if set to ``True``
        :type reduceOnly: bool, optional
        :param stopPrice: Define a price when to exit the order. Required for
            specific order types
        :type stopPrice: str, optional
        :param triggerSignal: Define a trigger for specific orders (must be one
            of ``mark``, ``index``, ``last``)
        :type triggerSignal: str, optional
        :param trailingStopDeviationUnit: See referenced Kraken documentation
        :type trailingStopDeviationUnit: str, optional
        :param trailingStopMaxDeviation: See referenced Kraken documentation
        :type trailingStopMaxDeviation: str, optional
        :param processBefore: Process before timestamp otherwise reject
        :type processBefore: str, optional
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Create and submit a new market order

            >>> trade.create_order(
            ...     orderType="mkt",
            ...     size=5,
            ...     side="buy",
            ...     symbol="PI_ETHUSD",
            ... )
            {
                'result': 'success',
                'sendStatus': {
                    'order_id': '67d3a732-b0d3-49e7-9577-45b31bceb833',
                    'status': 'placed',
                    'receivedTime': '2023-04-08T11:59:23.887Z',
                    'orderEvents': [
                        {
                            'executionId': '495aae73-7cf7-4dfc-8963-3b766d8150de',
                            'price': 1869.175,
                            'amount': 5,
                            'orderPriorEdit': None,
                            'orderPriorExecution': {
                                'orderId': '67d3a732-b0d3-49e7-9577-45b31bceb833',
                                'cliOrdId': None,
                                'type': 'ioc',
                                'symbol': 'pi_ethusd',
                                'side': 'buy',
                                'quantity': 5,
                                'filled': 0,
                                'limitPrice': 1887.85,
                                'reduceOnly': False,
                                'timestamp': '2023-04-08T11:59:23.887Z',
                                'lastUpdateTimestamp': '2023-04-08T11:59:23.887Z'
                            },
                            'takerReducedQuantity': None,
                            'type': 'EXECUTION'
                        }
                    ]
                },
                'serverTime': '2023-04-08T11:59:23.888Z'
            }

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Create and submit a new limit order

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

        .. code-block:: python
            :linenos:
            :caption: Futures Trade: Create and submit a new take profit order

            >>> trade.create_order(
            ...     orderType="take_profit",
            ...     size=10,
            ...     side="buy",
            ...     symbol="PI_ETHUSD",
            ...     limitPrice=2500.0,
            ...     triggerSignal="last",
            ...     stopPrice=2498.4,
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

        sides: tuple[str, str] = ("buy", "sell")
        if side not in sides:
            raise ValueError(f"Invalid side. One of [{sides}] is required!")

        params: dict = {
            "orderType": orderType,
            "side": side,
            "size": size,
            "symbol": symbol,
        }
        if defined(cliOrdId):
            params["cliOrdId"] = cliOrdId
        if defined(limitPrice):
            params["limitPrice"] = limitPrice
        if defined(reduceOnly):
            params["reduceOnly"] = reduceOnly
        if defined(stopPrice):
            params["stopPrice"] = stopPrice
        if defined(triggerSignal):
            trigger_signals: tuple = ("mark", "spot", "last")
            if triggerSignal not in trigger_signals:
                raise ValueError(f"Trigger signal must be in [{trigger_signals}]!")
            params["triggerSignal"] = triggerSignal
        if defined(trailingStopDeviationUnit):
            params["trailingStopDeviationUnit"] = trailingStopDeviationUnit
        if defined(trailingStopMaxDeviation):
            params["trailingStopMaxDeviation"] = trailingStopMaxDeviation
        if defined(processBefore):
            params["processBefore"] = processBefore

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/derivatives/api/v3/sendorder",
            post_params=params,
            auth=True,
            extra_params=extra_params,
        )


__all__ = ["Trade"]
