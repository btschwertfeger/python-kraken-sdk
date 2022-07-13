from kraken.market.market import MarketData
from kraken.trade.trade import TradeData
from kraken.user.user import UserData
from kraken.funding.funding import FundingData
from kraken.staking.staking import StakingData
from kraken.ws_client.ws_client import WsClientData

class User(UserData):
    pass

class Trade(TradeData):
    pass

class Market(MarketData):
    pass

class Funding(FundingData):
    pass

class Staking(StakingData):
    pass

class WsClient(WsClientData):
    pass
