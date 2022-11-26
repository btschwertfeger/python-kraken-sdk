#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import requests
import logging
import hmac
import hashlib
import base64
import time
from uuid import uuid1
import urllib.parse
import sys

try:
    from kraken.exceptions.exceptions import KrakenExceptions
except ModuleNotFoundError:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.exceptions.exceptions import KrakenExceptions

class KrakenErrorHandler(object):

    def __init__(self): 
        self.__kexceptions = KrakenExceptions()

    def __get_exception(self, msg):
        return self.__kexceptions.get_exception(msg)

    def check(self, data: dict) -> dict:
        '''Check if the error message is a known Kraken error response 
            than raise a custom exception or return the data containing the 'error' 
        '''
        if len(data.get('error', [])) == 0 and 'result' in data: return data['result']
        else:
            exception = self.__get_exception(data['error'])
            if exception: raise exception(data)
            else: return data

    def check_sendStatus(self, data: dict) -> dict:
        if 'sendStatus' in data and 'status' in data['sendStatus']:
            exception = self.__get_exception(data['sendStatus']['status'])
            if exception: raise exception(data)
            else: return data
        else: return data

    def check_batchStatus(self, data: [dict]) -> dict:
        if 'batchStatus' in data:
            batchStatus = data['batchStatus']
            for status in batchStatus:
                if 'status' in status:
                    exception = self.__get_exception(status['status'])
                    if exception: raise exception(data)
        return data

class KrakenBaseRestAPI(object):
    ''' Base class for all Spot clients

        Handles un/signed requests and returns exception handled results

        ====== P A R A M E T E R S ======
        key: str, defualt: ''
            Spot API public key
        secret: str, default: ''
            Spot API secret key
        url: str, default: 'https://api.kraken.com'
            optional url
        sandbox: bool, default: False
            not used so far
    '''

    URL = 'https://api.kraken.com'
    API_V = '/0'

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False, **kwargs):
        if sandbox: raise ValueError('Sandbox not availabel for Kraken Spot trading.')
        if url != '': self.url = url
        else: self.url = self.URL

        self.__key = key
        self.__secret = secret
        self.__err_handler = KrakenErrorHandler()
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': 'python-kraken-sdk'})

    def _request(self, 
        method: str, 
        uri: str, 
        timeout: int=10, 
        auth: bool=True,
        params: dict={}, 
        do_json: bool=False, 
        return_raw: bool=False
    ) -> dict:
        method = method.upper()
        data_json = ''
        if method in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params): strl.append(f'{key}={params[key]}')
                data_json += '&'.join(strl)
                uri += f'?{data_json}'.replace(' ', '%20')

        headers = { } 
        if auth:
            if not self.__key or self.__key == '' or not self.__secret or self.__secret == '': raise ValueError('Missing credentials')
            params['nonce'] = str(int(time.time() * 1000))
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'API-Key': self.__key,
                'API-Sign': self.get_kraken_signature(f'{self.API_V}{uri}', params)
            })

        url = f'{self.url}{self.API_V}{uri}'
        if method in ['GET', 'DELETE']:
            return self.__check_response_data(self.__session.request(method=method, url=url, headers=headers, timeout=timeout), return_raw)
        elif do_json:
            return self.__check_response_data(self.__session.request(method=method, url=url, headers=headers, json=params, timeout=timeout), return_raw)
        else:
            return self.__check_response_data(self.__session.request(method=method, url=url, headers=headers, data=params, timeout=timeout), return_raw)

    def get_kraken_signature(self, urlpath: str, data: dict) -> str:
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self.__secret), 
                urlpath.encode() + hashlib.sha256((str(data['nonce']) + urllib.parse.urlencode(data)).encode()).digest(),
                hashlib.sha512
            ).digest()
        ).decode()

    def __check_response_data(self, response_data, return_raw: bool=False) -> dict:
        if response_data.status_code in [ '200', 200 ]:
            if return_raw: return response_data
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)
            else:
                if 'error' in data: return self.__err_handler.check(data)
                else: return data
        else: raise Exception(f'{response_data.status_code} - {response_data.text}')

    @property
    def return_unique_id(self) -> str:
        return ''.join([each for each in str(uuid1()).split('-')])

    def _to_str_list(self, a) -> str:
        if type(a) == str: return a
        elif type(a) == list: return ','.join([i for i in a])
        else: raise ValueError('a must be string or list of strings')

