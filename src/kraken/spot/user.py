# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#
# (PLR0904): Too many public methods
# ruff: noqa: PLR0904
# pylint: disable=too-many-lines

"""Module that implements the Kraken Spot User client"""

from __future__ import annotations

from decimal import Decimal
from typing import TypeVar

from kraken.base_api import SpotClient, defined, ensure_string

Self = TypeVar("Self")


class User(SpotClient):
    """
    Class that implements the Kraken Spot User client

    Requires the ``Query funds`` permission in the API key settings.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional
    :param url: The URL to access the Kraken API (default:
        https://api.kraken.com)
    :type url: str, optional
    :param proxy: proxy URL, may contain authentication information
    :type proxy: str, optional

    .. code-block:: python
        :linenos:
        :caption: Spot User: Create the user client

        >>> from kraken.spot import User
        >>> user = User() # unauthenticated
        >>> auth_user = User(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: Spot User: Create the user client as context manager

        >>> from kraken.spot import User
        >>> with User(key="api-key", secret="secret-key") as user:
        ...     print(user.get_account_balances())
    """

    def __init__(  # nosec: B107
        self: User,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, proxy=proxy)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def get_account_balance(
        self: User,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the current balances of the user.

        Requires the ``Query funds`` permission in the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-account-balance

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the account balances

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_account_balances()
            {
                'ZUSD': '241983.1415',
                'KFEE': '8020.22',
                'BCH': '0.0000077100',
                'ETHW': '0.0000040',
                'XXLM': '0.00000000',
                'ZEUR': '0.0000',
                'DOT': '32011.21197000',
                ...
            }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Balance",
            extra_params=extra_params,
        )

    def get_balances(
        self: User,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve the user's asset balances and the the corresponding amount held
        by open orders.

        Requires the ``Query funds`` permission in the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-extended-balance

        :return: Dictionary containing the ``currency`` as keys, that hold a
            dictionary containing the ``balance`` key holding the actual balance
            including the value in orders and the ``hold_trade`` key that
            represents the amount held in open orders.
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get balances

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_balances()
            {
                'XXLM': {
                    'balance': '0.00000000', 'hold_trade': '0.00000000'
                },
                'ZEUR': {
                    'balance': '500.0000', 'hold_trade': '0.0000'
                },
                'XXBT': {
                    'balance': '2.1031709100', 'hold_trade': '0.1401000000'
                },
                'KFEE': {
                    'balance': '1407.73', 'hold_trade': '0.00'
                },
                ...
            }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/BalanceEx",
            extra_params=extra_params,
        )

    def get_balance(self: User, currency: str) -> dict:
        """
        Returns the balance and available balance of a given currency.

        Requires the ``Query funds`` permission in the API key settings.

        :param currency: The currency to get the balances from
        :type currency: str
        :return: Dictionary containing the ``currency`` (currency as string),
            ``balance`` (including value in orders), and ``available_balance``
            (amount that is not in orders)
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get balance

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_balance(currency="EUR")
            {
                'currency': 'ZEUR',
                'balance': 6011.2119,
                'available_balance': 4999.0619
            }
        """
        balance: Decimal = Decimal(0)
        available_balance: Decimal = Decimal(0)

        curr_opts: tuple = (currency, f"Z{currency}", f"X{currency}")
        for symbol, data in self.get_balances().items():
            if symbol in curr_opts:
                currency = symbol
                balance = Decimal(data["balance"])
                available_balance = balance - Decimal(data["hold_trade"])
                break

        return {
            "currency": currency,
            "balance": float(balance),
            "available_balance": float(available_balance),
        }

    def get_trade_balance(
        self: User,
        asset: str | None = "ZUSD",
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the summary of all collateral balances.

        Requires the ``Query funds``, ``Query open orders & trades``, and
        ``Query closed orders & trades`` permissions in the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-trade-balance

        :param asset: The base asset to determine the balances (default:
            ``ZUSD``)
        :type asset: str, optional

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the trade balance

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_trade_balance()
            {
                'eb': '983691.5512', # Equivalent balance - all currencies combined
                'tb': '322296.9914', # Trade balance - balance of all equity currencies
                'm': '0.0000',       # Margin amount of open positions
                'uv': '0.0000',      # Unexecuted value of partly filled orders/positions
                'n': '0.0000',       # Unrealized net profit/loss of open positions
                'c': '0.0000',       # Cost basis of open positions
                'v': '0.0000',       # Current floating value of open positions
                'e': '983691.5512',  # Equity ( eb + n )
                'mf': '322296.9914'  # Free margin ( tb / initial margin ) * 100
            }
        """
        params: dict = {}
        if defined(asset):
            params["asset"] = asset
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/TradeBalance",
            params=params,
            extra_params=extra_params,
        )

    def get_open_orders(
        self: User,
        userref: int | None = None,
        *,
        trades: bool | None = False,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about the open orders.

        Requires the ``Query open orders & trades`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/rest-api/get-open-orders

        :param userref: Filter the results by user reference id
        :type userref: int, optional
        :param trades: Include trades related to position or not into the
            response (default: ``False``)
        :type trades: bool

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the open orders

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_open_orders()
            {
                'open': {
                    'OCUG7Z-4EM5R-7ZCJ47': {
                        'refid': None,
                        'userref': 0,
                        'status':
                        'open',
                        'opentm': 1680777427.576083,
                        'starttm': 0,
                        'expiretm': 0,
                        'descr': {
                            'pair': 'ETHUSD',
                            'type': 'buy',
                            'ordertype': 'limit',
                            'price': '1720.37',
                            'price2': '0',
                            'leverage': 'none',
                            'order': 'buy 0.02000000 ETHUSD @ limit 1720.37',
                            'close': ''
                        },
                        'vol': '0.02000000',
                        'vol_exec': '0.00000000',
                        'cost': '0.00000',
                        'fee': '0.00000',
                        'price': '0.00000',
                        'stopprice': '0.00000',
                        'limitprice': '0.00000',
                        'misc': '',
                        'oflags': 'fciq'
                    },
                    'OFZP3V-UMMUJ-6HMRMB': {
                        ...
                    }
                }
            }
        """
        params: dict = {"trades": trades}
        if defined(userref):
            params["userref"] = userref
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/OpenOrders",
            params=params,
            extra_params=extra_params,
        )

    def get_closed_orders(
        self: User,
        userref: int | None = None,
        start: int | None = None,
        end: int | None = None,
        ofs: int | None = None,
        closetime: str | None = "both",
        *,
        trades: bool | None = False,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the 50 latest closed (filled or canceled) orders.

        Requires the ``Query closed orders & trades`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/rest-api/get-closed-orders

        :param userref: Filter the results by user reference id
        :type userref: int, optional
        :param start: Unix timestamp to start the search from
        :type start: int, optional
        :param end: Unix timestamp to define the last result to include
        :type end: int, optional
        :param ofs: Offset for pagination
        :type ofs: int, optional
        :param closetime: Specify the exact time frame, one of: ``both``,
            ``open``, ``close`` (default: ``both``)
        :type closetime: str, optional
        :param trades: Include trades related to position into the response or
            not (default: ``False``)
        :type trades: bool

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the closed orders

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_closed_orders()
            {
                'closed': {
                    'OBGFYP-XVQNL-P4GMWF': {
                        'refid': None,
                        'userref': 0,
                        'status': 'closed',
                        'opentm': 1680698929.9052045,
                        'starttm': 0,
                        'expiretm': 0,
                        'descr': {
                            'pair': 'ETHUSD',
                            'type': 'buy',
                            'ordertype': 'limit',
                            'price': '1860.76',
                            'price2': '0',
                            'leverage': 'none',
                            'order': 'buy 0.02000000 ETHUSD @ limit 1860.76',
                            'close': ''
                        },
                        'vol': '0.02000000',
                        'vol_exec': '0.02000000',
                        'cost': '37.21520',
                        'fee': '0.05954',
                        'price': '1860.76',
                        'stopprice': '0.00000',
                        'limitprice': '0.00000',
                        'misc': '',
                        'oflags': 'fciq',
                        'reason': None,
                        'closetm': 1680777419.8115675
                    },
                    'OAUHYR-YCVK6-P22G6P': {
                        ...
                    }
                }
            }
        """
        params: dict = {"trades": trades, "closetime": closetime}
        if defined(userref):
            params["userref"] = userref
        if defined(start):
            params["start"] = start
        if defined(end):
            params["end"] = end
        if defined(ofs):
            params["ofs"] = ofs

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/ClosedOrders",
            params=params,
            extra_params=extra_params,
        )

    @ensure_string("txid")
    def get_orders_info(
        self: User,
        txid: list[str] | str,
        userref: int | None = None,
        *,
        trades: bool | None = False,
        consolidate_taker: bool | None = True,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about one or more orders.

        Requires the ``Query open orders & trades`` and ``Query closed orders &
        trades`` permissions in the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-orders-info

        :param txid: A transaction id of a specific order, a list of txids or a
            string containing a comma delimited list of txids
        :type txid: str | list[str]
        :param userref: Filter results by user reference id
        :type userref: int, optional
        :param trades: Include trades in the result or not (default: ``False``)
        :type trades: bool, optional
        :param consolidate_taker: Consolidate trades by individual taker trades
            (default: ``True``)
        :type consolidate_taker: bool, optional

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get order information

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_orders_info(txid="OG5IL4-6AR7I-ZAPZEZ")
            {
                'OG5IL4-6AR7I-ZAPZEZ': {
                    'refid': None,
                    'userref': 0,
                    'status': 'open',
                    'opentm': 1680618712.3723278,
                    'starttm': 0,
                    'expiretm': 0,
                    'descr': {
                        'pair': 'MATICUSD',
                        'type': 'buy',
                        'ordertype': 'limit',
                        'price': '1.0922',
                        'price2': '0',
                        'leverage': 'none',
                        'order': 'buy 45.77910000 MATICUSD @ limit 1.0922',
                        'close': ''
                    },
                    'vol': '45.77910000',
                    'vol_exec': '0.00000000',
                    'cost': '0.000000',
                    'fee': '0.000000',
                    'price': '0.000000',
                    'stopprice': '0.000000',
                    'limitprice': '0.000000',
                    'misc': '',
                    'oflags': 'fciq',
                    'reason': None
                }
            }
            >>> user.get_orders_info(txid=["OAUHYR-YCVK6-P22G6P", "OG5IL4-6AR7I-ZAPZEZ"])
            {
                'OAUHYR-YCVK6-P22G6P': {
                    'refid': None,
                    'userref': 0,
                    'status': 'canceled',
                    'opentm': 1680618716.4409518,
                    'starttm': 0,
                    'expiretm': 0,
                    'descr': {
                        'pair': 'MATICUSD',
                        'type': 'buy',
                        'ordertype': 'limit',
                        'price': '1.0501',
                        'price2': '0',
                        'leverage': 'none',
                        'order': 'buy 47.61450000 MATICUSD @ limit 1.0501',
                        'close': ''
                    },
                    'vol': '47.61450000',
                    'vol_exec': '0.00000000',
                    'cost': '0.000000',
                    'fee': '0.000000',
                    'price': '0.000000',
                    'stopprice': '0.000000',
                    'limitprice': '0.000000',
                    'misc': '',
                    'oflags': 'fciq',
                    'reason': 'User requested',
                    'closetm': 1680756419.5768735
                }
            }
        """
        params: dict = {
            "txid": txid,
            "trades": trades,
            "consolidate_taker": consolidate_taker,
        }
        if defined(userref):
            params["userref"] = userref
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/QueryOrders",
            params=params,
            extra_params=extra_params,
        )

    def get_order_amends(
        self: User,
        order_id: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about historical order amends.

        Requires the ``Query open orders & trades`` and ``Query closed orders &
        trades`` permissions in the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-order-amends

        :param order_id: The ``order_id`` to filter for.
        :type txid: str

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get order amends

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_order_amends(txid="OVM3PT-56ACO-53SM2T")
            {'amends': [], 'count': 0}
        """
        params = {}
        if defined(order_id):
            params["order_id"] = order_id
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/OrderAmends",
            params=params,
            extra_params=extra_params,
        )

    def get_trades_history(  # pylint: disable=too-many-arguments
        self: User,
        type_: str | None = "all",
        start: int | None = None,
        end: int | None = None,
        ofs: int | None = None,
        *,
        trades: bool | None = False,
        consolidate_taker: bool = True,
        ledgers: bool = False,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about the latest 50 trades and fills. Can be paginated.

        Requires the ``Query closed orders & trades`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/rest-api/get-trade-history

        :param type_: Filter by type of trade, one of: ``all``, ``any
            position``, ``closed position``, ``closing position``, and ``no
            position`` (default: ``all``)
        :type type_: str, optional
        :param start: Timestamp or txid to start the search
        :type start: int, optional
        :param end: Timestamp or txid to define the last included result
        :type end: int, optional
        :param trades: Include trades related to a position or not (default:
            ``False``)
        :type trades: bool, optional
        :param consolidate_taker: Consolidate trades by individual taker trades
            (default: ``True``)
        :type consolidate_taker: bool
        :param ledgers: Include related leger entries for filtered trade
            (default: ``False``)
        :type ledgers: bool

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the trade history

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_trades_history()
            {
                'count': 630,
                'trades': {
                    'TPLJ5E-NONOU-5LH7JL': {
                        'ordertxid': 'OBGFYP-XVQNL-P4GMWF',
                        'postxid': 'TKH2SE-M7IF5-CFI7LT',
                        'pair': 'XETHZUSD',
                        'time': 1680777419.8115635,
                        'type': 'buy',
                        'ordertype': 'limit',
                        'price': '1860.76000',
                        'cost': '37.21520',
                        'fee': '0.05954',
                        'vol': '0.02000000',
                        'margin': '0.00000',
                        'leverage': '0',
                        'misc': '',
                        'trade_id': 43914718
                    },
                    'TNGMNU-XQSRA-LKCWOK': { ... },
                    ...
                }
            }
        """
        params: dict = {
            "type": type_,
            "trades": trades,
            "ledgers": ledgers,
            "consolidate_taker": consolidate_taker,
        }
        if defined(start):
            params["start"] = start
        if defined(end):
            params["end"] = end
        if defined(ofs):
            params["ofs"] = ofs
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/TradesHistory",
            params=params,
            extra_params=extra_params,
        )

    @ensure_string("txid")
    def get_trades_info(
        self: User,
        txid: str | list[str],
        *,
        trades: bool | None = False,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about specific trades/filled orders. 20 txids can be
        queried maximum.

        Requires the ``Query open orders & trades`` and ``Query closed orders &
        trades`` permission in the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-trades-info

        :param txid: txid or list of txids or comma delimited list of txids as
            string
        :type txid: str | list[str]
        :param trades: Include trades related to position in result (default:
            ``False``)
        :type trades: bool

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the historical trade information

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_trades_info(txid="TNGMNU-XQSRA-LKCWOK")
            {
                'TNGMNU-XQSRA-LKCWOK': {
                    'ordertxid': 'OHAJCS-ON45W-UIXHT7',
                    'postxid': 'TKH2SE-M7IF5-CFI7LT',
                    'pair': 'XETHZUSD',
                    'time': 1680606470.360982,
                    'type': 'sell',
                    'ordertype': 'limit',
                    'price': '1855.16000',
                    'cost': '37.10320',
                    'fee': '0.05937',
                    'vol': '0.02000000',
                    'margin': '0.00000',
                    'leverage': '0',
                    'misc': '',
                    'trade_id': 43878042
                }
            }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/QueryTrades",
            params={
                "trades": trades,
                "txid": txid,
            },
            extra_params=extra_params,
        )

    @ensure_string("txid")
    def get_open_positions(
        self: User,
        txid: str | list[str] | None = None,
        consolidation: str | None = "market",
        *,
        docalcs: bool | None = False,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about the open margin positions.

        Requires the ``Query open orders & trades`` permission in the API key
        settings.

        - https://docs.kraken.com/api/docs/rest-api/get-open-positions

        :param txid: Filter by txid or list of txids or comma delimited list of
            txids as string
        :type txid: str | list[str], optional
        :param consolidation: Consolidate positions by market/pair (default:
            ``market``)
        :type consolidation: str, optional
        :param docalcs: Include profit and loss calculation into the result
            (default: ``False``)
        :type docalcs: bool, optional
        :return: List of open positions
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the open margin positions

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_open_positions()
            {
                'TF5GVO-T7ZZ2-6NBKBI': {
                    'ordertxid': 'O0SFFP-ABH4R-LOLNFG',
                    'posstatus': 'open',
                    'pair': 'XXBTZUSD',
                    'time': 1618748097.12341,
                    'type': 'buy',
                    'ordertype': 'limit',
                    'cost': '801243.52842',
                    'fee': '208.44527',
                    'vol': '8.82412861',
                    'vol_closed': '0.20200000',
                    'margin': '17234.123968',
                    'value": '231463.1',
                    'net": '+134186.9728',
                    'terms": '0.0100% per 4 hours',
                    'rollovertm': '1623672637',
                    'misc': '',
                    'oflags": ''
                }, ...
            }
        """
        params: dict = {"docalcs": docalcs, "consolidation": consolidation}
        if defined(txid):
            params["txid"] = txid
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/OpenPositions",
            params=params,
            extra_params=extra_params,
        )

    @ensure_string("asset")
    def get_ledgers_info(
        self: User,
        asset: str | list[str] | None = "all",
        aclass: str | None = "currency",
        type_: str | None = "all",
        start: int | None = None,
        end: int | None = None,
        ofs: int | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about the users ledger entries. 50 results can be
        returned at a time.

        Requires the ``Query funds`` and ``Query ledger entries`` permissions in
        the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-ledgers

        :param asset: The asset(s) to filter for (default: ``all``)
        :type asset: str | list[str]
        :param aclass: The asset class (default: ``currency`` )
        :type aclass: str
        :param type_: Ledger type, one of: ``all``, ``deposit``, ``withdrawal``,
         ``trade``, ``margin``, ``rollover``, ``credit``, ``transfer``,
         ``settled``, ``staking``, and ``sale`` (default: ``all``)
        :type type_: str, optional
        :param start: Unix timestamp to start the search from
        :type start: int, optional
        :param end: Unix timestamp to define the last result
        :type end: int, optional
        :param ofs: Offset for pagination
        :type ofs: int, optional

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get ledgers info

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_ledgers_info(asset=["KFEE","EUR","ETH"])
            {
                'count': 519,
                'ledger': {
                    'LKLSX7-VUXD4-HDLK2P': {
                        'aclass': 'currency',
                        'amount': '0.00',
                        'asset': 'KFEE',
                        'balance': '8020.22',
                        'fee': '5.95',
                        'refid': 'TPLJ5E-NONOU-5LH7JL',
                        'time': 1680777419.8115911,
                        'type': 'trade',
                        'subtype': ''
                    },
                    'L4BF6E-FIFW7-6UB2CI': { ... },
                    ...
                }
            }
        """
        params: dict = {"asset": asset, "aclass": aclass, "type": type_}
        if defined(start):
            params["start"] = start
        if defined(end):
            params["end"] = end
        if defined(ofs):
            params["ofs"] = ofs
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/Ledgers",
            params=params,
            extra_params=extra_params,
        )

    @ensure_string("id_")
    def get_ledgers(
        self: User,
        id_: str | list[str],
        *,
        trades: bool | None = False,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get information about specific ledeger entries.

        Requires the ``Query funds`` and ``Query ledger entries`` permissions in
        the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-ledgers-info

        :param id_: Ledger id as string, list of strings, or comma delimited
            list of ledger ids as string
        :type id_: str | list[str]
        :param trades: Include trades related to a position or not (default:
            ``False``)
        :type trades: bool, optional

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get ledgers

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_ledgers(id_="LKLSX7-VUXD4-HDLK2P")
            {
                'LKLSX7-VUXD4-HDLK2P': {
                    'aclass': 'currency',
                    'amount': '0.00',
                    'asset': 'FEE',
                    'balance': '8020.22',
                    'fee': '5.95',
                    'refid': 'TPLJ5E-NONOU-5LH7JL',
                    'time': 1680777419.8115911,
                    'type': 'trade',
                    'subtype': ''
                }
            }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/QueryLedgers",
            params={"trades": trades, "id": id_},
            extra_params=extra_params,
        )

    @ensure_string("pair")
    def get_trade_volume(
        self: User,
        pair: str | list[str] | None = None,
        *,
        fee_info: bool = True,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the 30-day user specific trading volume in USD.

        Requires the ``Query funds`` permission in the API key settings.

        - https://docs.kraken.com/api/docs/rest-api/get-trade-volume

        :param pair: Asset pair, list of asset pairs or comma delimited list (as
            string) of asset pairs to filter
        :type pair: str | list[str], optional
        :param fee_info: Include fee information or not (default: ``True``)
        :type fee_info: bool, optional

        .. code-block:: python
            :linenos:
            :caption: Spot User: Get the 30-day trade volume

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.get_trade_volume()
            {
                'currency': 'ZUSD',
                'volume': '212220.9741',
                'fees': None,
                'fees_maker': None
            }
            >>> u.get_trade_volume(pair="DOTUSD")
            {
                'currency': 'ZUSD',
                'volume': '212243.1210',
                'fees': {
                    'DOTUSD': {
                        'fee': '0.2200',
                        'minfee': '0.1000',
                        'maxfee': '0.2200',
                        'nextfee': '0.2000',
                        'tiervolume': '0.0000',
                        'nextvolume': '250000.0000'
                    }
                },
                'fees_maker': {
                    'DOTUSD': {
                        'fee': '0.1200',
                        'minfee': '0.0000',
                        'maxfee': '0.1200',
                        'nextfee': '0.1000',
                        'tiervolume': '0.0000',
                        'nextvolume': '250000.0000'
                    }
                }
            }

        """
        params: dict = {"fee-info": fee_info}
        if defined(pair):
            params["pair"] = pair
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/TradeVolume",
            params=params,
            extra_params=extra_params,
        )

    @ensure_string("fields")
    def request_export_report(  # pylint: disable=too-many-arguments
        self: User,
        report: str,
        description: str,
        format_: str | None = "CSV",
        fields: str | list[str] | None = "all",
        starttm: int | None = None,
        endtm: int | None = None,
        *,
        timeout: int | None = 10,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Request to export the trades or ledgers of the user.

        Requires the ``Export data`` permission. In addition for exporting
        trades data the permissions ``Query open orders & trades`` and ``Query
        closed orders & trades`` must be set. For exporting ledgers the ``Query
        funds`` and ``Query ledger entries`` must be set.

        - https://docs.kraken.com/api/docs/rest-api/add-export

        :param report: Kind of report, one of: ``trades`` and ``ledgers``
        :type report: str
        :param format_: The export format of the requesting report, one of
            ``CSV`` and ``TSV`` (default: ``CSV``)
        :type format_: str
        :param fields: Fields to include in the report (default: ``all``)
        :type fields: str | list[str], optional
        :param starttm: Unix timestamp to start
        :type starttm: int, optional
        :param endtm: Unix timestamp of the last result
        :type endtm: int, optional
        :param timeout: The timeout for that request (default: ``10``)
        :type timeout: int
        :return: A dictionary containing the export id
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot User: Request an report export

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.request_export_report(
            ...     report="ledgers", description="myLedgers1", format="CSV"
            ... )
            { 'id': 'GEHI' }
        """
        if report not in {"trades", "ledgers"}:
            raise ValueError('`report` must be either "trades" or "ledgers".')

        params: dict = {
            "report": report,
            "description": description,
            "format": format_,
            "fields": fields,
        }
        if defined(starttm):
            params["starttm"] = starttm
        if defined(endtm):
            params["endtm"] = endtm
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/AddExport",
            params=params,
            extra_params=extra_params,
            timeout=timeout,
        )

    def get_export_report_status(
        self: User,
        report: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get the status of the current pending report.

        Requires the ``Export data`` permission. In addition for exporting
        trades data the permissions ``Query open orders & trades`` and ``Query
        closed orders & trades`` must be set. For exporting ledgers the ``Query
        funds`` and ``Query ledger entries`` must be set.

        - https://docs.kraken.com/api/docs/rest-api/export-status

        :param report: Kind of report, one of: ``trades``, ``ledgers``
        :type report: str
        :return: Information about the pending report
        :rtype: list[dict]

        .. code-block:: python
            :linenos:
            :caption: Example

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> response = user.request_export_report(
            ...     report="ledgers", description="myLedgers1", format="CSV"
            ... )
            { 'id': 'GEHI' }
            >>> user.get_export_report_status(report="ledgers")
            [
                {
                    'id': 'GEHI',
                    'descr': 'myLedgers1',
                    'format': 'CSV',
                    'report': 'ledgers',
                    'status': 'Queued',
                    'aclass': 'currency',
                    'fields': 'all',
                    'asset': 'all',
                    'subtype': 'all',
                    'starttm': '1680307200',
                    'endtm': '1680855267',
                    'createdtm': '1680855267',
                    'expiretm': '1682064867',
                    'completedtm': '0',
                    'datastarttm': '1680307200',
                    'dataendtm': '1680855267',
                    'flags': '0'
                }
            ]
        """
        if report not in {"trades", "ledgers"}:
            raise ValueError('report must be one of "trades", "ledgers"')
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/ExportStatus",
            params={"report": report},
            extra_params=extra_params,
        )

    def retrieve_export(
        self: User,
        id_: str,
        timeout: int = 10,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve the requested report export.

        Requires the ``Export data`` permission. In addition for exporting
        trades data the permissions ``Query open orders & trades`` and ``Query
        closed orders & trades`` must be set. For exporting ledgers the ``Query
        funds`` and ``Query ledger entries`` must be set.

        - https://docs.kraken.com/api/docs/rest-api/retrieve-export

        :param id_: Id of the report that was requested
        :type id_: str
        :param timeout: Timeout for that request, default: ``10`` seconds
        :type timeout: int, optional
        :return: The response - a zipped report
        :rtype: requests.Response

        .. code-block:: python
            :linenos:
            :caption: Spot User: Save the exported report to CSV

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> response = user.request_export_report(
            ...     report="ledgers", description="myLedgers1", format="CSV"
            ... )
            { 'id': 'GEHI' }
            >>> ledgers_data = user.retrieve_export(id_=response["id"])
            >>> with open("myExport.zip", "wb") as file:
            ...     for chunk in ledgers_data.iter_content(chunk_size=512):
            ...         if chunk:
            ...             file.write(chunk)

        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/RetrieveExport",
            params={"id": id_},
            timeout=timeout,
            return_raw=True,
            extra_params=extra_params,
        )

    def delete_export_report(
        self: User,
        id_: str,
        type_: str | None = "delete",
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Delete a report from the Kraken server.

        Requires the ``Export data`` permission. In addition for exporting
        trades data the permissions ``Query open orders & trades`` and ``Query
        closed orders & trades`` must be set. For exporting ledgers the ``Query
        funds`` and ``Query ledger entries`` must be set.

        - https://docs.kraken.com/api/docs/rest-api/remove-export

        :param id_: The id of the report
        :type id_: str
        :param type_: The type of the export, one of: ``cancel`` and ``delete``
            (default: ``delete``)
        :type type_: str, optional
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot User: Delete or cancel the report

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.delete_export_report(id_="GEHI", type_="delete")
            { 'delete': True }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/RemoveExport",
            params={"id": id_, "type": type_},
            extra_params=extra_params,
        )

    def create_subaccount(
        self: User,
        username: str,
        email: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Create a subaccount for trading. This is currently *only available for
        institutional clients*.

        - https://docs.kraken.com/api/docs/rest-api/create-subaccount

        :param username: The username for the new subaccount
        :type username: str
        :param email: The E-Mail address for the new subaccount
        :type email: str
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot User: Create a subaccount

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.create_subaccount(username="user", email="user@domain.com")
            { 'result': True }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/CreateSubaccount",
            params={"username": username, "email": email},
            extra_params=extra_params,
        )

    def account_transfer(
        self: User,
        asset: str,
        amount: str | float,
        from_: str,
        to_: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Transfer funds between master and subaccounts. This is currently *only
        available for institutional clients and must be called by the master
        account*.

        - https://docs.kraken.com/api/docs/rest-api/account-transfer

        :param asset: The asset to transfer
        :type asset: str
        :param amount: The amount of that asset to transfer
        :type amount: str | float
        :param from_: The source account (IIBAN)
        :type from_: str
        :param to_: The destination account (IIBAN)
        :type to_: str
        :return: Success or failure
        :rtype: dict

        .. code-block:: python
            :linenos:
            :caption: Spot User: Transfer funds between accounts

            >>> from kraken.spot import User
            >>> user = User(key="api-key", secret="secret-key")
            >>> user.account_transfer(
            ...     "asset": "XBT",
            ...     "amount": 1.0,
            ...     "from": "ABCD 1234 EFGH 5678"
            ...     "to": "IJKL 0987 MNOP 6543"
            ... )
            {
                'result': {
                    'transfer_id': 'TOH3AS2-LPCWR8-JDQGEU',
                    'status': 'complete'
                }
            }
        """
        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/AccountTransfer",
            params={"asset": asset, "amount": amount, "from": from_, "to": to_},
            extra_params=extra_params,
        )


__all__ = ["User"]
