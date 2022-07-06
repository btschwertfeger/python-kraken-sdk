import os, sys

sys.path.append('/Users/benjamin/repositories/Trading/')

import asyncio


from client import User, Market, Trade, Funding, Staking, WsClient
from dotenv import dotenv_values
from websocket.websocket import KrakenWsClient

async def main() -> None:

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

    class Bot():
        once=0
        def __init__(self):
            pass
        async def callback_method(self,event, ws_send_message_func=None, error=None) -> None:
            print(f'callback-method: {event}')
            if self.once == 0:
                once = 1
                try:
                    await ws_send_message_func(msg={
                        'event': 'addOrder',
                    }, private=True)
                except:
                    print('____')


    bot = Bot()

    wsClient_pub = await KrakenWsClient.create(
        client=wsClient,
        callback=bot.callback_method,
        private=False
    )
    #wsClient_priv = await KrakenWsClient.create(
    #    client=wsClient,
    #    callback=bot.callback_method,
    #    private=True
    #)


    #await wsClient_pub.subscribe(pair=['BTC/EUR'], subscription={ 'name': 'ticker' })
    while True:
        try:
            # some strategy
            pass

        except:
            pass

        await asyncio.sleep(6)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
