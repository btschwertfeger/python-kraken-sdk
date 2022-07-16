from kraken.base_api.base_api import KrakenBaseRestAPI

class FuturesTradeClient(KrakenBaseRestAPI):

    def __init__(self, key: str='', secret: str='', url: str='', futures: bool=True, sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, futures=futures, url=url, sandbox=sandbox)

    def send_order(
        self, 
        orderType: str, 
        symbol: str, 
        side: str, 
        size: int,
        limitPrice: float=None,
        stopPrice: float=None,
        triggerSignal: str=None,
        cliOrdId: str=None,
        reduceOnly: bool=False,
        **kwargs
    ) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022839691-Send-order'''
        params = {
            'orderType': orderType,
            'symbol': symbol,
            'side': side,
            'size': size,
            'reduceOnly': reduceOnly
        }
        if limitPrice != None: params['limitPrice'] = limitPrice
        if stopPrice != None: params['stopPrice'] = stopPrice
        if triggerSignal != None: params['triggerSignal'] = triggerSignal
        if cliOrdId != None: params['cliOrdId'] = cliOrdId
        params.update(kwargs)
        return self._request('POST', '/derivatives/api/v3/sendorder',params=params)

    def edit_order(
        self,
        orderId: str=None,
        cliOrdId: str=None,
        size: int=None,
        limitPrice: float=None,
        stopPrice: float=None,
        **kwargs
    ) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360031518331-Edit-Order'''
        if cliOrdId == None and orderId == None: raise ValueError('Missing clliOrdId or orderId')
        params = {}
        if orderId != None: params['orderId'] = orderId
        if cliOrdId != None: params['cliOrdId'] = cliOrdid
        if size != None: params['size'] = size
        if limitPrice != None: params['limitPrice'] = limitPrice
        if stopPrice != None: params['stopPrice'] = stopPrice
        params.update(kwargs)
        return self._request('POST', '/derivatives/api/v3/editorder', params=params)

    def cancel_order(self, orderId: str=None, cliOrdId: str=None) -> dict:
        '''https://support.kraken.com/hc/en-us/articles/360022635872-Cancel-Order'''
        if cliOrdId == None and orderId == None: raise ValueError('Missing clliOrdId or orderId')
        params = {}
        if orderId != None: params['order_id'] = orderId
        if cliOrdId != None: params['cliOrdId'] = cliOrdId
        print(params)
        return self._request('POST', '/derivatives/api/v3/cancelorder', params=params)
