from kraken.base_api.base_api import KrakenBaseRestAPI


api_version = 0
class MarketData(KrakenBaseRestAPI):

    def get_assets(self, assets=None, aclass=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getAssetInfo'''
        params = {}
        if assets != None:
            if type(assets) == str: assets = [assets]
            params['asset'] = ','.join(assets)
        if aclass != None: params['aclass'] = aclass
        return self._request('GET', '/public/Assets', params=params, auth=False)

    def get_tradable_asset_pair(self, pair, info=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTradableAssetPairs'''
        params = {}
        if type(pair) == str: pair = [pair]
        params['pair'] = ','.join(pair)
        if info != None: params['info'] = info

        return self._request('GET', '/public/AssetPairs', params=params, auth=False)

    def get_ticker(self, pair) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTickerInformation'''
        return self._request('GET', '/public/Ticker', params={'pair': pair}, auth=False)

    def get_ohlc(self, pair, interval: int=None, since: int=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getOHLCData
        interval in minutes
        '''
        params = { 'pair': pair }
        if interval != None: params['interval'] = interval
        if since != None: params['since'] = since
        return self._request('GET', '/public/OHLC', params=params, auth=False)

    def get_order_book(self, pair, count=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getOrderBook'''
        params = { 'pair': pair }
        if count != None: params['count'] = count
        return self._request('GET', '/public/Depth', params=params, auth=False)

    def get_recent_trades(self, pair, since=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getRecentTrades'''
        params = { 'pair': pair }
        if since != None: params['since'] = None
        return self._request('GET', '/public/Trades', params=params, auth=False)

    def get_recend_spreads(self, pair, since=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getRecentSpreads'''
        params = { 'pair': pair }
        if since != None: params['since'] = since
        return self._request('GET', '/public/Spread', params=params, auth=False)

    def get_system_status(self) -> dict:
        return self._request('GET', '/public/SystemStatus', auth=False)
