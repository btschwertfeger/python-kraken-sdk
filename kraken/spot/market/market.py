from kraken.base_api.base_api import KrakenBaseRestAPI

class MarketClient(KrakenBaseRestAPI):

    def get_assets(self, assets=None, aclass: str=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getAssetInfo'''
        params = {}
        if assets != None: params['asset'] = self._to_str_list(assets)
        if aclass != None: params['aclass'] = aclass
        return self._request('GET', '/public/Assets', params=params, auth=False)

    def get_tradable_asset_pair(self, pair: str, info=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTradableAssetPairs'''
        params = {}
        # if type(pair) == str: pair = [pair]
        params['pair'] = self._to_str_list(pair)#','.join(pair)
        if info != None: params['info'] = info

        return self._request('GET', '/public/AssetPairs', params=params, auth=False)

    def get_ticker(self, pair: str=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTickerInformation'''
        params = { }
        if pair != None: params['pair'] = self._to_str_list(pair)
        return self._request('GET', '/public/Ticker', params=params, auth=False)

    def get_ohlc(self, pair: str, interval: int=None, since: int=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getOHLCData
        interval in minutes
        '''
        params = { 'pair': pair }
        if interval != None: params['interval'] = interval
        if since != None: params['since'] = since
        return self._request('GET', '/public/OHLC', params=params, auth=False)

    def get_order_book(self, pair: str, count=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getOrderBook'''
        params = { 'pair': pair }
        if count != None: params['count'] = count
        return self._request('GET', '/public/Depth', params=params, auth=False)

    def get_recent_trades(self, pair: str, since=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getRecentTrades'''
        params = { 'pair': pair }
        if since != None: params['since'] = None
        return self._request('GET', '/public/Trades', params=params, auth=False)

    def get_recend_spreads(self, pair: str, since=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getRecentSpreads'''
        params = { 'pair': pair }
        if since != None: params['since'] = since
        return self._request('GET', '/public/Spread', params=params, auth=False)

    def get_system_status(self) -> dict:
        return self._request('GET', '/public/SystemStatus', auth=False)
