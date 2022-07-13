import os, sys

sys.path.append('/Users/benjamin/repositories/Trading/')

import asyncio
import logging
import logging.config
from dotenv import dotenv_values
from datetime import datetime

from kraken.client import WsClient
from kraken.websocket.websocket import KrakenWsClient

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
            # ... it is also possible to call regular REST endpoints
            # but using the websocket messages is more efficient

    bot = Bot(WsClient(key=key, secret=secret))
    await bot.subscribe(pair=['BTC/EUR'], subscription={ 'name': 'ticker' }, private=False)

    while True: await asyncio.sleep(6)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
