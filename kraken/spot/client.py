"""Module that provides the Spot REST clients"""
from kraken.spot.funding.funding import FundingClient
from kraken.spot.market.market import MarketClient
from kraken.spot.staking.staking import StakingClient
from kraken.spot.trade.trade import TradeClient
from kraken.spot.user.user import UserClient
from kraken.spot.websocket.websocket import KrakenSpotWSClientCl


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


class Staking(StakingClient):
    """Class that is used as a client to access the staking-related
    Kraken Futures endpoints.
    """


class KrakenSpotWSClient(KrakenSpotWSClientCl):
    """Class that is used as a client to create a websocket connection
    and handle un/subscribing, reconnecting, ...
    """
