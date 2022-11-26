from kraken.base_api.base_api import KrakenBaseRestAPI
from typing import List


class TradeClient(KrakenBaseRestAPI):

    def create_order(self,
        ordertype: str,
        side: str,
        volume: str,
        pair: str,
        price: str=None,
        price2: str=None,
        trigger: str=None,
        leverage: str=None,
        stp_type: str='cancel-newest',
        oflags: List[str]=None,
        timeinforce: str=None,
        starttm: str='0',
        expiretm: str='0',
        close_ordertype: str=None,
        close_price: str=None,
        close_price2: str=None,
        deadline: str=None,
        validate: bool=False,
        userref: int=None
    ) -> dict:
        '''https://docs.kraken.com/rest/#operation/addOrder'''
        params = {
            'ordertype': str(ordertype),
            'type': str(side),
            'volume': str(volume),
            'pair': str(pair),
            'stp_type': stp_type,
            'starttm': starttm,
            'expiretm': expiretm,
            'validate': validate
        }
        if trigger != None:
            if ordertype in ['stop-loss', 'stop-loss-limit', 'take-profit-limit', 'take-profit-limit']:
                if timeinforce != None: params['trigger'] = trigger
                else: raise ValueError(f'Cannot use trigger {trigger} and timeinforce {timeinforce} together')
            else: raise ValueError(f'Cannot use trigger on ordertype {ordertype}')
        elif timeinforce != None: params['timeinforce'] = timeinforce
        if price != None: params['price'] = str(price)
        if price2 != None: params['price2'] = str(price2)
        if leverage != None: params['leverage'] = str(leverage)
        if oflags != None: params['oflags'] = self._to_str_list(oflags)
        if close_ordertype != None: params['close[ordertype]'] = close_ordertype
        if close_price != None: params['close[price]'] = close_price
        if close_price2 != None: params['close[price2]'] = close_price2
        return self._request(method='POST', uri='/private/AddOrder', params=params)


    def create_order_batch(self, orders: List[dict], pair: str, deadline: str=None, validate: bool=False) -> dict:
        '''https://docs.kraken.com/rest/#operation/addOrderBatch'''
        params = {
            'orders': orders,
            'pair': pair,
            'validate': validate
        }
        if deadline != None: params['deadline'] = deadline
        return self._request(method='POST', uri='/private/AddOrderBatch', params=params, do_json=True)

    def edit_order(self, 
        txid: str, 
        pair: str, 
        volume: str=None, 
        price: str=None, 
        price2: str=None, 
        oflags=None, 
        deadline: str=None, 
        cancel_response: bool=None, 
        validate: str=False, 
        userref: int=None
    ) -> dict:
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
        if deadline != None: params['deadline'] = deadline
        return self._response('POST', uri='/private/EditOrder', params=params)

    def cancel_order(self, txid) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelOrder'''
        return self._request(method='POST', uri='/private/CancelOrder', params={ 'txid': txid })

    def cancel_all_orders(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelAllOrders'''
        return self._request(method='POST', uri='/private/CancelAll')

    def cancel_all_orders_after_x(self, timeout: int) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelAllOrdersAfter'''
        return self._request(method='POST', uri='/private/CancelAllOrdersAfter', params={ 'timeout': timeout })

    def cancel_order_batch(self, orders: List[str]) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelOrderBatch'''
        return self._request(method='POST', uri='/private/CancelOrderBatch', params={ 'orders': orders })


