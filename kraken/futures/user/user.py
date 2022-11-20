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
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-account-information-get-position-percentile-of-unwind-queue'''
        return self._request('GET', f'/derivatives/api/v3/unwindqueue', auth=True)

    def get_notificatios(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-general-get-notifications'''
        return self._request('GET', '/derivatives/api/v3/notifications', auth=True)

    def get_account_log(self,
        before: int=None,
        count: str=None,
        from_: str=None,
        info: str=None,
        since: str=None,
        sort: str=None,
        to: str=None
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-account-log'''
        params = {}
        if before != None: params['before'] = before
        if count != None: params['count'] = count
        if from_ != None: params['from'] = from_
        if info != None: params['info'] = info
        if since != None: params['since'] = since
        if sort != None: params['sort'] = sort
        if to != None: params['to'] = to
        return self._request('GET', '/api/history/v2/account-log', queryParams=params, auth=True)


    def get_account_log_csv(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-account-log-get-recent-account-log-csv'''
        return self._request('GET', '/api/history/v2/accountlogcsv', auth=True)


