import os, sys

sys.path.append('/Users/benjamin/repositories/Trading/')

import asyncio
import logging
import logging.config
from dotenv import dotenv_values
from datetime import datetime

from client import User, Market, Trade, Funding, Staking, WsClient
from websocket.websocket import KrakenWsClient


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

    # ---- R E S T - E N D P O I N T S ----

    # ___User_________________________
    user = User(key=key, secret=secret)

    # print(user.get_account_balance())
    # print(user.get_trade_balance())#asset='BTC'
    # print(user.get_open_orders())
    # print(user.get_closed_orders())
    # print(user.get_orders_info(txid='someid')) # or txid='id1,id2,id3' or txid=['id1','id2']
    # print(user.get_trades_history())
    # print(user.get_trades_info(txid='someid'))
    # print(user.get_open_positions())#txid='someid'
    # print(user.get_ledgers_info())#asset='BTC' or asset='BTC,EUR' or asset=['BTC','EUR']
    # print(user.get_ledgers(id='LNBK7T-BLEFU-C6NGIS'))
    # print(user.get_trade_volume())#pair='BTC/EUR'

    #____export_report____
    # print(user.request_export_report(report='ledgers', description='myLedgers1', format='CSV'))#report='trades'
    # print(user.get_export_report_status(report='ledgers'))

    # save report to file
    # response_data = user.retrieve_export(id='INSG')
    # handle = open('myexport.zip', 'wb')
    # for chunk in response_data.iter_content(chunk_size=512):
    #     if chunk: handle.write(chunk)
    # handle.close()

    #print(user.delete_export_report(id='INSG', type='delete'))#type=cancel


    # ___Market___________________________
    market = Market(key=key, secret=secret)

    # print(market.get_assets(assets=['XBT']))
    # print(market.get_tradable_asset_pair(pair=['BTCEUR','DOTEUR']))
    # print(market.get_ticker(pair='BTCUSD'))
    # print(market.get_ohlc(pair='BTCUSD', interval=5))
    # print(market.get_order_book(pair='BTCUSDT', count=10))
    # print(market.get_recent_trades(pair='BTCUSDT'))


    # ____Trade_________________________
    trade = Trade(key=key, secret=secret)


    # ____Funding___________________________
    funding = Funding(key=key, secret=secret)


    # ____Staking___________________________
    staking = Staking(key=key, secret=secret)


    # ____Websocket_Client____________________
    wsClient = WsClient(key=key, secret=secret)

    # print(wsClient.get_ws_token())


    # ---- W E B S O C K E T - S T U F F ----
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
                #     price=20000,
                #     volume=1
                # )



    # bot = Bot(wsClient)
    # await bot.subscribe(pair=['BTC/EUR'], subscription={ 'name': 'ticker' }, private=False)

    # while True:
    #     await asyncio.sleep(6)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
