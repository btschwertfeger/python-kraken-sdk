#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Trade Spot client"""
from typing import List, Union

from kraken.base_api import KrakenBaseSpotAPI


class Trade(KrakenBaseSpotAPI):
    """
    Class that implements the Kraken Trade Spot client

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: The URL to access the Kraken API (default: https://api.kraken.com)
    :type url: str, optional
    :param sandbox: Use the sandbox (not supported for Spot trading so far, default: ``False``)
    :type sandbox: bool, optional

    .. code-block:: python
        :linenos:
        :caption: Spot Trade: Create the trade client

        >>> from kraken.spot import Trade
        >>> trade = Trade() # unauthenticated
        >>> auth_trade = Trade(key="api-key", secret="secret-key") # authenticated
    """

    def create_order(
        self,
        ordertype: str,
        side: str,
        volume: Union[str, int, float],
        pair: str,
        price: Union[str, int, float, None] = None,
        price2: Union[str, int, float, None] = None,
        trigger: Union[str, None] = None,
        leverage: Union[str, None] = None,
        reduce_only: bool = False,
        stptype: str = "cancel-newest",
        oflags: Union[str, List[str], None] = None,
        timeinforce: Union[str, None] = None,
        displayvol: Union[str, None] = None,
        starttm: str = "0",
        expiretm: Union[str, None] = None,
        close_ordertype: Union[str, None] = None,
        close_price: Union[str, int, float, None] = None,
        close_price2: Union[str, int, float, None] = None,
        deadline: Union[str, None] = None,
        validate: bool = False,
        userref: Union[int, None] = None,
    ) -> dict:
        r"""
        Create a new order and place it on the market.

        Requires the ``Create and modify orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/addOrder

        :param ordertype: The kind of the order, one of: ``market``, ``limit``, ``take-profit``,
            ``stop-loss-limit``, ``take-profit-limit`` and ``settle-position``
            (see: https://support.kraken.com/hc/en-us/sections/200577136-Order-types)
        :type ordertype: str
        :param side: ``buy`` or ``sell``
        :type side: str
        :param volume: The volume of the position to create
        :type volume: str | int | float
        :param price: The limit price for ``limit`` orders and the trigger price for orders with
            ``ordertype`` one of ``stop-loss``, ``stop-loss-limit``, ``take-profit``, and ``take-profit-limit``
        :type price: str | int | float | None, optional
        :param price2: The limit price for ``stop-loss-limit`` and ``take-profit-limit`` orders
            The price2 can also be set to absolut or relative changes.
                * Prefixed using ``+`` or ``-`` defines the change in the quote asset
                * Prefixed by # is the same as ``+`` and ``-`` but the sign is set automatically
                * The percentate sign ``%`` can be used to define relative changes.

        :type price2: str | int | float | None, optional
        :param trigger: What triggers the position of ``stop-loss``, ``stop-loss-limit``, ``take-profit``, and
            ``take-profit-limit`` orders. Will also be used for associated conditional close orders.
            Kraken will use ``last`` if nothing is specified.
        :type trigger: str | None, optional
        :param leverage: The leverage
        :type leverage: str | int | float | None, optional
        :param reduce_only: (default: ``False``)
        :type reduce_only: bool, optional
        :param stptype: Define what cancells the order, one of ``cancel-newest``,
            ``cancel-oldest``, ``cancel-both`` (default: ``cancel-newest``)
        :type stptype: str | None, optional
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``,
            ``viqc`` (see the referenced Kraken documentaion for more information)
        :type oflags: str | List[str] | None, optional
        :param timeinforce: how long the order raimains in the orderbook, one of:
            ``GTC``, `ÌOC``, ``GTD`` (see the referenced Kraken documentaion for more information)
        :type timeinforce: str | None, optional
        :param displayvol: Define how much of the volume is visible in the order book (iceberg)
        :type displayvol: str | int | float | None, optional
        :param starttim: Unix timestamp or seconds defining the start time (default: ``"0"``)
        :type starttim: str, optional
        :param expiretm: Unix timestamp or time in seconds defining the expiration of the order,
            (default: ``"0"`` - i.e., no expiration)
        :type expiretm: str, optional
        :param close_ordertype: Conditional close order type, one of: ``limit``, ``stop-loss``,
            ``take-profit``, ``stop-loss-limit``, ``take-profit-limit``
                (see the referenced Kraken documentaion for more information)
        :type close_ordertype: str | None, optional
        :param close_price: Conditional close price
        :type close_price: str | int | float | None, optional
        :param close_price2: The price2 for the conditional order - see the price2 parameter description
        :type close_price2: str | int | float | None, optional
        :param deadline: RFC3339 timestamp + {0..60} seconds that defines when the matching
            engine should reject the order.
        :type deadline: str, optional
        :param validate: Validate the order without placing on the market (default: ``False``)
        :type validate: bool, optional
        :param userref: User reference id for example to group orders
        :type userref: int, optional
        :raises ValueError: If input is not correct
        :return: The transaction id
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Create a market order

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_order(
            ...     ordertype="market",
            ...     side="buy",
            ...     pair="XBTUSD",
            ...     volume="0.0001"
            ... )
            {
                'txid': 'TNGMNU-XQSRA-LKCWOK',
                'descr': { ...}
            }

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Create limit order

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_order(
            ...     ordertype="limit",
            ...     side="buy",
            ...     pair="XBTUSD",
            ...     volume=4,
            ...     price=23000,
            ...     expiretm=121,
            ...     displayvol=0.5,
            ...     oflags=["post", "fcib"]
            ... )
            {
                'txid': 'TPPI2H-CUZZ2-EQR2IE',
                'descr': {
                    'order': 'buy 4.0000 XBTUSD @ limit 23000.0'
                }
            }

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Create a stop loss order

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_order(
            ...     ordertype="stop-loss",
            ...     pair="XBTUSD",
            ...     volume=20,
            ...     price=22000,
            ...     side="buy",
            ... )
            { 'txid': 'THNUL1-8ZAS5-EEF3A8' }

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Create stop-loss-limit and take-profit-limit orders

            '''
            When the price hits $25000:
               1. A limit buy order will be placed at $24000 with 2x leverage.
               2. When the limit order gets closed/filled at $24000
                  The stop-loss-limit part is done and the tale-profit-limit
                  part begins.
               3. When the price hits $27000 a limit order will be placed at
                  $26800 to sell 1.2 BTC. This ensures that the asset will
                  be sold for $26800 or better.
            '''
            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> from datetime import datetime, timedelta, timezone
            >>> deadline = (
            ... datetime.now(timezone.utc) + timedelta(seconds=20)
            ... ).isoformat()
            >>> trade.create_order(
            ...     ordertype="stop-loss-limit",
            ...     pair="XBTUSD",
            ...     side="buy",
            ...     volume=1.2,
            ...     price=24000,
            ...     price2=25000,
            ...     validate=True, # just validate the input, do not place on the market
            ...     trigger="last",
            ...     timeinforce="GTC",
            ...     leverage=4,
            ...     deadline=deadline,
            ...     close_ordertype="take-profit-limit",
            ...     close_price=27000,
            ...     close_price2=26800,
            ... )
            {
                'descr': {
                    'order': 'buy 0.00100000 XBTUSD @ stop loss 24000.0 -> limit 25000.0 with 2:1 leverage',
                    'close': 'close position @ take profit 27000.0 -> limit 26800.0'
                }
            }

            '''
            The price2 and close_price2 can also be set to absolut or relative changes.
                * Prefixed using "+" or "-" defines the change in the quote asset
                * Prefixed by # is the same as "+" and "-" but the sign is set automatically
                * The the percentate sign "%" can be used to define relative changes.
            '''
            >>> trade.create_order(
            ...     ordertype="stop-loss-limit",
            ...     pair="XBTUSD",
            ...     side="buy",
            ...     volume=1.2,
            ...     price=24000,
            ...     price2="+1000",
            ...     validate=True,
            ...     trigger="last",
            ...     timeinforce="GTC",
            ...     close_ordertype="take-profit-limit",
            ...     close_price=27000,
            ...     close_price2="#2%",
            ... )
            {
                'descr': {
                    'order': 'buy 0.00100000 XBTUSD @ stop loss 24000.0 -> limit +1000.0',
                    'close': 'close position @ take profit 27000.0 -> limit -2.0000%'
                }
            }
        """
        params = {
            "ordertype": str(ordertype),
            "type": str(side),
            "volume": str(volume),
            "pair": str(pair),
            "stp_type": stptype,
            "starttm": starttm,
            "validate": validate,
            "reduce_only": reduce_only,
        }
        trigger_ordertypes = (
            "stop-loss",
            "stop-loss-limit",
            "take-profit-limit",
            "take-profit-limit",
        )
        if trigger is not None:
            if ordertype not in trigger_ordertypes:
                raise ValueError(f"Cannot use trigger on ordertype {ordertype}!")
            params["trigger"] = trigger

        if timeinforce is not None:
            params["timeinforce"] = timeinforce
        if expiretm is not None:
            params["expiretm"] = str(expiretm)
        if price is not None:
            params["price"] = str(price)

        if ordertype in ("stop-loss-limit", "take-profit-limit"):
            if price2 is None:
                raise ValueError(
                    f"Ordertype {ordertype} requires a secondary price (price2)!"
                )
            params["price2"] = str(price2)
        elif price2 is not None:
            raise ValueError(
                f"Ordertype {ordertype} dont allow a second price (price2)!"
            )

        if leverage is not None:
            params["leverage"] = str(leverage)
        if oflags is not None:
            params["oflags"] = self._to_str_list(oflags)
        if close_ordertype is not None:
            params["close[ordertype]"] = close_ordertype
        if close_price is not None:
            params["close[price]"] = str(close_price)
        if close_price2 is not None:
            params["close[price2]"] = str(close_price2)
        if deadline is not None:
            params["deadline"] = deadline
        if userref is not None:
            params["userref"] = userref
        if displayvol is not None:
            params["displayvol"] = str(displayvol)

        return self._request(method="POST", uri="/private/AddOrder", params=params)

    def create_order_batch(
        self,
        orders: List[dict],
        pair: str,
        deadline: Union[str, None] = None,
        validate: bool = False,
    ) -> dict:
        """
        Create a batch of max 15 orders for a specifc asset pair.

        Requires the ``Create and modify orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/addOrderBatch

        :param orders: Dictionary of order objects (see the referenced Kraken documentaion for more information)
        :type orders: List[dict]
        :param pair: Asset pair to place the orders for
        :type pair: str
        :param deadline: RFC3339 timestamp + {0..60} seconds that defines when the matching engine should reject the order.
        :type deadline: str, optional
        :param validate: Validate the orders without placing them. (default: ``False``)
        :type validate: bool, optional
        :return: Information about the placed orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Create a batch order

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_order_batch(orders=[
            ...         {
            ...             "close": {
            ...                 "ordertype": "stop-loss-limit",
            ...                 "price": 21000,
            ...                 "price2": 20000,
            ...             },
            ...             "ordertype": "limit",
            ...             "price": 25000,
            ...             "timeinforce": "GTC",
            ...             "type": "buy",
            ...             "userref": "147145322246",
            ...             "volume": 1,
            ...         },
            ...         {
            ...             "ordertype": "limit",
            ...             "price": 1000000,
            ...             "timeinforce": "GTC",
            ...             "type": "sell",
            ...             "userref": "16861348843",
            ...             "volume": 2,
            ...         },
            ...     ],
            ...     pair="BTC/USD"
            ... )
            {
                'orders': [{
                    'order': 'buy 1 BTCUSD @ limit 25000',
                    'txid': 'O5TLGX-DKKTU-WKRAZ5',
                    'close': 'close position @ stop loss 21000.0 -> limit 20000.0'
                }, {
                    'order': "sell 2 BTCUSD @ limit 1000000',
                    'txid': 'OBGFYP-XVQNL-P4GMWF'
                }]
            }
        """
        params = {"orders": orders, "pair": pair, "validate": validate}
        if deadline is not None:
            params["deadline"] = deadline
        return self._request(
            method="POST", uri="/private/AddOrderBatch", params=params, do_json=True
        )

    def edit_order(
        self,
        txid: str,
        pair: str,
        volume: Union[str, int, float, None] = None,
        price: Union[str, int, float, None] = None,
        price2: Union[str, int, float, None] = None,
        oflags: Union[str, None] = None,
        deadline: Union[str, None] = None,
        cancel_response: Union[bool, None] = None,
        validate: bool = False,
        userref: Union[int, None] = None,
    ) -> dict:
        """
        Edit an open order.

        Requires the ``Create and modify orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/editOrder

        :param txid: The txid of the order to edit
        :type txid: str
        :param pair: The asset pair of the order
        :type pair: str
        :param volume: Set a new volume
        :type volume: str | int | float | None, optional
        :param price: Set a new price
        :type price: str | int | float | None, optional
        :param price2: Set a new second price
        :type price2: str | int | float | None, optional
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``, ``viqc`` (see the referenced Kraken documentaion for more information)
        :type oflags: str | List[str] | None, optional
        :param deadline: (see the referenced Kraken documentaion for more information)
        :type deadline: string
        :param cancel_response: See the referenced Kraken documentaion for more information
        :type cancel_response: bool, optional
        :param validate: Validate the order without placing on the market (default: ``False``)
        :type validate: bool, optional
        :param userref: User reference id for example to group orders
        :type userref: int
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Modify an order

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.edit_order(txid="OBGFYP-XVQNL-P4GMWF",
            ...     volume=0.75,
            ...     pair="XBTUSD",
            ...     price=1250000
            ... )
            {
                'status': 'ok',
                'txid': 'OFVXHJ-KPQ3B-VS7ELA',
                'originaltxid': 'OBGFYP-XVQNL-P4GMWF',
                'volume': '0.75',
                'price': '1250000',
                'orders_cancelled': 1,
                'descr': {
                    'order': 'sell 0.75 XXBTZUSD @ limit 1250000'
                }
            }
        """
        params = {"txid": txid, "pair": pair, "validate": validate}
        if userref is not None:
            params["userref"] = userref
        if volume is not None:
            params["volume"] = volume
        if price is not None:
            params["price"] = price
        if price2 is not None:
            params["price2"] = price2
        if oflags is not None:
            params["oflags"] = self._to_str_list(oflags)
        if cancel_response is not None:
            params["cancel_response"] = cancel_response
        if deadline is not None:
            params["deadline"] = deadline
        return self._request("POST", uri="/private/EditOrder", params=params)

    def cancel_order(self, txid: str) -> dict:
        """
        Cancel a specific order by ``txid``. Instead of a transaction id
        a user reference id can be passed.

        Requires the ``Cancel/close orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/cancelOrder

        :param txid: Transaction id or comma delimited list of user reference ids to cancel.
        :type txid: str
        :return: Success or failure - Number of closed orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Cancel an order

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.cancel_order(txid="OAUHYR-YCVK6-P22G6P")
            { 'count': 1 }
        """
        return self._request(
            method="POST",
            uri="/private/CancelOrder",
            params={"txid": self._to_str_list(txid)},
        )

    def cancel_all_orders(self) -> dict:
        """
        Cancel all open orders.

        Requires the ``Cancel/close orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/cancelAllOrders

        :return: Success or failure - Number of closed orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Cancel all open orders

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.cancel_all_orders()
            { 'count': 2 }
        """
        return self._request(method="POST", uri="/private/CancelAll")

    def cancel_all_orders_after_x(self, timeout: int = 0) -> dict:
        """
        Cancel all orders after a timeout. This can be used as Dead Man's Switch.

        Requires the ``Create and modify orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/cancelAllOrdersAfter

        :param timeout: Optional The timeout in seconds, decativate by passing the default: ``0``
        :type timeout: int
        :return: Current time and trigger time
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Set the Death Man's Switch

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.cancel_all_orders_after_x(timeout=60)
            {
                'currentTime': '2023-04-06T06:51:56Z',
                'triggerTime': '2023-04-06T06:52:56Z'
            }
        """
        return self._request(
            method="POST",
            uri="/private/CancelAllOrdersAfter",
            params={"timeout": timeout},
        )

    def cancel_order_batch(self, orders: List[Union[str, int]]) -> dict:
        """
        Cancel a a list of orders by ``txid`` or ``userref``
        This endpoint is broken, see https://github.com/btschwertfeger/Python-Kraken-SDK/issues/65

        Requires the ``Cancel/close orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/cancelOrderBatch

        :param orders: List of orders to cancel
        :type orders: List[str | int]
        :return: Success or failure - Number of closed orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Cancel multiple orders

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.cancel_order_batch(
            ...     orders=["OG5IL4-6AR7I-ZAPZEZ", "OAUHYR-YCVK6-P22G6P"]
            ... )
            { count': 2 }
        """
        return self._request(
            method="POST",
            uri="/private/CancelOrderBatch",
            params={"orders": orders},
            do_json=True,
        )
