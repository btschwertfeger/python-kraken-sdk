from kraken.base_api.base_api import KrakenBaseRestAPI

class FuturesUserClient(KrakenBaseRestAPI):

    def __init__(self, key: str='', secret: str='', url: str='', futures: bool=True, sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, futures=futures, url=url, sandbox=sandbox)

    def get_accounts(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022635792-Accounts'''
        return self._request('GET', '/derivatives/api/v3/accounts')
    
    def get_open_positions(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022635832-Open-positions'''
        return self._request('GET', '/derivatives/api/v3/openpositions')

    def get_open_orders(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022839631-Open-orders'''
        return self._request('GET', '/derivatives/api/v3/openorders')

    def get_fills(self, lastFillTime: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022839671-Fills'''
        params = {}
        if lastFillTime != None: params['lastFillTime'] = lastFillTime
        return self._request('GET', '/derivatives/api/v3/fills', params=params)

    def get_pnl_preferences(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/7374071335828-Get-PnL-Preferences-details'''
        return self._request('GET', '/derivatives/api/v3/pnlpreferences')
    
    def get_leverage_preferences(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/7374217912084-Get-Leverage-Preferences-details'''
        return self._request('GET', '/derivatives/api/v3/leveragepreferences')

    def get_subaccounts(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/6503273042580-Get-subaccount-details'''
        return self._request('GET', '/derivatives/api/v3/subaccounts')