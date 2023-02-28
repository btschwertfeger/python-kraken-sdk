'''Module to test the Kraken Futures Rest endpoints'''

import os 
import random
import unittest

try:
    from kraken.futures.client import User, Market, Trade, Funding
    from kraken.exceptions.exceptions import KrakenExceptions
except ModuleNotFoundError:
    import sys
    sys.path.append('/Users/benjamin/repositories/Finance/Kraken/python-kraken-sdk')
    from kraken.futures.client import User, Market, Trade, Funding
    from kraken.exceptions.exceptions import KrakenExceptions
    print('USING LOCAL MODULE')

def is_success(value) -> bool:
    '''Returns true if result is success'''
    return isinstance(value, dict) and 'result' in value and value['result'] == 'success'

def is_not_error(value) -> bool:
    '''Returns true if result is not error'''
    return isinstance(value, dict) and 'error' not in value.keys()


class UserTests(unittest.TestCase):

    def setUp(self):
        self.__auth_user = User(
            key=os.getenv('FUTURES_API_KEY'),
            secret=os.getenv('FUTURES_SECRET_KEY')
        )

    def test_get_wallets(self):
        assert is_success(self.__auth_user.get_wallets())

    def test_get_open_orders(self):
        assert is_success(self.__auth_user.get_open_orders())

    def test_get_open_positions(self):    
        assert is_success(self.__auth_user.get_open_positions())

    def test_get_subaccounts(self):
        assert is_success(self.__auth_user.get_subaccounts())

    def test_get_unwindqueue(self):
        assert is_success(self.__auth_user.get_unwindqueue())

    def test_get_notificatios(self):
        assert is_success(self.__auth_user.get_notificatios())

    def test_get_account_log(self):
        assert isinstance(self.__auth_user.get_account_log(), dict)
        assert isinstance(self.__auth_user.get_account_log(info='futures liquidation'), dict)

    def test_get_account_log_csv(self):
        response = self.__auth_user.get_account_log_csv()
        assert response.status_code in [200, '200']
        with open(f'account_log-{random.randint(0, 10000)}.csv', 'wb') as file:
            for chunk in response.iter_content(chunk_size=512):
                if chunk: file.write(chunk)
        
class MarketTests(unittest.TestCase):

    def setUp(self):
        self.__market = Market()
        self.__auth_market = Market(
            key=os.getenv('FUTURES_API_KEY'),
            secret=os.getenv('FUTURES_SECRET_KEY')
        )

    def test_get_ohlc(self):
        assert isinstance(self.__market.get_ohlc(
            tick_type='trade',
            symbol='PI_XBTUSD',
            resolution='1m',
            from_='1668989233',
            to='1668999233'
        ), dict)

    def test_get_tick_types(self):
        assert isinstance(self.__market.get_tick_types(), list)

    def test_get_tradeable_products(self):
        assert isinstance(self.__market.get_tradeable_products(tick_type='mark'), list)

    def test_get_resolutions(self):
        assert isinstance(self.__market.get_resolutions(tick_type='trade', tradeable='PI_XBTUSD'), list)

    def test_get_fee_schedules(self):
        assert is_success(self.__market.get_fee_schedules())

    def test_get_orderbook(self):
        # assert type(market.get_orderbook()) == dict # raises 500-INTERNAL_SERVER_ERROR on Kraken, but symbol is optional as described in the API documentation (Dec, 2022)
        assert is_success(self.__market.get_orderbook(symbol='PI_XBTUSD'))

    def test_get_tickers(self):
        assert is_success(self.__market.get_tickers())

    def test_get_instruments(self):
        assert is_success(self.__market.get_instruments())

    def test_get_instruments_status(self):
        assert is_success(self.__market.get_instruments_status())

    def test_get_instruments_status(self):
        assert is_success(self.__market.get_instruments_status(instrument='PI_XBTUSD'))

    def test_get_trade_history(self):
        assert is_success(self.__market.get_trade_history(symbol='PI_XBTUSD'))

    def test_get_historical_funding_rates(self):
        assert is_success(self.__market.get_historical_funding_rates(symbol='PI_XBTUSD'))

    @unittest.skip('Skipping Futures set_leverage_preference endpoint, because this needs full access')
    def test_set_leverage_preference(self):
        
        old_leverage_preferences = self.__auth_market.get_leverage_preference()
        assert 'result' in old_leverage_preferences.keys() and old_leverage_preferences['result'] == 'success'
        assert is_success(self.__auth_market.set_leverage_preference(symbol='PF_XBTUSD',maxLeverage=2))

        new_leverage_preferences = self.__auth_market.get_leverage_preference()
        assert 'result' in new_leverage_preferences.keys() and new_leverage_preferences['result'] == 'success'
        assert 'leveragePreferences' in new_leverage_preferences.keys() and dict(symbol='PF_XBTUSD', maxLeverage=float(2.0)) in new_leverage_preferences['leveragePreferences']
        
        if 'leveragePreferences' in old_leverage_preferences.keys():
            for setting in old_leverage_preferences['leveragePreferences']:
                if 'symbol' in setting.keys() and setting['symbol'] == 'PF_XBTUSD':
                    assert is_success(self.__auth_market.set_leverage_preference(symbol='PF_XBTUSD')) 
                    break

    @unittest.skip('Skipping Futures set_pnl_preference endpoint, because this needs full access')
    def test_set_pnl_preference(self):
        
        old_pnl_preference = self.__auth_market.get_pnl_preference()
        assert 'result' in old_pnl_preference.keys() and old_pnl_preference['result'] == 'success'
        assert is_success(self.__auth_market.set_pnl_preference(symbol='PF_XBTUSD', pnlPreference='BTC'))
        
        new_pnl_preference = self.__auth_market.get_pnl_preference()
        assert 'result' in new_pnl_preference.keys() and new_pnl_preference['result'] == 'success'
        assert 'preferences' in new_pnl_preference.keys() and dict(symbol='PF_XBTUSD', pnlCurrency='BTC') in new_pnl_preference['preferences'] 
        
        if 'preferences' in old_pnl_preference.keys():
            for setting in old_pnl_preference['preferences']:
                if 'symbol' in setting.keys() and setting['symbol'] == 'PF_XBTUSD':
                    assert is_success(self.__auth_market.set_pnl_preference(symbol='PF_XBTUSD', pnlPreference=setting['pnlCurrency']))
                    break
     
    def test_get_public_execution_events(self):
        assert is_not_error(self.__market.get_public_execution_events(tradeable='PF_SOLUSD', since=1668989233))

    def get_public_order_events(self):
        assert is_not_error(self.__market.get_public_order_events(tradeable='PF_SOLUSD', since=1668989233))

    def get_public_mark_price_events(self):
        assert is_not_error(self.__market.get_public_mark_price_events(tradeable='PF_SOLUSD', since=1668989233))
        
