import os, sys
from dotenv import dotenv_values
import random
import time
import logging, logging.config
from tqdm import tqdm

sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
from kraken.spot.client import User, Market, Trade, Funding, Staking

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filemode='w',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

key = dotenv_values('.env')['API_KEY']
secret = dotenv_values('.env')['SECRET_KEY']

def test_user_endpoints() -> None:
    k = 'USER'
    logging.info(f'{k}: Creating user clients')

    user = User()
    auth_user = User(key=key, secret=secret)
    
    logging.info(f'{k}: Checking balance endpoints')
    assert type(auth_user.get_account_balance()) == dict
    assert type(auth_user.get_balances(currency='USD')) == dict
    assert type(auth_user.get_trade_balance()) == dict
    assert type(auth_user.get_trade_balance(asset='EUR')) == dict
    time.sleep(5)

    logging.info(f'{k}: Checking open orders and open trades endpoints')
    assert type(auth_user.get_open_orders(trades=True)) == dict
    assert type(auth_user.get_open_orders(trades=False)) == dict
    assert type(auth_user.get_closed_orders()) == dict
    assert type(auth_user.get_closed_orders(trades=True)) == dict
    assert type(auth_user.get_closed_orders(trades=True, start='1668431675.4778206')) == dict
    assert type(auth_user.get_closed_orders(trades=True, start='1668431675.4778206', end='1668455555.4778206', ofs=2)) == dict
    time.sleep(10)

    for closetime in ['open', 'close', 'both']:
        assert type (auth_user.get_closed_orders(
            trades=True, 
            start='1668431675.4778206', 
            end='1668455555.4778206', 
            ofs=1,
            closetime=closetime
        )) == dict
        time.sleep(2)

    # txids must exist
    assert type(auth_user.get_orders_info(txid='OXBBSK-EUGDR-TDNIEQ')) == dict
    assert type(auth_user.get_orders_info(txid='OXBBSK-EUGDR-TDNIEQ', trades=True)) == dict
    
    for t in ['all', 'any position', 'closed position', 'closing position', 'no position']:
        assert type(auth_user.get_trades_history(type_=t, trades=True)) == dict
        assert type(auth_user.get_trades_history(type_=t, trades=False)) == dict
        time.sleep(2)

    # only works if margin txids are valid
    # assert type(auth_user.get_trades_info(txid='OQQYNL-FXCFA-FBFVD7')) == dict
    # assert type(auth_user.get_trades_info(txid=['OE3B4A-NSIEQ-5L6HW3','O23GOI-WZDVD-XWGC3R'])) == dict

    assert type(auth_user.get_open_positions()) == list
    assert type(auth_user.get_open_positions(txid='OQQYNL-FXCFA-FBFVD7')) == list
    assert type(auth_user.get_open_positions(txid='OQQYNL-FXCFA-FBFVD7', docalcs=True)) == list
    time.sleep(5)

    logging.info(f'{k}: Checking ledeger endpoints')
    assert type(auth_user.get_ledgers_info()) == dict
    for t in tqdm([
        'all', 'deposit', 'withdrawal', 
        'trade', 'margin', 'rollover', 
        'credit', 'transfer', 'settled', 
        'staking', 'sale'
    ]): 
        assert type(auth_user.get_ledgers_info(type_=t)) == dict
        time.sleep(3)

    assert type(auth_user.get_ledgers_info(asset='GBP')) == dict
    assert type(auth_user.get_ledgers_info(asset='GBP,EUR')) == dict
    assert type(auth_user.get_ledgers_info(asset=['GBP','EUR'], start='1668431675.4778206', end='1668455555.4778206', ofs=2)) == dict
    
    assert type(auth_user.get_ledgers(id='LNYQGU-SUR5U-UXTOWM')) == dict
    assert type(auth_user.get_ledgers(id=['LNYQGU-SUR5U-UXTOWM', 'LTCMN2-5DZHX-6CPRC4'], trades=True)) == dict
    
    assert type(auth_user.get_trade_volume()) == dict
    assert type(auth_user.get_trade_volume(pair='DOT/EUR', fee_info=False)) == dict
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
        assert type(response) == dict and 'id' in response 
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
    k = 'MARKET'
    logging.info(f'{k}: Creating clients')
    market = Market()
    # auth_market = Market(key=key, secret=secret)

    assert type(market.get_system_status()) == dict

    logging.info(f'{k}: Checking assets')
    assert type(market.get_assets()) == dict
    assert type(market.get_assets(assets='USD')) == dict
    assert type(market.get_assets(assets=['USD'])) == dict
    assert type(market.get_assets(assets=['XBT','USD'])) == dict
    assert type(market.get_assets(assets=['XBT','USD'], aclass='currency')) == dict
    time.sleep(3)

    assert type(market.get_tradable_asset_pair(pair='XBTUSD')) == dict
    assert type(market.get_tradable_asset_pair(pair=['DOT/EUR', 'XBTUSD'])) == dict
    for i in ['info', 'leverage', 'fees', 'margin']:
        assert type(market.get_tradable_asset_pair(pair='DOT/EUR', info=i)) == dict
        time.sleep(2)
    
    logging.info(f'{k}: Checking ticker')
    assert type(market.get_ticker()) == dict
    assert type(market.get_ticker(pair='XBTUSD')) == dict
    assert type(market.get_ticker(pair=['DOTUSD', 'XBTUSD'])) == dict
    time.sleep(2)

    logging.info(f'{k}: Checking ohlc, orderbook, trades and spreads')
    assert type(market.get_ohlc(pair='XBTUSD')) == dict
    assert type(market.get_ohlc(pair='XBTUSD', interval=240)) == dict # interval in [1 5 15 30 60 240 1440 10080 21600]
    
    assert type(market.get_order_book(pair='XBTUSD')) == dict
    assert type(market.get_order_book(pair='XBTUSD', count=2)) == dict # count in [1...500]
    time.sleep(2)

    assert type(market.get_recent_trades(pair='XBTUSD')) == dict
    assert type(market.get_recent_trades(pair='XBTUSD', since='1616663618')) == dict

    assert type(market.get_recent_trades(pair='XBTUSD')) == dict
    assert type(market.get_recent_trades(pair='XBTUSD', since='1616663618')) == dict
    
    assert type(market.get_recend_spreads(pair='XBTUSD')) == dict
    assert type(market.get_recend_spreads(pair='XBTUSD', since='1616663618')) == dict
    time.sleep(2)
    
    logging.info(f'{k}: ALL ENDPOINTS AVAILABLE!')

