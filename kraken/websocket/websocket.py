import asyncio
import json
import time
import websockets
from random import random
from uuid import uuid4
import logging
import traceback


class ConnectWebsocket:
    MAX_RECONNECTS = 5
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

        asyncio.ensure_future(self.run_forever(), loop=asyncio.get_running_loop())

    @property
    def subscriptions(self) -> list:
        return self._subscriptions

    @property
    def private(self) -> bool:
        return self._private

    async def _run(self, event: asyncio.Event):
        keep_alive = True
        self._last_ping = time.time()
        self._ws_details = None
        self._ws_details = self._client.get_ws_token(self.private)
        logging.debug(self._ws_details)

        async with websockets.connect(f'wss://{self._ws_endpoint}', ping_interval=None) as socket:
            logging.info(f'Websocket connected!')

            if self.private: self._client.websocket_priv = self
            else: self._client.websocket_pub = self

            self._socket = socket
            self._reconnect_num = 0

            if not event.is_set():
                await self.send_ping()
                event.set()

            while keep_alive:
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
                        await self._callback(msg)

    async def run_forever(self):
        while True:
            await self._reconnect()

    async def _reconnect(self):
        logging.info('Websocket start connect/reconnect')

        self._reconnect_num += 1
        reconnect_wait = self._get_reconnect_wait(self._reconnect_num)
        logging.info(f'asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self._reconnect_num}')
        await asyncio.sleep(reconnect_wait)
        logging.info(f'asyncio sleep ok')
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
                    message = f'{task} got an exception {task.exception()}'
                    message += f'\nTRACEBACK: {traceback.format_exc()}'
                    logging.warning(message)
                    for pt in pending:
                        logging.warning(f'pending {pt}')
                        try: pt.cancel()
                        except asyncio.CancelledError: logging.exception('CancelledError ')
                        logging.warning('cancel ok.')
                    await self._callback({ 'ws-error': message })
            if exception_occur: break
        logging.warning('_reconnect over.')

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
        logging.info(f'send_message (private: {private}; tries: {retry_count}): {msg}')
        if not self._socket:
            if retry_count < self.MAX_RECONNECTS:
                await asyncio.sleep(1)
                await self.send_message(msg, private=private, retry_count=retry_count + 1)
        else:
            msg['reqid'] = int(time.time() * 1000)
            if private and 'subscription' in msg: msg['subscription']['token'] = self._ws_details['token']
            elif private: msg['token'] = self._ws_details['token']
            await self._socket.send(json.dumps(msg))


class KrakenWsClient(object):
    '''https://docs.kraken.com/websockets/#overview'''

    PROD_ENV_URL = 'ws.kraken.com'
    AUTH_PROD_ENV_URL = 'ws-auth.kraken.com'
    BETA_ENV_URL = 'beta-ws.kraken.com'
    AUTH_BETA_ENV_URL = 'beta-ws-auth.kraken.com'

    def __init__(self, client, callback=None, beta: bool=False):
        self._callback = callback
        self._client = client


        self._pub_conn = ConnectWebsocket(
            client=self._client,
            endpoint=self.PROD_ENV_URL if not beta else BETA_ENV_URL,
            callback=self.on_message,
            private=False
        )

        self._priv_conn = ConnectWebsocket(
             client=self._client,
             endpoint=self.AUTH_PROD_ENV_URL if not beta else AUTH_BETA_ENV_URL,
             callback=self.on_message,
             private=True
        )

    async def on_message(self, msg):
        ''' Call callback function or overload this'''
        if self._callback != None: await self._callback(msg)
        else:
            logging.warning('Received event but no callback is defined')
            print(msg)

    async def subscribe(self, private: bool=False, pair: [str]=None, subscription: dict=None, **kwargs) -> None:
        '''Subscribe to a channel'''

        payload = { 'event': 'subscribe' }
        if pair != None: payload['pair'] = pair
        if subscription != None: payload['subscription'] = subscription
        payload.update(kwargs)

        if private:
            self._priv_conn._subscriptions.append(payload)
            await self._priv_conn.send_message(payload, private=private)
        else:
            self._pub_conn._subscriptions.append(payload)
            await self._pub_conn.send_message(payload, private=private)

    async def unsubscribe(self, private: bool=False, pair: [str]=None, subscription: dict=None, **kwargs) -> None:
        '''Unsubscribe from a topic'''

        payload = { 'event': 'unsubscribe' }
        if pair != None: payload['pair'] = pair
        if subscription != None: payload['subscription'] = subscription
        payload.update(kwargs)
        if private:
            self._priv_conn._subscriptions.remove(payload)
            await self._priv_conn.send_message(payload, private=private)
        else:
            self._pub_conn._subscriptions.remove(payload)
            await self._pub_conn.send_message(payload, private=private)

    @staticmethod
    def get_available_subscriptions() -> [str]:
        '''https://docs.kraken.com/websockets/#message-subscribe'''
        return [ 'book', 'ohlc', 'openOrders', 'ownTrades', 'spread', 'ticker', 'trade', '*']
