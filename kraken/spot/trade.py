#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Trade Spot client"""

from __future__ import annotations

from decimal import Decimal
from functools import lru_cache
from math import floor
from typing import Optional, TypeVar

from kraken.base_api import KrakenSpotBaseAPI, defined, ensure_string
from kraken.spot.market import Market

Self = TypeVar("Self")


class Trade(KrakenSpotBaseAPI):
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

    .. code-block:: python
        :linenos:
        :caption: Spot Trade: Create the trade client as context manager

        >>> from kraken.spot import Trade
        >>> with Trade(key="api-key", secret="secret-key") as trade:
        ...     print(trade.create_order(...))

    """

    def __init__(
        self: Trade,
        key: str = "",
        secret: str = "",
        url: str = "",
    ) -> None:
        super().__init__(key=key, secret=secret, url=url)
        self.__market: Market = Market()

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    @ensure_string("oflags")
    def create_order(  # pylint: disable=too-many-branches # noqa: PLR0913 PLR0912
        self: Trade,
        ordertype: str,
        side: str,
        pair: str,
        volume: str | float,
        price: Optional[str | float] = None,
        price2: Optional[str | float] = None,
        trigger: Optional[str] = None,
        leverage: Optional[str] = None,
        stptype: Optional[str] = "cancel-newest",
        oflags: Optional[str | list[str]] = None,
        timeinforce: Optional[str] = None,
        displayvol: Optional[str] = None,
        starttm: Optional[str] = "0",
        expiretm: Optional[str] = None,
        close_ordertype: Optional[str] = None,
        close_price: Optional[str | float] = None,
        close_price2: Optional[str | float] = None,
        deadline: Optional[str] = None,
        userref: Optional[int] = None,
        *,
        truncate: bool = False,
        reduce_only: Optional[bool] = False,
        validate: bool = False,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
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
        :param pair: The asset to trade
        :type pair: str
        :param volume: The volume of the position to create
        :type volume: str | float
        :param price: The limit price for ``limit`` orders and the trigger price for orders with
            ``ordertype`` one of ``stop-loss``, ``stop-loss-limit``, ``take-profit``, and ``take-profit-limit``
        :type price: str | float, optional
        :param price2: The limit price for ``stop-loss-limit`` and ``take-profit-limit`` orders
            The price2 can also be set to absolut or relative changes.
                * Prefixed using ``+`` or ``-`` defines the change in the quote asset
                * Prefixed by # is the same as ``+`` and ``-`` but the sign is set automatically
                * The percentage sign ``%`` can be used to define relative changes.
        :type price2: str | float, optional
        :param trigger: What triggers the position of ``stop-loss``, ``stop-loss-limit``, ``take-profit``, and
            ``take-profit-limit`` orders. Will also be used for associated conditional close orders.
            Kraken will use ``last`` if nothing is specified.
        :type trigger: str, optional
        :param leverage: The leverage
        :type leverage: str | float, optional
        :param stptype: Define what cancels the order, one of ``cancel-newest``,
            ``cancel-oldest``, ``cancel-both`` (default: ``cancel-newest``)
        :type stptype: str, optional
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``,
            ``viqc`` (see the referenced Kraken documentation for more information)
        :type oflags: str | list[str], optional
        :param timeinforce: how long the order remains in the orderbook, one of:
            ``GTC``, ``IOC``, ``GTD`` (see the referenced Kraken documentation for more information)
        :type timeinforce: str, optional
        :param displayvol: Define how much of the volume is visible in the orderbook (iceberg)
        :type displayvol: str | float, optional
        :param starttim: Unix timestamp or seconds defining the start time (default: ``"0"``)
        :type starttim: str, optional
        :param expiretm: Unix timestamp or time in seconds defining the expiration of the order,
            (default: ``"0"`` - i.e., no expiration)
        :type expiretm: str, optional
        :param close_ordertype: Conditional close order type, one of: ``limit``, ``stop-loss``,
            ``take-profit``, ``stop-loss-limit``, ``take-profit-limit``
            (see the referenced Kraken documentation for more information)
        :type close_ordertype: str, optional
        :param close_price: Conditional close price
        :type close_price: str | float, optional
        :param close_price2: The price2 for the conditional order - see the price2 parameter description
        :type close_price2: str | float, optional
        :param deadline: RFC3339 timestamp + {0..60} seconds that defines when the matching
            engine should reject the order.
        :type deadline: str, optional
        :param truncate: If enabled: round the ``price`` and ``volume`` to Kraken's
            maximum allowed decimal places. See https://support.kraken.com/hc/en-us/articles/4521313131540
            fore more information about decimals.
        :type truncate: bool, optional
        :param reduce_only: Reduce existing orders (default: ``False``)
        :type reduce_only: bool, optional
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
                'txid': ['TNGMNU-XQSRA-LKCWOK'],
                'descr': {
                    'order': 'buy 4.00000000 XBTUSD @ limit 23000.0'
                }
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
                'txid': ['TPPI2H-CUZZ2-EQR2IE'],
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
            {
                'txid': ['THNUL1-8ZAS5-EEF3A8'],
                'descr': {
                    'order': 'buy 20.00000000 XBTUSD @ stop loss 22000.0'
                }
            }

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
            ...     datetime.now(timezone.utc) + timedelta(seconds=20)
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
                * The the percentage sign "%" can be used to define relative changes.
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
        params: dict = {
            "ordertype": ordertype,
            "type": side,
            "pair": pair,
            "volume": volume
            if not truncate
            else self.truncate(amount=volume, amount_type="volume", pair=pair),
            "stp_type": stptype,
            "starttm": starttm,
            "validate": validate,
            "reduce_only": reduce_only,
        }

        trigger_ordertypes: tuple = (
            "stop-loss",
            "stop-loss-limit",
            "take-profit-limit",
            "take-profit-limit",
        )

        if defined(trigger):
            if ordertype not in trigger_ordertypes:
                raise ValueError(f"Cannot use trigger on ordertype {ordertype}!")
            params["trigger"] = trigger
        if defined(timeinforce):
            params["timeinforce"] = timeinforce
        if defined(expiretm):
            params["expiretm"] = str(expiretm)
        if defined(price):
            params["price"] = (
                price
                if not truncate
                else self.truncate(amount=price, amount_type="price", pair=pair)
            )
        if ordertype in ("stop-loss-limit", "take-profit-limit"):
            if not defined(price2):
                raise ValueError(
                    f"Ordertype {ordertype} requires a secondary price (price2)!",
                )
            params["price2"] = str(price2)
        elif price2 is not None:
            raise ValueError(
                f"Ordertype {ordertype} dos not allow a second price (price2)!",
            )
        if defined(leverage):
            params["leverage"] = str(leverage)
        if defined(oflags):
            params["oflags"] = oflags
        if defined(close_ordertype):
            params["close[ordertype]"] = close_ordertype
        if defined(close_price):
            params["close[price]"] = str(close_price)
        if defined(close_price2):
            params["close[price2]"] = str(close_price2)
        if defined(deadline):
            params["deadline"] = deadline
        if defined(userref):
            params["userref"] = userref
        if defined(displayvol):
            params["displayvol"] = str(displayvol)

        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/AddOrder",
            params=params,
            extra_params=extra_params,
        )

    def create_order_batch(
        self: Trade,
        orders: list[dict],
        pair: str,
        deadline: Optional[str] = None,
        *,
        validate: bool = False,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Create a batch of max 15 orders for a specific asset pair.

        Requires the ``Create and modify orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/addOrderBatch

        :param orders: Dictionary of order objects (see the referenced Kraken documentation for more information)
        :type orders: list[dict]
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
            ...             "userref": 16861348843,
            ...             "volume": 1,
            ...         },
            ...         {
            ...             "ordertype": "limit",
            ...             "price": 1000000,
            ...             "timeinforce": "GTC",
            ...             "type": "sell",
            ...             "userref": 16861348843,
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
        params: dict = {"orders": orders, "pair": pair, "validate": validate}
        if defined(deadline):
            params["deadline"] = deadline
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/AddOrderBatch",
            params=params,
            do_json=True,
            extra_params=extra_params,
        )

    @ensure_string("oflags")
    def edit_order(  # noqa: PLR0913
        self: Trade,
        txid: str,
        pair: str,
        volume: Optional[str | float] = None,
        price: Optional[str | float] = None,
        price2: Optional[str | float] = None,
        oflags: Optional[str] = None,
        deadline: Optional[str] = None,
        cancel_response: Optional[bool] = None,
        userref: Optional[int] = None,
        *,
        truncate: bool = False,
        validate: bool = False,
        extra_params: Optional[dict] = None,
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
        :type volume: str | float, optional
        :param price: Set a new price
        :type price: str | float, optional
        :param price2: Set a new second price
        :type price2: str | float, optional
        :param oflags: Order flags like ``post``, ``fcib``, ``fciq``, ``nomp``,
            ``viqc`` (see the referenced Kraken documentation for more information)
        :type oflags: str | list[str], optional
        :param deadline: (see the referenced Kraken documentation for more information)
        :type deadline: string
        :param cancel_response: See the referenced Kraken documentation for more information
        :type cancel_response: bool, optional
        :param truncate: If enabled: round the ``price`` and ``volume`` to Kraken's
            maximum allowed decimal places. See https://support.kraken.com/hc/en-us/articles/4521313131540
            fore more information about decimals.
        :type truncate: bool, optional
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
        params: dict = {"txid": txid, "pair": pair, "validate": validate}
        if defined(userref):
            params["userref"] = userref
        if defined(volume):
            params["volume"] = (
                str(volume)
                if not truncate
                else self.truncate(amount=volume, amount_type="volume", pair=pair)
            )
        if defined(price):
            params["price"] = (
                str(price)
                if not truncate
                else self.truncate(amount=price, amount_type="price", pair=pair)
            )
        if defined(price2):
            params["price2"] = price2
        if defined(oflags):
            params["oflags"] = oflags
        if defined(cancel_response):
            params["cancel_response"] = cancel_response
        if defined(deadline):
            params["deadline"] = deadline
        return self._request(  # type: ignore[return-value]
            "POST",
            uri="/private/EditOrder",
            params=params,
            extra_params=extra_params,
        )

    @ensure_string("txid")
    def cancel_order(
        self: Trade,
        txid: str,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
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
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/CancelOrder",
            params={"txid": txid},
            extra_params=extra_params,
        )

    def cancel_all_orders(
        self: Trade,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
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
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/CancelAll",
            extra_params=extra_params,
        )

    def cancel_all_orders_after_x(
        self: Trade,
        timeout: int = 0,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Cancel all orders after a timeout. This can be used as Dead Man's Switch.

        Requires the ``Create and modify orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/cancelAllOrdersAfter

        :param timeout: Optional The timeout in seconds, deactivate by passing the default: ``0``
        :type timeout: int, optional
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
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/CancelAllOrdersAfter",
            params={"timeout": timeout},
            extra_params=extra_params,
        )

    def cancel_order_batch(
        self: Trade,
        orders: list[str | int],
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Cancel a a list of orders by ``txid`` or ``userref``

        Requires the ``Cancel/close orders`` permission in
        the API key settings.

        - https://docs.kraken.com/rest/#operation/cancelOrderBatch

        :param orders: List of orders to cancel
        :type orders: list[str | int]
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
        return self._request(  # type: ignore[return-value]
            method="POST",
            uri="/private/CancelOrderBatch",
            params={"orders": orders},
            do_json=True,
            extra_params=extra_params,
        )

    @lru_cache()
    def truncate(
        self: Trade,
        amount: Decimal | float | str,
        amount_type: str,
        pair: str,
    ) -> str:
        """
        Kraken only allows volume and price amounts to be specified with a specific number of
        decimal places, and these vary depending on the currency pair used.

        This function converts an amount of a specific type and pair to a string that uses
        the correct number of decimal places.

        - https://support.kraken.com/hc/en-us/articles/4521313131540

        This function uses caching. Run ``truncate.clear_cache()`` to clear.

        :param amount: The floating point number to represent
        :type amount: Decimal | float | str
        :param amount_type: What the amount represents. Either ``"price"`` or ``"volume"``
        :type amount_type: str
        :param pair: The currency pair the amount is in reference to.
        :type pair: str
        :raises ValueError: If the ``amount_type`` is ``price`` and the price is less
            than the costmin.
        :raises ValueError: If the ``amount_type`` is ``volume`` and the volume is
            less than the ordermin.
        :raises ValueError: If no valid ``amount_type`` was passed.
        :return: A string representation of the amount.
        :rtype: str

        .. code-block:: python
            :linenos:
            :caption: Spot Trade: Truncate

            >>> print(trade.truncate(
            ...     amount=0.123456789,
            ...     amount_type="volume",
            ...     pair="XBTUSD"
            ... ))
            0.12345678

            >>> print(trade.truncate(
            ...     amount=21123.12849829993,
            ...     amount_type="price",
            ...     pair="XBTUSD")
            ... ))
            21123.1

            >>> print(trade.truncate(
            ...     amount=0.1,
            ...     amount_type="volume",
            ...     pair="XBTUSD"
            ... ))
            0.10000000

            >>> print(trade.truncate(
            ...     amount=21123,
            ...     amount_type="price",
            ...     pair="XBTUSD"
            ... ))
            21123.0
        """
        if amount_type not in ("price", "volume"):
            raise ValueError("Amount type must be 'volume' or 'price'!")

        pair_data: dict = self.__market.get_asset_pairs(pair=pair)
        data: dict = pair_data[next(iter(pair_data))]

        pair_decimals: int = int(data["pair_decimals"])
        lot_decimals: int = int(data["lot_decimals"])

        ordermin: Decimal = Decimal(data["ordermin"])
        costmin: Decimal = Decimal(data["costmin"])

        amount = Decimal(amount)
        decimals: int

        if amount_type == "price":
            if costmin > amount:
                raise ValueError(f"Price is less than the costmin: {costmin}!")
            decimals = pair_decimals
        else:  # amount_type == "volume":
            if ordermin > amount:
                raise ValueError(f"Volume is less than the ordermin: {ordermin}!")
            decimals = lot_decimals

        amount_rounded: float = floor(float(amount) * 10**decimals) / 10**decimals
        return f"{amount_rounded:.{decimals}f}"


__all__ = ["Trade"]