def test_trade_endpoints() -> None:
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
    k = 'STAKING'
    logging.info(f'{k}: Creating clients')
    staking = Staking(key=key, secret=secret)

    logging.info(f'{k}: Checking endpoints')
    assert type(staking.list_stakeable_assets()) == list    
    # assert type(staking.stake_asset(asset='DOT', amount='4500000', method='polkadot-staked')) == dict
    # assert type(staking.stake_asset(asset='DOT', amount='4500000', method='polkadot-staked')) == dict
    assert type(staking.get_pending_staking_transactions()) == list
    assert type(staking.list_staking_transactions()) == list
    logging.info(f'{k}: ALL ENDPOINTS AVAILABLE!')

def test_funding_endpoints() -> None:
    k = 'FUNDING'
    logging.info(f'{k}: Creating clients')

    funding = Funding(key=key, secret=secret)

    logging.info(f'{k}: Checking ...')
    assert type(funding.get_deposit_methods(asset='XLM')) == list
    assert type(funding.get_deposit_address(asset='XLM', method='Stellar XLM')) == list

    assert type(funding.get_recend_deposits_status(asset='XLM')) == list
    assert type(funding.get_recend_deposits_status(asset='XLM', method='Stellar XLM')) == list
    time.sleep(2)
    
    if False:
        # print(funding.withdraw_funds(asset='XLM', key='enter-withdraw-key', amount=100000))
        # print(funding.get_withdrawal_info(asset='XLM', amount=100000, key='enter-withdraw-key')) # idk what key is
        pass

    assert type(funding.get_recend_withdraw_status(asset='XLM')) == list
    # print(funding.cancel_withdraw(asset='XLM', refid='AUBZC2T-6WMDG2-HYWFC7')) # only works with real refid

    # only works if futures wallet exists
    # print(funding.wallet_transfer(asset='XLM', from_='Spot Wallet', to_='Futures Wallet', amount=10000))
 
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