from kraken.base_api.base_api import KrakenBaseFuturesAPI

class MarketClient(KrakenBaseFuturesAPI):

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_ohlc(self, tick_type: str, symbol: str, resolution: int, from_: int=None, to: int=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-charts-ohlc-get-ohlc
            https://support.kraken.com/hc/en-us/articles/4403284627220-OHLC
        '''
        params = { }
        if from_ != None: params['from'] = from_
        if to != None: params['to'] = to
        return self._request('GET', f'/api/charts/v1/{tick_type}/{symbol}/{resolution}', queryParams=params, auth=False)

    def get_tick_types(self) -> dict:
        '''https://docs.futures.kraken.com/#http-api-charts-ohlc-get-tick-types'''
        return self._request('GET', '/api/charts/v1/', auth=False)

    def get_tradeable_products(self, tick_type: str) -> dict:
        '''https://docs.futures.kraken.com/#http-api-charts-ohlc-get-tradeable-products'''
        return self._request('GET', f'/api/charts/v1/{tick_type}', auth=False)

    def get_resolutions(self, tick_type: str, tradeable: str) -> dict:
        '''https://docs.futures.kraken.com/#http-api-charts-ohlc-get-resolutions'''
        return self._request('GET', f'/api/charts/v1/{tick_type}/{tradeable}', auth=False)
    
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

    def _get_historical_events(self,
        endpoint: str,
        before: int=None,
        continuation_token: str=None,
        since: int=None,
        sort: str=None,
        tradeable: str=None,
        auth: bool=True,
        **kwargs
    ) -> dict:  
        params = {}
        if before != None: params['before'] = before
        if continuation_token != None: params['continuation_token'] = continuation_token
        if since != None: params['since'] = since
        if sort != None: params['sort'] = sort
        if tradeable != None: params['tradeable'] = tradeable
        params.update(kwargs)
        return self._request('GET', endpoint, postParams=params, auth=auth)

    def get_execution_events(self,
        before: int=None,
        continuation_token: str=None,
        since: int=None,
        sort: str=None,
        tradeable: str=None
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-market-history-get-execution-events'''

        return self._get_historical_events(
            endpoint='/api/history/v2/executions',
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
            auth=True
        )

    def get_public_execution_events(self,
        tradeable: str,
        before: int=None,
        continuation_token: str=None,
        since: int=None,
        sort: str=None,
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-market-history-get-public-execution-events
        https://support.kraken.com/hc/en-us/articles/4401755685268-Market-History-Executions
        '''
        return self._get_historical_events(
            endpoint=f'/api/history/v2/market/{tradeable}/executions',
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            auth=False
        )

    def get_public_order_events(self,
        tradeable: str,
        before: int=None,
        continuation_token: str=None,
        since: int=None,
        sort: str=None,
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-market-history-get-public-order-events
        https://support.kraken.com/hc/en-us/articles/4401755906452-Market-History-Orders
        '''
        return self._get_historical_events(
            endpoint=f'/api/history/v2/market/{tradeable}/orders',
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            auth=False
        )

    def get_public_mark_price_events(self,
        tradeable: str,
        before: int=None,
        continuation_token: str=None,
        since: int=None,
        sort: str=None,
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-market-history-get-public-mark-price-events
        https://support.kraken.com/hc/en-us/articles/4401748276116-Market-History-Mark-Price
        '''
        return self._get_historical_events(
            endpoint=f'/api/history/v2/market/{tradeable}/price',
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            auth=False
        )

    def get_order_events(self,
        before: int=None,
        continuation_token: str=None,
        since: int=None,
        sort: str=None,
        tradeable: str=None
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-market-history-get-order-events'''
        return self._get_historical_events(
            endpoint='/api/history/v2/orders',
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
            auth=True
        )

    def get_trigger_events(self,
        before: int=None,
        continuation_token: str=None,
        since: int=None,
        sort: str=None,
        tradeable: str=None
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-history-market-history-get-trigger-events'''
        return self._get_historical_events(
            endpoint='/api/history/v2/triggers',
            before=before,
            continuation_token=continuation_token,
            since=since,
            sort=sort,
            tradeable=tradeable,
            auth=True
        )
