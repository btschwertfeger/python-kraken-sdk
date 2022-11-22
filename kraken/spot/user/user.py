from kraken.base_api.base_api import KrakenBaseRestAPI

class UserClient(KrakenBaseRestAPI):

    def get_account_balance(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getAccountBalance'''
        return self._request('POST', '/private/Balance')

    def get_balances(self, currency: str) -> dict:
        
        balance = float(0)   
        currency_found = False
        for symbol, value in self.get_account_balance().items():
            if balance != float(0): break
            elif symbol in [ currency, f'Z{currency}', f'X{currency}' ]: 
                balance = float(value) 
                currency_found = True
        if not currency_found: raise ValueError('Currency not found!') 

        available_balance = balance
        for txid, order in self.get_open_orders()['open'].items():
            if currency in order['descr']['pair'][0:len(currency)]:
                if order['descr']['type'] == 'sell': 
                    available_balance -= float(order['vol'])
            elif currency in order['descr']['pair'][-len(currency):]:
                if order['descr']['type'] == 'buy': 
                    available_balance -= float(order['vol']) * float(order['descr']['price'])
        
        return {
            'currency': currency,
            'balance': balance,
            'available_balance': available_balance
        }


    def get_trade_balance(self, asset: str=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTradeBalance'''
        params = {}
        if asset != None: params['asset'] = asset
        return self._request('POST', '/private/TradeBalance', params=params)

    def get_open_orders(self, trades: bool=False, userref: int=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getOpenOrders'''
        params = { 'trades': trades }
        if userref != None: params['userref'] = userref
        return self._request('POST', '/private/OpenOrders', params=params)

    def get_closed_orders(self, 
        trades: bool=False, 
        userref: int=None, 
        start: int=None, 
        end: int=None, 
        ofs: int=None, 
        closetime: str='both'
    ) -> dict:
        '''https://docs.kraken.com/rest/#operation/getClosedOrders'''
        params = {
            'trades': trades,
            'closetime': closetime
        }
        if userref != None: params['userref'] = userref
        if start != None: params['start'] = start
        if end != None: params['end'] = end
        if ofs != None: params['ofs'] = ofs

        return self._request('POST', '/private/ClosedOrders', params=params)

    def get_orders_info(self, txid, trades: bool=False, userref: int=None) -> dict:
        '''https://docs.kraken.com/rest/#tag/User-Data/operation/getOrdersInfo'''
        params = {
            'txid': txid,
            'trades': trades
        }
        if type(txid) == list: params['txid'] = self._to_str_list(txid)
        if userref != None: params['userref'] = userref
        return self._request('POST', '/private/QueryOrders', params=params)

    def get_trades_history(self, 
        type_: str='all', 
        trades: bool=False, 
        start: int=None, 
        end: int=None, 
        ofs: int=None
    ) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTradeHistory'''
        params = {
            'type': type_,
            'trades': trades
        }
        if start != None: params['start'] = start
        if end != None: params['end'] = end
        if ofs != None: params['ofs'] = ofs
        return self._request('POST', '/private/TradesHistory', params=params)

    def get_trades_info(self, txid: str, trades: bool=False) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTradesInfo'''
        return self._request('POST', '/private/QueryTrades', params={ 
            'trades': trades,
            'txid': self._to_str_list(txid)
        })

    def get_open_positions(self, txid=None, docalcs: bool=False, consolidation: str='market') -> dict:
        '''https://docs.kraken.com/rest/#operation/getOpenPositions'''
        params = {
            'docalcs': docalcs,
            'consolidation': consolidation
        }
        if txid != None: params['txid'] = self._to_str_list(txid)
        return self._request('POST', '/private/OpenPositions', params=params)

    def get_ledgers_info(self, 
        asset: str='all', 
        aclass: str='currency', 
        type_: str='all', 
        start: int=None, 
        end: int=None, 
        ofs: int=None
    ) -> dict:
        '''https://docs.kraken.com/rest/#operation/getLedgers'''
        params = {
            'asset': asset,
            'aclass': aclass,
            'type': type_
        }
        if type(params['asset']) == list: params['asset'] = self._to_str_list(asset)
        if start != None: params['start'] = start
        if end != None: params['end'] = end
        if ofs != None: params['ofs'] = ofs
        return self._request('POST', '/private/Ledgers', params=params)

    def get_ledgers(self, id, trades: bool=False) -> dict:
        '''https://docs.kraken.com/rest/#operation/getLedgersInfo'''
        return self._request('POST', '/private/QueryLedgers', params={ 
            'trades': trades,
            'id': self._to_str_list(id)
        })

    def get_trade_volume(self, pair=None, fee_info: bool=True) -> dict:
        '''https://docs.kraken.com/rest/#operation/getTradeVolume'''
        params = { 'fee-info': fee_info}
        if pair != None: params['pair'] = self._to_str_list(pair)
        return self._request('POST', '/private/TradeVolume', params=params)

    def request_export_report(self, 
        report: str, 
        description: str, 
        format_: str='CSV', 
        fields: str='all', 
        starttm: int=None, 
        endtm: int=None,
        **kwargs
    ) -> dict:
        '''https://docs.kraken.com/rest/#operation/addExport

        ---- RESPONSE ----
            {'id': 'INSG'}
        '''
        if report not in ['trades', 'ledgers']: 
            raise ValueError('report must be one of "trades", "ledgers"')
        params = {
            'report': report,
            'description': description,
            'format': format_,
            'fields': self._to_str_list(fields)
        }
        params.update(kwargs)
        if starttm != None: params['starttm'] = starttm
        if endtm != None: params['endtm'] = endtm
        return self._request('POST', '/private/AddExport', params=params)

    def get_export_report_status(self, report: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/exportStatus
        
        ---- RESPONSE ----
        [{'id': 'INSG', 'descr': 'myLedgers1', 'format': 'CSV', 'report': 'ledgers', 'status': 'Processed', 'aclass': 'currency', 'fields': 'all', 'asset': 'all', 'subtype': 'all', 'starttm': '1656633600', 'endtm': '1657355882', 'createdtm': '1657355882', 'expiretm': '1658565482', 'completedtm': '1657355887', 'datastarttm': '1656633600', 'dataendtm': '1657355882', 'flags': '0'}]
        '''
        if report not in ['trades', 'ledgers']: 
            raise ValueError('report must be one of "trades", "ledgers"')
        return self._request('POST', '/private/ExportStatus', params={ 'report': report })

    def retrieve_export(self, id_: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/retrieveExport'''
        return self._request('POST', '/private/RetrieveExport', params={ 'id': id_ }, return_raw=True)

    def delete_export_report(self, id_: str, type_: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/removeExport'''
        return self._request('POST', '/private/RemoveExport', params={
            'id': id_,
            'type': type_
        })
