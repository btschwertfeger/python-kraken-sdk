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


class KrakenBaseRestAPI(object):

    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False, **kwargs):

        self._api_v = ''
        if url: self.url = url
        self.url = 'https://api.kraken.com'
        self._api_v = '/0'

        self.key = key
        self.secret = secret

    def _request(self, 
        method: str, 
        uri: str, 
        timeout: int=10, 
        auth: bool=True,
        params: dict={}, 
        do_json: bool=False, 
        return_raw: bool=False
    ) -> dict:
        uri_path = uri
        data_json = ''

        if method.upper() in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append(f'{key}={params[key]}')
                data_json += '&'.join(strl)
                uri += f'?{data_json}'
                uri_path = uri

        headers = {}
        if auth:
            if not self.key or self.key == '' or not self.secret or self.secret == '': raise ValueError('Missing credentials')
            params['nonce'] = str(int(time.time() * 1000)) # generate nonce
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'API-Key': self.key,
                'API-Sign': self.get_kraken_signature(f'{self._api_v}{uri}', params)
            }

        headers['User-Agent'] = 'kraken-python-sdk'
        url = f'{self.url}{self._api_v}{uri}'


        if method in ['GET', 'DELETE']:
            return self.check_response_data(requests.request(method, url, headers=headers, timeout=timeout), return_raw)
        else:
            if do_json:
                return self.check_response_data(requests.request(method, url, headers=headers, json=params, timeout=timeout), return_raw)
            else:
                return self.check_response_data(requests.request(method, url, headers=headers, data=params, timeout=timeout), return_raw)

    def get_kraken_signature(self, urlpath: str, data: dict) -> str:
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        return  base64.b64encode(mac.digest()).decode()

    @staticmethod
    def check_response_data(response_data, return_raw: bool=False) -> dict:
        if response_data.status_code in [ '200', 200 ]:
            if return_raw: return response_data
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)
            else:
                if 'error' in data:
                    if len(data.get('error')) == 0 and 'result' in data: return data['result']
                    else: raise Exception(f'{response_data.status_code} - {response_data.text}')
                else: return data
        else: raise Exception(f'{response_data.status_code}-{response_data.text}')

    @property
    def return_unique_id(self) -> str:
        return ''.join([each for each in str(uuid1()).split('-')])

    def _to_str_list(self, a) -> str:
        if type(a) == str: return a
        elif type(a) == list: return ','.join([i for i in a])
        else: raise ValueError('a must be string or list of strings')



class KrakenBaseFuturesAPI(object):
    def __init__(self, key: str='', secret: str='', url: str='', sandbox: bool=False, **kwargs):
        
        self.sandbox = sandbox
        if self.sandbox: self.url = 'https://demo-futures.kraken.com'
        else: self.url = 'https://futures.kraken.com'
        
        self.key = key
        self.secret = secret
        self.nonce = 0

    def _request(self, 
        method: str, 
        uri: str, 
        timeout: int=10, 
        auth: bool=True, 
        postParams: dict={},
        queryParams: dict={}, 
        return_raw: bool=False
    ) -> dict:

        postString: str = ''
        if postParams:
            strl: [str] = []
            for key in sorted(postParams):
                strl.append(f'{key}={postParams[key]}')
            postString += '&'.join(strl)

        queryString: str = ''
        if queryParams:
            strl: [str] = []
            for key in sorted(queryParams):
                strl.append(f'{key}={queryParams[key]}')
            queryString += '&'.join(strl)

        headers = {}
        if auth:
            if not self.key or self.key == '' or not self.secret or self.secret == '': raise ValueError('Missing credentials')
            self.nonce = (self.nonce + 1) % 1
            nonce = str(int(time.time() * 1000)) + str(self.nonce).zfill(4)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Nonce': nonce,
                'APIKey': self.key,
                'Authent': self.get_kraken_futures_signature(uri, queryString + postString, nonce)
            }

        headers['User-Agent'] = 'kraken-python-sdk'

        url = f'{self.url}{uri}'
        if queryString != '': url = f'{url}?{queryString}'

        if method.upper() in ['GET', 'DELETE']:
            return self.check_response_data(requests.request(method, url, headers=headers, timeout=timeout), return_raw)
        elif method.upper() == 'PUT':
            return self.check_response_data(requests.request(method, f'{self.url}{uri}', params=str.encode(queryString), headers=headers, timeout=timeout), return_raw)
        else:
            return self.check_response_data(requests.request(method, f'{url}?{postString}', data=str.encode(postString), headers=headers, timeout=timeout), return_raw)

    def get_kraken_futures_signature(self, endpoint: str, data: str, nonce: str) -> str:
        # https://github.com/CryptoFacilities/REST-v3-Python/blob/ee89b9b324335d5246e2f3da6b52485eb8391d50/cfRestApiV3.py#L295-L296
        if endpoint.startswith('/derivatives'): endpoint = endpoint[len('/derivatives'):] 
        sha256_hash = hashlib.sha256()
        sha256_hash.update((data + nonce + endpoint).encode('utf8'))
        return base64.b64encode(hmac.new(base64.b64decode(self.secret), sha256_hash.digest(), hashlib.sha512).digest())

    @staticmethod
    def check_response_data(response_data, return_raw: bool=False) -> dict:
        if response_data.status_code in [ '200', 200 ]:
            if return_raw: return response_data
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)
            else:
                if 'error' in data:
                    if len(data.get('error')) == 0 and 'result' in data: return data['result']
                    else: raise Exception(f'{response_data.status_code} - {response_data.text}')
                else: return data
        else: raise Exception(f'{response_data.status_code}-{response_data.text}')

    @property
    def return_unique_id(self) -> str:
        return ''.join([each for each in str(uuid1()).split('-')])

