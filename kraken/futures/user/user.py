from kraken.base_api.base_api import KrakenBaseFuturesAPI

class UserClient(KrakenBaseFuturesAPI):

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_wallets(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-wallets'''
        return self._request('GET', f'/derivatives/api/v3/accounts', auth=True)

    def get_open_orders(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-orders'''
        return self._request('GET', f'/derivatives/api/v3/openorders', auth=True)
    
    def get_open_positions(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-open-positions'''
        return self._request('GET', f'/derivatives/api/v3/openpositions', auth=True)

    def get_subaccounts(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-subaccounts'''
        return self._request('GET', f'/derivatives/api/v3/subaccounts', auth=True)

    def get_unwindqueue(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-subaccounts'''
        return self._request('GET', f'/derivatives/api/v3/unwindqueue', auth=True)

    def get_notificatios(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-general-get-notifications'''
        return self._request('GET', '/derivatives/api/v3/notifications', auth=True)