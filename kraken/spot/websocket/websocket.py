import json
import time
import asyncio
import websockets
from random import random
from uuid import uuid4
import logging
import traceback
import copy

try:
    from kraken.spot.ws_client.ws_client import SpotWsClientCl
except:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.spot.client.ws_client import SpotWsClientCl

class ConnectSpotWebsocket:
    '''
        This class is only called by the KrakenSpotWSClient class
        to establish and handle a websocket connection.

        ====== P A R A M E T E R S ======
        client: kraken.spot.client.KrakenSpotWSClient
            the websocket client
        endpoint: str
            endpoint/url to connect with
        callback: function [optional], default=None
            callback function to call when a message is received
        private: bool [optional], default=False
            if client is authenticated to send signed messages
            and get private feeds

        ====== E X A M P L E ======
    '''

    def __init__(self, client, endpoint: str, callback, isAuth: bool=False):
        self.__client = client
        self.__ws_endpoint = endpoint
        self.__callback = callback 

        self.__reconnect_num = 0
        self.__ws_conn_details = None

        self.__isAuth = isAuth

        self.__last_ping = None
        self.__socket = None
        self.__subscriptions = []

        asyncio.ensure_future(self.run_forever(), loop=asyncio.get_running_loop())

    @property
    def subscriptions(self) -> list:
        return self.__subscriptions

    @property
    def isAuth(self) -> bool:
        return self.__isAuth

    async def _run(self, event: asyncio.Event):
        self.__last_ping = time.time()
        self.__ws_conn_details = None if not self.__isAuth else self.__client.get_ws_token()
        keep_alive = True
        logging.debug(f'Websocket token: {self.__ws_conn_details}')

        async with websockets.connect(f'wss://{self.__ws_endpoint}', ping_interval=None) as socket:
            logging.info(f'Websocket connected!')

            self.__socket = socket

            if not event.is_set():
                await self.send_ping()
                event.set()

            while keep_alive:
                if time.time() - self.__last_ping > 10: await self.send_ping()
                try:
                    _msg = await asyncio.wait_for(self.__socket.recv(), timeout=15)
                except asyncio.TimeoutError:
                    await self.send_ping()
                except asyncio.CancelledError:
                    logging.exception('asyncio.CancelledError')
                    keep_alive = False
                    await self.__callback({'event': 'ws-cancelled-error'})
                else:
                    try:
                        msg = json.loads(_msg)
                    except ValueError:
                        logger.warning(_msg)
                    else: 
                        if 'event' in msg:
                            if msg['event'] == 'subscriptionStatus' and 'status' in msg:
                                # remove/assign un/subscriptions
                                try:
                                    if msg['status'] == 'subscribed':
                                        sub = { 'subscription': msg['subscription'] }
                                        if 'pair' in msg: # public endpoint
                                            sub['pair'] = msg['pair'] 
                                        else: # private endpoint
                                            sub['subscription'] = { 'name': msg['subscription']['name']}
                                        self.__subscriptions.append(sub)

                                    elif msg['status'] == 'unsubscribed': 
                                        sub = { 'subscription': msg['subscription'] }
                                        if 'pair' in msg: # public endpoint
                                            sub['pair'] = msg['pair']
                                        elif msg['subscription']['name']: # private endpoint
                                            sub['subscription'] = { 'name': msg['subscription']['name']}
                                        self.__subscriptions.remove(sub)       

                                    elif msg['status'] == 'error': logging.warn(msg)
                                except AttributeError: pass
                        await self.__callback(msg)

    async def run_forever(self):
        while True: await self._reconnect()

    async def _reconnect(self):
        logging.info('Websocket start connect/reconnect')

        self.__reconnect_num += 1
        reconnect_wait = round(random() * min(60, (2 ** self.__reconnect_num) - 1) + 1) 
        logging.debug(f'asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self.__reconnect_num}')
        await asyncio.sleep(reconnect_wait)
        logging.debug(f'asyncio sleep done')
        event = asyncio.Event()

        tasks = {
            asyncio.ensure_future(self._recover_subscriptions(event)): self._recover_subscriptions,
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
                        except asyncio.CancelledError: logging.exception('asyncio.CancelledError')
                        logging.warning('Cancel OK')
                    await self.__callback({ 'ws-error': message })
            if exception_occur: break
        logging.warning('reconnect over')

    async def _recover_subscriptions(self, event):
        logging.info(f'Recover subscriptions {self.__subscriptions} waiting.')
        await event.wait()
        for sub in self.__subscriptions:
            private = False
            if 'token' in sub['subscription']:
                sub['subscription']['token'] = self.__ws_conn_details['token']
                private = True
            await self.send_message(sub, private=private)
            logging.info(f'{sub} OK')

        logging.info(f'Recovering subscriptions {self.__subscriptions} done.')

    async def send_ping(self):
        msg = {
            'event': 'ping',
            'reqid': int(time.time() * 1000),
        }
        await self.__socket.send(json.dumps(msg))
        self.__last_ping = time.time()

    async def send_message(self, msg, private: bool=False, retry_count: int=0):
        while not self.__socket: await asyncio.sleep(.4)

        if private and not self.__isAuth:
            raise ValueError('Cannot send private message with public websocket.')
        else:
            msg['reqid'] = int(time.time() * 1000)
            if private and 'subscription' in msg: msg['subscription']['token'] = self.__ws_conn_details['token']
            elif private: msg['token'] = self.__ws_conn_details['token']
            await self.__socket.send(json.dumps(msg))


class KrakenSpotWSClientCl(SpotWsClientCl):
    '''https://docs.kraken.com/websockets/#overview
    
        Class to access public and (optional) 
        private/authenticated websocket connection.

        ====== P A R A M E T E R S ======
        key: str, [optional], default: ''
            API Key for the Kraken API
        secret: str, [optional], default: ''
            Secret API Key for the Kraken API
        url: str, [optional], default: ''
            Set a specific/custom url
        callback: async function [optional], default=None
            callback function which receives the websocket messages
        beta: bool [optional], default=False
            use the Kraken beta url

        ====== P R O P E R T I E S ======
        public_sub_names: [str]
            list of available public subscription names
        private_sub_names: [str]
            list of available private subscription names
        active_public_subscriptions: [dict]
            list of active public subscriptions
        active_private_subscriptions: [dict]
            list of active private subscriptions

        ====== E X A M P L E ======
        import asyncio
        from kraken.spot.client import KrakenSpotWSClient

        async def main() -> None:
            class Bot(KrakenSpotWSClient):

                async def on_message(self, event) -> None:
                    print(event)
            
            bot = Bot() # unauthenticated client
            auth_bot = Bot(key='kraken-api-key', secret='kraken-secret-key')
            
            # ... now call for example subscribe and so on

            while True: await asyncio.sleep(6)

        if __name__ == '__main__':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try: asyncio.run(main())
            except KeyboardInterrupt: loop.close()
    '''

    PROD_ENV_URL = 'ws.kraken.com'
    AUTH_PROD_ENV_URL = 'ws-auth.kraken.com'
    BETA_ENV_URL = 'beta-ws.kraken.com'
    AUTH_BETA_ENV_URL = 'beta-ws-auth.kraken.com'

    def __init__(self, key: str='', secret: str='', url: str='', callback=None, beta: bool=False) -> None:
        super().__init__(key=key, secret=secret, sandbox=beta)
        self.__callback = callback
        self.__isAuth = key and secret        
       
        self._pub_conn = ConnectSpotWebsocket(
            client=self,
            endpoint=self.PROD_ENV_URL if not beta else BETA_ENV_URL,
            isAuth=False,
            callback=self.on_message
        )

        self._priv_conn = ConnectSpotWebsocket(
             client=self,
             endpoint=self.AUTH_PROD_ENV_URL if not beta else AUTH_BETA_ENV_URL,
             isAuth=True,
             callback=self.on_message
        ) if self.__isAuth else None

    async def on_message(self, msg: dict):
        ''' Calls the defined callback function (if defined) 
            or overload this function
            
            ====== P A R A M E T E R S ======
            msg: dict
                message received from Kraken via the websocket connection

            ====== N O T E S ======
            Can be overloaded like in the documentation of this class.
        '''
        if self.__callback != None: await self.__callback(msg)
        else:
            logging.warning('Received event but no callback is defined')
            print(msg)

    async def subscribe(self, subscription: dict, pair: [str]=None) -> None:
        '''Subscribe to a channel
            https://docs.kraken.com/websockets-beta/#message-subscribe
            
            ====== P A R A M E T E R S ======
            subscription: dict
                the subscription to subscribe to
            pair: [str]
                list of asset pairs or list of a single pair

            ====== E X A M P L E ======
            # ... initialize bot as documented on top of this class.
            bot.subscribe(subscription={"name": ticker}, pair=["XBTUSD", "DOT/EUR"])

            ====== N O T E S ====== 
            Success or failures are sent over the websocket connection and can be  
            received via the on_message callback function.
        '''

        if 'name' not in subscription: raise AttributeError('Subscription requires a "name" key."')
        private = True if subscription['name'] in self.private_sub_names else False

        payload = { 
            'event': 'subscribe',
            'subscription': subscription
        }
        if pair != None: 
            if type(pair) != list: raise ValueError('Parameter pair must be type of [str] (e.g. pair=["XBTUSD"])')
            else: payload['pair'] = pair        

        if private: # private == without pair
            if not self.__isAuth: raise ValueError('Cannot subscribe to private feeds without valid credentials!')
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

            ====== P A R A M E T E R S ======
            subscription: dict
                the subscription to unsubscribe from
            pair: [str]
                list of asset pairs or list of a single pair

            ====== E X A M P L E ======
            # ... initialize bot as documented on top of this class.
            bot.unsubscribe(subscription={"name": ticker}, pair=["XBTUSD", "DOT/EUR"])

            ====== N O T E S ====== 
            Success or failures are sent over the websocket connection and can be  
            received via the on_message callback function.
        '''
        if 'name' not in subscription: raise AttributeError('Subscription requires a "name" key."')
        private = True if subscription['name'] in self.private_sub_names else False

        payload = { 
            'event': 'unsubscribe',
            'subscription': subscription
        }
        if pair != None: 
            if type(pair) != list: raise ValueError('Parameter pair must be type of [str] (e.g. pair=["XBTUSD"])')
            else: payload['pair'] = pair
        
        if private: # private == without pair
            if not self.__isAuth: raise ValueError('Cannot unsubscribe from private feeds without valid credentials!')
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
        if self._pub_conn != None:
            return self._pub_conn.subscriptions 
        else: return []

    @property
    def active_private_subscriptions(self) -> [str]:
        if self._priv_conn != None:
            return self._priv_conn.subscriptions
        else: return []


