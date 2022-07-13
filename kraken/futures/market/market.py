from kraken.base_api.base_api import KrakenBaseRestAPI

class MarketClient(KrakenBaseRestAPI):

    def __init__(self, key: str='', secret: str='', url: str='', futures: bool=True, sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, url=url, futures=futures, sandbox=sandbox)

    def get_ohlc(self, price_type: str, symbol: str, interval: int, from_: int=None, to: int=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/4403284627220-OHLC'''
        params = { }
        if from_ != None: params['from'] = from_
        if to != None: params['to'] = to

        return self._request('GET', f'/api/charts/v1/{price_type}/{symbol}/{interval}', auth=False)

    def get_fee_schedules(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360049269572-Fee-Schedules'''
        return self._request('GET', '/derivatives/api/v3/feeschedules', auth=False)

    def get_orderbook(self, symbol: str) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022839551-Order-Book'''
        return self._request('GET', '/derivatives/api/v3/orderbook', params={'symbol': symbol}, auth=False)

    def get_tickers(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022839531-Tickers'''
        return self._request('GET', '/derivatives/api/v3/tickers', auth=False)

    def get_instruments(self) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022635672-Instruments'''
        return self._request('GET', '/derivatives/api/v3/instruments', auth=False)

    def get_history(self, symbol: str, lastTime: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022839511-History'''
        params = { 'symbol': symbol }
        if lastTime != None: params['lastTime'] = lastTime
        return self._request('GET', '/derivatives/api/v3/history', params=params, auth=False)

    def get_historical_funding_rates(self, symbol: str) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360061979852-Historical-Funding-Rates'''
        return self._request('GET', '/derivatives/api/v4/historicalfundingrates', params={ 'symbol': symbol }, auth=False)

    def get_market_history_execution(self, symbol: str, since int=None, before: int=None, sort: str=None, continuationToken: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/4401755685268-Market-History-Executions'''
        params = {}
        if since != None: params['since'] = since
        if before != None: params['before'] = before
        if sort != None: params['sort'] = sort
        if continuationToken != None: params['continuationToken'] = continuationToken
        return self._request('GET', f'/api/history/v2/market/{symbol}/executions', params=params, auth=False)

    def get_market_history_mark_price(self, symbol: str, since: int=None, before: int=None, sort: str=None, continuationToken: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/4401748276116-Market-History-Mark-Price'''
        params = {}
        if since != None: params['since'] = since
        if before != None: params['before'] = before
        if sort != None: params['sort'] = sort
        if continuationToken != None: params['continuationToken'] = continuationToken
        return self._request('GET'. f'/api/history/v2/market/{symbol}/price', params=params, auth=False)

     def get_market_history_orders(self, symbol: str, since: int=None, before: int=None, sort: str=None, continuationToken: str=None) -> dict:
         '''https://support.kraken.com/hc/en-us/articles/4401755906452-Market-History-Orders'''
        params = {}
        if since != None: params['since'] = since
        if before != None: params['before'] = before
        if sort != None: params['sort'] = sort
        if continuationToken != None: params['continuationToken'] = continuationToken
        return self._request('GET'. f'/api/history/v2/market/{symbol}/orders', params=params, auth=False)