class KrakenBaseFuturesAPI(object):
    ''' Base class for all Futures clients

        Handles un/signed requests and returns exception handled results

        ====== P A R A M E T E R S ======
        key: str, defualt: ''
            Futures API public key
        secret: str, default: ''
            Futures API secret key
        url: str, default: 'https://futures.kraken.com'
            optional url
        sandbox: bool, default: False
            if set to true the url will be 'https://demo-futures.kraken.com'
        
        ====== N O T E S ======
        If the sandbox environment is chosen, the keys must be generated here:
            https://demo-futures.kraken.com/settings/api
    '''

    URL = 'https://futures.kraken.com'
    SANDBOX_URL = 'https://demo-futures.kraken.com'

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False, **kwargs):
        
        self.sandbox = sandbox
        if url: self.url = url
        elif self.sandbox: self.url = self.SANDBOX_URL
        else: self.url = self.URL
        
        self.__key = key
        self.__secret = secret
        self.__nonce = 0

        self.__err_handler = KrakenErrorHandler()
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': 'python-kraken-sdk'})

    def _request(self, 
        method: str, 
        uri: str, 
        timeout: int=10, 
        auth: bool=True, 
        postParams: dict={},
        queryParams: dict={}, 
        return_raw: bool=False
    ) -> dict:
        method = method.upper()

        postString: str = ''
        if postParams:
            strl: [str] = []
            for key in sorted(postParams): strl.append(f'{key}={postParams[key]}')
            postString = '&'.join(strl)

        queryString: str = ''
        if queryParams:
            strl: [str] = []
            for key in sorted(queryParams): strl.append(f'{key}={queryParams[key]}')
            queryString = '&'.join(strl).replace(' ', '%20')

        headers = { } 
        if auth:
            if not self.__key or self.__key == '' or not self.__secret or self.__secret == '': raise ValueError('Missing credentials')
            self.__nonce = (self.__nonce + 1) % 1
            nonce = str(int(time.time() * 1000)) + str(self.__nonce).zfill(4)
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Nonce': nonce,
                'APIKey': self.__key,
                'Authent': self.get_kraken_futures_signature(uri, queryString + postString, nonce)
            })

        if method in ['GET', 'DELETE']:
            return self.__check_response_data(
                self.__session.request(
                    method=method,
                    url=f'{self.url}{uri}' if queryString == '' else f'{self.url}{uri}?{queryString}', 
                    headers=headers, 
                    timeout=timeout
                ), 
                return_raw
            )
        elif method == 'PUT':
            return self.__check_response_data(
                self.__session.request(
                method=method, 
                url=f'{self.url}{uri}', 
                params=str.encode(queryString), 
                headers=headers, 
                timeout=timeout
                ), 
                return_raw
            )
        else:
            return self.__check_response_data(
                self.__session.request(
                    method=method, 
                    url=f'{self.url}{uri}?{postString}', 
                    data=str.encode(postString), 
                    headers=headers, 
                    timeout=timeout
                ), return_raw
            )

    def get_kraken_futures_signature(self, endpoint: str, data: str, nonce: str) -> str:
        # reference: https://github.com/CryptoFacilities/REST-v3-Python/blob/ee89b9b324335d5246e2f3da6b52485eb8391d50/cfRestApiV3.py#L295-L296
        if endpoint.startswith('/derivatives'): endpoint = endpoint[len('/derivatives'):] 
        sha256_hash = hashlib.sha256()
        sha256_hash.update((data + nonce + endpoint).encode('utf8'))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self.__secret), 
                sha256_hash.digest(), 
                hashlib.sha512
            ).digest()
        )
   
    def __check_response_data(self, response_data, return_raw: bool=False) -> dict:
        if response_data.status_code in [ '200', 200 ]:
            if return_raw: return response_data
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)
            else:
                if 'error' in data: return self.__err_handler.check(data)
                elif 'sendStatus' in data: return self.__err_handler.check_sendStatus(data)
                elif 'batchStatus' in data: return self.__err_handler.check_batchStatus(data)
                else: return data
        else: raise Exception(f'{response_data.status_code} - {response_data.text}')