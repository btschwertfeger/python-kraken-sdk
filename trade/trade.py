from kraken.base_request.base_request import KrakenBaseRestAPI


class TradeData(object):

    def create_order(self, ordertype: str, side: str, volume: str, pair: str, price: str=None, price2: str=None, trigger: str='last', leverage: str=None, stp_type: str='cancel-newest', oflags: [str]=None, timeinforce: str='GTC', starttm: str='0', expiretm: str='0', close_ordertype: str=None, close_price: str=None, close_price2: str=None, deadline: str=None, validate: bool=False, userref: int=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/addOrder'''
        params = {
            'ordertype': str(ordertype),
            'type': str(side),
            'volume': str(volume),
            'pair': str(pair),
            'trigger': trigger,
            'stp_type': stp_type,
            'timeinforce': timeinforce,
            'starttm': starttm,
            'expiretm': expiretm,
            'validate': validate
        }
        if price != None: params['price'] = str(price)
        if price2 != None: params['price2'] = str(price2)
        if leverage != None: params['leverage'] = str(leverage)
        if oflags != None: params['oflags'] = self._to_str_list(oflags)
        if close_ordertype != None: params['close[ordertype]'] = close_ordertype
        if close_price != None: params['close[price]'] = close_price
        if close_price2 != None: params['close[price2]'] = close_price2
        return self._request('POST', '/private/AddOrder', params=params)


    def create_order_batch(self, orders: dict, pair: str, deadline: str=None, validate: bool=False) -> dict:
        '''https://docs.kraken.com/rest/#operation/addOrderBatch'''
        params = {
            'orders': orders,
            'pair': pair,
            'validate': validate
        }
        if deadline != None: params['deadline'] = deadline
        return self._request('POST', '/private/AddOrderbatch', params=params, do_json=True)

    def edit_order(self, txid, pair: str, volume: str=None, price: str=None, price2: str=None, oflags=None, deadline: str=None, cancel_response: bool=None, validate: str=False, userref: int=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/editOrder'''
        params = {
            'txid': txid,
            'pair': pair,
            'validate': validate
        }
        if userref != None: params['userref'] = userref
        if volume != None: params['volume'] = volume
        if price != None: params['price'] = price
        if price2 != None: params['price2'] = price2
        if oflags != None: params['oflags'] = self._to_str_list(oflags)
        if cancel_response != None: params['cancel_response'] = cancel_response
        return self._response('POST', '/private/EditOrder', params=params)

    def cancel_order(self, txid) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelOrder'''
        params = { 'txid': txid }
        return self._request('POST', '/private/CancelOrder', params=params)

    def cancel_all_prders(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelAllOrders'''
        return self._request('POST', '/private/CancelAll')

    def cancel_all_orders_after_x(self, timeout: int) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelAllOrdersAfter'''
        params = { 'timeout': timeout }
        return self._request('POST', '/private/CancelAllOrdersAfter')

    def cancel_order_batch(self, orders: [str]) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelOrderBatch'''
        params = { 'orders': orders }
        return self._request('POST', '/private/CancelOrderBatch')


    def test():
        dsfdsfd
sdfdsf
        sdfsdf

