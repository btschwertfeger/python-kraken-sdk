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

# print(Market().get_ohlc(price_type='trade', symbol='PI_XBTUSD', interval='5m'))
print(Market().get_orderbook(symbol='fi_xbtusd_180615'))
