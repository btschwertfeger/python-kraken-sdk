from kraken.base_api.base_api import KrakenBaseFuturesAPI

class FundingClient(KrakenBaseFuturesAPI):

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_historical_funding_rates(self, symbol: str) -> dict:
        '''https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-funding-rates-historicalfundingrates'''
        return self._request('GET', f'/derivatives/api/v4/historicalfundingrates', queryParams={'symbol': symbol}, auth=False)


