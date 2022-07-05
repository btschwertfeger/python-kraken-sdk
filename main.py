import os, sys

sys.path.append('/Users/benjamin/repositories/Trading/')

from client import User, Market, Trade
from dotenv import dotenv_values

def main() -> None:

    user = User(
        key=dotenv_values('.env')['API_KEY'],
        secret=dotenv_values('.env')['SECRET_KEY']
    )
    market = Market()

    # ____User_____
    # print(market.get_assets(assets=['XBT']))
    # print(market.get_tradable_asset_pair(pair=['BTCEUR','DOTEUR']))
    # print(market.get_ticker(pair='BTCUSD'))
    # print(market.get_ohlc(pair='BTCUSD', interval=5))
    # print(market.get_order_book(pair='BTCUSDT', count=10))
    # print(market.get_recent_trades(pair='BTCUSDT'))
    # print(user.get_account_balance())
    # print(user.get_closed_orders())

    # ____Trade____



if __name__ == '__main__':
    main()
