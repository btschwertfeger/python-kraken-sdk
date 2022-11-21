import asyncio
import json
import time
import websockets
from random import random
from uuid import uuid4
import logging
import traceback
import copy

class ConnectSpotWebsocket:
    MAX_SEND_MESSAGE_RETRIES = 5
    MAX_RECONNECT_SECONDS = 60

    def __init__(self, client, endpoint: str, callback=None, private: bool=False, beta: bool=False):
        self._client = client
        self._ws_endpoint = endpoint
        self._callback = callback

        self._reconnect_num = 0
        self._ws_details = None
        self._connect_id = None

        self._private = private
        self._beta = beta

        self._last_ping = None
        self._socket = None
        self._subscriptions = []

        self._private = private

        asyncio.ensure_future(self.run_forever(), loop=asyncio.get_running_loop())

    @property
    def subscriptions(self) -> list:
        return self._subscriptions

    @property
    def private(self) -> bool:
        return self._private

    async def _run(self, event: asyncio.Event):
        self._last_ping = time.time()
        self._ws_details = None if not self._private else self._client.get_ws_token(self._private)
        
        logging.debug(self._ws_details)

        async with websockets.connect(f'wss://{self._ws_endpoint}', ping_interval=None) as socket:
            logging.info(f'Websocket connected!')

            if self.private: self._client.websocket_priv = self
            else: self._client.websocket_pub = self

            self.connected = True
            self._socket = socket

            if not event.is_set():
                await self.send_ping()
                event.set()

            while True:
                if time.time() - self._last_ping > self._get_ws_pingtimeout():
                    await self.send_ping()
                try:
                    _msg = await asyncio.wait_for(self._socket.recv(), timeout=15)
                except asyncio.TimeoutError:
                    await self.send_ping()
                except asyncio.CancelledError:
                    logging.exception('CancelledError')
                    await self._socket.ping()
                else:
                    try:
                        msg = json.loads(_msg)
                    except ValueError:
                        logger.warning(_msg)
                    else: 
                        if 'event' in msg:
                            if msg['event'] == 'subscriptionStatus' and 'status' in msg:
                                try:
                                    if msg['status'] == 'subscribed':
                                        sub = { 'subscription': msg['subscription'] }
                                        if 'pair' in msg: # public endpoint
                                            sub['pair'] = msg['pair'] 
                                        else: # private endpoint
                                            sub['subscription'] = { 'name': msg['subscription']['name']}
                                        self._subscriptions.append(sub)

                                    elif msg['status'] == 'unsubscribed': 
                                        sub = { 'subscription': msg['subscription'] }
                                        if 'pair' in msg: # public endpoint
                                            sub['pair'] = msg['pair']
                                        elif msg['subscription']['name']: # private endpoint
                                            sub['subscription'] = { 'name': msg['subscription']['name']}
                                        self._subscriptions.remove(sub)       

                                    elif msg['status'] == 'error': logging.warn(msg)
                                except AttributeError: pass
                        await self._callback(msg)

    async def run_forever(self):
        while True: await self._reconnect()

    async def _reconnect(self):
        logging.info('Websocket start connect/reconnect')

        self._reconnect_num += 1
        reconnect_wait = self._get_reconnect_wait(self._reconnect_num)
        logging.debug(f'asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self._reconnect_num}')
        await asyncio.sleep(reconnect_wait)
        logging.debug(f'asyncio sleep done')
        event = asyncio.Event()

        tasks = {
            asyncio.ensure_future(self._recover_subscription_req_msg(event)): self._recover_subscription_req_msg,
            asyncio.ensure_future(self._run(event)): self._run
        }

        while set(tasks.keys()):
            finished, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_EXCEPTION)
            exception_occur = False
            for task in finished:
                if task.exception():
                    exception_occur = True
                    message = f'{task} got an exception {task.exception()}\nTRACEBACK: {traceback.format_exc()}'
                    logging.warning(message)
                    for process in pending:
                        logging.warning(f'pending {process}')
                        try: process.cancel()
                        except asyncio.CancelledError: logging.exception('CancelledError')
                        logging.warning('cancel ok')
                    await self._callback({ 'ws-error': message })
            if exception_occur: break
        logging.warning('reconnect over')

    async def _recover_subscription_req_msg(self, event):
        logging.info(f'recover subscription {self._subscriptions} waiting')
        await event.wait()
        for sub in self._subscriptions:
            private = False
            if 'token' in sub['subscription']:
                sub['subscription']['token'] = self._ws_details['token']
                private = True
            await self.send_message(sub, private=private)
            logging.info(f'{sub} OK')

        logging.info(f'recover subscription {self._subscriptions} done.')

    def _get_reconnect_wait(self, attempts):
        return round(random() * min(self.MAX_RECONNECT_SECONDS, (2 ** attempts) - 1) + 1)

    def _get_ws_pingtimeout(self):
        '''TODO: add some good ping timeout'''
        return 10

    async def send_ping(self):
        msg = {
            'event': 'ping',
            'reqid': int(time.time() * 1000),
        }
        await self._socket.send(json.dumps(msg))
        self._last_ping = time.time()

    async def send_message(self, msg, private: bool=False, retry_count: int=0):
        while not self._socket: await asyncio.sleep(.4)

        if private and not self._private:
            raise ValueError('Cannot send private message with public websocket.')
        else:
            msg['reqid'] = int(time.time() * 1000)
            if private and 'subscription' in msg: msg['subscription']['token'] = self._ws_details['token']
            elif private: msg['token'] = self._ws_details['token']
            await self._socket.send(json.dumps(msg))


