import os, sys
from dotenv import dotenv_values
import random
import time
import logging, logging.config
from tqdm import tqdm

try:
    from kraken.futures.client import User, Market, Trade, Funding
except:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.futures.client import User, Market, Trade, Funding

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filemode='w',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

key = dotenv_values('.env')['Futures_API_KEY']
secret = dotenv_values('.env')['Futures_SECRET_KEY']

isSuccess = lambda r: type(r) == dict and 'result' in r and r['result'] == 'success'

def test_user_endpoints() -> None: 
    k = 'USER'
    logging.info(f'{k}: Creating user clients')
    user = User()
    auth_user = User(key=key, secret=secret)
    logging.info(f'{k}: Checking endpoints')

    assert isSuccess(auth_user.get_wallets())
    assert isSuccess(auth_user.get_open_orders())
    assert isSuccess(auth_user.get_open_positions())
    assert isSuccess(auth_user.get_subaccounts())
    assert isSuccess(auth_user.get_unwindqueue())
    assert isSuccess(auth_user.get_notificatios())
    time.sleep(2)

    assert type(auth_user.get_account_log()) == dict
    assert type(auth_user.get_account_log(info='futures liquidation')) == dict
    
    response = auth_user.get_account_log_csv()
    assert response.status_code in [200, '200']
    handle = open('account_log.csv', 'wb')
    for chunk in response.iter_content(chunk_size=512):
        if chunk: handle.write(chunk)
    handle.close()        

    logging.info(f'{k}: ALL (tested) ENDPOINTS AVAILABLE!')

def test_market_endpoints() -> None:
    k = 'MARKET'
    logging.info(f'{k}: Creating clients')
    market = Market()
    auth_market = Market(key=key, secret=secret)

    assert type (market.get_ohlc(
        tick_type='trade', 
        symbol='PI_XBTUSD', 
        resolution='1m',
        from_='1668989233'
    )) == dict
    assert type(market.get_tick_types()) == list

    assert type(market.get_tradeable_products(tick_type='mark')) == list
    assert type(market.get_resolutions(tick_type='trade', tradeable='PI_XBTUSD')) == list
    assert type(market.get_fee_schedules()) == dict
    time.sleep(2)

    # assert type(market.get_orderbook()) == dict # raises 500-INTERNAL_SERVER_ERROR on Kraken
    # this endpoint is broken: https://futures.kraken.com/derivatives/api/v3/orderbook
    # assert type(market.get_orderbook()) == dict
    # assert type(market.get_orderbook(symbol='PI_XBTUSD')) == dict

    assert type(market.get_tickers()) == dict
    assert type(market.get_instruments()) == dict
    assert isSuccess(market.get_instruments_status())
    assert isSuccess(market.get_instruments_status(instrument='PI_XBTUSD'))
    time.sleep(2)

    assert isSuccess(market.get_trade_history(symbol='PI_XBTUSD'))
    assert isSuccess(market.get_historical_funding_rates(symbol='PI_XBTUSD'))

    assert isSuccess(auth_market.set_leverage_preference(symbol='PF_SOLUSD', maxLeverage=2))
    assert isSuccess(auth_market.get_leverage_preference())
    assert isSuccess(auth_market.set_leverage_preference(symbol='PF_SOLUSD')) # reset setted preference
    time.sleep(2)

    assert isSuccess(auth_market.set_pnl_preference(symbol='PF_SOLUSD', pnlPreference='USD'))
    assert isSuccess(auth_market.get_pnl_preference())

    assert type(market.get_public_execution_events(tradeable='PF_SOLUSD', since=1668989233)) == dict
    assert type(market.get_public_order_events(tradeable='PF_SOLUSD', since=1668989233)) == dict
    assert type(market.get_public_mark_price_events(tradeable='PF_SOLUSD', since=1668989233)) == dict
    time.sleep(3)

    # needs a higher auth level...
    # assert type(auth_market.get_execution_events(tradeable='PF_SOLUSD', sort='asc', since=1668989233)) == dict
    # assert type(auth_market.get_order_events(tradeable='PF_SOLUSD', since=1668989233)) == dict
    # assert type(auth_market.get_trigger_events(tradeable='PF_SOLUSD', since=1668989233)) == dict
   
    logging.info(f'{k}: ALL (tested) ENDPOINTS AVAILABLE!')

