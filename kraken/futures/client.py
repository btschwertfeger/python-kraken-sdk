from kraken.futures.market.market import MarketClient
from kraken.futures.trade.trade import TradeClient
from kraken.futures.user.user import UserClient
from kraken.futures.funding.funding import FundingClient
from kraken.futures.websocket.websocket import KrakenFuturesWSClientCl
from kraken.exceptions.exceptions import KrakenExceptions 
class User(UserClient):
    pass

class Trade(TradeClient):
    pass

class Market(MarketClient):
    pass

class Funding(FundingClient):
    pass

class KrakenFuturesWSClient(KrakenFuturesWSClientCl):
    pass