import sys, os

try:
    from kraken.futures.client import FuturesUser, FuturesMarket, FuturesTrade
except:
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.futures.client import FuturesUser, FuturesMarket, FuturesTrade

import logging
logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filemode='w',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

from dotenv import dotenv_values

def main() -> None:

    key = dotenv_values('.env')['Futures_SANDBOX_KEY']
    secret = dotenv_values('.env')['Futures_SANDBOX_SECRET']


    user = FuturesUser(key=key, secret=secret, sandbox=True)
    # print(user.get_accounts())
    # print(user.get_open_positions())
    # print(user.get_open_orders())
    # print(user.get_fills())
    # print(user.get_pnl_preferences())
    # print(user.get_leverage_preferences())
    # print(user.get_subaccounts())

    market = FuturesMarket()
    # print(market.get_ohlc(price_type='trade', symbol='PI_XBTUSD', interval='5m'))
    # print(market.get_fee_schedules())
    # print(market.get_orderbook(symbol='fi_xbtusd_180615'))
    # print(market.get_tickers())
    # print(market.get_instruments())
    # print(market.get_history(symbol='pi_xbtusd'))
    # print(market.get_historical_funding_rates(symbol='PI_XBTUSD'))
    # print(market.get_market_history_execution(symbol='pi_xbtusd'))
    # print(market.get_market_history_mark_price(symbol='pi_xbtusd'))
    # print(market.get_market_history_orders(symbol='pi_xbtusd'))

    trade = FuturesTrade(key=key, secret=secret, sandbox=True)
    # print(trade.send_order(orderType='lmt', symbol='pi_xbtusd', side='buy', size=1000, limitPrice=18000))
    # print(trade.edit_order(orderId=123456789, side='buy', size=800, limitPrice=18100))
    # print(trade.cancel_order(orderId=123456789))

if __name__ == '__main__':
    main()
