from kraken.base_request.base_request import KrakenBaseRestAPI

class UserData(KrakenBaseRestAPI):

    def get_account_balance(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getAccountBalance'''
        return self._request('POST', '/private/Balance')

    def get_trade_balance(self, asset=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTradeBalance'''
        params = {}
        if asset != None: params['asset'] = asset
        return self._request('POST', '/private/TradeBalance', params=params)

    def get_open_orders(self, trades: bool=False, userref: int=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getOpenOrders'''
        params = { 'trades': trades }
        if userref != None: params['userref'] = userref
        return self._request('POST', '/private/OpenOrders', params=params)

    def get_closed_orders(self, trades: bool=False, userref: int=None, start: int=None, end: int=None, ofs: int=None, closetime: str='both') -> dict:
        '''https://docs.kraken.com/rest/#operation/getClosedOrders'''
        params = {
            'trades': trades,
            'closetime': closetime
        }
        if userref != None: params['userref'] = userref
        if start != None: params['start'] = start
        if end != None: params['end'] = end
        if ofs != None: params['ofs'] = ofs

        return self._request('POST', '/private/ClosedOrders', params=params)