def test_trade_endpoints() -> None:
    k = 'TRADE'
    logging.info(f'{k}: Creating clients')
    trade = Trade(key=key, secret=secret)

    assert isSuccess(trade.get_fills())
    assert isSuccess(trade.get_fills(lastFillTime='2020-07-21T12:41:52.790Z'))
    assert isSuccess(trade.dead_mans_switch(timeout=60))
    assert isSuccess(trade.dead_mans_switch(timeout=0)) # reset
    assert isSuccess(trade.get_orders_status(orderIds='378etweirzgu'))
    
        
    if False:
        raise ValueError('Dont do this')
        time.sleep(2)
        
        assert isSuccess(trade.create_order(
            orderType='lmt',
            size=10,
            symbol='PI_XBTUSD',
            side='buy',
            limitPrice=1,
            stopPrice=10
        ))
        assert isSuccess(trade.create_batch_order(
            batchorder_list = [{
                'order': 'send',
                'order_tag': '1',
                'orderType': 'lmt',
                'symbol': 'PI_XBTUSD',
                'side': 'buy',
                'size': 1,
                'limitPrice': 1.00,
                'cliOrdId': 'my_another_client_id'
            }, {
                'order': 'send',
                'order_tag': '2',
                'orderType': 'stp',
                'symbol': 'PI_XBTUSD',
                'side': 'buy',
                'size': 1,
                'limitPrice': 2.00,
                'stopPrice': 3.00,
            }, {
                'order': 'cancel',
                'order_id': 'e35d61dd-8a30-4d5f-a574-b5593ef0c050',
            }, {
                'order': 'cancel',
                'cliOrdId': 'my_client_id',
            }],
        ))
        time.sleep(2)
        assert isSuccess(trade.edit_order(orderId='my_another_client_id', limitPrice=3))
        time.sleep(.1)
        assert isSuccess(trade.cancel_order(cliOrdId='my_another_client_id'))
        assert isSuccess(trade.cancel_all_orders(symbol='pi_xbtusd'))
        assert isSuccess(trade.cancel_all_orders())
        assert isSuccess(trade.cancel_order(order_id='1234'))

    logging.info(f'{k}: ALL (tested) ENDPOINTS AVAILABLE!')

def test_funding_endpoints() -> None:
    k = 'FUNDING'
    logging.info(f'{k}: Creating clients')
    funding = Funding(key=key, secret=secret)
    
    assert type(funding.get_historical_funding_rates(symbol='PF_SOLUSD')) == dict
    if False:
        # accounts must exist.. 
        # print(funding.initiate_wallet_transfer(
        #     amount=200, fromAccount='Futures Wallet', toAccount='Spot Wallet', unit='XBT'
        # ))
        
        # print(funding.initiate_subccount_transfer(
        #     amount=200,
        #     fromAccount='The wallet (cash or margin account) from which funds should be debited',
        #     fromUser='The user account (this or a sub account) from which funds should be debited',
        #     toAccount='The wallet (cash or margin account) to which funds should be credited',
        #     toUser='The user account (this or a sub account) to which funds should be credited',
        #     unit='XBT',
        # ))

        # print(funding.initiate_withdrawal_to_spot_wallet(
        #     amount=200,
        #     currency='XBT',
        #     sourceWallet='Futures Wallet'
        # ))
        pass

    logging.info(f'{k}: ALL (tested) ENDPOINTS AVAILABLE!')

def main() -> None:
    
    logging.info('''

        Starting tests... 
        to access all endpoints you need to have all API permissions enabled.
        
        Some tests are disabled, to protect open positions, orders, trades, withdrawals, balances etc.
    ''')
    test_user_endpoints()
    test_market_endpoints()
    test_trade_endpoints()
    test_funding_endpoints()

if __name__ == '__main__': main()