class TradeTests(unittest.TestCase):

    def setUp(self):
        self.__auth_trade = Trade(
            key=os.getenv('FUTURES_API_KEY'),
            secret=os.getenv('FUTURES_SECRET_KEY')
        )

    @unittest.skip('Skipping Futures get_fills endpoint')
    def test_get_fills(self):
        assert is_success(self.__auth_trade.get_fills())
        assert is_success(self.__auth_trade.get_fills(lastFillTime='2020-07-21T12:41:52.790Z'))

    @unittest.skip('Skipping Futures dead_mans_switch endpoint')
    def test_dead_mans_switch(self):
        assert is_success(self.__auth_trade.dead_mans_switch(timeout=60))
        assert is_success(self.__auth_trade.dead_mans_switch(timeout=0)) # reset dead mans switch

    @unittest.skip('Skipping Futures get_order_status endpoint')
    def test_get_orders_status(self):
        assert is_success(self.__auth_trade.get_orders_status(orderIds='378etweirzgu'))
        
    @unittest.skip('Skipping Futures create_order endpoint')
    def test_create_order(self):
        assert is_success(self.__auth_trade.create_order(
            orderType='lmt',
            size=10,
            symbol='PI_XBTUSD',
            side='buy',
            limitPrice=1,
            stopPrice=10
        ))

    @unittest.skip('Skipping Futures create_batch_oder endpoint')
    def test_create_batch_order(self):
        assert is_success(self.__auth_trade.create_batch_order(
            batchorder_list = [{
                'order': 'send',
                'order_tag': '1',
                'orderType': 'lmt',
                'symbol': 'PI_XBTUSD',
                'side': 'buy',
                'size': 5,
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

    @unittest.skip('Skipping Futures edit_order endpoint')
    def test_edit_order(self):
        assert is_success(self.__auth_trade.edit_order(orderId='my_another_client_id', limitPrice=3))

    @unittest.skip('Skipping Futures cancel_order endpoint')
    def test_cancel_order(self):
        assert is_success(self.__auth_trade.cancel_order(cliOrdId='my_another_client_id'))
        assert is_success(self.__auth_trade.cancel_order(order_id='1234'))

    @unittest.skip('Skipping Futures cancel_all_orders endpoint')
    def test_cancel_all_orders(self):
        assert is_success(self.__auth_trade.cancel_all_orders(symbol='pi_xbtusd'))
        assert is_success(self.__auth_trade.cancel_all_orders())


class FundingTests(unittest.TestCase):

    def setUp(self):
        self.__auth_funding = Funding(
            key=os.getenv('FUTURES_API_KEY'),
            secret=os.getenv('FUTURES_SECRET_KEY')
        )

    @unittest.skip('Skipping Futures get_historical_funding_rates endpoint')
    def test_get_historical_funding_rates(self):
        assert is_success(self.__auth_funding.get_historical_funding_rates(symbol='PF_SOLUSD'))

    @unittest.skip('Skipping Futures initiate_wallet_transfer endpoint')
    def test_initiate_wallet_transfer(self):
        # accounts must exist..
        # print(self.__auth_funding.initiate_wallet_transfer(
        #     amount=200, fromAccount='Futures Wallet', toAccount='Spot Wallet', unit='XBT'
        # ))
        pass

    @unittest.skip('Skipping Futures initiate_subaccount_transfer endpoint')
    def test_initiate_subccount_transfer(self):
        # print(self.__auth_funding.initiate_subccount_transfer(
        #     amount=200,
        #     fromAccount='The wallet (cash or margin account) from which funds should be debited',
        #     fromUser='The user account (this or a sub account) from which funds should be debited',
        #     toAccount='The wallet (cash or margin account) to which funds should be credited',
        #     toUser='The user account (this or a sub account) to which funds should be credited',
        #     unit='XBT',
        # ))
        pass

    @unittest.skip('Skipping Futures withdrawal_to_spot_wallet endpoint')
    def test_initiate_withdrawal_to_spot_wallet(self):
        # print(self.__auth_funding.initiate_withdrawal_to_spot_wallet(
        #     amount=200,
        #     currency='XBT',
        # ))
        pass

if __name__ == '__main__': 
    unittest.main()
