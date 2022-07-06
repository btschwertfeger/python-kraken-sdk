import asyncio
import json
import time
import websockets
from random import random
from uuid import uuid4
import logging
import traceback

logger = logging.getLogger(__name__)

class ConnectWebsocket:
    MAX_RECONNECTS = 5
    MAX_RECONNECT_SECONDS = 60

    def __init__(self, client, endpoint, callback=None, private: bool=False, beta: bool=False):
        self._loop = asyncio.get_running_loop()
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
    def topics(self):
        return self._topics

    async def _run(self, event: asyncio.Event):
        keep_alive = True
        self._last_ping = time.time()  # record last ping
        self._ws_details = None
        self._ws_details = self._client.get_ws_token(self._private)
        logger.debug(self._ws_details)

        async with websockets.connect(f'wss://{self._ws_endpoint}', ping_interval=None) as socket:
            logger.info(f'Websocket connected!')
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
                    logger.exception('CancelledError')
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
        logger.info('Websocket start connect/reconnect')

        self._reconnect_num += 1
        reconnect_wait = self._get_reconnect_wait(self._reconnect_num)
        logger.info(f'asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self._reconnect_num}')
        await asyncio.sleep(reconnect_wait)
        logger.info(f'asyncio sleep ok')
        event = asyncio.Event()

        tasks = {
            asyncio.ensure_future(self._recover_topic_req_msg(event)): self._recover_topic_req_msg,
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
                    logger.warning(message)
                    for pt in pending:
                        logger.warning(f'pending {pt}')
                        try: pt.cancel()
                        except asyncio.CancelledError: logger.exception('CancelledError ')
                        logger.warning('cancel ok.')
                    await self._callback({ 'ws-error': message })
            if exception_occur: break
        logger.warning('_reconnect over.')

    async def _recover_topic_req_msg(self, event):
        logger.info(f'recover topic event {self._subscriptions} waiting')
        await event.wait()
        for sub in self._subscriptions:
            if 'token' in sub['subscription']:
                sub['subscription']['token'] = self._ws_details['token']
            await self.send_message(sub)
            logger.info(f'{sub} OK')

        logger.info(f'recover topic event {self._subscriptions} done.')

    def _get_reconnect_wait(self, attempts):
        expo = 2 ** attempts
        return round(random() * min(self.MAX_RECONNECT_SECONDS, expo - 1) + 1)

    def _get_ws_pingtimeout(self):
        return 10

    async def send_ping(self):
        msg = {
            'event': 'ping',
            'reqid': int(time.time() * 1000),
        }
        print(msg)
        await self._socket.send(json.dumps(msg))
        self._last_ping = time.time()

    async def send_message(self, msg, private: bool=False, response: bool=False, retry_count: int=0):
        if not self._socket:
            if retry_count < self.MAX_RECONNECTS:
                await asyncio.sleep(1)
                await self.send_message(msg, retry_count + 1)
        else:
            msg['reqid'] = int(time.time() * 1000)
            if private and 'subscription' in msg: msg['subscription']['token'] = self._ws_details['token']
            await self._socket.send(json.dumps(msg))



class KrakenWsClient:
    '''https://docs.kraken.com/websockets/#overview'''

    PROD_ENV_URL = 'ws.kraken.com'
    AUTH_PROD_ENV_URL = 'ws-auth.kraken.com'
    BETA_ENV_URL = 'beta-ws.kraken.com'
    AUTH_BETA_ENV_URL = 'beta-ws-auth.kraken.com'

    def __init__(self):
        self._callback = None
        self._conn = None
        self._loop = None
        self._client = None
        self._private = False
        self._topics = set()

    @classmethod
    async def create(cls, client, callback=None, private=False, beta=False):
        self = KrakenWsClient()
        self._client = client
        self._private = private

        self._callback = callback

        if private:
            if beta: self._ws_endpoint = self.AUTH_BETA_ENV_URL
            else: self._ws_endpoint = self.AUTH_PROD_ENV_URL
        else:
            if beta: self._ws_endpoint = self.BETA_ENV_URL
            else: self._ws_endpoint = self.PROD_ENV_URL

        self._conn = ConnectWebsocket(
            client=self._client,
            endpoint=self._ws_endpoint,
            callback=self._recv,
            private=private, beta=beta
        )
        return self

    async def _recv(self, msg):
        #if 'data' in msg or '' in msg:
        await self._callback(msg)

    async def subscribe(self, pair: [str]=None, subscription: dict=None, **kwargs) -> None:
        '''Subscribe to a channel'''

        payload = { 'event': 'subscribe' }
        if pair != None: payload['pair'] = pair
        if subscription != None: req_msg['subscription'] = subscription
        req_msg.update(kwargs)
        self._conn.subscriptions.append(payload)
        await self._conn.send_message(payload)

    async def unsubscribe(self, pair: [str]=None, subscription: dict=None, **kwargs) -> None:
        '''Unsubscribe from a topic'''

        payload = { 'event': 'unsubscribe' }
        if pair != None: payload['pair'] = pair
        if subscription != None: payload['subscription'] = subscription
        payload.update(kwargs)
        self._conn.topics.remove(payload)
        await self._conn.send_message(payload)



