#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
This module provides the base class that is used to create and maintain
websocket connections to Kraken.

It also provides derived classes for using the Kraken Websocket API v1 and v2.
"""

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
    from kraken.spot.websocket import KrakenSpotWSClientBase


class ConnectSpotWebsocketBase:
    """
    This class serves as the base for
    :class:`kraken.spot.websocket.connectors.ConnectSpotWebsocket` and
    :class:`kraken.spot.websocket.connectors.ConnectSpotWebsocketV2`.

    It creates and holds a websocket connection, reconnects and handles
    errors. Its functions only serve as base for the classes mentioned above,
    since it combines the functionalities that is used for both Websocket API v1
    and v2.

    **This is an internal class and should not be used outside.**

    :param client: The websocket client that wants to connect
    :type client: :class:`kraken.spot.KrakenSpotWSClientBase`
    :param endpoint: The websocket endpoint
    :type endpoint: str
    :param callback: Callback function that receives the websocket messages
    :type callback: function
    :param is_auth: If the websocket connects to endpoints that
        require authentication (default: ``False``)
    :type is_auth: bool, optional
    """

    MAX_RECONNECT_NUM: int = 7
    LOG: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self: ConnectSpotWebsocketBase,
        client: KrakenSpotWSClientBase,
        endpoint: str,
        callback: Any,
        is_auth: bool = False,
    ):
        self.__client: KrakenSpotWSClientBase = client
        self.__ws_endpoint: str = endpoint
        self.__callback: Any = callback

        self.__reconnect_num: int = 0
        self.ws_conn_details: Optional[dict] = None

        self.__is_auth: bool = is_auth

        self._last_ping: Optional[Union[int, float]] = None
        self.socket: Optional[Any] = None
        self._subscriptions: List[dict] = []
        self.task: asyncio.Task = asyncio.create_task(self.__run_forever())

    @property
    def is_auth(self: ConnectSpotWebsocketBase) -> bool:
        """Returns ``True`` if the connection can access privat endpoints"""
        return self.__is_auth

    @property
    def client(self: ConnectSpotWebsocketBase) -> KrakenSpotWSClientBase:
        """Return the websocket client"""
        return self.__client

    async def __run(self: ConnectSpotWebsocketBase, event: asyncio.Event) -> None:
        """
        This function establishes the websocket connection and runs until
        some error occurs.

        :param event: Event used to control the information flow
        :type event: asyncio.Event
        """
        keep_alive: bool = True
        self._last_ping = time()
        self.ws_conn_details = (
            None if not self.__is_auth else self.__client.get_ws_token()
        )
        self.LOG.debug(f"Websocket token: {self.ws_conn_details}")

        async with websockets.connect(  # pylint: disable=no-member
            f"wss://{self.__ws_endpoint}", ping_interval=30
        ) as socket:
            self.LOG.info("Websocket connected!")
            self.socket = socket

            if not event.is_set():
                await self.send_ping()
                event.set()
            self.__reconnect_num = 0

            while keep_alive:
                if time() - self._last_ping > 10:
                    await self.send_ping()
                try:
                    _msg = await asyncio.wait_for(self.socket.recv(), timeout=15)
                except asyncio.TimeoutError:  # important
                    await self.send_ping()
                except asyncio.CancelledError:
                    self.LOG.exception("asyncio.CancelledError")
                    keep_alive = False
                    await self.__callback({"error": "asyncio.CancelledError"})
                else:
                    try:
                        message: dict = json.loads(_msg)
                    except ValueError:
                        self.LOG.warning(_msg)
                    else:
                        self._manage_subscriptions(message=message)
                        await self.__callback(message)

    async def __run_forever(self: ConnectSpotWebsocketBase) -> None:
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
            await self.__callback({"error": "KrakenSpotWSClient*: exception_occur"})
            self.__client.exception_occur = True

    async def __reconnect(self: ConnectSpotWebsocketBase) -> None:
        """
        Handles the reconnect - before starting the connection and after an
        error.

        :raises KrakenException.MaxReconnectError: If there are to many
            reconnect retries
        """
        self.LOG.info("Websocket start connect/reconnect")

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            raise KrakenException.MaxReconnectError(
                "The KrakenSpotWebsocketClient encountered to many reconnects!"
            )

        reconnect_wait: float = self.__get_reconnect_wait(self.__reconnect_num)
        self.LOG.debug(
            f"asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self.__reconnect_num}"
        )
        await asyncio.sleep(reconnect_wait)

        event: asyncio.Event = asyncio.Event()
        tasks: List[asyncio.Task] = [
            asyncio.create_task(self._recover_subscriptions(event)),
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

    def __get_reconnect_wait(
        self: ConnectSpotWebsocketBase, attempts: int
    ) -> Union[float, Any]:
        """
        Get some random wait time that increases by any attempt.

        :param attempts: Number of reconnects that failed
        :type attempts: int
        :return: Wait time
        :rtype: float | Any
        """
        return round(random() * min(60 * 3, (2**attempts) - 1) + 1)

    # --------------------------------------------------------------------------
    # Functions to overload

    async def send_ping(self: ConnectSpotWebsocketBase) -> None:
        """Function that is to be overloaded.

        Has to implement the ping to Kraken.
        """
        raise NotImplementedError(  # coverage: disable
            "This function must be overloaded."
        )

    def _manage_subscriptions(
        self: ConnectSpotWebsocketBase, message: Union[dict, list]
    ) -> None:
        """Function that is to be overloaded.

        Has to manage incoming messages about subscriptions - and then trigger
        the local management of new un-/subscriptions.
        """
        raise NotImplementedError(  # coverage: disable
            "This function must be overloaded."
        )

    async def _recover_subscriptions(
        self: ConnectSpotWebsocketBase, event: asyncio.Event
    ) -> None:
        """Function that is to be overloaded.

        Is responsible for recovering subscriptions if the connection was
        closed.
        """
        raise NotImplementedError(  # coverage: disable
            "This function must be overloaded."
        )


class ConnectSpotWebsocketV2(ConnectSpotWebsocketBase):
    """
    This class extends the
    :class:`kraken.spot.websocket.connectors.ConnectSpotWebsocketBase` and
    can be instantiated to create and maintain a websocket connection using
    the Kraken Websocket API v2.

    **This is an internal class and should not be used outside.**

    :param client: The websocket client that wants to connect
    :type client: :class:`kraken.spot.KrakenSpotWSClientBase`
    :param endpoint: The websocket endpoint
    :type endpoint: str
    :param callback: Callback function that receives the websocket messages
    :type callback: function
    :param is_auth: If the websocket connects to endpoints that
        require authentication (default: ``False``)
    :type is_auth: bool, optional
    """

    def __init__(
        self: ConnectSpotWebsocketV2,
        client: KrakenSpotWSClientBase,
        endpoint: str,
        callback: Any,
        is_auth: bool = False,
    ) -> None:
        super().__init__(
            client=client, endpoint=endpoint, callback=callback, is_auth=is_auth
        )

    async def send_ping(self: ConnectSpotWebsocketV2) -> None:
        """Sends ping to Kraken"""
        await self.socket.send(json.dumps({"method": "ping"}))
        self._last_ping = time()

    async def _recover_subscriptions(
        self: ConnectSpotWebsocketV2, event: asyncio.Event
    ) -> None:
        """
        Executes the subscribe function for all subscriptions that were  tracked
        locally. This function is called when the connection was closed to
        recover the subscriptions.

        :param event: Event to wait for (so this is only executed when
            it is set to ``True`` - which is when the connection is ready)
        :type event: asyncio.Event
        """
        log_msg: str = f'Recover {"authenticated" if self.is_auth else "public"} subscriptions {self._subscriptions}'
        self.LOG.info(f"{log_msg} waiting.")
        await event.wait()

        for subscription in self._subscriptions:
            await self.client.subscribe(params=subscription)
            self.LOG.info(f"{subscription} OK")

        self.LOG.info(f"{log_msg} done.")

    def _manage_subscriptions(self: ConnectSpotWebsocketV2, message: dict) -> None:  # type: ignore[override]
        """
        Checks if the message contains events about un-/subscriptions
        to add or remove these from the list of current tracked subscriptions.

        :param message: The message to check for subscriptions
        :type message: dict
        """
        if message.get("method") == "subscribe":
            if message.get("success") and message.get("result"):
                self.__append_subscription(subscription=message["result"])
            else:
                self.LOG.warning(message)

        elif message.get("method") == "unsubscribe":
            if message.get("success") and message.get("result"):
                self.__remove_subscription(subscription=message["result"])
            else:
                self.LOG.warning(message)

    def __append_subscription(self: ConnectSpotWebsocketV2, subscription: dict) -> None:
        """
        Appends a subscription to the local list of tracked subscriptions.

        :param subscription: The subscription to append
        :type subscription: dict
        """
        self.__remove_subscription(subscription=subscription)
        self._subscriptions.append(subscription)

    def __remove_subscription(self: ConnectSpotWebsocketV2, subscription: dict) -> None:
        """
        Removes a subscription from the list of locally tracked subscriptions.

        :param subscription: The subscription to remove.
        :type subscription: dict
        """
        self._subscriptions = [
            sub for sub in self._subscriptions if sub != subscription
        ]


class ConnectSpotWebsocketV1(ConnectSpotWebsocketBase):
    """
    This class extends the
    :class:`kraken.spot.websocket.connectors.ConnectSpotWebsocketBase` and
    can be instantiated to create and maintain a websocket connection using
    the Kraken Websocket API v1.

    **This is an internal class and should not be used outside.**

    :param client: The websocket client that wants to connect
    :type client: :class:`kraken.spot.KrakenSpotWSClientBase`
    :param endpoint: The websocket endpoint
    :type endpoint: str
    :param callback: Callback function that receives the websocket messages
    :type callback: function
    :param is_auth: If the websocket connects to endpoints that
        require authentication (default: ``False``)
    :type is_auth: bool, optional
    """

    def __init__(
        self: ConnectSpotWebsocketV1,
        client: KrakenSpotWSClientBase,
        endpoint: str,
        callback: Any,
        is_auth: bool = False,
    ) -> None:
        super().__init__(
            client=client, endpoint=endpoint, callback=callback, is_auth=is_auth
        )

    async def send_ping(self: ConnectSpotWebsocketV1) -> None:
        """Sends ping to Kraken"""
        await self.socket.send(
            json.dumps(
                {
                    "event": "ping",
                    "reqid": int(time() * 1000),
                }
            )
        )
        self._last_ping = time()

    async def _recover_subscriptions(
        self: ConnectSpotWebsocketV1, event: asyncio.Event
    ) -> None:
        """
        Executes the subscribe function for all subscriptions that were  tracked
        locally. This function is called when the connection was closed to
        recover the subscriptions.

        :param event: Event to wait for (so this is only executed when
            it is set to ``True`` - which is when the connection is ready)
        :type event: asyncio.Event
        """
        log_msg: str = f'Recover {"authenticated" if self.is_auth else "public"} subscriptions {self._subscriptions}'
        self.LOG.info(f"{log_msg} waiting.")
        await event.wait()

        for sub in self._subscriptions:
            cpy = deepcopy(sub)
            private = False
            if (
                "subscription" in sub
                and "name" in sub["subscription"]
                and sub["subscription"]["name"] in self.client.private_channel_names
            ):
                cpy["subscription"]["token"] = self.ws_conn_details["token"]
                private = True

            await self.client.send_message(cpy, private=private)
            self.LOG.info(f"{sub} OK")

        self.LOG.info(f"{log_msg} done.")

    def _manage_subscriptions(
        self: ConnectSpotWebsocketV1, message: Union[dict, list]
    ) -> None:
        """
        Checks if the message contains events about un-/subscriptions
        to add or remove these from the list of current tracked subscriptions.

        :param message: The message to check for subscriptions
        :type message: dict | list
        """
        if (
            isinstance(message, dict)
            and message.get("event") == "subscriptionStatus"
            and message.get("status")
        ):
            if message["status"] == "subscribed":
                self.__append_subscription(message=message)
            elif message["status"] == "unsubscribed":
                self.__remove_subscription(message=message)
            elif message["status"] == "error":
                self.LOG.warning(message)

    def __append_subscription(self: ConnectSpotWebsocketV1, message: dict) -> None:
        """
        Appends a subscription to the local list of tracked subscriptions.

        :param subscription: The subscription to append
        :type subscription: dict
        """
        # remove from list, to avoid duplicate entries
        self.__remove_subscription(message)
        self._subscriptions.append(self.__build_subscription(message))

    def __remove_subscription(self: ConnectSpotWebsocketV1, message: dict) -> None:
        """
        Removes a subscription from the list of locally tracked subscriptions.

        :param subscription: The subscription to remove.
        :type subscription: dict
        """
        subscription: dict = self.__build_subscription(message=message)
        self._subscriptions = [
            sub for sub in self._subscriptions if sub != subscription
        ]

    def __build_subscription(self: ConnectSpotWebsocketV1, message: dict) -> dict:
        """
        Builds a subscription dictionary that can be used to subscribe to a
        feed. This is also used to prepare the local active subscription list.

        :param message: The information to build the subscription from
        :type message: dict
        :raises ValueError: If attributes are missing
        :return: The built subscription
        :rtype: dict
        """
        sub: dict = {"event": "subscribe"}

        if not "subscription" in message or "name" not in message["subscription"]:
            raise ValueError("Cannot remove subscription with missing attributes.")
        if (
            message["subscription"]["name"] in self.client.public_channel_names
        ):  # public endpoint
            if message.get("pair"):
                sub["pair"] = (
                    message["pair"]
                    if isinstance(message["pair"], list)
                    else [message["pair"]]
                )
            sub["subscription"] = message["subscription"]
        elif (
            message["subscription"]["name"] in self.client.private_channel_names
        ):  # private endpoint
            sub["subscription"] = {"name": message["subscription"]["name"]}
        else:
            self.LOG.warning(
                "Feed not implemented. Please contact the python-kraken-sdk "
                "package maintainer."
            )
        return sub
