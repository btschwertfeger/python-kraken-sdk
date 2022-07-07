import os, sys

sys.path.append('/Users/benjamin/repositories/Trading/')

import asyncio
import logging
import logging.config
from dotenv import dotenv_values
from datetime import datetime

from client import User, Market, Trade, Funding, Staking, WsClient
from websocket.websocket import KrakenWsClient


# def myLogger(file_name):
logging.basicConfig(
    #filename=f'{LOG_DIR}/{file_name}.log',
    format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filemode='w',
    level=logging.INFO
)
logging.getLogger().setLevel(logging.INFO)
# screen_handler = logging.StreamHandler(stream=sys.stdout)
# screen_handler.setFormatter(logging.Formatter(
#     fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S' # %I:%M:%S %p AM|PM format
# ))
# logging.getLogger().addHandler(screen_handler)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

async def main() -> None:

    key = dotenv_values('.env')['API_KEY']
    secret = dotenv_values('.env')['SECRET_KEY']

    # ___User_________________________
    user = User(key=key, secret=secret)

    # print(market.get_assets(assets=['XBT']))
    # print(market.get_tradable_asset_pair(pair=['BTCEUR','DOTEUR']))
    # print(market.get_ticker(pair='BTCUSD'))
    # print(market.get_ohlc(pair='BTCUSD', interval=5))
    # print(market.get_order_book(pair='BTCUSDT', count=10))
    # print(market.get_recent_trades(pair='BTCUSDT'))
    # print(user.get_account_balance())
    # print(user.get_closed_orders())

    # ___Market___________________________
    market = Market(key=key, secret=secret)

    # ____Trade_________________________
    trade = Trade(key=key, secret=secret)

    # ____Funding___________________________
    funding = Funding(key=key, secret=secret)

    # ____Staking___________________________
    staking = Staking(key=key, secret=secret)

    # ____Websocket_Client____________________
    wsClient = WsClient(key=key, secret=secret)

    # print(wsClient.get_ws_token())


    # ___Trading_Bot_Integration______________

    class Bot(KrakenWsClient):

        async def on_message(self, event) -> None:
            if 'event' in event:
                topic = event['event']
                if topic == 'heartbeat': return
                elif topic == 'pong': return
            print(f'--->{event}')
                # await self._client.create_order(
                #     ordertype='limit',
                #     side='buy',
                #     pair='BTC/EUR',
                #     price=2,
                #     volume=100
                # )



    bot = Bot(wsClient)
    await bot.subscribe(pair=['BTC/EUR'], subscription={ 'name': 'ticker' }, private=False)

    while True:
        await asyncio.sleep(6)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
