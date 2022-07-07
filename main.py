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
# logging.getLogger('asyncio').setLevel(logging.WARNING)
# logging.getLogger('asyncio.coroutines').setLevel(logging.WARNING)
# logging.getLogger('websockets.server').setLevel(logging.WARNING)
# logging.getLogger('websockets.protocol').setLevel(logging.WARNING)
logging.info('Logger object created successfully..')



async def main() -> None:
    # logger_name = f'botLog_{datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")}'
    # logger = myLogger(logger_name)

    key, secret = dotenv_values('.env')['API_KEY'], dotenv_values('.env')['SECRET_KEY']


    user = User(key=key, secret=secret)
    market = Market(key=key, secret=secret)
    trade = Trade(key=key, secret=secret)
    funding = Funding(key=key, secret=secret)
    staking = Staking(key=key, secret=secret)
    wsClient = WsClient(key=key, secret=secret)



    # ____User_____
    # print(market.get_assets(assets=['XBT']))
    # print(market.get_tradable_asset_pair(pair=['BTCEUR','DOTEUR']))
    # print(market.get_ticker(pair='BTCUSD'))
    # print(market.get_ohlc(pair='BTCUSD', interval=5))
    # print(market.get_order_book(pair='BTCUSDT', count=10))
    # print(market.get_recent_trades(pair='BTCUSDT'))
    # print(user.get_account_balance())
    # print(user.get_closed_orders())

    # ____Trade____

    # ____Funding__

    # ___Staking___

    # ___WS_Token__
    # print(wsClient.get_ws_token())

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
