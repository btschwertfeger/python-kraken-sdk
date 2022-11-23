import os, sys, time
import asyncio
import logging, logging.config
from dotenv import dotenv_values
from datetime import datetime

try:
    # from kraken.futures.client import WsClient
    from kraken.futures.client import KrakenFuturesWSClient
    # from kraken.futures.websocket.websocket import KrakenFuturesWSClient
except:
    print('USING LOCAL MODULE')
    sys.path.append('/Users/benjamin/repositories/Trading/python-kraken-sdk')
    # from kraken.futures.client import WsClient
    from kraken.futures.client import KrakenFuturesWSClient
    # from kraken.futures.websocket.websocket import KrakenFuturesWSClient

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

    key = dotenv_values('.env')['Futures_API_KEY']
    secret = dotenv_values('.env')['Futures_SECRET_KEY']

    # ___Custom_Trading_Bot__________
    class Bot(KrakenFuturesWSClient):

        async def on_message(self, event) -> None:
            logging.info(event)
            # ... apply your trading strategy here
            # you can also combine this with the Futures REST clients

    # _____Public_Websocket_Feeds___________________
    bot = Bot()
    # print(bot.get_available_public_subscription_feeds())

    products = ['PI_XBTUSD']
    # subscribe to a public websocket feed
    await bot.subscribe(feed='ticker', products=products)
    # await bot.subscribe(feed='book', products=products)
    # await bot.subscribe(feed='trade', products=products)
    # await bot.subscribe(feed='ticker_lite', products=products)
    # await bot.subscribe(feed='heartbeat')

    # unsubscribe from a websocket feed
    time.sleep(2) # in case subscribe is not done yet
    await bot.unsubscribe(feed='ticker', products=products)
    # ....

    # _____Private_Websocket_Feeds_________________
    auth_bot = Bot(key=key, secret=secret)
    # print(auth_bot.get_available_private_subscription_feeds())

    # subscribe to a private/authenticated websocket feed
    await auth_bot.subscribe(feed='fills')
    # await auth_bot.subscribe(feed='open_positions')
    # await auth_bot.subscribe(feed='open_orders')
    # await auth_bot.subscribe(feed='open_orders_verbose')
    # await auth_bot.subscribe(feed='deposits_withdrawals')
    # await auth_bot.subscribe(feed='account_balances_and_margins')
    # await auth_bot.subscribe(feed='balances')
    # await auth_bot.subscribe(feed='account_log')
    # await auth_bot.subscribe(feed='notifications_auth')

    # authenticaed clients can also subscribe to public feeds
    # await auth_bot.subscribe(feed='ticker', products=['PI_XBTUSD', 'PF_ETHUSD'])

    time.sleep(1)
    # unsubscribe from a private/authenticaed websocket feed
    await auth_bot.unsubscribe(feed='fills')
    # ....

    while True: await asyncio.sleep(6)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        loop.close()
        # the websocket client will send {'event': 'ws-cancelled-error'} via on_message
        # so you can handle the behavior/next actions individually within you bot

    # old way will be deprecated in python 3.11:
    # asyncio.get_event_loop().run_until_complete(main())
