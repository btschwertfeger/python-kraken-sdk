from kraken.base_api.base_api import KrakenBaseRestAPI
import logging

class SpotWsClientCl(KrakenBaseRestAPI):

    def __init__(self, key: str='', secret: str='', sandbox: bool=False):
        super().__init__(key=key, secret=secret, sandbox=sandbox)

        self._pub_conn = None
        self._priv_conn = None
     
    def get_ws_token(self) -> dict:
        '''https://docs.kraken.com/rest/#tag/Websockets-Authentication'''
        return self._request('POST', '/private/GetWebSocketsToken')

    async def create_order(
        self,
        ordertype: str,
        side: str,
        pair: str,
        price: str=None,
        price2: str=None,
        volume: str=None,
        leverage: int=None,
        oflags: [str]=None,
        starttm: str=None,
        expiretm: str=None,
        deadline: str=None,
        userref: str=None,
        validate: str=None,
        close_ordertype: str=None,
        close_price: float=None,
        close_price2: float=None,
        timeinforce: str=None
    ) -> None:
        '''https://docs.kra)en.com/websockets/#message-addOrder'''
        if not self._priv_conn:
            logging.warning('Websocket not connected!')
            return
        elif not self._priv_conn.isAuth:
            raise ValueError('Cannot create_order on public Websocket Client!')

        payload = {
            'event': 'addOrder',
            'ordertype': str(ordertype),
            'type': str(side),
            'pair': str(pair),
            'price': str(price)
        }
        if price2 != None: payload['price2'] = str(price2)
        if volume != None: payload['volume'] = str(volume)
        if oflags != None:
            if type(oflags) == str: payload['oflags'] = oflags
            elif type(oflags) == list: payload['oflags'] = self._to_str_list(oflags)
            else: raise ValueError('oflags must be type [str] or comma delimited list of order flags. Available flags: viqc,fcib, fciq, nompp, post')
        if starttm != None: payload['starttm'] = starttm
        if expiretm != None: payload['expiretm'] = expiretm
        if deadline != None: payload['deadline'] = deadline
        if userref != None: payload['userref'] = userref
        if validate != None: payload['validate'] = validate
        if close_ordertype != None: payload['close[ordertype]'] = close_ordertype
        if close_price != None: payload['close[price]'] = close_price
        if close_price2 != None: payload['close[price2]'] = close_price2
        if timeinforce != None: payload['timeinforce'] = timeinforce

        await self._priv_conn.send_message(msg=payload, private=True)

    async def edit_order(
        self, orderid: str,
        reqid: int=None,
        pair: str=None,
        price: str=None,
        price2: str=None,
        volume: str=None,
        oflags: [str]=None,
        newuserref: str=None,
        validate: str=None
    ) -> None:
        '''https://docs.kraken.com/websockets/#message-editOrder'''
        if not self._priv_conn:
            logging.warning('Websocket not connected!')
            return
        elif not self._priv_conn.isAuth:
            raise ValueError('Cannot edit_order on public Websocke Client!')

        payload = {
            'event': 'editOrder',
            'orderid': orderid
        }
        if reqid != None: payload['reqid'] = reqid
        if pair != None: payload['pair'] = pair
        if price != None: payload['price'] = str(price)
        if price2 != None: payload['price2'] = str(price2)
        if volume != None: payload['volume'] = str(volume)
        if oflags != None: payload['oflags'] = self._to_str_list(oflags)
        if newuserref != None: payload['newuserref'] = str(newuserref)
        if validate != None: payload['validate'] = str(validate)

        await self._priv_conn.send_message(msg=payload, private=True)

    async def cancel_order(self, txid) -> None:
        '''https://docs.kraken.com/websockets/#message-cancelOrder'''
        if not self._priv_conn:
            logging.warning('Websocket not connected!')
            return
        elif not self._priv_conn.isAuth:
            raise ValueError('Cannot cancel_order on public Websocke Client!')
        else: await self._priv_conn.send_message(msg={ 
            'event': 'cancelOrder', 
            'txid': self._to_str_list(txid)
        }, private=True)

    async def cancel_all_orders(self) -> None:
        '''https://docs.kraken.com/websockets/#message-cancelAll'''
        if not self._priv_conn:
            logging.warning('Websocket not connected!')
            return
        elif not self._priv_conn.isAuth:
            raise ValueError('Cannot use cancel_all_orders on public Websocke Client!')
        else: await self._priv_conn.send_message(msg={ 'event': 'cancelAll' }, private=True, reponse=True)

    async def cancel_all_orders_after(self, timeout: int) -> None:
        '''https://docs.kraken.com/websockets/#message-cancelAllOrdersAfter'''
        if not self._priv_conn:
            logging.warning('Websocket not connected!')
            return
        elif not self._priv_conn.isAuth:
            raise ValueError('Cannot use cancel_all_orders_after on public Websocke Client!')
        else: await self._priv_conn.send_message(msg={
            'event': 'cancelAllOrdersAfter',
            'timeout': timeout
        }, private=True)
