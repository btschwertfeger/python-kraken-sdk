# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pylint: disable=attribute-defined-outside-init

"""Module that implements the Kraken Futures websocket client"""

from __future__ import annotations

import asyncio
import json
import logging
import traceback
from copy import deepcopy
from random import random
from typing import TYPE_CHECKING, Any

from websockets.asyncio.client import connect

from kraken.exceptions import MaxReconnectError

if TYPE_CHECKING:
    from collections.abc import Callable

    from kraken.futures import FuturesWSClient
from kraken.utils.utils import WSState

LOG: logging.Logger = logging.getLogger(__name__)


class ConnectFuturesWebsocket:  # pylint: disable=too-many-instance-attributes
    """
    This class is only called by the
    :class:`kraken.futures.FuturesWSClient` to establish the websocket
    connection.

    :param client: The Futures websocket client that instantiates this class
    :type client: :class:`kraken.futures.FuturesWSClient`
    :param endpoint: The endpoint to access (either the live Kraken API or the
        sandbox environment)
    :type endpoint: str
    :param callback: The function that is used to receive the message objects
    :type callback: function
    """

    MAX_RECONNECT_NUM: int = 3

    def __init__(
        self: ConnectFuturesWebsocket,
        client: FuturesWSClient,
        endpoint: str,
        callback: Callable,
    ) -> None:
        self.state = WSState.INIT
        self.__client: FuturesWSClient = client
        self.__ws_endpoint: str = endpoint
        self.__callback: Any = callback

        self.__reconnect_num: int = 0

        self.__last_challenge: str | None = None
        self.__new_challenge: str | None = None
        self.__challenge_ready: bool = False

        self.socket: Any = None
        self.__subscriptions: list[dict] = []
        self.keep_alive = True
        self.exception_occur = False

    @property
    def subscriptions(self: ConnectFuturesWebsocket) -> list[dict]:
        """Returns the active subscriptions"""
        return self.__subscriptions

    async def start(self: ConnectFuturesWebsocket) -> None:
        """Starts the websocket connection"""
        if (
            hasattr(self, "task")
            and not self.task.done()  # pylint: disable=access-member-before-definition
        ):
            return
        self.task: asyncio.Task = asyncio.create_task(
            self.__run_forever(),
        )

    async def stop(self: ConnectFuturesWebsocket) -> None:
        """Stops the websocket connection"""
        self.state = WSState.CANCELLING
        self.keep_alive = False
        if hasattr(self, "task") and not self.task.done():
            await self.task
        self.state = WSState.CLOSED

    async def __run(  # noqa: C901
        self: ConnectFuturesWebsocket,
        event: asyncio.Event,
    ) -> None:
        self.state = WSState.CONNECTING
        self.__new_challenge = None
        self.__last_challenge = None

        async with connect(  # pylint: disable=no-member # noqa: PLR1702
            f"wss://{self.__ws_endpoint}",
            additional_headers={"User-Agent": "btschwertfeger/python-kraken-sdk"},
            ping_interval=30,
            max_queue=None,  # FIXME: This is not recommended by the docs https://websockets.readthedocs.io/en/stable/reference/asyncio/client.html#module-websockets.asyncio.client
        ) as socket:
            self.state = WSState.CONNECTED
            LOG.info("Websocket connection established!")
            self.socket = socket

            if not event.is_set():
                event.set()
            self.__reconnect_num = 0

            while self.keep_alive:
                try:
                    _message = await asyncio.wait_for(self.socket.recv(), timeout=10)
                except TimeoutError:
                    LOG.debug(  # important
                        "Timeout error in %s",
                        self.__ws_endpoint,
                    )
                except asyncio.CancelledError:
                    LOG.exception("asyncio.CancelledError")
                    self.keep_alive = False
                else:
                    try:
                        message: dict = json.loads(_message)
                    except ValueError:
                        LOG.warning(_message)
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
        self.keep_alive = True
        self.exception_occur = False
        try:
            while self.keep_alive:
                await self.__reconnect()
        except MaxReconnectError:
            self.state = WSState.ERROR
            await self.__callback(
                {"python-kraken-sdk": {"error": "kraken.exceptions.MaxReconnectError"}},
            )
            self.exception_occur = True
        except Exception:  # pylint: disable=broad-except
            self.state = WSState.ERROR
            LOG.exception(traceback.format_exc())
            self.exception_occur = True

    async def close_connection(self: ConnectFuturesWebsocket) -> None:
        """Closes the connection -/ will force reconnect"""
        self.state = WSState.CANCELLING
        await self.socket.close()

    async def __reconnect(self: ConnectFuturesWebsocket) -> None:
        self.state = WSState.RECONNECTING
        LOG.info("Websocket start connect/reconnect")

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            raise MaxReconnectError

        reconnect_wait: float = self.__get_reconnect_wait(attempts=self.__reconnect_num)
        LOG.debug(
            "asyncio sleep reconnect_wait=%f s reconnect_num=%d",
            reconnect_wait,
            self.__reconnect_num,
        )
        await asyncio.sleep(reconnect_wait)

        event: asyncio.Event = asyncio.Event()
        tasks: dict = {
            asyncio.ensure_future(
                self.__recover_subscription_req_msg(event),
            ): self.__recover_subscription_req_msg,
            asyncio.ensure_future(self.__run(event)): self.__run,
        }

        while self.keep_alive:
            finished, pending = await asyncio.wait(
                tasks.keys(),
                return_when=asyncio.FIRST_EXCEPTION,
            )
            exception_occur = False
            for task in finished:
                if task.exception():
                    self.state = WSState.ERRORHANDLING
                    exception_occur = True
                    self.__challenge_ready = False
                    message = f"{task} got an exception {task.exception()}\n {task.get_stack()}"
                    LOG.warning(message)
                    for process in pending:
                        LOG.warning("Pending %s", process)
                        try:
                            process.cancel()
                            LOG.warning("Cancelled %s", process)
                        except asyncio.CancelledError:
                            LOG.error("Failed to cancel %s", process)
                    await self.__callback({"python-kraken-sdk": {"error": message}})
            if exception_occur:
                break
        self.state = WSState.CLOSED
        LOG.info("Connection closed!")

    async def __recover_subscription_req_msg(
        self: ConnectFuturesWebsocket,
        event: asyncio.Event,
    ) -> None:
        LOG.info(
            "Recover subscriptions %s: waiting",
            self.__subscriptions,
        )
        await event.wait()

        for sub in self.__subscriptions:
            if sub["feed"] in self.__client.get_available_private_subscription_feeds():
                await self.send_message(deepcopy(sub), private=True)
            elif sub["feed"] in self.__client.get_available_public_subscription_feeds():
                await self.send_message(deepcopy(sub), private=False)
            LOG.info("%s: OK", sub)

        LOG.info(
            "Recover subscriptions %s: done",
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
        while not self.socket:
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

        await self.socket.send(json.dumps(message))

    def __handle_new_challenge(self: ConnectFuturesWebsocket, message: dict) -> None:
        self.__last_challenge = message["message"]
        self.__new_challenge = self.__client.get_sign_challenge(self.__last_challenge)
        self.__challenge_ready = True

    async def __check_challenge_ready(self: ConnectFuturesWebsocket) -> None:
        await self.socket.send(
            json.dumps({"event": "challenge", "api_key": self.__client.key}),
        )

        LOG.debug("Awaiting challenge...")
        while not self.__challenge_ready:
            await asyncio.sleep(0.2)

    def __get_reconnect_wait(self, attempts: int) -> float:
        return round(  # type: ignore[no-any-return]
            random() * min(60 * 3, (2**attempts) - 1) + 1,  # noqa: S311 # nosec: B311
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
            LOG.warning(
                "Feed not implemented. Please contact the python-kraken-sdk package author.",
            )
        return sub

    def get_active_subscriptions(self: ConnectFuturesWebsocket) -> list[dict]:
        """Returns the active subscriptions"""
        return self.__subscriptions


__all__ = ["ConnectFuturesWebsocket"]
