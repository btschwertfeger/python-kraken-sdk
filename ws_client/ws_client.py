from kraken.base_request.base_request import KrakenBaseRestAPI

class WsClientData(KrakenBaseRestAPI):

    def get_ws_token(self, private: bool=True) -> dict:
        '''https://docs.kraken.com/rest/#tag/Websockets-Authentication'''
        return self._request('POST', '/private/GetWebSocketsToken')

