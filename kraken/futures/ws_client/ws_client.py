from kraken.base_api.base_api import KrakenBaseFuturesAPI
import logging
import hashlib, hmac, base64

class FuturesWsClientCl(KrakenBaseFuturesAPI):
    '''This class will be used in future if Kraken implements for example
        sending orders via websocket feed for Futures
    '''

    websocket = None

    def _get_sign_challenge(self, challenge: str) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(challenge.encode('utf8'))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self.secret), 
                sha256_hash.digest(), 
                hashlib.sha512
            ).digest()
        ).decode('utf-8')