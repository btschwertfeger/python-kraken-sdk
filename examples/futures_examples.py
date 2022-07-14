import sys, os

sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')

from kraken.futures.client import Market
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


def main() -> None:

    market = Market()

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

if __name__ == '__main__':
    main()
