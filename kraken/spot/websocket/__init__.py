#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the kraken Spot websocket clients"""

from __future__ import annotations

import asyncio
import json
import logging
import traceback
from copy import deepcopy
from random import random
from time import time
from typing import TYPE_CHECKING, Any, List, Optional, Union

import websockets

from kraken.exceptions import KrakenException

if TYPE_CHECKING:
    from kraken.spot import KrakenSpotWSClient


class ConnectSpotWebsocket:
    """
    This class is only called by the :class:`kraken.spot.KrakenSpotWSClient`
    to establish and handle a websocket connection.

    :param client: The websocket client that wants to connect
    :type client: :class:`kraken.spot.KrakenSpotWSClient`
    :param endpoint: The websocket endpoint
    :type endpoint: str
    :param callback: Callback function that receives the websocket messages
    :type callback: function
    :param private: If the websocket connects to endpoints that
        require authentication (default: ``False``)
    :type private: bool, optional
    """

    MAX_RECONNECT_NUM: int = 7
    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: "ConnectSpotWebsocket",
        client: KrakenSpotWSClient,
        endpoint: str,
        callback: Any,
        is_auth: bool = False,
    ):
        self.__client: KrakenSpotWSClient = client
        self.__ws_endpoint: str = endpoint
        self.__callback: Any = callback

        self.__reconnect_num: int = 0
        self.__ws_conn_details: Optional[dict] = None

        self.__is_auth: bool = is_auth

        self.__last_ping: Optional[Union[int, float]] = None
        self.__socket: Optional[Any] = None
        self.__subscriptions: List[dict] = []

        self.task: asyncio.Task = asyncio.create_task(self.__run_forever())

    @property
    def subscriptions(self: "ConnectSpotWebsocket") -> list:
        """Returns the active subscriptions"""
        return self.__subscriptions

    @property
    def is_auth(self: "ConnectSpotWebsocket") -> bool:
        """Returns true if the connection can access privat endpoints"""
        return self.__is_auth

    async def __run(self: "ConnectSpotWebsocket", event: asyncio.Event) -> None:
        keep_alive: bool = True
        self.__last_ping = time()
        self.__ws_conn_details = (
            None if not self.__is_auth else self.__client.get_ws_token()
        )
        self.LOG.debug(f"Websocket token: {self.__ws_conn_details}")

        async with websockets.connect(  # pylint: disable=no-member
            f"wss://{self.__ws_endpoint}", ping_interval=30
        ) as socket:
            self.LOG.info("Websocket connected!")
            self.__socket = socket

            if not event.is_set():
                await self.send_ping()
                event.set()
            self.__reconnect_num = 0

            while keep_alive:
                if time() - self.__last_ping > 10:
                    await self.send_ping()
                try:
                    _msg = await asyncio.wait_for(self.__socket.recv(), timeout=15)
                except asyncio.TimeoutError:  # important
                    await self.send_ping()
                except asyncio.CancelledError:
                    self.LOG.exception("asyncio.CancelledError")
                    keep_alive = False
                    await self.__callback({"error": "asyncio.CancelledError"})
                else:
                    try:
                        msg: dict = json.loads(_msg)
                    except ValueError:
                        self.LOG.warning(_msg)
                    else:
                        if "event" in msg:
                            if msg["event"] == "subscriptionStatus" and "status" in msg:
                                ##      remove and assign un-/subscriptions
                                ##
                                try:
                                    if msg["status"] == "subscribed":
                                        self.__append_subscription(msg)
                                    elif msg["status"] == "unsubscribed":
                                        self.__remove_subscription(msg)
                                    elif msg["status"] == "error":
                                        self.LOG.warning(msg)
                                except AttributeError:
                                    pass

                        await self.__callback(msg)

    async def __run_forever(self: "ConnectSpotWebsocket") -> None:
        """
        This function ensures the reconnects.

        todo: This is stupid. There must be a better way for passing
              the raised exception to the client class - not
              through this ``exception_occur`` flag
        """
        try:
            while True:
                await self.__reconnect()
        except KrakenException.MaxReconnectError:
            await self.__callback(
                {"error": "kraken.exceptions.KrakenException.MaxReconnectError"}
            )
        except Exception as exc:
            traceback_: str = traceback.format_exc()
            logging.error(f"{exc}: {traceback_}")
            await self.__callback({"error": traceback_})
        finally:
            self.__client.exception_occur = True

    async def __reconnect(self: "ConnectSpotWebsocket") -> None:
        self.LOG.info("Websocket start connect/reconnect")

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            self.LOG.error(
                "The KrakenSpotWebsocketClient encountered to many reconnects!"
            )
            raise KrakenException.MaxReconnectError()

        reconnect_wait: float = self.__get_reconnect_wait(self.__reconnect_num)
        self.LOG.debug(
            "asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self.__reconnect_num}"
        )
        await asyncio.sleep(reconnect_wait)

        event: asyncio.Event = asyncio.Event()
        tasks: List[asyncio.Task] = [
            asyncio.create_task(self.__recover_subscriptions(event)),
            asyncio.create_task(self.__run(event)),
        ]

        while True:
            finished, pending = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_EXCEPTION
            )
            exception_occur: bool = False
            for task in finished:
                if task.exception():
                    exception_occur = True
                    traceback.print_stack()
                    message: str = f"{task} got an exception {task.exception()}\n {task.get_stack()}"
                    self.LOG.warning(message)
                    for process in pending:
                        self.LOG.warning(f"pending {process}")
                        try:
                            process.cancel()
                        except asyncio.CancelledError:
                            self.LOG.exception("asyncio.CancelledError")
                    await self.__callback({"error": message})
            if exception_occur:
                break
        self.LOG.warning("reconnect over")

    async def __recover_subscriptions(
        self: "ConnectSpotWebsocket", event: asyncio.Event
    ) -> None:
        self.LOG.info(
            f'Recover {"auth" if self.__is_auth else "public"} subscriptions {self.__subscriptions} waiting.'
        )
        await event.wait()

        for sub in self.__subscriptions:
            cpy = deepcopy(sub)
            private = False
            if (
                "subscription" in sub
                and "name" in sub["subscription"]
                and sub["subscription"]["name"] in self.__client.private_sub_names
            ):
                cpy["subscription"]["token"] = self.__ws_conn_details["token"]
                private = True
            await self.send_message(cpy, private=private)
            self.LOG.info(f"{sub} OK")

        self.LOG.info(
            f'Recovering {"auth" if self.__is_auth else "public"} subscriptions {self.__subscriptions} done.'
        )

    async def send_ping(self: "ConnectSpotWebsocket") -> None:
        """Sends ping to Kraken"""
        await self.__socket.send(
            json.dumps(
                {
                    "event": "ping",
                    "reqid": int(time() * 1000),
                }
            )
        )
        self.__last_ping = time()

    async def send_message(
        self: "ConnectSpotWebsocket", msg: dict, private: Optional[bool] = False
    ) -> None:
        """
        Sends a message via websocket

        :param msg: The content to send
        :type msg: dict
        :param private: Use authentication (default: ``False``)
        :type private: bool, optional
        """
        if private and not self.__is_auth:
            raise ValueError("Cannot send private message with public websocket.")

        while not self.__socket:
            await asyncio.sleep(0.4)

        msg["reqid"] = int(time() * 1000)
        if private and "subscription" in msg:
            msg["subscription"]["token"] = self.__ws_conn_details["token"]
        elif private:
            msg["token"] = self.__ws_conn_details["token"]
        await self.__socket.send(json.dumps(msg))

    def __append_subscription(self: "ConnectSpotWebsocket", msg: dict) -> None:
        """
        Add a dictionary containing subscription information to list
        This is used to recover when the connection gets interrupted.

        :param msg: The subscription
        :type msg: dict

        This function should only be called in
        when self.__run receives a msg and the following conditions met:
        - ``msg.get("event") == "subscriptionStatus"```
        - ``msg.get("status") == "subscribed"``
        """
        self.__remove_subscription(msg)  # remove from list, to avoid duplicate entries
        self.__subscriptions.append(self.__build_subscription(msg))

    def __remove_subscription(self: "ConnectSpotWebsocket", msg: dict) -> None:
        """
        Remove a dictionary containing subscription information from list.

        :param msg: The subscription to remove
        :type msg: dict

        This function should only be called in
        when self.__run receives a msg and the following conditions met:
        - ``msg.get("event") == "subscriptionStatus"```
        - ``msg.get("status") == "unsubscribed"``
        """
        sub: dict = self.__build_subscription(msg)
        self.__subscriptions = [x for x in self.__subscriptions if x != sub]

    def __build_subscription(self: "ConnectSpotWebsocket", msg: dict) -> dict:
        sub: dict = {"event": "subscribe"}

        if not "subscription" in msg or "name" not in msg["subscription"]:
            raise ValueError("Cannot remove subscription with missing attributes.")
        if (
            msg["subscription"]["name"] in self.__client.public_sub_names
        ):  # public endpoint
            if "pair" in msg:
                sub["pair"] = (
                    msg["pair"] if isinstance(msg["pair"], list) else [msg["pair"]]
                )
            sub["subscription"] = msg["subscription"]
        elif (
            msg["subscription"]["name"] in self.__client.private_sub_names
        ):  # private endpoint
            sub["subscription"] = {"name": msg["subscription"]["name"]}
        else:
            self.LOG.warning(
                "Feed not implemented. Please contact the python-kraken-sdk package author."
            )
        return sub

    def __get_reconnect_wait(self, attempts: int) -> Union[float, Any]:
        return round(random() * min(60 * 3, (2**attempts) - 1) + 1)
