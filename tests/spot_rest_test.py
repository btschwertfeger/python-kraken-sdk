'''Module that tests the Kraken Spot REST endpoints'''
import random
import time
import logging
from tqdm import tqdm
from dotenv import dotenv_values

try:
    from kraken.spot.client import User, Market, Trade, Funding, Staking
    from kraken.exceptions.exceptions import KrakenExceptions
except ModuleNotFoundError:
    import sys
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.spot.client import User, Market, Trade, Funding, Staking
    from kraken.exceptions.exceptions import KrakenExceptions
    print('USING LOCAL MODULE')

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:{kind}',
    level=logging.INFO
)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

key = dotenv_values('.env')['API_KEY']
secret = dotenv_values('.env')['SECRET_KEY']

def is_not_error(value) -> bool:
    '''Returns True if 'error' in dict.'''
    return isinstance(value, dict) and 'error' not in value

def test_user_endpoints() -> None:
    '''
    #  _   _
    # | | | |___  ___ _ __
    # | | | / __|/ _ \ '__|
    # | |_| \__ \  __/ |
    #  \___/|___/\___|_|
    '''

    logging.info('USER: Creating user clients')

    auth_user = User(key=key, secret=secret)
    logging.info('USER: Checking balance endpoints')

    assert is_not_error(auth_user.get_account_balance())
    assert is_not_error(auth_user.get_balances(currency='USD'))
    assert is_not_error(auth_user.get_trade_balance())
    assert is_not_error(auth_user.get_trade_balance(asset='EUR'))
    time.sleep(3)

    logging.info('USER: Checking open orders and open trades endpoints')
    assert is_not_error(auth_user.get_open_orders(trades=True))
    assert is_not_error(auth_user.get_open_orders(trades=False))
    assert is_not_error(auth_user.get_closed_orders())
    assert is_not_error(auth_user.get_closed_orders(trades=True))
    assert is_not_error(auth_user.get_closed_orders(trades=True, start='1668431675.4778206'))
    assert is_not_error(auth_user.get_closed_orders(
        trades=True, start='1668431675.4778206', end='1668455555.4778206', ofs=2
    ))
    time.sleep(3)

    for closetime in ['open', 'close', 'both']:
        assert is_not_error(auth_user.get_closed_orders(
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
        try: assert is_not_error(method(**params))
        except KrakenExceptions.KrakenInvalidOrderError: pass
        finally: time.sleep(1.5)

    for type_ in ['all', 'any position', 'closed position', 'closing position', 'no position']:
        assert is_not_error(auth_user.get_trades_history(type_=type_, trades=True))
        assert is_not_error(auth_user.get_trades_history(type_=type_, trades=False))
        time.sleep(2)

    assert isinstance(auth_user.get_open_positions(), list)
    assert isinstance(auth_user.get_open_positions(txid='OQQYNL-FXCFA-FBFVD7'), list)
    assert isinstance(auth_user.get_open_positions(txid='OQQYNL-FXCFA-FBFVD7', docalcs=True), list)
    time.sleep(4)

    logging.info('USER: Checking ledeger endpoints')
    assert is_not_error(auth_user.get_ledgers_info())
    for type_ in tqdm([
        'all', 'deposit', 'withdrawal',
        'trade', 'margin', 'rollover',
        'credit', 'transfer', 'settled',
        'staking', 'sale'
    ]):
        assert is_not_error(auth_user.get_ledgers_info(type_=type_))
        time.sleep(2)

    for params in [
        { 'asset': 'GBP' },
        { 'asset': 'GBP,EUR'} ,
        { 'asset': ['GBP','EUR'], 'start':'1668431675.4778206', 'end': '1668455555.4778206', 'ofs': 2 }
    ]:
        assert is_not_error(auth_user.get_ledgers_info(**params))
        time.sleep(1)

    assert is_not_error(auth_user.get_ledgers(id_='LNYQGU-SUR5U-UXTOWM'))
    assert is_not_error(auth_user.get_ledgers(id_=['LNYQGU-SUR5U-UXTOWM', 'LTCMN2-5DZHX-6CPRC4'], trades=True))

    assert is_not_error(auth_user.get_trade_volume())
    assert is_not_error(auth_user.get_trade_volume(pair='DOT/EUR', fee_info=False))
    time.sleep(5)

    logging.info('USER: Checking export report endpoints')
    #report_formats = ['CSV', 'TSV']
    for report in ['trades', 'ledgers']:
        if report == 'trades':
            fields = [
                'ordertxid', 'time', 'ordertype',
                'price', 'cost', 'fee', 'vol', 'margin',
                'misc', 'ledgers'
            ]
        elif report == 'ledgers':
            fields = [
                'refid', 'time', 'type', 'aclass',
                'asset', 'amount', 'fee', 'balance'
            ]
        #else: fields == 'all' # never; but 'all' can also be used to get all fields

        export_descr = f'{report}-export-{random.randint(0, 10000)}'
        logging.info(f'Requesting export {export_descr}')
        response = auth_user.request_export_report(
            report=report,
            description=export_descr,
            fields=fields,
            format_='CSV',
            starttm='1662100592'
        )
        assert is_not_error(response) and 'id' in response
        time.sleep(2)

        status = auth_user.get_export_report_status(report=report)
        assert isinstance(status, list)
        time.sleep(5)

        result = auth_user.retrieve_export(id_=response['id'])
        with open(f'{export_descr}.zip', 'wb') as file:
            for chunk in result.iter_content(chunk_size=512):
                if chunk: file.write(chunk)

        logging.info(f'Export {export_descr} done!')

        status = auth_user.get_export_report_status(report=report)
        assert isinstance(status, list)
        for response in status:
            assert 'id' in response
            try:
                assert isinstance(auth_user.delete_export_report(id_=response['id'], type_='delete'), dict)
            except Exception: # '200 - {"error":["WDatabase:No change"],"result":{"delete":true}}'
                pass
            time.sleep(2)

    logging.info('USER: ALL ENDPOINTS AVAILABLE!')

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

    assert is_not_error(market.get_system_status())

    logging.info('MARKET: Checking assets')
    for params in [
        { },
        { 'assets': 'USD' },
        { 'assets': ['USD'] },
        { 'assets': ['XBT','USD'] },
        { 'assets': ['XBT','USD'], 'aclass': 'currency' },
    ]:
        assert is_not_error(market.get_assets(**params))
        time.sleep(1.5)

    assert is_not_error(market.get_tradable_asset_pair(pair='XBTUSD'))
    assert is_not_error(market.get_tradable_asset_pair(pair=['DOT/EUR', 'XBTUSD']))
    for i in ['info', 'leverage', 'fees', 'margin']:
        assert is_not_error(market.get_tradable_asset_pair(pair='DOT/EUR', info=i))
        time.sleep(3)

    logging.info('MARKET{kind}: Checking ticker')
    assert is_not_error(market.get_ticker())
    assert is_not_error(market.get_ticker(pair='XBTUSD'))
    assert is_not_error(market.get_ticker(pair=['DOTUSD', 'XBTUSD']))
    time.sleep(2)

    logging.info('MARKET: Checking ohlc, orderbook, trades and spreads')
    assert is_not_error(market.get_ohlc(pair='XBTUSD'))
    assert is_not_error(market.get_ohlc(pair='XBTUSD', interval=240)) # interval in [1 5 15 30 60 240 1440 10080 21600]

    assert is_not_error(market.get_order_book(pair='XBTUSD'))
    assert is_not_error(market.get_order_book(pair='XBTUSD', count=2)) # count in [1...500]
    time.sleep(2)

    assert is_not_error(market.get_recent_trades(pair='XBTUSD'))
    assert is_not_error(market.get_recent_trades(pair='XBTUSD', since='1616663618'))

    assert is_not_error(market.get_recend_spreads(pair='XBTUSD'))
    assert is_not_error(market.get_recend_spreads(pair='XBTUSD', since='1616663618'))
    time.sleep(2)

    logging.info('MARKET: ALL ENDPOINTS AVAILABLE!')

def test_trade_endpoints() -> None:
    '''
    #  _____              _
    # |_   _| __ __ _  __| | ___
    #   | || '__/ _` |/ _` |/ _ \
    #   | || | | (_| | (_| |  __/
    #   |_||_|  \__,_|\__,_|\___|
    '''

    # return
    logging.info('TRADE: Creating clients')
    trade = Trade(key=key, secret=secret)

    raise ValueError('DONT TEST THIS, YOUR BOTS WILL DIE; WAIT FOR RELEASING DEMO SPOT ENVIRONMENT')

    if False: 
        # print(trade.create_order(
        #     ordertype='limit',
        #     side='buy',
        #     volume=1,
        #     pair='BTC/EUR',
        #     price=0.01,
        #     validate=True # important to just test this endpoint without risking money
        # ))
        # print(trade.create_order_batch(
        #     orders=[{
        #     'close': {
        #             'ordertype': 'stop-loss-limit',
        #             'price': 120,
        #             'price2': 110
        #         },
        #             'ordertype': 'limit',
        #             'price': 140,
        #             'price2': 130,
        #             'timeinforce': 'GTC',
        #             'type': 'buy',
        #             'userref': '345dsdfddfgdsgdfgsfdsfsdf',
        #             'volume': 1000
        #         },{
        #             'ordertype': 'limit',
        #             'price': 150,
        #             'timeinforce': 'GTC',
        #             'type': 'sell',
        #             'userref': '1dfgesggwe5t3',
        #             'volume': 123
        #         }
        #     ],
        #     pair='BTC/USD',
        #     validate=True
        # ))

        # print(trade.edit_order(
        #     txid='sometxid',
        #     pair='BTC/EUR',
        #     volume=4.2,
        #     price=17000,
        #     validate=True
        # ))
        # time.sleep(2)

        # print(trade.cancel_order(txid='O2JLFP-VYFIW-35ZAAE'))
        # print(trade.cancel_all_orders())
        # print(trade.cancel_all_orders_after_x(timeout=6))

        # # __ not working, idk why
        # print(trade.cancel_order_batch(orders=['O2JLFP-VYFIW-35ZAAE', 'O523KJ-DO4M2-KAT243', 'OCDIAL-YC66C-DOF7HS', 'OVFPZ2-DA2GV-VBFVVI']))
        pass

    logging.info('TRADE: ALL ENDPOINTS AVAILABLE!')

def test_staking_endpoints() -> None:
    '''
    #  ____  _        _    _
    # / ___|| |_ __ _| | _(_)_ __   __ _
    # \___ \| __/ _` | |/ / | '_ \ / _` |
    #  ___) | || (_| |   <| | | | | (_| |
    # |____/ \__\__,_|_|\_\_|_| |_|\__, |
    #                               |___/
    '''
    
    logging.info('STAKING: Creating clients')
    staking = Staking(key=key, secret=secret)

    logging.info('STAKING: Checking endpoints')
    assert isinstance(staking.list_stakeable_assets(), list)

    try:
        assert is_not_error(staking.stake_asset(asset='DOT', amount='4500000', method='polkadot-staked'))
    except KrakenExceptions.KrakenInvalidAmountError:
        pass

    assert isinstance(staking.get_pending_staking_transactions(), list)
    assert isinstance(staking.list_staking_transactions(), list)
    time.sleep(2)
    logging.info('STAKING: ALL ENDPOINTS AVAILABLE!')

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

    logging.info('FUNDING: Checking ...')

    # assert isinstance(funding.get_deposit_methods(asset='XBT'), list)
    # assert isNotError(funding.get_deposit_address(asset='XBT', method='Bitcoin'))

    assert isinstance(funding.get_recend_deposits_status(asset='XLM'), list)
    assert isinstance(funding.get_recend_deposits_status(asset='XLM', method='Stellar XLM'), list)
    time.sleep(2)

    try:
        assert is_not_error(funding.withdraw_funds(asset='XLM', key='enter-withdraw-key', amount=100000))
    except KrakenExceptions.KrakenUnknownWithdrawKeyError:
        pass

    try:
        assert is_not_error(
            funding.get_withdrawal_info(
                asset='XLM',
                amount=100000,
                key='enter-withdraw-key')
            ) # idk what key is
    except KrakenExceptions.KrakenUnknownWithdrawKeyError:
        pass

    assert isinstance(funding.get_recend_withdraw_status(asset='XLM'), list)
    try:
        assert is_not_error(
            funding.cancel_withdraw(
                asset='XLM',
                refid='AUBZC2T-6WMDG2-HYWFC7')
            ) # only works with real refid
    except KrakenExceptions.KrakenInvalidReferenceIdError:
        pass

    try:
        # only works if futures wallet exists
        assert is_not_error(
            funding.wallet_transfer(
                asset='XLM',
                from_='Spot Wallet',
                to_='Futures Wallet',
                amount=10000)
            )
    except KrakenExceptions.KrakenUnknownWithdrawKeyError:
        pass

    logging.info('FUNDING: ALL ENDPOINTS AVAILABLE!')

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
    test_staking_endpoints()
    test_funding_endpoints()


if __name__ == '__main__': main()
