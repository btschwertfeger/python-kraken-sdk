"""This module provides the Kraken Futures clients"""

from kraken.futures.funding.funding import FundingClient
from kraken.futures.market.market import MarketClient
from kraken.futures.trade.trade import TradeClient
from kraken.futures.user.user import UserClient
from kraken.futures.websocket.websocket import KrakenFuturesWSClientCl


class User(UserClient):
    """Class that is used as a client to access the user-related
    Kraken Futures endpoints.
    """


class Trade(TradeClient):
    """Class that is used as a client to access the trade-related
    Kraken Futures endpoints.
    """


class Market(MarketClient):
    """Class that is used as a client to access the market-related
    Kraken Futures endpoints.
    """


class Funding(FundingClient):
    """Class that is used as a client to access the funding-related
    Kraken Futures endpoints.
    """


class KrakenFuturesWSClient(KrakenFuturesWSClientCl):
    """Class that is used as a client to create a websocket connection
    and handle un/subscribing, reconnecting, ...
    """
