import os, sys
from dotenv import dotenv_values
import random
import time
import logging, logging.config
from tqdm import tqdm

try:
    from kraken.spot.client import User, Market, Trade, Funding, Staking
    from kraken.exceptions.exceptions import KrakenExceptions 
except ModuleNotFoundError:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.spot.client import User, Market, Trade, Funding, Staking
    from kraken.exceptions.exceptions import KrakenExceptions 

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

key = dotenv_values('.env')['API_KEY']
secret = dotenv_values('.env')['SECRET_KEY']

isNotError = lambda x: True if type(x) == dict and 'error' not in x else False

def test_user_endpoints() -> None:
    #  _   _               
    # | | | |___  ___ _ __ 
    # | | | / __|/ _ \ '__|
    # | |_| \__ \  __/ |   
    #  \___/|___/\___|_|   

    k = 'USER'
    logging.info(f'{k}: Creating user clients')

    user = User()
    auth_user = User(key=key, secret=secret)
    logging.info(f'{k}: Checking balance endpoints')
    
    assert isNotError(auth_user.get_account_balance()) 
    assert isNotError(auth_user.get_balances(currency='USD'))
    assert isNotError(auth_user.get_trade_balance())
    assert isNotError(auth_user.get_trade_balance(asset='EUR'))
    time.sleep(3)

    logging.info(f'{k}: Checking open orders and open trades endpoints')
    assert isNotError(auth_user.get_open_orders(trades=True))
    assert isNotError(auth_user.get_open_orders(trades=False))
    assert isNotError(auth_user.get_closed_orders())
    assert isNotError(auth_user.get_closed_orders(trades=True))
    assert isNotError(auth_user.get_closed_orders(trades=True, start='1668431675.4778206'))
    assert isNotError(auth_user.get_closed_orders(trades=True, start='1668431675.4778206', end='1668455555.4778206', ofs=2))
    time.sleep(3)

    for closetime in ['open', 'close', 'both']:
        assert isNotError(auth_user.get_closed_orders(
            trades=True, 
            start='1668431675.4778206', 
            end='1668455555.4778206', 
            ofs=1,
            closetime=closetime
        ))
        time.sleep(.6)

    for params, method in zip([
        {'txid': 'OXBBSK-EUGDR-TDNIEQ'},
        {'txid': 'OXBBSK-EUGDR-TDNIEQ', 'trades': True},
        {'txid': 'OQQYNL-FXCFA-FBFVD7'},
        {'txid': ['OE3B4A-NSIEQ-5L6HW3','O23GOI-WZDVD-XWGC3R']}
    ], [
        auth_user.get_orders_info, auth_user.get_orders_info,
        auth_user.get_trades_info, auth_user.get_trades_info
    ]): 
        try: assert isNotError(method(**params))   
        except KrakenExceptions.KrakenInvalidOrderError: pass
        finally: time.sleep(1.5)

    for t in ['all', 'any position', 'closed position', 'closing position', 'no position']:
        assert isNotError(auth_user.get_trades_history(type_=t, trades=True))
        assert isNotError(auth_user.get_trades_history(type_=t, trades=False))
        time.sleep(2)

    assert type(auth_user.get_open_positions()) == list
    assert type(auth_user.get_open_positions(txid='OQQYNL-FXCFA-FBFVD7')) == list
    assert type(auth_user.get_open_positions(txid='OQQYNL-FXCFA-FBFVD7', docalcs=True)) == list
    time.sleep(4)

    logging.info(f'{k}: Checking ledeger endpoints')
    assert isNotError(auth_user.get_ledgers_info())
    for t in tqdm([
        'all', 'deposit', 'withdrawal', 
        'trade', 'margin', 'rollover', 
        'credit', 'transfer', 'settled', 
        'staking', 'sale'
    ]): 
        assert isNotError(auth_user.get_ledgers_info(type_=t))
        time.sleep(2)

    for params in [
        { 'asset': 'GBP' }, 
        { 'asset': 'GBP,EUR'} , 
        { 'asset': ['GBP','EUR'], 'start':'1668431675.4778206', 'end': '1668455555.4778206', 'ofs': 2 }
    ]:
        assert isNotError(auth_user.get_ledgers_info(**params))
        time.sleep(1)
        
    assert isNotError(auth_user.get_ledgers(id='LNYQGU-SUR5U-UXTOWM'))
    assert isNotError(auth_user.get_ledgers(id=['LNYQGU-SUR5U-UXTOWM', 'LTCMN2-5DZHX-6CPRC4'], trades=True))
    
    assert isNotError(auth_user.get_trade_volume())
    assert isNotError(auth_user.get_trade_volume(pair='DOT/EUR', fee_info=False))
    time.sleep(5)

    logging.info(f'{k}: Checking export report endpoints')
    report_formats = ['CSV', 'TSV']
    for report in ['trades', 'ledgers']:
        if report == 'trades': fields = ['ordertxid', 'time', 'ordertype', 'price', 'cost', 'fee', 'vol', 'margin', 'misc', 'ledgers']
        elif report == 'ledgers': fields = ['refid', 'time', 'type', 'aclass', 'asset', 'amount', 'fee', 'balance']
        else: fields == 'all' # never; but 'all' can also be used to get all fields

        export_descr = f'{report}-export-{random.randint(0, 10000)}'
        logging.info(f'Requesting export {export_descr}')
        response = auth_user.request_export_report(
            report=report, 
            description=export_descr,
            fields=fields,
            format_='CSV',
            starttm='1662100592'
        )
        assert isNotError(response) and 'id' in response 
        time.sleep(2)

        status = auth_user.get_export_report_status(report=report)
        assert type(status) == list
        time.sleep(5)

        result = auth_user.retrieve_export(id_=response['id'])
        handle = open(f'{export_descr}.zip', 'wb')
        for chunk in result.iter_content(chunk_size=512):
            if chunk: handle.write(chunk)
        handle.close()        
        logging.info(f'Export {export_descr} done!')

        status = auth_user.get_export_report_status(report=report)
        assert type(status) == list
        for r in status:
            assert 'id' in r
            try:
                assert type(auth_user.delete_export_report(id_=r['id'], type_='delete')) == dict    
            except Exception: # '200 - {"error":["WDatabase:No change"],"result":{"delete":true}}'
                pass
            time.sleep(2)

    logging.info(f'{k}: ALL ENDPOINTS AVAILABLE!')

