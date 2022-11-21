import asyncio
import json
import time
import websockets
from random import random
from uuid import uuid4
import logging
import traceback


class ConnectFuturesWebsocket:
    MAX_SEND_MESSAGE_RETRIES = 5
    MAX_RECONNECT_SECONDS = 60

    def __init__(self, client, endpoint: str, callback=None, private: bool=False, sandbox: bool=False):
        self._client = client
        self._ws_endpoint = endpoint
        self._callback = callback

        self._reconnect_num = 0

        self._last_challenge = None
        self._new_challenge = None
        self._challenge_ready = False

        self._connect_id = None

        self._private = private
        self._demo = sandbox

        self._socket = None
        self._subscriptions = []

        asyncio.ensure_future(self.run_forever(), loop=asyncio.get_running_loop())

        self.connected = False

    @property
    def subscriptions(self) -> list:
        return self._subscriptions

    @property
    def private(self) -> bool:
        return self._private

    async def _run(self, event: asyncio.Event):
        keep_alive = True
        self._new_challenge = None
        self._last_challenge = None

        async with websockets.connect(f'wss://{self._ws_endpoint}', ping_interval=30) as socket:
            logging.info(f'Websocket connected!')

            if self.private: self._client.websocket_priv = self
            else: self._client.websocket_pub = self

            self.connected = True
            self._socket = socket
            self._reconnect_num = 0

            while keep_alive:
                try:
                    _msg = await asyncio.wait_for(self._socket.recv(), timeout=15)
                except asyncio.TimeoutError:
                    # logging.exception('TimeoutError')
                    pass
                except asyncio.CancelledError:
                    logging.exception('CancelledError')
                    self._reconnect()
                else:
                    try:
                        msg = json.loads(_msg)
                        if msg.get('event', '') == 'challenge':
                            self._last_challenge = msg['message']
                            self._new_challenge = self._client._get_sign_challenge(self._last_challenge)
                            self._challenge_ready = True
                    except ValueError:
                        logger.warning(_msg)
                    else:
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
                        logging.warning('cancel ok.')
                    await self._callback({ 'ws-error': message })
            if exception_occur: break
        logging.warning('_reconnect over.')

    async def _recover_subscription_req_msg(self, event):
        logging.info(f'recover subscription {self._subscriptions} waiting')
        # await event.wait()
        # for sub in self._subscriptions:
        #     private = False
        #     if 'token' in sub['subscription']:
        #         sub['subscription']['token'] = self._ws_details['token']
        #         private = True
        #     await self.send_message(sub, private=private)
        #     logging.info(f'{sub} OK')

        # logging.info(f'recover subscription {self._subscriptions} done.')

    def _get_reconnect_wait(self, attempts):
        return round(random() * min(self.MAX_RECONNECT_SECONDS, (2 ** attempts) - 1) + 1)

    async def send_message(self, msg, private: bool=False, retry_count: int=0):
        logging.info(f'send_message (private: {private}; tries: {retry_count}): {msg}')
        if not self._socket: # if not connected
            if retry_count < self.MAX_SEND_MESSAGE_RETRIES:
                await asyncio.sleep(2)
                await self.send_message(msg, private=private, retry_count=retry_count + 1)
        else:
            if private:
                if not self._challenge_ready:
                   await self._check_challenge_ready()

                msg['api_key'] = self._client.key
                msg['original_challenge']: self._last_challenge
                msg['signed_challenge']: self._new_challenge
                await self._socket.send(json.dumps(msg))

            else: await self._socket.send(json.dumps(msg))

        pass
    
    async def _check_challenge_ready(self) -> None:
        await self._send_challenge_request()
        
        logging.info('Awaiting challenge...')
        while not self._challenge_ready: time.sleep(1)

    async def _send_challenge_request(self):
        await self._socket.send(json.dumps({
            'event': 'challenge',
            'api_key': self._client.key
        }))


class KrakenFuturesWSClient(object):

    PROD_ENV_URL = 'futures.kraken.com/ws/v1'
    # DEMO_ENV_URL = 'demo.futuers.kraken.com'

    def __init__(self, client, callback=None, sandbox: bool=False):
        self._callback = callback
        self._client = client
        
        self._pub_conn = ConnectFuturesWebsocket(
            client=self._client,
            endpoint=self.PROD_ENV_URL, #if not sandbox else BETA_ENV_URL,
            callback=self.on_message,
            private=False
        )

        # self._priv_conn = ConnectFuturesWebsocket(
        #      client=self._client,
        #      endpoint=self.PROD_ENV_URL, #if not sandbox else AUTH_BETA_ENV_URL,
        #      callback=self.on_message,
        #      private=True
        # )

    async def on_message(self, msg):
        ''' Call callback function or overload this'''
        if self._callback != None: await self._callback(msg)
        else:
            logging.warning('Received event but no callback is defined')
            print(msg)

    async def subscribe(self, 
        feed: str,
        products: [str]=None,
        private: bool=False, 
        **kwargs
    ) -> None:
        '''Subscribe to a channel'''

        message = { 'event': 'subscribe', 'feed': feed }
        if products: message['product_ids'] = products
            
        if private:
            logging.info(f'Subscribe private to {feed}')
            self._priv_conn._subscriptions.append(message)
            await self._priv_conn.send_message(message, private=private)
        else:
            logging.info(f'Subscribe public to {feed}')
            self._pub_conn._subscriptions.append(message)
            await self._pub_conn.send_message(message, private=private)

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
    def get_available_public_subscription_feeds() -> [str]:
        return [ 'trade', 'book', 'ticker', 'ticker_lite', 'heartbeat']

    @staticmethod
    def get_available_private_subscription_feeds() -> [str]:
        return [ 'fills', 'open_positions', 'open_orders', 'deposits_withdrawals', 'account_balances_and_margins', 'account_log', 'notifications_auth']
