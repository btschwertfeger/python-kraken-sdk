from kraken.base_api.base_api import KrakenBaseFuturesAPI
import json
class TradeClient(KrakenBaseFuturesAPI):

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_fills(self, lastFillTime: str=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-data-get-your-fills'''
        queryParams = {}
        if lastFillTime: queryParams['lastFillTime'] = lastFillTime
        return self._request('GET', f'/derivatives/api/v3/fills', queryParams=queryParams, auth=True)

    def create_batch_order(self, batchorder_list: [dict]) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-batch-order-management'''
        batchorder = { 'batchOrder': batchorder_list }
        return self._request('POST', '/derivatives/api/v3/batchorder', postParams={ 'json': f'{batchorder}' }, auth=True)