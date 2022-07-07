import os, sys

sys.path.append('/Users/benjamin/repositories/Trading/')

import asyncio
import logging
import logging.config
from dotenv import dotenv_values
from datetime import datetime

from client import User, Market, Trade, Funding, Staking, WsClient
from websocket.websocket import KrakenWsClient


def myLogger(file_name):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S' # %I:%M:%S %p AM|PM format
    )
    logging.basicConfig(
        #filename=f'{LOG_DIR}/{file_name}.log',
        format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        filemode='w',
        level=logging.INFO
    )
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.INFO)
    # stream=sys.stdout is similar to normal print
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)
    log_obj.info('Logger object created successfully..')
    return log_obj



async def main() -> None:

    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    # logging.getLogger('asyncio').setLevel(logging.WARNING)
    # logging.getLogger('asyncio.coroutines').setLevel(logging.WARNING)
    # logging.getLogger('websockets.server').setLevel(logging.WARNING)
    # logging.getLogger('websockets.protocol').setLevel(logging.WARNING)
    logger_name = f'botLog_{datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")}'
    logger = myLogger(logger_name)

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

#     class Bot():
#         once=0
#         def __init__(self):
#             pass
#         async def callback_method(self, event, wsclient=None, error=None) -> None:
#             if 'event' in event and event['event'] == 'heartbeat': return
#             print(f'callback-method: {event}')
#             if self.once == 0:
#                 once = 1
#                 try:
#                     if False:
#                         response = await wsclient.create_order(
#                             ordertype='limit',
#                             side='buy',
#                             pair='DOT/EUR',
#                             price=5
#                         )
#                         print(response)
#                 except Exception as e:
#                     logging.error(e)


#     bot = Bot()

    # wsClient_pub = await KrakenWsClient.create(
    #     client=wsClient,
    #     callback=bot.callback_method,
    #     private=False
    # )
    # wsClient_priv = await KrakenWsClient.create(
    #     client=wsClient,
    #     callback=bot.callback_method,
    #     private=True
    # )


    # await wsClient_pub.subscribe(pair=['BTC/EUR'], subscription={ 'name': 'ticker' })

    class Bot2(KrakenWsClient):

        async def on_message(self, event) -> None:
            print('#####tRUE###')
            print(event)


    bot_pub = Bot2()
    await bot_pub.on_message('MESSAGE')
    bot_pub = await bot_pub.create(client=wsClient, private=False)
    await bot_pub.on_message('MESSAGE')
    await bot_pub.subscribe(pair=['DOT/EUR'], subscription={ 'name': 'ticker' })

    while True:
        try:
            # some strategy with bot
            pass

        except:
            pass

        await asyncio.sleep(6)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
