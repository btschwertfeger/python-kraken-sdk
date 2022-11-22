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

def main() -> None:
    key = dotenv_values('.env')['API_KEY']
    secret = dotenv_values('.env')['SECRET_KEY']

    # _____________________________________________________________
    #  _   _               
    # | | | |___  ___ _ __ 
    # | | | / __|/ _ \ '__|
    # | |_| \__ \  __/ |   
    #  \___/|___/\___|_|   
    
    logging.info('USER: Creating user clients')
    user = User()
    auth_user = User(key=key, secret=secret)
    logging.info('USER: Checking balance endpoints')
    assert type(auth_user.get_account_balance()) == dict
    assert type(auth_user.get_balances(currency='USD')) == dict
    assert type(auth_user.get_trade_balance()) == dict
    assert type(auth_user.get_trade_balance(asset='EUR')) == dict

    time.sleep(5)
    logging.info('USER: Checking open orders and trades endpoints')
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
    logging.info('USER: Checking ledeger endpoints')
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
    logging.info('USER: Checking export report endpoints')
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

    logging.info('USER: ALL ENDPOINTS AVAILABLE!')

    # assert type() == dict
    # assert type() == dict


if __name__ == '__main__': main()