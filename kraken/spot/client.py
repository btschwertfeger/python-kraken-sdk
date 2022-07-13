from kraken.spot.market.market import MarketClient
from kraken.spot.trade.trade import TradeClient
from kraken.spot.user.user import UserClient
from kraken.spot.funding.funding import FundingClient
from kraken.spot.staking.staking import StakingClient
from kraken.spot.ws_client.ws_client import SpotWsClientCl

class User(UserClient):
    pass

class Trade(TradeClient):
    pass

class Market(MarketClient):
    pass

class Funding(FundingClient):
    pass

class Staking(StakingClient):
    pass

class WsClient(SpotWsClientCl):
    pass
