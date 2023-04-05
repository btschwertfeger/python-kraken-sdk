#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Futures websocket client"""
import asyncio
import json
import logging
import traceback
from copy import deepcopy
from random import random
from typing import List

import websockets

from kraken.exceptions import KrakenExceptions


class ConnectFuturesWebsocket:
    """
    This class is only called by the :class:`kraken.futures.KrakenFuturesWSClient`
    to establish the websocket connection.

    :param client: The Futures websocket client that instantiates this class
    :type client: :class:`kraken.futures.KrakenFuturesWSClient`
    :param endpoint: The endpoint to access (either the live Kraken API or the sandbox environment)
    :type endpoint: str
    :param callback: The function that is used to receive the message objects
    :type callback: function
    """

    MAX_RECONNECT_NUM = 2

    def __init__(self, client, endpoint: str, callback):
        self.__client = client
        self.__ws_endpoint = endpoint
        self.__callback = callback

        self.__reconnect_num = 0

        self.__last_challenge = None
        self.__new_challenge = None
        self.__challenge_ready = False

        self.__socket = None
        self.__subscriptions = []

        asyncio.ensure_future(self.__run_forever(), loop=asyncio.get_running_loop())

    @property
    def subscriptions(self) -> list:
        """Returns the active subscriptions"""
        return self.__subscriptions

    async def __run(self, event: asyncio.Event):
        keep_alive = True
        self.__new_challenge = None
        self.__last_challenge = None

        async with websockets.connect(
            f"wss://{self.__ws_endpoint}", ping_interval=30
        ) as socket:
            logging.info("Websocket connected!")
            self.__socket = socket

            if not event.is_set():
                event.set()
            self.__reconnect_num = 0

            while keep_alive:
                try:
                    _msg = await asyncio.wait_for(self.__socket.recv(), timeout=15)
                except asyncio.TimeoutError:
                    pass  # important
                except asyncio.CancelledError:
                    logging.exception("asyncio.CancelledError")
                    keep_alive = False
                    await self.__callback({"error": "asyncio.CancelledError"})
                else:
                    try:
                        msg = json.loads(_msg)
                    except ValueError:
                        logging.warning(_msg)
                    else:
                        forward = True
                        if "event" in msg:
                            _event = msg["event"]
                            if _event == "challenge" and "message" in msg:
                                forward = False
                                self.__handle_new_challenge(msg)
                            elif _event == "subscribed":
                                self.__append_subscription(msg)
                            elif _event == "unsubscribed":
                                self.__remove_subscription(msg)
                        if forward:
                            await self.__callback(msg)

    async def __run_forever(self) -> None:
        try:
            while True:
                await self.__reconnect()
        except KrakenExceptions.MaxReconnectError:
            await self.__callback(
                {
                    "error": "kraken.exceptions.exceptions.KrakenExceptions.MaxReconnectError"
                }
            )
        except Exception:
            # for task in asyncio.all_tasks(): task.cancel()
            logging.error(traceback.format_exc())
        # except asyncio.CancelledError: pass
        finally:
            self.__client.exception_occur = True

    async def __reconnect(self):
        logging.info("Websocket start connect/reconnect")

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            raise KrakenExceptions.MaxReconnectError()

        reconnect_wait = self.__get_reconnect_wait(self.__reconnect_num)
        logging.debug(
            f"asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self.__reconnect_num}"
        )
        await asyncio.sleep(reconnect_wait)
        logging.debug("asyncio sleep done")
        event = asyncio.Event()

        tasks = {
            asyncio.ensure_future(
                self.__recover_subscription_req_msg(event)
            ): self.__recover_subscription_req_msg,
            asyncio.ensure_future(self.__run(event)): self.__run,
        }

        while set(tasks.keys()):
            finished, pending = await asyncio.wait(
                tasks.keys(), return_when=asyncio.FIRST_EXCEPTION
            )
            exception_occur = False
            for task in finished:
                if task.exception():
                    exception_occur = True
                    traceback.print_stack()
                    message = f"{task} got an exception {task.exception()}\n {task.get_stack()}"
                    logging.warning(message)
                    for process in pending:
                        logging.warning(f"pending {process}")
                        try:
                            process.cancel()
                        except asyncio.CancelledError:
                            logging.exception("CancelledError")
                        logging.warning("cancel ok")
                    await self.__callback({"error": message})
            if exception_occur:
                break
        logging.warning("reconnect over")

    async def __recover_subscription_req_msg(self, event) -> None:
        logging.info(f"Recover subscriptions {self.__subscriptions} waiting.")
        await event.wait()

        for sub in self.__subscriptions:
            if sub["feed"] in self.__client.get_available_private_subscription_feeds():
                await self.send_message(deepcopy(sub), private=True)
            elif sub["feed"] in self.__client.get_available_public_subscription_feeds():
                await self.send_message(deepcopy(sub), private=False)
            logging.info(f"{sub}: OK")

        logging.info(f"Recover subscriptions {self.__subscriptions} done.")

    async def send_message(self, msg: dict, private: bool = False) -> None:
        """
        Enables sending a message via the websocket connection

        :param msg: The message as dictionary
        :type msg: dict
        :param private: Optional - If the message requires authentication (default: ``False``)
        :type msg: bool
        :rtype: None
        """
        while not self.__socket:
            await asyncio.sleep(0.4)

        if private:
            if not self.__client.is_auth:
                raise ValueError(
                    "Cannot access private endpoints with unauthenticated client!"
                )
            if not self.__challenge_ready:
                await self.__check_challenge_ready()

            msg["api_key"] = self.__client._key
            msg["original_challenge"] = self.__last_challenge
            msg["signed_challenge"] = self.__new_challenge

        await self.__socket.send(json.dumps(msg))

    def __handle_new_challenge(self, msg: dict) -> None:
        self.__last_challenge = msg["message"]
        self.__new_challenge = self.__client._get_sign_challenge(self.__last_challenge)
        self.__challenge_ready = True

    async def __check_challenge_ready(self) -> None:
        await self.__socket.send(
            json.dumps({"event": "challenge", "api_key": self.__client._key})
        )

        logging.debug("Awaiting challenge...")
        while not self.__challenge_ready:
            await asyncio.sleep(0.2)

    def __get_reconnect_wait(self, attempts: int) -> float:
        return round(random() * min(60 * 3, (2**attempts) - 1) + 1)

    def __append_subscription(self, msg: dict) -> None:
        self.__remove_subscription(msg=msg)  # remove from list, to avoid duplicates
        sub = self.__build_subscription(msg)
        self.__subscriptions.append(sub)

    def __remove_subscription(self, msg: dict) -> None:
        sub = self.__build_subscription(msg)
        self.__subscriptions = [x for x in self.__subscriptions if x != sub]

    def __build_subscription(self, subscription: dict) -> dict:
        sub = {"event": "subscribe"}

        if (
            "event" not in subscription
            or subscription["event"] not in ["subscribed", "unsubscribed"]
            or "feed" not in subscription
        ):
            raise ValueError(
                "Cannot append/remove subscription with missing attributes."
            )

        if (
            subscription["feed"]
            in self.__client.get_available_public_subscription_feeds()
        ):
            # public subscribe
            if "product_ids" in subscription:
                if isinstance(subscription["product_ids"], list):
                    sub["product_ids"] = subscription["product_ids"]
                else:
                    sub["product_ids"] = [subscription["product_ids"]]
            sub["feed"] = subscription["feed"]

        elif (
            subscription["feed"]
            in self.__client.get_available_private_subscription_feeds()
        ):
            # private subscription
            sub["feed"] = subscription["feed"]
        else:
            logging.warning(
                "Feed not implemented. Please contact the python-kraken-sdk package author."
            )
        return sub

    def _get_active_subscriptions(self) -> List[dict]:
        """Returns the active subscriptions"""
        return self.__subscriptions
