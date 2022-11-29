'''Module to test the Kraken Futures Rest endpoints'''

import random
import time
import logging
from dotenv import dotenv_values

try:
    from kraken.futures.client import User, Market, Trade, Funding
    from kraken.exceptions.exceptions import KrakenExceptions
except ModuleNotFoundError:
    import sys
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.futures.client import User, Market, Trade, Funding
    from kraken.exceptions.exceptions import KrakenExceptions
    print('USING LOCAL MODULE')

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

key = dotenv_values('.env')['Futures_API_KEY']
secret = dotenv_values('.env')['Futures_SECRET_KEY']

def is_success(value) -> bool:
    '''Returns true if result is success'''
    return isinstance(value, dict) and 'result' in value and value['result'] == 'success'

def is_not_error(value) -> bool:
    '''Returns true if result is not error'''
    return isinstance(value, dict) and 'error' not in value.keys()

def test_user_endpoints() -> None:
    '''
    #  _   _
    # | | | |___  ___ _ __
    # | | | / __|/ _ \ '__|
    # | |_| \__ \  __/ |
    #  \___/|___/\___|_|
    '''
    
    logging.info('USER: Creating user clients')
    user = User()
    auth_user = User(key=key, secret=secret)
    logging.info('USER: Checking endpoints')

    assert is_success(auth_user.get_wallets())
    assert is_success(auth_user.get_open_orders())
    assert is_success(auth_user.get_open_positions())
    assert is_success(auth_user.get_subaccounts())
    assert is_success(auth_user.get_unwindqueue())
    assert is_success(auth_user.get_notificatios())
    time.sleep(3)

    assert isinstance(auth_user.get_account_log(), dict)
    assert isinstance(auth_user.get_account_log(info='futures liquidation'), dict)

    response = auth_user.get_account_log_csv()
    assert response.status_code in [200, '200']
    with open(f'account_log-{random.randint(0, 10000)}.csv', 'wb') as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk: file.write(chunk)
    time.sleep(3)

    logging.info('USER: ALL (tested) ENDPOINTS AVAILABLE!')

def test_market_endpoints() -> None:
    '''
    #  __  __            _        _
    # |  \/  | __ _ _ __| | _____| |_
    # | |\/| |/ _` | '__| |/ / _ \ __|
    # | |  | | (_| | |  |   <  __/ |_
    # |_|  |_|\__,_|_|  |_|\_\___|\__|
    '''
    
    logging.info('MARKET: Creating clients')
    market = Market()
    auth_market = Market(key=key, secret=secret)

    assert isinstance(market.get_ohlc(
        tick_type='trade',
        symbol='PI_XBTUSD',
        resolution='1m',
        from_='1668989233',
        to='1668999233'
    ), dict)
    assert isinstance(market.get_tick_types(), list)

    assert isinstance(market.get_tradeable_products(tick_type='mark'), list)
    assert isinstance(market.get_resolutions(tick_type='trade', tradeable='PI_XBTUSD'), list)

    assert is_success(market.get_fee_schedules())
    time.sleep(2)

    # assert type(market.get_orderbook()) == dict # raises 500-INTERNAL_SERVER_ERROR on Kraken, but symbol is optinal as described in the api documentation
    assert is_success(market.get_orderbook(symbol='PI_XBTUSD'))

    assert is_success(market.get_tickers())
    assert is_success(market.get_instruments())
    assert is_success(market.get_instruments_status())
    assert is_success(market.get_instruments_status(instrument='PI_XBTUSD'))
    time.sleep(2)

    assert is_success(market.get_trade_history(symbol='PI_XBTUSD'))
    assert is_success(market.get_historical_funding_rates(symbol='PI_XBTUSD'))

    assert is_success(auth_market.set_leverage_preference(symbol='PF_SOLUSD', maxLeverage=2))
    assert is_success(auth_market.get_leverage_preference())
    assert is_success(auth_market.set_leverage_preference(symbol='PF_SOLUSD')) # reset setted preference
    time.sleep(3)

    assert is_success(auth_market.set_pnl_preference(symbol='PF_SOLUSD', pnlPreference='USD'))
    assert is_success(auth_market.get_pnl_preference())

    assert is_not_error(market.get_public_execution_events(tradeable='PF_SOLUSD', since=1668989233))
    assert is_not_error(market.get_public_order_events(tradeable='PF_SOLUSD', since=1668989233))
    assert is_not_error(market.get_public_mark_price_events(tradeable='PF_SOLUSD', since=1668989233))
    time.sleep(3)

    # needs a higher auth level...
    # assert type(auth_market.get_execution_events(tradeable='PF_SOLUSD', sort='asc', since=1668989233)) == dict
    # assert type(auth_market.get_order_events(tradeable='PF_SOLUSD', since=1668989233)) == dict
    # assert type(auth_market.get_trigger_events(tradeable='PF_SOLUSD', since=1668989233)) == dict

    logging.info('MARKET: ALL (tested) ENDPOINTS AVAILABLE!')

