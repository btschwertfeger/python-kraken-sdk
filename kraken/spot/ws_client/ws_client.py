from kraken.base_api.base_api import KrakenBaseRestAPI
import logging

class SpotWsClientCl(KrakenBaseRestAPI):

    websocket_pub = None
    websocket_priv = None

    def get_ws_token(self, private: bool=True) -> dict:
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
    ) -> dict:
        '''https://docs.kra)en.com/websockets/#message-addOrder'''
        if not self.websocket_priv:
            logging.warning('Websocket not connected!')
            return
        elif not self.websocket_priv.private:
            raise ValueError('Cannot create order on public Websocket Client!')

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

        return await self.websocket_priv.send_message(msg=payload, private=True)

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
    ) -> dict:
        '''https://docs.kraken.com/websockets/#message-editOrder'''
        if not self.websocket_priv:
            logging.warning('Websocket not connected!')
            return
        elif not self.websocket_priv.private:
            raise ValueError('Cannot edit order on public Websocke Client!')

        payload = {
            'event': 'editOrder',
            'orderid': orderid
        }
        if reqid != None: payload['reqid'] = reqid
        if pair != None: payload['pair'] = pair
        if price != None: payload['price'] = str(price)
        if price2 != None: payload['price2'] = str(price2)
        if volume != None: payload['volume'] = str(volume)
        if oflags != None:
            if type(oflags) == str: payload['oflags'] = oflags
            elif type(oflags) == list: payload['oflags'] = self._to_str_list(oflags)
            else: raise ValueError('Oflags must be type [str] or comma delimited list of order flags. Available flags: viqc,fcib, fciq, nompp, post')
        if newuserref != None: payload['newuserref'] = str(newuserref)
        if validate != None: payload['validate'] = str(validate)

        return await self.websocket_priv.send_message(msg=payload, private=True)

    async def cancel_order(self, txid, reqid: int=None) -> dict:
        '''https://docs.kraken.com/websockets/#message-cancelOrder'''
        if not self.websocket_priv:
            logging.warning('Websocket not connected!')
            return
        elif not self.websocket_priv.private:
            raise ValueError('Cannot edit order on public Websocke Client!')

        payload = { 'event': 'cancelOrder' }
        if type(txid) == str: payload['txid'] = [txid]
        elif type(txid) == list: payload['txid'] = txid
        else: raise ValueError('txid must be string or list of strings!')

        return await self.websocket_priv.send_message(msg=payload, private=True)

    async def cancel_all_orders(self, reqid: int=None) -> dict:
        '''https://docs.kraken.com/websockets/#message-cancelAll'''
        if not self.websocket_priv:
            logging.warning('Websocket not connected!')
            return
        elif not self.websocket_priv.private:
            raise ValueError('Cannot edit order on public Websocke Client!')

        payload = { 'event': 'cancelAll' }
        if reqid != None: payload['reqid'] = reqid

        return await self.websocket_priv.send_message(msg=payload, private=True, reponse=True)

    async def cancel_all_orders_after(self, timeout: int, reqid: int=None) -> dict:
        '''https://docs.kraken.com/websockets/#message-cancelAllOrdersAfter'''
        if not self.websocket_priv:
            logging.warning('Websocket not connected!')
            return
        elif not self.websocket_priv.private:
            raise ValueError('Cannot use Dead Man\'s Switch on public Websocke Client!')

        payload = {
            'event': 'cancelAllOrdersAfter',
            'timeout': timeout
        }
        if reqid != None: payload['reqid'] = reqid

        return await self.websocket_priv.send_message(msg=payload, private=True)