class KrakenSpotWSClient(object):
    '''https://docs.kraken.com/websockets/#overview'''

    PROD_ENV_URL = 'ws.kraken.com'
    AUTH_PROD_ENV_URL = 'ws-auth.kraken.com'
    BETA_ENV_URL = 'beta-ws.kraken.com'
    AUTH_BETA_ENV_URL = 'beta-ws-auth.kraken.com'

    def __init__(self, client, callback=None, beta: bool=False):
        self._callback = callback
        self._client = client

        self._isAuth = self._client.key and self._client.secret
        
        self._pub_conn = ConnectSpotWebsocket(
            client=self._client,
            endpoint=self.PROD_ENV_URL if not beta else BETA_ENV_URL,
            callback=self.on_message,
            private=False
        )

        self._priv_conn = ConnectSpotWebsocket(
             client=self._client,
             endpoint=self.AUTH_PROD_ENV_URL if not beta else AUTH_BETA_ENV_URL,
             callback=self.on_message,
             private=True
        ) if self._isAuth else None

    async def on_message(self, msg):
        ''' Call callback function or overload this'''
        if self._callback != None: await self._callback(msg)
        else:
            logging.warning('Received event but no callback is defined')
            print(msg)

    async def subscribe(self, subscription: dict, pair: [str]=None) -> None:
        '''Subscribe to a channel'''

        if 'name' not in subscription: raise AttributeError('Subscription requires a "name" key."')
        private = True if subscription['name'] in self.private_sub_names else False

        payload = { 
            'event': 'subscribe',
            'subscription': subscription
        }
        if pair != None: payload['pair'] = pair        
        if private: # private == without pair
            if not self._isAuth: raise ValueError('Cannot subscribe to private feeds without valid credentials!')
            elif pair != None: raise ValueError('Cannot subscribe to private endpoint with specific pair!')
            else: await self._priv_conn.send_message(payload, private=True)

        elif pair != None: # public with pair
            for p in pair:
                sub = copy.deepcopy(payload)
                sub['pair'] = [p]
                await self._pub_conn.send_message(sub, private=False)

        else: await self._pub_conn.send_message(payload, private=False)

    async def unsubscribe(self, subscription: dict, pair: [str]=None) -> None:
        '''Unsubscribe from a topic
            https://docs.kraken.com/websockets/#message-unsubscribe
        '''
        if 'name' not in subscription: raise AttributeError('Subscription requires a "name" key."')
        private = True if subscription['name'] in self.private_sub_names else False

        payload = { 
            'event': 'unsubscribe',
            'subscription': subscription
        }
        if pair != None: payload['pair'] = pair
        
        if private: # private == without pair
            if not self._isAuth: raise ValueError('Cannot unsubscribe from private feeds without valid credentials!')
            elif pair != None: raise ValueError('Cannot unsubscribe from private endpoint with specific pair!')
            else:
                sub = copy.deepcopy(payload)
                sub['event'] = 'subscribe'
                await self._priv_conn.send_message(payload, private=True)
                
        elif pair != None: # public with pair
            for p in pair:
                sub = copy.deepcopy(payload)
                sub['pair'] = [p]
                await self._pub_conn.send_message(sub, private=False)
                                
        else: await self._pub_conn.send_message(payload, private=False)

    @property
    def private_sub_names(self) -> [str]:
        return  ['ownTrades', 'openOrders']

    @property
    def public_sub_names(self) -> [str]:
        return ['ticker', 'spread', 'book', 'ohlc', 'trade', '*']

    @property
    def active_public_subscriptions(self) -> [dict]:
        return self._pub_conn._subscriptions

    @property
    def active_private_subscriptions(self) -> [str]:
        return self._priv_conn._subscriptions

