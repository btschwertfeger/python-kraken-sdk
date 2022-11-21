import os, sys
import asyncio
import logging
import logging.config
from dotenv import dotenv_values
from datetime import datetime

try:
    from kraken.futures.client import WsClient
    from kraken.futures.websocket.websocket import KrakenFuturesWSClient
except:
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    from kraken.futures.client import WsClient
    from kraken.futures.websocket.websocket import KrakenFuturesWSClient

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
    class Bot(KrakenFuturesWSClient):

        async def on_message(self, event) -> None:
            logging.info(event)
            if 'event' in event:
                topic = event['event']
                if topic == 'heartbeat': return
                elif topic == 'pong': return


    bot = Bot(WsClient(key=key, secret=secret))
    # print(bot.get_available_public_subscription_feeds())
    # print(bot.get_available_private_subscription_feeds())

    products = ['PI_XBTUSD']
    # _____PUBLIC_SUBS______
    # await bot.subscribe(feed='ticker', products=products, private=False)
    # await bot.subscribe(feed='book', products=products, private=False)
    # await bot.subscribe(feed='trade', products=products, private=False)
    # await bot.subscribe(feed='ticker_lite', products=products, private=False)
    # await bot.subscribe(feed='heartbeat', private=False)
    
    # _____PRIVATE_SUBS______
    await bot.subscribe(feed='fills', private=True)
    # await bot.subscribe(feed='open_positions', private=True)
    # await bot.subscribe(feed='open_orders', private=True)
    # await bot.subscribe(feed='deposits_withdrawals', private=True)
    # await bot.subscribe(feed='account_balances_and_margins', private=True)
    # await bot.subscribe(feed='account_log', private=True)
    # await bot.subscribe(feed='notifications_auth', private=True)

    while True: await asyncio.sleep(6)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
