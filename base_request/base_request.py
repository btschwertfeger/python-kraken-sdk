#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import requests
import hmac
import hashlib
import base64
import time
from uuid import uuid1
import urllib.parse

__version__ = "v1.0.0"
version = __version__

class KrakenBaseRestAPI(object):

    def __init__(self, key='', secret='', url='', api_version=0):

        if url: self.url = url
        else: self.url = 'https://api.kraken.com'

        self.key = key
        self.secret = secret
        self.api_v = api_version

    def _request(self, method, uri, timeout=10, auth=True, params={}, do_json=False):
        uri_path = uri
        data_json = ''
        params['nonce'] = str(int(time.time()*1000)) # generate nonce

        if method.upper() in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append(f'{key}={params[key]}')
                data_json += '&'.join(strl)
                uri += f'?{data_json}'
                uri_path = uri
        else:
            if params:
                pass
                #data_json = json.dumps(params)
                #uri_path = f'{uri}{data_json}'

        headers = {}
        if auth:
            if not self.key or self.key == '' or not self.secret or self.secret == '': raise ValueError('Missing credentials')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'API-Key': self.key,
                'API-Sign': self.get_kraken_signature(f'/{self.api_v}{uri}', params)
            }

        headers['User-Agent'] = 'Kraken-Python-SDK'
        url = f'{self.url}/{self.api_v}{uri}'

        print(url)

        if method in ['GET', 'DELETE']:
            response_data = requests.request(method, url, headers=headers, timeout=timeout)
        else:
            if do_json:
                response_data = requests.request(method, url, headers=headers, json=params, timeout=timeout)
            else:
                response_data = requests.request(method, url, headers=headers, data=params, timeout=timeout)
        return self.check_response_data(response_data)

    def get_kraken_signature(self, urlpath, data):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    @staticmethod
    def check_response_data(response_data):
        if response_data.status_code == 200:
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)
            else:
                if len(data.get('error')) == 0:
                    if data.get('result'): return data['result']
                    else: return data
                else:
                    print(data)
                    raise Exception(f'{response_data.status_code}-{response_data.text}')
        else: raise Exception(f'{response_data.status_code}-{response_data.text}')

    @property
    def return_unique_id(self):
        return ''.join([each for each in str(uuid1()).split('-')])

    def _to_str_list(self, a) -> str:
        if type(a) == str: a = [a]
        return ','.join(a)
