import time
import asyncio
import websockets
from random import random
import logging
import traceback
import json
import sys
import copy

try:
    from kraken.futures.ws_client.ws_client import FuturesWsClientCl
    from kraken.exceptions.exceptions import KrakenExceptions 
except:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.futures.ws_client.ws_client import FuturesWsClientCl
    from kraken.exceptions.exceptions import KrakenExceptions 

class ConnectFuturesWebsocket(object):
    '''
        This class is only called by the KrakenFuturesWSClientCl class
        to establish and handle a websocket connection.

        ====== P A R A M E T E R S ======
        client: kraken.futures.client.KrakenFuturesWSClient
            the websocket client
        endpoint: str
            endpoint/url to connect with
        callback: function [optional], default=None
            callback function to call when a message is received
    '''

    MAX_RECONNECT_NUM = 2

    def __init__(self, client, endpoint: str, callback):
        self.__client = client
        self.__ws_endpoint = endpoint
        self.__callback = callback

        self.__reconnect_num = 0

        self.__last_challenge = None
        self.__new_challenge = None
        self.__challenge_ready = False

        self.__socket = None
        self.__subscriptions = []        
        
        self.__task = asyncio.ensure_future(
            self.__run_forever(), 
            loop=asyncio.get_running_loop()      
        )
    
    @property
    def subscriptions(self) -> list:
        return self.__subscriptions

    async def __run(self, event: asyncio.Event):
        keep_alive = True
        self.__new_challenge = None
        self.__last_challenge = None

        async with websockets.connect(f'wss://{self.__ws_endpoint}', ping_interval=30) as socket:
            logging.info(f'Websocket connected!')            
            self.__socket = socket

            if not event.is_set(): event.set()
            self.__reconnect_num = 0

            while keep_alive:
                try:
                    _msg = await asyncio.wait_for(self.__socket.recv(), timeout=15)
                except asyncio.TimeoutError:
                    pass
                except asyncio.CancelledError:
                    logging.exception('asyncio.CancelledError')
                    keep_alive = False    
                    await self.__callback({'event': 'asyncio.CancelledError'}) 
                else:
                    try:
                        msg = json.loads(_msg)
                    except ValueError:
                        logger.warning(_msg)
                    else:
                        forward = True
                        if 'event' in msg:
                            e = msg['event']
                            if e == 'challenge' and 'message' in msg:
                                forward = False
                                self.__handle_new_challenge(msg)                                
                            elif e == 'subscribed': self.__append_subscription(msg)
                            elif e == 'unsubscribed': self.__remove_subscription(msg)
                        if forward: await self.__callback(msg)

    async def __run_forever(self) -> None:
        try:
            while True: await self.__reconnect()
        except KrakenExceptions.MaxReconnectError: 
            await self.__callback({'event': 'KrakenExceptions.MaxReconnectError'})
        except Exception as e:
            # for task in asyncio.all_tasks(): task.cancel()
            logging.error(traceback.format_exc())
        # except asyncio.CancelledError: pass
        finally: self.__client.exception_occur = True

    async def __reconnect(self):
        logging.info('Websocket start connect/reconnect')

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            raise KrakenExceptions.MaxReconnectError()

        reconnect_wait = self.__get_reconnect_wait(self.__reconnect_num)
        logging.debug(f'asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self.__reconnect_num}')
        await asyncio.sleep(reconnect_wait)
        logging.debug(f'asyncio sleep done')
        event = asyncio.Event()

        tasks = {
            asyncio.ensure_future(self.__recover_subscription_req_msg(event)): self.__recover_subscription_req_msg,
            asyncio.ensure_future(self.__run(event)): self.__run
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
                    await self.__callback({ 'ws-error': message })
            if exception_occur: break            
        logging.warning('reconnect over')

    async def __recover_subscription_req_msg(self, event) -> None:
        logging.info(f'Recover subscriptions {self.__subscriptions} waiting.')
        await event.wait()
        
        for sub in self.__subscriptions:            
            if sub['feed'] in self.__client.get_available_private_subscription_feeds():
                await self.send_message(copy.deepcopy(sub), private=True)
            elif sub['feed'] in self.__client.get_available_public_subscription_feeds():
                await self.send_message(copy.deepcopy(sub), private=False)
            else: pass
            logging.info(f'{sub}: OK')

        logging.info(f'Recover subscriptions {self.__subscriptions} done.')

    async def send_message(self, msg: dict, private: bool=False) -> None:
        while not self.__socket: await asyncio.sleep(.4)
        
        if private:
            if not self.__client.isAuth:
                raise ValueError('Cannot access private endpoints with unauthenticated client!')
            elif not self.__challenge_ready: await self.__check_challenge_ready()

            msg['api_key'] = self.__client._key
            msg['original_challenge'] = self.__last_challenge
            msg['signed_challenge'] = self.__new_challenge
            
        await self.__socket.send(json.dumps(msg))

    def __handle_new_challenge(self, msg: dict) -> None:
        self.__last_challenge = msg['message']
        self.__new_challenge = self.__client._get_sign_challenge(self.__last_challenge)
        self.__challenge_ready = True

    async def __check_challenge_ready(self) -> None:
        await self.__socket.send(json.dumps({
            'event': 'challenge',
            'api_key': self.__client._key
        }))

        logging.debug('Awaiting challenge...')
        while not self.__challenge_ready: await asyncio.sleep(.1)

    def __get_reconnect_wait(self, attempts: int) -> float:
        return round(random() * min(60*3, (2 ** attempts) - 1) + 1)

    def __append_subscription(self, msg: dict) -> None:
        self.__remove_subscription(msg=msg) # remove from list, to avoid duplicates
        sub = self.__build_subscription(msg)
        self.__subscriptions.append(sub)

    def __remove_subscription(self, msg: dict) -> None:
        sub = self.__build_subscription(msg)
        self.__subscriptions = [x for x in self.__subscriptions if x != sub]

    def __build_subscription(self, subscription: dict) -> dict:
        sub = { 'event': 'subscribe' }

        if 'event' not in subscription                                        \
            or subscription['event'] not in ['subscribed', 'unsubscribed']    \
            or 'feed' not in subscription: 
            raise ValueError('Cannot append/remove subscription with missing attributes.')
        
        elif subscription['feed'] in self.__client.get_available_public_subscription_feeds(): # public subscribe
            if 'product_ids' in subscription:
                sub['product_ids'] = subscription['product_ids'] if type(subscription['product_ids']) == list else [subscription['product_ids']]
            sub['feed'] = subscription['feed']
        
        elif subscription['feed'] in self.__client.get_available_private_subscription_feeds(): # private subscription
            sub['feed'] = subscription['feed']
        else: logging.warn('Feed not implemented. Please contact the python-kraken-sdk package author.')
        return sub

    def get_active_subscriptions(self) -> [dict]:
        return self.__subscriptions


class KrakenFuturesWSClientCl(FuturesWsClientCl):
    '''https://docs.futures.kraken.com/#websocket-api
    
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
        sandbox: bool [optional], default=False
            use the Kraken Futures demo url

        ====== E X A M P L E ======
        import asyncio
        from kraken.futures.client import KrakenFuturesWSClient

        async def main() -> None:

            # ___Custom_Trading_Bot__________
            class Bot(KrakenFuturesWSClient):

                async def on_message(self, event) -> None:
                    print(event)

            bot = Bot() # unauthenticated 
            auth_bot = Bot(key=key, secret=secret) # authenticated

            # ... now call for example subscribe and so on

            while True: await asyncio.sleep(6)

        if __name__ == '__main__':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try: asyncio.run(main())
            except KeyboardInterrupt: loop.close()
    '''

    PROD_ENV_URL = 'futures.kraken.com/ws/v1'
    DEMO_ENV_URL = 'demo-futures.kraken.com/ws/v1'

    def __init__(self, key: str='', secret: str='', url: str='', callback=None, sandbox: bool=False): 
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

        self.exception_occur = False
        self.__callback = callback        
        self._conn = ConnectFuturesWebsocket(
            client=self,
            endpoint= url if url != '' else self.DEMO_ENV_URL if sandbox else self.PROD_ENV_URL,
            callback=self.on_message 
        )

    async def on_message(self, msg) -> None:
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
            loggin.info(msg)

    async def subscribe(self, feed: str, products: [str]=None) -> None:
        '''Subscribe to a channel/feed
            https://docs.futures.kraken.com/#websocket-api-websocket-api-introduction-subscriptions

            ====== P A R A M E T E R S ======
            subscription: dict
                the subscription to subscribe to
            products: [str]
                list of assets or list of a single product

            ====== E X A M P L E ======
            # ... initialize bot as documented on top of this class.
            await bot.subscribe(feed='ticker', products=["XBTUSD", "DOT/EUR"])

            ====== N O T E S ====== 
            Success or failures are sent over the websocket connection and can be  
            received via the on_message callback function.
        '''

        message = { 'event': 'subscribe', 'feed': feed }

        if products != None: 
            if type(products) != list: raise ValueError('Parameter products must be type of [str] (e.g. pair=["PI_XBTUSD"])')
            else: message['product_ids'] = products     
            
        if feed in self.get_available_private_subscription_feeds():
            if products != None: raise ValueError('There is no private feed that accepts products!')
            else: await self._conn.send_message(message, private=True)
        elif feed in self.get_available_public_subscription_feeds():
            if products != None:
                for product in products:
                    sub = copy.deepcopy(message)
                    sub['product_ids'] = [product]
                    await self._conn.send_message(sub, private=False)
            else: await self._conn.send_message(message, private=False)
        else: raise ValueError(f'Feed: {feed} not found. Not subscribing to it.')

    async def unsubscribe(self, feed: str, products: [str]=None) -> None:
        '''Unsubscribe from a topic/feed
            https://docs.futures.kraken.com/#websocket-api-websocket-api-introduction-subscriptions
        
            ====== P A R A M E T E R S ======
            subscription: dict
                the subscription to unsubscribe from
            products: [str]
                list of assets or list of a single product

            ====== E X A M P L E ======
            # ... initialize bot as documented on top of this class.
            bot.unsubscribe(feed='ticker', products=["XBTUSD", "DOT/EUR"])

            ====== N O T E S ====== 
            Success or failures are sent over the websocket connection and can be  
            received via the on_message callback function.
        '''

        message = { 'event': 'unsubscribe', 'feed': feed }

        if products != None: 
            if type(products) != list: raise ValueError('Parameter products must be type of [str] (e.g. pair=["PI_XBTUSD"])')
            else: message['product_ids'] = products     

        if feed in self.get_available_private_subscription_feeds():
            if products != None: raise ValueError('There is no private feed that accepts products!')
            else: await self._conn.send_message(message, private=True)
        elif feed in self.get_available_public_subscription_feeds():
            if products != None:
                for product in products:
                    sub = copy.deepcopy(message)
                    sub['product_ids'] = [product]
                    await self._conn.send_message(sub, private=False)                    
            else: await self._conn.send_message(message, private=False)
        else: raise ValueError(f'Feed: {feed} not found. Not unsubscribing it.')

    @staticmethod
    def get_available_public_subscription_feeds() -> [str]:
        return [ 'trade', 'book', 'ticker', 'ticker_lite', 'heartbeat']

    @staticmethod
    def get_available_private_subscription_feeds() -> [str]:
        return [ 
            'fills', 
            'open_positions', 'open_orders', 'open_orders_verbose',
            'balances', 
            'deposits_withdrawals', 'account_balances_and_margins', 
            'account_log', 'notifications_auth'
        ]

    @property
    def isAuth(self) -> bool:
        return self._key and self._secret

    def get_active_subscriptions(self) -> [dict]:
        return self._conn.get_active_subscriptions()