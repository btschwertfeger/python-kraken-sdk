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

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: ``False``)
    :type sandbox: bool

    .. code-block:: python
        :linenos:
        :caption: Example

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
        """
        Create a new order and place it on the market.

        - https://docs.kraken.com/rest/#operation/addOrder

        :param ordertype: The kind of the order, one of: ``market``, ``limit``, ``take-profit``, ``stop-loss-limit``, ``take-profit-limit`` and ``settle-position``
        :type ordertype: str
        :param side: ``buy`` or ``sell``
        :type side: str
        :param volume: The volume of the position to create
        :type volume: str | int | float
        :param price: Optional - The limit price for ``limit`` orders or the trigger price for orders with ``ordertype`` one of ``stop-loss``, ``stop-loss-limit``, ``take-profit``, and ``take-profit-limit``
        :type price: str | int | float | None
        :param price2: Optional - The second price for ``stop-loss-limit`` and ``take-profit-limit`` orders (see the referenced Kraken documentaion for more information)
        :type price2: str | int | float | None
        :param trigger: Optional - What triggers the position of ``top-loss``, ``stop-loss-limit``, ``take-profit``, and ``take-profit-limit`` orders.
        :type trigger: str | None
        :param leverage: Optional - The leverage
        :type leverage: str | int | float | None
        :param reduce_only: (default: ``False``)
        :type reduce_only: bool
        :param stptype: Define what cancells the order, one of ``cancel-newest``, ``cancel-oldest``, ``cancel-both`` (default: ``cancel-newest``)
        :type stptype: str | None
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``, ``viqc`` (see the referenced Kraken documentaion for more information)
        :type oflags: str | List[str] | None
        :param timeinforce: Optional - how long the order raimains in the orderbook, one of: ``GTC``, `ÌOC``, ``GTD`` (see the referenced Kraken documentaion for more information)
        :type timeinforce: str | None
        :param displayvol: Optional - Define how much of the volume is visible in the order book (iceberg)
        :type displayvol: str | int | float | None
        :param starttim: Unix timestamp or seconds defining the start time (default: ``"0"``)
        :type starttim: str
        :param expiretm: Unix timestamp or time in seconds defining the expiration of the order, (default: ``"0"`` - i.e., no expiration)
        :type expiretm: str
        :param close_ordertype: Optional - Conditional close order type, one of: ``limit``, ``stop-loss``, ``take-profit``, ``stop-loss-limit``, ``take-profit-limit`` (see the referenced Kraken documentaion for more information)
        :type close_ordertype: str | None
        :param close_price: Optional - Conditional close price
        :type close_price: str | int | float | None
        :param close_price2: Optional - Second conditional close price
        :type close_price2: str | int | float | None
        :param deadline: (see the referenced Kraken documentaion for more information)
        :type deadline: str
        :param validate: Optinal - Validate the order without placing on the market (default: ``False``)
        :type validate: bool
        :param userref: User reference id for example to group orders
        :type userref: int
        :raises ValueError: If input is not correct
        :return: The transaction id
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import Trade
            >>> trade = Trade(key="api-key", secret="secret-key")
            >>> trade.create_order(
            ...     ordertype="market",
            ...     side="buy",
            ...     pair="XBTUSD",
            ...     volume="0.0001"
            ... )
            { 'txid': 'TNGMNU-XQSRA-LKCWOK' }
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
            { 'txid': 'TPPI2H-CUZZ2-EQR2IE' }
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
        if trigger is not None:
            if ordertype in [
                "stop-loss",
                "stop-loss-limit",
                "take-profit-limit",
                "take-profit-limit",
            ]:
                if timeinforce is None:
                    params["trigger"] = trigger
                else:
                    raise ValueError(
                        f"Cannot use trigger {trigger} and timeinforce {timeinforce} together"
                    )
            else:
                raise ValueError(f"Cannot use trigger on ordertype {ordertype}")
        elif timeinforce is not None:
            params["timeinforce"] = timeinforce

        if expiretm is not None:
            params["expiretm"] = str(expiretm)
        if price is not None:
            params["price"] = str(price)
        if price2 is not None:
            params["price2"] = str(price2)
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

        - https://docs.kraken.com/rest/#operation/addOrderBatch

        :param orders: Dictionary of order objects (see the referenced Kraken documentaion for more information)
        :type orders: List[dict]
        :param pair: Asset pair to place the orders for
        :type pair: str
        :param deadline: Optional - (see the referenced Kraken documentaion for more information)
        :type deadline: str
        :param validate: Optional - Validate the orders without placing them. (default: ``False``)
        :type validate: bool
        :return: Information about the placed orders
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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

        - https://docs.kraken.com/rest/#operation/editOrder

        :param txid: The txid of the order to edit
        :type txid: str
        :param pair: The asset pair of the order
        :type pair: str
        :param volume: Optional - Set a new volume
        :type volume: str | int | float | None
        :param price: Optional - Set a new price
        :type price: str | int | float | None
        :param price2: Optional - Set a new second price
        :type price2: str | int | float | None
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``, ``viqc`` (see the referenced Kraken documentaion for more information)
        :type oflags: str | List[str] | None
        :param deadline: (see the referenced Kraken documentaion for more information)
        :type deadline: string
        :param cancel_response: Optional - (see the referenced Kraken documentaion for more information)
        :type cancel_response: bool
        :param validate: Optinal - Validate the order without placing on the market (default: ``False``)
        :type validate: bool
        :param userref: User reference id for example to group orders
        :type userref: int
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Example

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
        Cancel a specific order by txid. Instead of a transaction id
        a comma delimited list of ``userref`` (user reference ids) can be passed.

        (see: https://docs.kraken.com/rest/#operation/cancelOrder)

        :param txid: Transaction id or comma delimited list of user reference ids to cancel.
        :type txid: str
        """
        return self._request(
            method="POST", uri="/private/CancelOrder", params={"txid": txid}
        )

    def cancel_all_orders(self) -> dict:
        """
        Cancel all open orders.
        (see: https://docs.kraken.com/rest/#operation/cancelAllOrders)
        """
        return self._request(method="POST", uri="/private/CancelAll")

    def cancel_all_orders_after_x(self, timeout: int) -> dict:
        """
        Cancel all orders after a timeout. This can be used as Dead Man's Switch.

        (see: https://docs.kraken.com/rest/#operation/cancelAllOrdersAfter)

        :param timeout: The timeout in seconds, decativate by passing ``0``
        :type timeout: int
        """
        return self._request(
            method="POST",
            uri="/private/CancelAllOrdersAfter",
            params={"timeout": timeout},
        )

    def cancel_order_batch(self, orders: List[Union[str, int]]) -> dict:
        """
        Cancel a a list of orders by ``txid`` or ``userref``

        (see: https://docs.kraken.com/rest/#operation/cancelOrderBatch)

        :param orders: List of orders to cancel
        :type orders: List[str | int]
        """
        return self._request(
            method="POST",
            uri="/private/CancelOrderBatch",
            params={"orders": orders},
            do_json=True,
        )
