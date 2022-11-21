import asyncio
import json
import time
import websockets
from random import random
import logging
import traceback

class ConnectFuturesWebsocket:
    MAX_SEND_MESSAGE_RETRIES = 5
    MAX_RECONNECT_SECONDS = 60

    def __init__(self, client, endpoint: str, callback=None):
        self._client = client
        self._ws_endpoint = endpoint
        self._callback = callback

        self._reconnect_num = 0

        self._last_challenge = None
        self._new_challenge = None
        self._challenge_ready = False

        self._socket = None
        self._subscriptions = []

        asyncio.ensure_future(self.run_forever(), loop=asyncio.get_running_loop())

    @property
    def subscriptions(self) -> list:
        return self._subscriptions

    async def _run(self, event: asyncio.Event):
        self._new_challenge = None
        self._last_challenge = None

        async with websockets.connect(f'wss://{self._ws_endpoint}', ping_interval=30) as socket:
            logging.info(f'Websocket connected!')
            self._client.websocket = self
            self._socket = socket

            while True:
                try:
                    _msg = await asyncio.wait_for(self._socket.recv(), timeout=15)
                except asyncio.TimeoutError:
                    pass
                except asyncio.CancelledError:
                    logging.exception('CancelledError')
                    self._reconnect()
                else:
                    try:
                        msg = json.loads(_msg)
                    except ValueError:
                        logger.warning(_msg)
                    else:
                        if msg.get('event', '') == 'challenge':
                            self._last_challenge = msg['message']
                            self._new_challenge = self._client._get_sign_challenge(self._last_challenge)
                            self._challenge_ready = True
                        else: await self._callback(msg)

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

    async def _recover_subscription_req_msg(self, event) -> None:
        logging.info(f'Recover subscription {self._subscriptions} waiting.')
        await event.wait()

        for sub in self._subscriptions:
            if sub['feed'] in self._client.get_available_private_subscription_feeds():
                await self.send_message(message, private=True)
            elif sub['feed'] in self._client.get_available_public_subscription_feeds():
                await self.send_message(message, private=False)
            else: pass
            logging.info(f'{sub}: OK')

        logging.info(f'Recover subscription {self._subscriptions} done.')

    def _get_reconnect_wait(self, attempts: str) -> float:
        return round(random() * min(self.MAX_RECONNECT_SECONDS, (2 ** attempts) - 1) + 1)

    async def send_message(self, msg, private: bool=False, retry_count: int=0) -> None:
        while not self._socket: await asyncio.sleep(.4)
        
        if private:
            if not self._client.secret or not self._client.key:
                raise ValueError('Cannot access private endpoints with unauthenticated client!')
            elif not self._challenge_ready: await self._check_challenge_ready()

            msg['api_key'] = self._client.key
            msg['original_challenge'] = self._last_challenge
            msg['signed_challenge'] = self._new_challenge
            
        await self._socket.send(json.dumps(msg))

    async def _check_challenge_ready(self) -> None:
        await self._socket.send(json.dumps({
            'event': 'challenge',
            'api_key': self._client.key
        }))

        logging.debug('Awaiting challenge...')
        while not self._challenge_ready: await asyncio.sleep(.1)

class KrakenFuturesWSClient(object):

    PROD_ENV_URL = 'futures.kraken.com/ws/v1'

    def __init__(self, client, callback=None, url: str=''):
        self._callback = callback
        self._client = client
        
        self._conn = ConnectFuturesWebsocket(
            client=self._client,
            endpoint=self.PROD_ENV_URL if url == '' else url, 
            callback=self.on_message
        )

    async def on_message(self, msg) -> None:
        ''' Call callback function or overload this'''
        if self._callback != None: await self._callback(msg)
        else:
            logging.warning('Received event but no callback is defined')
            loggin.info(msg)

    async def subscribe(self, feed: str, products: [str]=None) -> None:
        '''Subscribe to a channel/feed'''

        message = { 'event': 'subscribe', 'feed': feed }
        if products: message['product_ids'] = products
            
        if feed in self.get_available_private_subscription_feeds():
            logging.info(f'Subscribe private to {feed}')
            await self._conn.send_message(message, private=True)
        elif feed in self.get_available_public_subscription_feeds():
            logging.info(f'Subscribe public to {feed}')
            await self._conn.send_message(message, private=False)
        else: raise ValueError(f'Feed: {feed} not found. Not subscribing to it.')
        self._conn._subscriptions.append(message)

    async def unsubscribe(self, feed: str, products: [str]=None) -> None:
        '''Unsubscribe from a topic/feed'''
        self._conn._subscriptions = [
            sub for sub in self._conn._subscriptions if sub['feed'] != feed
        ]

        message = { 'event': 'unsubscribe', 'feed': feed }
        if products: message['product_ids'] = products

        if feed in self.get_available_private_subscription_feeds():
            logging.info(f'Unsubscribe private from {feed}')
            await self._conn.send_message(message, private=True)
        elif feed in self.get_available_public_subscription_feeds():
            logging.info(f'Unsubscribe public from {feed}')
            await self._conn.send_message(message, private=False)
        else: raise ValueError(f'Feed: {feed} not found. Not unsubscribing it.')

    @staticmethod
    def get_available_public_subscription_feeds() -> [str]:
        return [ 'trade', 'book', 'ticker', 'ticker_lite', 'heartbeat']

    @staticmethod
    def get_available_private_subscription_feeds() -> [str]:
        return [ 
            'fills', 'open_positions', 'open_orders', 
            'deposits_withdrawals', 'account_balances_and_margins', 
            'account_log', 'notifications_auth'
        ]
