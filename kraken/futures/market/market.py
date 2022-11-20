from kraken.base_api.base_api import KrakenBaseFuturesAPI

class MarketClient(KrakenBaseFuturesAPI):

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_ohlc(self, price_type: str, symbol: str, interval: int, from_: int=None, to: int=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/4403284627220-OHLC'''
        params = { }
        if from_ != None: params['from'] = from_
        if to != None: params['to'] = to
        return self._request('GET', f'/api/charts/v1/{price_type}/{symbol}/{interval}', queryParams=params, auth=False)

    def get_fee_schedules(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-fee-schedules-get-fee-schedules
            https://support.kraken.com/hc/en-us/articles/360049269572-Fee-Schedules
        '''
        return self._request('GET', '/derivatives/api/v3/feeschedules', auth=False)

    def get_fee_schedules_vol(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-fee-schedules-get-fee-schedule-volumes'''
        return self._request('GET', '/derivatives/api/v3/feeschedules/volumes', auth=True)
        
    def get_orderbook(self, symbol: str=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-orderbook
            https://support.kraken.com/hc/en-us/articles/360022839551-Order-Book
        '''
        params = {}
        if symbol: params['symbol'] = symbol
        return self._request('GET', '/derivatives/api/v3/orderbook', queryParams=params, auth=False)

    def get_tickers(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-tickers
            https://support.kraken.com/hc/en-us/articles/360022839531-Tickers
        '''
        return self._request('GET', '/derivatives/api/v3/tickers', auth=False)

    def get_instruments(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instruments
            https://support.kraken.com/hc/en-us/articles/360022635672-Instruments
        '''
        return self._request('GET', '/derivatives/api/v3/instruments', auth=False)
    
    def get_instruments_status(self, instrument: str=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instrument-status-list
           https://docs.futures.kraken.com/#http-api-trading-v3-api-instrument-details-get-instrument-status
        '''
        if instrument:
            return self._request('GET', f'/derivatives/api/v3/instruments/{instrument}/status', auth=False)
        else:
            return self._request('GET', '/derivatives/api/v3/instruments/status', auth=False)

    def get_trade_history(self, symbol: str=None, lastTime: str=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-market-data-get-trade-history
            https://support.kraken.com/hc/en-us/articles/360022839511-History
        '''
        params = {}
        if symbol != None:  params['symbol'] = symbol 
        if lastTime != None: params['lastTime'] = lastTime
        if params == {}: raise ValueError('Either symbol or lastTime must be specified!')
        return self._request('GET', '/derivatives/api/v3/history', queryParams=params, auth=False)

    def get_historical_funding_rates(self, symbol: str) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360061979852-Historical-Funding-Rates'''
        return self._request('GET', '/derivatives/api/v4/historicalfundingrates', queryParams={ 'symbol': symbol }, auth=False)

    def get_market_history_execution(self, symbol: str, since: int=None, before: int=None, sort: str=None, continuationToken: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/4401755685268-Market-History-Executions'''
        params = {}
        if since != None: params['since'] = since
        if before != None: params['before'] = before
        if sort != None: params['sort'] = sort
        if continuationToken != None: params['continuationToken'] = continuationToken
        return self._request('GET', f'/api/history/v2/market/{symbol}/executions', queryParams=params, auth=False)

    def get_market_history_mark_price(self, symbol: str, since: int=None, before: int=None, sort: str=None, continuationToken: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/4401748276116-Market-History-Mark-Price'''
        params = {}
        if since != None: params['since'] = since
        if before != None: params['before'] = before
        if sort != None: params['sort'] = sort
        if continuationToken != None: params['continuationToken'] = continuationToken
        return self._request('GET', f'/api/history/v2/market/{symbol}/price', queryParams=params, auth=False)

    def get_market_history_orders(self, symbol: str, since: int=None, before: int=None, sort: str=None, continuationToken: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/4401755906452-Market-History-Orders'''
        params = {}
        if since != None: params['since'] = since
        if before != None: params['before'] = before
        if sort != None: params['sort'] = sort
        if continuationToken != None: params['continuationToken'] = continuationToken
        return self._request('GET', f'/api/history/v2/market/{symbol}/orders', queryParams=params, auth=False)

    def get_leverage_preference(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-get-the-leverage-setting-for-a-market'''
        return self._request('GET', f'/derivatives/api/v3/leveragepreferences', auth=True)

    def set_leverage_preference(self, symbol: str, maxLeverage: float=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-set-the-leverage-setting-for-a-market'''
        params = {'symbol': symbol}
        if maxLeverage != None: params['maxLeverage'] = maxLeverage
        return self._request('PUT', '/derivatives/api/v3/leveragepreferences', queryParams=params, auth=True)

    def get_pnl_preference(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-get-pnl-currency-preference-for-a-market'''
        return self._request('GET', '/derivatives/api/v3/pnlpreferences', auth=True)

    def set_pnl_preference(self, symbol: str, pnlPreference: str) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-multi-collateral-set-pnl-currency-preference-for-a-market'''

        return self._request('PUT', '/derivatives/api/v3/pnlpreferences', queryParams={
            'symbol': symbol,
            'pnlPreference': pnlPreference
        }, auth=True)