def test_trade_endpoints() -> None:
    '''
    #  _____              _
    # |_   _| __ __ _  __| | ___
    #   | || '__/ _` |/ _` |/ _ \
    #   | || | | (_| | (_| |  __/
    #   |_||_|  \__,_|\__,_|\___|
    '''

    logging.info('TRADE: Creating clients')
    trade = Trade(key=key, secret=secret)

    assert is_success(trade.get_fills())
    assert is_success(trade.get_fills(lastFillTime='2020-07-21T12:41:52.790Z'))
    assert is_success(trade.dead_mans_switch(timeout=60))
    assert is_success(trade.dead_mans_switch(timeout=0)) # reset dead mans switch
    assert is_success(trade.get_orders_status(orderIds='378etweirzgu'))

    if False:
        raise ValueError('Execute this lines only if you know what it does!')
        # time.sleep(2)

        # assert isSuccess(trade.create_order(
        #     orderType='lmt',
        #     size=10,
        #     symbol='PI_XBTUSD',
        #     side='buy',
        #     limitPrice=1,
        #     stopPrice=10
        # ))
        # assert isSuccess(trade.create_batch_order(
        #     batchorder_list = [{
        #         'order': 'send',
        #         'order_tag': '1',
        #         'orderType': 'lmt',
        #         'symbol': 'PI_XBTUSD',
        #         'side': 'buy',
        #         'size': 5,
        #         'limitPrice': 1.00,
        #         'cliOrdId': 'my_another_client_id'
        #     }, {
        #         'order': 'send',
        #         'order_tag': '2',
        #         'orderType': 'stp',
        #         'symbol': 'PI_XBTUSD',
        #         'side': 'buy',
        #         'size': 1,
        #         'limitPrice': 2.00,
        #         'stopPrice': 3.00,
        #     }, {
        #         'order': 'cancel',
        #         'order_id': 'e35d61dd-8a30-4d5f-a574-b5593ef0c050',
        #     }, {
        #         'order': 'cancel',
        #         'cliOrdId': 'my_client_id',
        #     }],
        # ))
        # time.sleep(2)
        # assert isSuccess(trade.edit_order(orderId='my_another_client_id', limitPrice=3))
        # time.sleep(.1)
        # assert isSuccess(trade.cancel_order(cliOrdId='my_another_client_id'))
        # assert isSuccess(trade.cancel_all_orders(symbol='pi_xbtusd'))
        # assert isSuccess(trade.cancel_all_orders())
        # assert isSuccess(trade.cancel_order(order_id='1234'))

    logging.info('TRADE: ALL (tested) ENDPOINTS AVAILABLE!')

def test_funding_endpoints() -> None:
    '''
    #  _____                _ _
    # |  ___|   _ _ __   __| (_)_ __   __ _
    # | |_ | | | | '_ \ / _` | | '_ \ / _` |
    # |  _|| |_| | | | | (_| | | | | | (_| |
    # |_|   \__,_|_| |_|\__,_|_|_| |_|\__, |
    #                                 |___/
    '''
    
    logging.info('FUNDING: Creating clients')
    funding = Funding(key=key, secret=secret)

    assert is_success(funding.get_historical_funding_rates(symbol='PF_SOLUSD'))

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
        # ))
        pass

    logging.info('FUNDING: ALL (tested) ENDPOINTS AVAILABLE!')

def main() -> None:
    '''Main'''
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
