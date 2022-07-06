from market.market import MarketData
from trade.trade import TradeData
from user.user import UserData
from funding.funding import FundingData
from staking.staking import StakingData
from ws_client.ws_client import WsClientData

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
