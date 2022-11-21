import os, sys
import asyncio
import logging
import logging.config
from dotenv import dotenv_values
from datetime import datetime
import time

try:
    from kraken.spot.client import WsClient
    from kraken.spot.websocket.websocket import KrakenSpotWSClient
except:
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.spot.client import WsClient
    from kraken.spot.websocket.websocket import KrakenSpotWSClient

logging.basicConfig(
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filemode='w',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

async def main() -> None:

    key = dotenv_values('.env')['API_KEY']
    secret = dotenv_values('.env')['SECRET_KEY']

    # ___Custom_Trading_Bot______________
    class Bot(KrakenSpotWSClient):

        async def on_message(self, event) -> None:
            if 'event' in event:
                topic = event['event']
                if topic == 'heartbeat': return
                elif topic == 'pong': return

            print(event)
            # await self._client.create_order(
            #     ordertype='limit',
            #     side='buy',
            #     pair='BTC/EUR',
            #     price=20000,
            #     volume=1
            # )
            # ... it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient

    # ___Public_Websocket_Feed_____
    bot = Bot(WsClient()) # only use this one if you dont need private feeds
    # print(bot.public_sub_names) # list public subscription names
    
    await bot.subscribe(subscription={ 'name': 'ticker' }, pair=['XBT/EUR', 'DOT/EUR'])
    await bot.subscribe(subscription={ 'name': 'spread' }, pair=['XBT/EUR', 'DOT/EUR'])
    # await bot.subscribe(subscription={ 'name': 'book' }, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': 'book', 'depth': 25}, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': 'ohlc' }, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': 'ohlc', 'interval': 15}, pair=['XBT/EUR', 'DOT/EUR'])
    # await bot.subscribe(subscription={ 'name': 'trade' }, pair=['BTC/EUR'])
    # await bot.subscribe(subscription={ 'name': '*' } , pair=['BTC/EUR'])
    
    time.sleep(2) # wait because unsubscribing is faster than subscribing ... 
    await bot.unsubscribe(subscription={ 'name': 'ticker' }, pair=['XBT/EUR','DOT/EUR'])
    await bot.unsubscribe(subscription={ 'name': 'spread' }, pair=['XBT/EUR'])
    await bot.unsubscribe(subscription={ 'name': 'spread' }, pair=['DOT/EUR'])
    # ....

    auth_bot = Bot(WsClient(key=key, secret=secret))
    # print(auth_bot.private_sub_names) # list private subscription names
    # when using the authenticated bot, you can also subscribe to public feeds
    await auth_bot.subscribe(subscription={ 'name': 'ownTrades' })
    await auth_bot.subscribe(subscription={ 'name': 'openOrders' })
    
    time.sleep(2)
    await auth_bot.unsubscribe(subscription={ 'name': 'ownTrades' })
    await auth_bot.unsubscribe(subscription={ 'name': 'openOrders' },)   


    while True: 
        await asyncio.sleep(6)
        # display the active subscriptions ...
        # print(bot.active_public_subscriptions)

        # print(auth_bot.active_public_subscriptions)
        # print(auth_bot.active_private_subscriptions)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
