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

    def cancel_all_orders(self, symbol: str=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-all-orders'''
        params = {}
        if symbol != None: params['symbol'] = symbol
        return self._request('POST', '/derivatives/api/v3/cancelallorders', postParams=params, auth=True)

    def dead_mans_switch(self, timeout: int=60) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-dead-man-39-s-switch'''
        return self._request('POST', '/derivatives/api/v3/cancelallordersafter', postParams={'timeout': timeout})

    def cancel_order(self, orderId: str='', cliOrdId: str='') -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-cancel-order'''
        if orderId == '' and cliOrdId == '': raise ValueError('Either orderId or cliOrdId must be set!')

        params = {}
        if orderId != '': params['orderId'] = orderId
        elif cliOrdId != '': params['cliOrdId'] = cliOrdId
        return self._request('POST', '/derivatives/api/v3/cancelorder', postParams=params, auth=True)

    def edit_order(self, orderId: str=None, cliOrdId: str=None, limitPrice: float=None, size: float=None, stopPrice: float=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-edit-order'''
        if orderId == '' and cliOrdId == '': raise ValueError('Either orderId or cliOrdId must be set!')

        params = {}
        if orderId != '': params['orderId'] = orderId
        elif cliOrdId != '': params['cliOrdId'] = cliOrdId
        if limitPrice != None: params['limitPrice'] = limitPrice
        if size != None: params['size'] = size
        if stopPrice != None: params['stopPrice'] = stopPrice
        return self._request('POST', '/derivatives/api/v3/editorder', postParams=params, auth=True)


    def get_orders_status(self, orderIds: [str]=None, cliOrdIds: [str]=None) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-get-the-current-status-for-specific-orders'''
        if orderIds == None and cliOrdIds == None: raise ValueError('Either orderIds or cliOrdIds must be specified!')

        params = {}
        if orderIds != None: params['orderIds'] = orderIds
        elif cliOrdIds != None: params['cliOrdIds'] = cliOrdIds
        return self._request('POST', '/derivatives/api/v3/orders/status', postParams=params, auth=True)

    def create_order(self, 
        orderType: str,
        size: float,
        symbol: str,
        side: str,
        cliOrdId: str=None,
        limitPrice: float=None,
        reduceOnly: bool=None,
        stopPrice: float=None,
        triggerSignal: str=None,
    ) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order'''

        orderTypes = ['lmt', 'post', 'ioc', 'mkt', 'stp', 'take_profit']
        if orderType not in orderType: raise ValueError(f'Invalid orderType. One of [{orderTypes}] is required!')
        sides = ['buy', 'sell']
        if side not in sides: raise ValueError(f'Invalid side. One of [{sides}] is required!')

        params = {
            'orderType': orderType,
            'side': side,
            'size': size,
            'symbol': symbol
        }
        if cliOrdId != None: params['cliOrdId'] = cliOrdId
        if orderType in ['post', 'lmt']:
            if limitPrice == None: 
                raise ValueError(f'No limitPrice specified for order of type {orderType}!')
            else: params['limitPrice'] = limitPrice
        if reduceOnly != None: params['reduceOnly'] = reduceOnly
        if orderType in ['stp', 'take_profit']:
            if stopPrice == None:
                raise ValueError(f'Parammeter stopPrice must be set if orderType {orderType}!')
            if triggerSignal == None:
                raise ValueError(f'Parammeter triggerSignal must be set if orderType {orderType}!')
        if stopPrice != None: params['stopPrice'] = stopPrice
        if triggerSignal != None:
            triggerSignals = ['mark', 'spot', 'last']
            if triggerSignal not in triggerSignals:
                raise ValueError(f'Trigger signal must be in [{triggerSignals}]!')
            else: params['triggerSignal'] = triggerSignal

        return self._request('POST', '/derivatives/api/v3/sendorder', postParams=params, auth=True)


