#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the Kraken Futures websocket client"""

from __future__ import annotations

import asyncio
import json
import logging
import traceback
from copy import deepcopy
from random import random
from typing import TYPE_CHECKING, Any, Optional

import websockets

from kraken.exceptions import MaxReconnectError

if TYPE_CHECKING:
    from kraken.futures import KrakenFuturesWSClient


class ConnectFuturesWebsocket:
    """
    This class is only called by the
    :class:`kraken.futures.KrakenFuturesWSClient` to establish the websocket
    connection.

    :param client: The Futures websocket client that instantiates this class
    :type client: :class:`kraken.futures.KrakenFuturesWSClient`
    :param endpoint: The endpoint to access (either the live Kraken API or the
        sandbox environment)
    :type endpoint: str
    :param callback: The function that is used to receive the message objects
    :type callback: function
    """

    MAX_RECONNECT_NUM: int = 2

    def __init__(
        self: ConnectFuturesWebsocket,
        client: KrakenFuturesWSClient,
        endpoint: str,
        callback: Any,
    ):
        self.__client: KrakenFuturesWSClient = client
        self.__ws_endpoint: str = endpoint
        self.__callback: Any = callback

        self.__reconnect_num: int = 0

        self.__last_challenge: Optional[str] = None
        self.__new_challenge: Optional[str] = None
        self.__challenge_ready: bool = False

        self.__socket: Any = None
        self.__subscriptions: list[dict] = []

        self.task = asyncio.ensure_future(
            self.__run_forever(),
            loop=asyncio.get_running_loop(),
        )

    @property
    def subscriptions(self: ConnectFuturesWebsocket) -> list[dict]:
        """Returns the active subscriptions"""
        return self.__subscriptions

    async def __run(self: ConnectFuturesWebsocket, event: asyncio.Event) -> None:
        keep_alive: bool = True
        self.__new_challenge = None
        self.__last_challenge = None

        async with websockets.connect(  # pylint: disable=no-member
            f"wss://{self.__ws_endpoint}",
            ping_interval=30,
        ) as socket:
            logging.info("Websocket connected!")
            self.__socket = socket

            if not event.is_set():
                event.set()
            self.__reconnect_num = 0

            while keep_alive:
                try:
                    _message = await asyncio.wait_for(self.__socket.recv(), timeout=15)
                except asyncio.TimeoutError:
                    logging.debug(  # important
                        "Timeout error in %s",
                        self.__ws_endpoint,
                    )
                except asyncio.CancelledError:
                    logging.exception("asyncio.CancelledError")
                    keep_alive = False
                    await self.__callback({"error": "asyncio.CancelledError"})
                else:
                    try:
                        message: dict = json.loads(_message)
                    except ValueError:
                        logging.warning(_message)
                    else:
                        forward: bool = True
                        if "event" in message:
                            _event: str = message["event"]
                            if _event == "challenge" and "message" in message:
                                forward = False
                                self.__handle_new_challenge(message)
                            elif _event == "subscribed":
                                self.__append_subscription(message)
                            elif _event == "unsubscribed":
                                self.__remove_subscription(message)
                        if forward:
                            await self.__callback(message)

    async def __run_forever(self: ConnectFuturesWebsocket) -> None:
        try:
            while True:
                await self.__reconnect()
        except MaxReconnectError:
            await self.__callback(
                {"error": "kraken.exceptions.MaxReconnectError"},
            )
        except Exception:
            logging.exception(traceback.format_exc())
        finally:
            self.__client.exception_occur = True

    async def __reconnect(self: ConnectFuturesWebsocket) -> None:
        logging.info("Websocket start connect/reconnect")

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            raise MaxReconnectError

        reconnect_wait: float = self.__get_reconnect_wait(self.__reconnect_num)
        logging.debug(
            "asyncio sleep reconnect_wait=%f s reconnect_num=%d",
            reconnect_wait,
            self.__reconnect_num,
        )
        await asyncio.sleep(reconnect_wait)
        logging.debug("asyncio sleep done")
        event: asyncio.Event = asyncio.Event()

        tasks: dict = {
            asyncio.ensure_future(
                self.__recover_subscription_req_msg(event),
            ): self.__recover_subscription_req_msg,
            asyncio.ensure_future(self.__run(event)): self.__run,
        }

        while set(tasks.keys()):
            finished, pending = await asyncio.wait(
                tasks.keys(),
                return_when=asyncio.FIRST_EXCEPTION,
            )
            exception_occur: bool = False
            for task in finished:
                if task.exception():
                    exception_occur = True
                    traceback.print_stack()
                    message = f"{task} got an exception {task.exception()}\n {task.get_stack()}"
                    logging.warning(message)
                    for process in pending:
                        logging.warning("pending %s", process)
                        try:
                            process.cancel()
                        except asyncio.CancelledError:
                            logging.exception("CancelledError")
                        logging.warning("cancel ok")
                    await self.__callback({"error": message})
            if exception_occur:
                break
        logging.warning("reconnect over")

    async def __recover_subscription_req_msg(
        self: ConnectFuturesWebsocket,
        event: asyncio.Event,
    ) -> None:
        logging.info(
            "Recover subscriptions %s waiting.",
            self.__subscriptions,
        )
        await event.wait()

        for sub in self.__subscriptions:
            if sub["feed"] in self.__client.get_available_private_subscription_feeds():
                await self.send_message(deepcopy(sub), private=True)
            elif sub["feed"] in self.__client.get_available_public_subscription_feeds():
                await self.send_message(deepcopy(sub), private=False)
            logging.info("%s: OK", sub)

        logging.info(
            "Recover subscriptions %s done.",
            self.__subscriptions,
        )

    async def send_message(
        self: ConnectFuturesWebsocket,
        message: dict,
        *,
        private: bool = False,
    ) -> None:
        """
        Enables sending a message via the websocket connection

        :param message: The message as dictionary
        :type message: dict
        :param private: If the message requires authentication (default:
            ``False``)
        :type private: bool, optional
        :rtype: Coroutine
        """
        while not self.__socket:
            await asyncio.sleep(0.4)

        if private:
            if not self.__client.is_auth:
                raise AttributeError(
                    "Cannot access private endpoints with unauthenticated client!",
                )
            if not self.__challenge_ready:
                await self.__check_challenge_ready()

            message["api_key"] = self.__client.key
            message["original_challenge"] = self.__last_challenge
            message["signed_challenge"] = self.__new_challenge

        await self.__socket.send(json.dumps(message))

    def __handle_new_challenge(self: ConnectFuturesWebsocket, message: dict) -> None:
        self.__last_challenge = message["message"]
        self.__new_challenge = self.__client.get_sign_challenge(self.__last_challenge)
        self.__challenge_ready = True

    async def __check_challenge_ready(self: ConnectFuturesWebsocket) -> None:
        await self.__socket.send(
            json.dumps({"event": "challenge", "api_key": self.__client.key}),
        )

        logging.debug("Awaiting challenge...")
        while not self.__challenge_ready:
            await asyncio.sleep(0.2)

    def __get_reconnect_wait(self, attempts: int) -> float:
        return round(  # type: ignore[no-any-return]
            random() * min(60 * 3, (2**attempts) - 1) + 1,  # noqa: S311
        )

    def __append_subscription(self: ConnectFuturesWebsocket, message: dict) -> None:
        self.__remove_subscription(
            message=message,
        )  # remove from list, to avoid duplicates
        sub: dict = self.__build_subscription(message)
        self.__subscriptions.append(sub)

    def __remove_subscription(self: ConnectFuturesWebsocket, message: dict) -> None:
        sub: dict = self.__build_subscription(message)
        self.__subscriptions = [x for x in self.__subscriptions if x != sub]

    def __build_subscription(
        self: ConnectFuturesWebsocket,
        subscription: dict,
    ) -> dict:
        sub: dict = {"event": "subscribe"}

        if (
            "event" not in subscription
            or subscription["event"] not in {"subscribed", "unsubscribed"}
            or "feed" not in subscription
        ):
            raise AttributeError(
                "Cannot append/remove subscription with missing attributes.",
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
                "Feed not implemented. Please contact the python-kraken-sdk package author.",
            )
        return sub

    def get_active_subscriptions(self: ConnectFuturesWebsocket) -> list[dict]:
        """Returns the active subscriptions"""
        return self.__subscriptions


__all__ = ["ConnectFuturesWebsocket"]
