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

    def __init__(self, key: str='', secret: str='', url: str='', futures: bool=False, sandbox: bool=False):
        self._futures = futures
        self._api_v = ''

        if url: self.url = url
        elif futures:
            if sandbox: self.url = 'https://demo-futures.kraken.com'
            else: self.url = 'https://futures.kraken.com'
            # raise ValueError('Futures endpoints and clients not implemented yet.')
        else:
            self.url = 'https://api.kraken.com'
            self._api_v = '/0'

        self.key = key
        self.secret = secret

    def _request(self, method: str, uri: str, timeout: int=10, auth: bool=True, params: dict={}, do_json: bool=False, return_raw: bool=False):
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
            if self._futures:
                nonce = self.get_nonce()

                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                    'APIKey': self.key,
                    'Nonce': nonce,
                    'Authent': self.get_kraken_futures_signature(uri.split('?')[0], urllib.parse.urlencode(params), nonce=nonce)
                }

            else:
                params['nonce'] = self.get_nonce()
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                    'API-Key': self.key,
                    'API-Sign': self.get_kraken_signature(f'{self._api_v}{uri}', params)
                }

        headers['User-Agent'] = 'Kraken-Python-SDK'
        url = f'{self.url}{self._api_v}{uri}'

        # logging.info(f'Request: {url}')

        if method in ['GET', 'DELETE']:
            return self.check_response_data(requests.request(method, url, headers=headers, timeout=timeout), return_raw)
        else:
            if do_json:
                return self.check_response_data(requests.request(method, url, headers=headers, json=params, timeout=timeout), return_raw)
            else:
                return self.check_response_data(requests.request(method, url, headers=headers, data=params, timeout=timeout), return_raw)

    def get_kraken_signature(self, urlpath: str, data: dict):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def get_kraken_futures_signature(self, endpoint: str, post_data: str, nonce: str=''):
        '''https://support.kraken.com/hc/en-us/articles/360022635592-Generate-authentication-strings-REST-API-'''
        if endpoint.startswith('/derivatives'): endpoint = endpoint[len('/derivatives'):]
        message = post_data + nonce + endpoint

        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode('utf8'))
        hash_digest = sha256_hash.digest()

        secretDecoded = base64.b64decode(self.secret)
        hmac_digest = hmac.new(secretDecoded, hash_digest, hashlib.sha512).digest()

        return base64.b64encode(hmac_digest)

    @staticmethod
    def get_nonce():
        return str(int(time.time()*1000))

    @staticmethod
    def check_response_data(response_data, return_raw: bool=False):
        if response_data.status_code == 200:
            if return_raw: return response_data
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)
            else:
                if 'error' in data:
                    if len(data.get('error')) == 0 and data.get('result'): return data['result']
                    else: raise Exception(f'{response_data.status_code}-{response_data.text}')
                else: return data
        else: raise Exception(f'{response_data.status_code}-{response_data.text}')

    @property
    def return_unique_id(self):
        return ''.join([each for each in str(uuid1()).split('-')])

    def _to_str_list(self, a) -> str:
        if type(a) == str: a = [a]
        return ','.join(a)