def test_market_endpoints() -> None:

    #  __  __            _        _   
    # |  \/  | __ _ _ __| | _____| |_ 
    # | |\/| |/ _` | '__| |/ / _ \ __|
    # | |  | | (_| | |  |   <  __/ |_ 
    # |_|  |_|\__,_|_|  |_|\_\___|\__|
                                    
                                    
    k = 'MARKET'
    logging.info(f'{k}: Creating clients')
    market = Market()

    assert isNotError(market.get_system_status())

    logging.info(f'{k}: Checking assets')
    for params in [
        { },
        { 'assets': 'USD' },
        { 'assets': ['USD'] },
        { 'assets': ['XBT','USD'] },
        { 'assets': ['XBT','USD'], 'aclass': 'currency' },
    ]:
        assert isNotError(market.get_assets(**params))
        time.sleep(1.5)

    assert isNotError(market.get_tradable_asset_pair(pair='XBTUSD'))
    assert isNotError(market.get_tradable_asset_pair(pair=['DOT/EUR', 'XBTUSD']))
    for i in ['info', 'leverage', 'fees', 'margin']:
        assert isNotError(market.get_tradable_asset_pair(pair='DOT/EUR', info=i))
        time.sleep(2)
    
    logging.info(f'{k}: Checking ticker')
    assert isNotError(market.get_ticker())
    assert isNotError(market.get_ticker(pair='XBTUSD'))
    assert isNotError(market.get_ticker(pair=['DOTUSD', 'XBTUSD']))
    time.sleep(2)

    logging.info(f'{k}: Checking ohlc, orderbook, trades and spreads')
    assert isNotError(market.get_ohlc(pair='XBTUSD'))
    assert isNotError(market.get_ohlc(pair='XBTUSD', interval=240)) # interval in [1 5 15 30 60 240 1440 10080 21600]
    
    assert isNotError(market.get_order_book(pair='XBTUSD'))
    assert isNotError(market.get_order_book(pair='XBTUSD', count=2)) # count in [1...500]
    time.sleep(2)

    assert isNotError(market.get_recent_trades(pair='XBTUSD'))
    assert isNotError(market.get_recent_trades(pair='XBTUSD', since='1616663618'))
    
    assert isNotError(market.get_recend_spreads(pair='XBTUSD'))
    assert isNotError(market.get_recend_spreads(pair='XBTUSD', since='1616663618'))
    time.sleep(2)
    
    logging.info(f'{k}: ALL ENDPOINTS AVAILABLE!')

