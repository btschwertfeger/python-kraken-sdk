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

        if url != '': self.url = url
        else: self.url = 'https://api.kraken.com'
        self.api_v = '/0'

        self.__key = key
        self.__secret = secret

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

        headers = { 'User-Agent': 'python-kraken-sdk' }
        if auth:
            if not self.__key or self.__key == '' or not self.__secret or self.__secret == '': raise ValueError('Missing credentials')
            params['nonce'] = str(int(time.time() * 1000))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'API-Key': self.__key,
                'API-Sign': self.get_kraken_signature(f'{self.api_v}{uri}', params)
            }

        url = f'{self.url}{self.api_v}{uri}'
        if method in ['GET', 'DELETE']:
            return self.check_response_data(requests.request(method=method, url=url, headers=headers, timeout=timeout), return_raw)
        elif do_json:
            return self.check_response_data(requests.request(method=method, url=url, headers=headers, json=params, timeout=timeout), return_raw)
        else:
            return self.check_response_data(requests.request(method=method, url=url, headers=headers, data=params, timeout=timeout), return_raw)

    def get_kraken_signature(self, urlpath: str, data: dict) -> str:
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self.__secret), 
                urlpath.encode() + hashlib.sha256((str(data['nonce']) + urllib.parse.urlencode(data)).encode()).digest(),
                hashlib.sha512
            ).digest()
        ).decode()

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
        if url: self.url = url
        elif self.sandbox: self.url = 'https://demo-futures.kraken.com'
        else: self.url = 'https://futures.kraken.com'
        
        self.__key = key
        self.__secret = secret
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

        headers = { 'User-Agent': 'python-kraken-sdk' }
        if auth:
            if not self.__key or self.__key == '' or not self.__secret or self.__secret == '': raise ValueError('Missing credentials')
            self.nonce = (self.nonce + 1) % 1
            nonce = str(int(time.time() * 1000)) + str(self.nonce).zfill(4)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Nonce': nonce,
                'APIKey': self.__key,
                'Authent': self.get_kraken_futures_signature(uri, queryString + postString, nonce)
            }

        if method in ['GET', 'DELETE']:
            return self.check_response_data(
                requests.request(
                    method=method,
                    url=f'{self.url}{uri}' if queryString == '' else f'{self.url}{uri}?{queryString}', 
                    headers=headers, 
                    timeout=timeout
                ), 
                return_raw
            )
        elif method == 'PUT':
            return self.check_response_data(
                requests.request(
                method=method, 
                url=f'{self.url}{uri}', 
                params=str.encode(queryString), 
                headers=headers, 
                timeout=timeout
                ), 
                return_raw
            )
        else:
            return self.check_response_data(
                requests.request(
                    method=method, 
                    url=f'{self.url}{uri}?{postString}', 
                    data=str.encode(postString), 
                    headers=headers, 
                    timeout=timeout
                ), return_raw
            )

    def get_kraken_futures_signature(self, endpoint: str, data: str, nonce: str) -> str:
        # https://github.com/CryptoFacilities/REST-v3-Python/blob/ee89b9b324335d5246e2f3da6b52485eb8391d50/cfRestApiV3.py#L295-L296
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