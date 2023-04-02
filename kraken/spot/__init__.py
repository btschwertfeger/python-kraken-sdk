#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger


"""Module that provides the Spot REST clients"""
from kraken.spot.funding import FundingClient
from kraken.spot.market import MarketClient
from kraken.spot.staking import StakingClient
from kraken.spot.trade import TradeClient
from kraken.spot.user import UserClient
from kraken.spot.websocket import KrakenSpotWSClientCl


class User(UserClient):
    """
    Class that implements the Kraken Spot User client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: "https://api.kraken.com")
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: False)
    :type sandbox: bool
    """


class Trade(TradeClient):
    """
    Class that implements the Kraken Trade Spot client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: ``False``)
    :type sandbox: bool
    """


class Market(MarketClient):
    """
    Class that implements the Kraken Spot Market client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: ``False``)
    :type sandbox: bool
    """


class Funding(FundingClient):
    """
    Class that implements the Spot Funding client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: ``False``)
    :type sandbox: bool
    """


class Staking(StakingClient):
    """
    Class that implements the Kraken Spot Stakung client

    :param key: Optional Spot API public key (default: ``""``)
    :type key: str
    :param secret: Optional Spot API secret key (default: ``""``)
    :type secret: str
    :param url: Optional url to access the Kraken API (default: https://api.kraken.com)
    :type url: str
    :param sandbox: Optional use of the sandbox (not supported so far, default: False)
    :type sandbox: bool
    """


class KrakenSpotWSClient(KrakenSpotWSClientCl):
    """
    Class to access public and (optional)
    private/authenticated websocket connection.

    This class holds up to two websocket connections, one private
    and one public.

    (see: https://docs.kraken.com/websockets/#overview)

    :param key: Optional - API Key for the Kraken Spot API (default: ``""``)
    :type key: str
    :param secret: Optional -  Secret API Key for the Kraken Spot API (default: ``""``)
    :type secret: str
    :param url: Set a specific/custom url to access the Kraken API
    :type url: str
    :param callback: Optional - callback function which receives the websocket messages (default: ``None``)
    :type callback: function | None
    :param beta: Use the Beta websocket channels (maybe not supported anymore, default: ``False``)
    :type beta: bool

    .. code-block:: python
        :linenos:
        :caption: Example

        import asyncio
        from kraken.spot import KrakenSpotWSClient

        async def main() -> None:
            class Bot(KrakenSpotWSClient):

                async def on_message(self, event: dict) -> None:
                    print(event)

            bot = Bot()         # unauthenticated
            auth_bot = Bot(     # authenticated
                key='kraken-api-key',
                secret='kraken-secret-key'
            )

            # ... now call for example subscribe and so on

            while True:
                await asyncio.sleep(6)

        if __name__ == '__main__':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                loop.close()
    """
