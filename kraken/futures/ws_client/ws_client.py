from kraken.base_api.base_api import KrakenBaseFuturesAPI
import logging
import hashlib, hmac, base64

class FuturesWsClientCl(KrakenBaseFuturesAPI):
    '''This class will be extended in the future if Kraken implements for example
        sending orders via websocket feed for Futures
    '''
    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False):
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)
        self._conn = None
        self._key = key
        self._secret = secret

    def _get_sign_challenge(self, challenge: str) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(challenge.encode('utf8'))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self._secret), 
                sha256_hash.digest(), 
                hashlib.sha512
            ).digest()
        ).decode('utf-8')