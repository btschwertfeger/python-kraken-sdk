import os, sys, time
import asyncio
import logging, logging.config
from dotenv import dotenv_values
from datetime import datetime
import traceback
import urllib3
import requests 

try:
    from kraken.futures.client import KrakenFuturesWSClient
    from kraken.exceptions.exceptions import KrakenExceptions
    from kraken.futures.client import User, Market, Trade, Funding
except:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.futures.client import KrakenFuturesWSClient
    from kraken.exceptions.exceptions import KrakenExceptions
    from kraken.futures.client import User, Market, Trade, Funding

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filemode='w',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

class TradingBot(KrakenFuturesWSClient):
    '''
        Class that implements the trading strategy

        > The on_message function gets all events via the websocket connection
        > decisions can be made based on these events
        > for example placing trades using the self.__trade client
        > do everything you want

        ====== P A R A M E T E R S ======
        config: dict
            bot configuration like: {
                'key' 'kraken-futures-key', 
                'secret': 'kraken-secret-key',
                'products': ['PI_XBTUSD]'
            }
    '''

    def __init__(self, config: dict): 
        super().__init__(key=config['key'], secret=config['secret']) # initialize the KakenFuturesWSClient
        self.__config = config

        self.__user = User(key=config['key'], secret=config['secret'])
        self.__trade = Trade(key=config['key'], secret=config['secret'])
        self.__market = Market(key=config['key'], secret=config['secret'])
        self.__funding = Funding(key=config['key'], secret=config['secret'])

    async def on_message(self, event) -> None:
        logging.info(event)
        # ... apply your trading strategy here
        # call functions of self.__trade and other clients if conditions met... 

    # add more functions to customize the bot/strategy
    # ... 
    # ... 

    def save_exit(self, reason: str='') -> None:
        '''controlled shutdown of the bot'''
        logging.warn(f'Save exit triggered, reason: {reason}')
        # save data ... 
        # maybe close trades ...
        exit(1)


class ManagedBot(object):
    '''Class to manage the trading strategy/strategies

    subscribes to desired feeds, instantiates the strategy and runs until condition met

    ====== P A R A M E T E R S ======
    config: dict
        bot configuration like: {
            'key' 'kraken-futures-key', 
            'secret': 'kraken-secret-key',
            'products': ['PI_XBTUSD]'
        }
    '''

    def __init__(self, config: dict):
        self.__config = config
        self.__tratingStrategy = None
        
    def run(self) -> None:
        if not self.__check_credentials(): exit(1)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            asyncio.run(self.__main())
        except KeyboardInterrupt: pass
        finally: 
            loop.close()
            if self.__tratingStrategy != None:
                self.__tradingStrategy.save_exit(reason='Asyncio loop left')

    async def __main(self) -> None:
        self.__tratingStrategy = TradingBot(config=self.__config)

        await self.__tratingStrategy.subscribe(feed='ticker', products=self.__config['products'])
        await self.__tratingStrategy.subscribe(feed='book', products=self.__config['products'])

        await self.__tratingStrategy.subscribe(feed='fills')
        await self.__tratingStrategy.subscribe(feed='open_positions')
        await self.__tratingStrategy.subscribe(feed='open_orders')
        await self.__tratingStrategy.subscribe(feed='balances')       

        while not self.__tratingStrategy.exception_occur: 
            try:
                # check if bot feels good
                # maybe send a status update every day
                # ...
                pass

            except Exception as e:
                message = f'Exception in main: {e} {traceback.format_exc()}'
                logging.error(message)
                self.__tratingStrategy.save_exit(reason=message)
            
            await asyncio.sleep(6)
        self.__tratingStrategy.save_exit(reason='Left main loop because of exception in bot.')
        return

    def __check_credentials(self) -> bool:
        '''Checks the user credentials and the connection to Kraken'''
        try:
            User(self.__config['key'], self.__config['secret']).get_wallets()
            logging.info('Client credentials are valid')
            return True
        except urllib3.exceptions.MaxRetryError:
            logging.error('MaxRetryError, cannot connect.')
            return False
        except requests.exceptions.ConnectionError:
            logging.error('ConnectionError, Kraken not available.')
            return False
        except KrakenExceptions.KrakenAuthenticationError:
            logging.error('Invalid credentials!')
            return False

    def save_exit(self, reason: str='') -> None:
        self.__tratingStrategy.save_exit()

def main() -> None:
    bot_config = {
        'key': dotenv_values('.env')['Futures_API_KEY'],
        'secret': dotenv_values('.env')['Futures_SECRET_KEY'],
        'products': ['PI_XBTUSD', 'PF_SOLUSD']
    }
    managedBot = ManagedBot(config=bot_config)
    try:    
        managedBot.run()
    except Exception:
        managedBot.save_exit(reason=f'manageBot.run() has ended: {traceback.format_exc()}')

if __name__ == '__main__': 
    main()