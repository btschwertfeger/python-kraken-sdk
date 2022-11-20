from kraken.futures.market.market import MarketClient
from kraken.futures.trade.trade import TradeClient
from kraken.futures.user.user import UserClient
from kraken.futures.funding.funding import FundingClient
from kraken.futures.ws_client.ws_client import FuturesWsClientCl

class User(UserClient):
    pass

class Trade(TradeClient):
    pass

class Market(MarketClient):
    pass

class Funding(FundingClient):
    pass

class WsClient(FuturesWsClientCl):
    pass