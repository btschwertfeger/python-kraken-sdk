import sys, os

try:
    from kraken.futures.client import Market, User, Trade, Funding
except:
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.futures.client import Market, User, Trade, Funding

import logging
from dotenv import dotenv_values

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

    key = dotenv_values('.env')['Futures_SANDBOX_KEY']
    secret = dotenv_values('.env')['Futures_SANDBOX_SECRET']

    market = Market()
    # print(market.get_ohlc(price_type='trade', symbol='PI_XBTUSD', interval='5m'))
    # print(market.get_fee_schedules())
    # print(market.get_orderbook(symbol='fi_xbtusd_180615'))
    # print(market.get_tickers())
    # print(market.get_instruments())
    # print(market.get_instruments_status())
    # print(market.get_instruments_status(instrument='PI_XBTUSD'))
    # print(market.get_trade_history(symbol='PI_XBTUSD'))
    # print(market.get_historical_funding_rates(symbol='PI_XBTUSD'))
    # print(market.get_market_history_execution(symbol='PI_XBTUSD'))
    # print(market.get_market_history_mark_price(symbol='PI_XBTUSD'))
    # print(market.get_market_history_orders(symbol='PI_XBTUSD'))

    priv_market = Market(key=key,secret=secret, sandbox=True)
    # print(priv_market.get_fee_schedules_vol())
    # print(priv_market.get_leverage_preference())
    # print(priv_market.set_leverage_preference(symbol='PF_SOLUSD', maxLeverage=5)) # set max leverage
    # print(priv_market.set_leverage_preference(symbol='PF_SOLUSD')) # reset max leverage
    # print(priv_market.set_pnl_preference(symbol='PF_XBTUSD', pnlPreference='BTC'))

    user = User(key=key,secret=secret, sandbox=True)
    # print(user.get_wallets())
    # print(user.get_open_orders())
    # print(user.get_open_positions())
    # print(user.get_subaccounts())
    # print(user.get_unwindqueue())
    # print(user.get_notificatios())
    
    trade = Trade(key=key, secret=secret, sandbox=True)
    # print(trade.get_fills())
    # print(trade.get_fills(lastFillTime='2020-07-21T12:41:52.790Z'))
    # print(trade.create_batch_order(
    #     batchorder_list = [
    #         {
    #             "order": "send",
    #             "order_tag": "1",
    #             "orderType": "lmt",
    #             "symbol": "PI_XBTUSD",
    #             "side": "buy",
    #             "size": 1,
    #             "limitPrice": 1.00,
    #             "cliOrdId": "my_another_client_id"
    #         },
    #         {
    #             "order": "send",
    #             "order_tag": "2",
    #             "orderType": "stp",
    #             "symbol": "PI_XBTUSD",
    #             "side": "buy",
    #             "size": 1,
    #             "limitPrice": 2.00,
    #             "stopPrice": 3.00,
    #         },
    #         {
    #             "order": "cancel",
    #             "order_id": "e35d61dd-8a30-4d5f-a574-b5593ef0c050",
    #         },
    #         {
    #             "order": "cancel",
    #             "cliOrdId": "my_client_id",
    #         },
    #     ],
    # ))

    funding = Funding(key=key, secret=secret, sandbox=True)
    # print(funding.get_historical_funding_rates(symbol='PF_SOLUSD'))


if __name__ == '__main__':
    main()