def test_trade_endpoints() -> None:

    #  _____              _      
    # |_   _| __ __ _  __| | ___ 
    #   | || '__/ _` |/ _` |/ _ \
    #   | || | | (_| | (_| |  __/
    #   |_||_|  \__,_|\__,_|\___|

    return
    k = 'TRADE'
    logging.info(f'{k}: Creating clients')
    trade = Trade(key=key, secret=secret)

    raise ValueError('DONT TEST THIS, YOUR BOTS WILL DIE; WAIT FOR RELEASING DEMO SPOT ENVIRONMENT')

    if False:
        # trade.create_order...
        # trade.create_order_batch...
        # trade.edit_order...
        # trade.cancel_order...
        # trade.cancel_all_orders...
        # trade.cancel_all_orders_after_x...
        # trade.cancel_order_batch...
        pass

    logging.info(f'{k}: ALL ENDPOINTS AVAILABLE!')

def test_staking_endpoints() -> None:

    #  ____  _        _    _             
    # / ___|| |_ __ _| | _(_)_ __   __ _ 
    # \___ \| __/ _` | |/ / | '_ \ / _` |
    #  ___) | || (_| |   <| | | | | (_| |
    # |____/ \__\__,_|_|\_\_|_| |_|\__, |
    #                               |___/ 

    k = 'STAKING'
    logging.info(f'{k}: Creating clients')
    staking = Staking(key=key, secret=secret)

    logging.info(f'{k}: Checking endpoints')
    assert type(staking.list_stakeable_assets()) == list

    try:
        assert isNotError(staking.stake_asset(asset='DOT', amount='4500000', method='polkadot-staked'))
    except KrakenExceptions.KrakenInvalidAmountError:
        pass

    assert type(staking.get_pending_staking_transactions()) == list
    assert type(staking.list_staking_transactions()) == list
    logging.info(f'{k}: ALL ENDPOINTS AVAILABLE!')

def test_funding_endpoints() -> None:

    #  _____                _ _             
    # |  ___|   _ _ __   __| (_)_ __   __ _ 
    # | |_ | | | | '_ \ / _` | | '_ \ / _` |
    # |  _|| |_| | | | | (_| | | | | | (_| |
    # |_|   \__,_|_| |_|\__,_|_|_| |_|\__, |
    #                                 |___/ 

    k = 'FUNDING'
    logging.info(f'{k}: Creating clients')

    funding = Funding(key=key, secret=secret)

    logging.info(f'{k}: Checking ...')
    
    assert type(funding.get_deposit_methods(asset='XBT')) == list
    assert isNotError(funding.get_deposit_address(asset='XBT', method='Bitcoin'))

    assert type(funding.get_recend_deposits_status(asset='XLM')) == list
    assert type(funding.get_recend_deposits_status(asset='XLM', method='Stellar XLM')) == list
    time.sleep(2)
    
    try:
        assert isNotError(funding.withdraw_funds(asset='XLM', key='enter-withdraw-key', amount=100000))
    except KrakenExceptions.KrakenUnknownWithdrawKeyError:
        pass

    try:
        assert isNotError(funding.get_withdrawal_info(asset='XLM', amount=100000, key='enter-withdraw-key')) # idk what key is
    except KrakenExceptions.KrakenUnknownWithdrawKeyError:
        pass     

    assert type(funding.get_recend_withdraw_status(asset='XLM')) == list
    try:
        assert isNotError(funding.cancel_withdraw(asset='XLM', refid='AUBZC2T-6WMDG2-HYWFC7')) # only works with real refid
    except KrakenExceptions.KrakenInvalidReferenceIdError:
        pass

    try:
        # only works if futures wallet exists
        assert isNotError(funding.wallet_transfer(asset='XLM', from_='Spot Wallet', to_='Futures Wallet', amount=10000))
    except KrakenExceptions.KrakenUnknownWithdrawKeyError: 
        pass

    logging.info(f'{k}: ALL ENDPOINTS AVAILABLE!')

def main() -> None:
    
    logging.info('''

        Starting tests... 
        to access all endpoints you need to have all API permissions enabled.
        
        Some tests are disabled, to protect open positions, orders, trades, withdrawals, balances etc.
    ''')

    test_user_endpoints()
    test_market_endpoints()
    test_trade_endpoints()
    test_staking_endpoints()
    test_funding_endpoints()


if __name__ == '__main__': main()