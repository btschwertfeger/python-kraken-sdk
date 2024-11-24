#!/usr/bin/env python
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#
# pylint: disable=attribute-defined-outside-init

"""
This module provides the base class that is used to create and maintain
websocket connections to Kraken.

It also provides derived classes for using the Kraken Websocket API v2.
"""

from __future__ import annotations

import asyncio
import json
import logging
import traceback
from copy import deepcopy
from random import random
from time import time
from typing import TYPE_CHECKING, Any, Final

import websockets

from kraken.exceptions import MaxReconnectError

if TYPE_CHECKING:
    from collections.abc import Callable

    from kraken.spot.websocket import SpotWSClientBase

LOG: logging.Logger = logging.getLogger(__name__)


class ConnectSpotWebsocketBase:  # pylint: disable=too-many-instance-attributes
    """
    This class serves as the base for
    :class:`kraken.spot.websocket.connectors.ConnectSpotWebsocket`.

    It creates and holds a websocket connection, reconnects and handles
    errors.

    **This is an internal class and should not be used outside.**

    :param client: The websocket client that wants to connect
    :type client: :class:`kraken.spot.SpotWSClientBase`
    :param endpoint: The websocket endpoint
    :type endpoint: str
    :param callback: Callback function that receives the websocket messages
    :type callback: function
    :param is_auth: If the websocket connects to endpoints that
        require authentication (default: ``False``)
    :type is_auth: bool, optional
    """

    MAX_RECONNECT_NUM: int = 7
    PING_INTERVAL: int = 10  # seconds

    def __init__(
        self: ConnectSpotWebsocketBase,
        client: SpotWSClientBase,
        endpoint: str,
        callback: Callable,
        *,
        is_auth: bool = False,
    ) -> None:
        self.__client: SpotWSClientBase = client
        self.__ws_endpoint: str = endpoint
        self.__callback: Callable = callback

        self.__reconnect_num: int = 0
        self.ws_conn_details: dict | None = None

        self.__is_auth: bool = is_auth

        self._last_ping: int | float | None = None
        self.socket: Any | None = None
        self._subscriptions: list[dict] = []
        self.exception_occur: bool = False
        self.keep_alive: bool = True

    @property
    def is_auth(self: ConnectSpotWebsocketBase) -> bool:
        """Returns ``True`` if the connection can access privat endpoints"""
        return self.__is_auth

    @property
    def client(self: ConnectSpotWebsocketBase) -> SpotWSClientBase:
        """Return the websocket client"""
        return self.__client

    @property
    def subscriptions(self: ConnectSpotWebsocketBase) -> list[dict]:
        """Returns a copy of active subscriptions"""
        return deepcopy(self._subscriptions)

    async def start(self: ConnectSpotWebsocketBase) -> None:
        """Starts the websocket connection"""
        if (
            hasattr(self, "task")
            and not self.task.done()  # pylint: disable=access-member-before-definition
        ):
            return
        self.task: asyncio.Task = asyncio.create_task(
            self.__run_forever(),
        )

    async def stop(self: ConnectSpotWebsocketBase) -> None:
        """Stops the websocket connection"""
        self.keep_alive = False
        if hasattr(self, "task") and not self.task.done():
            await self.task

    async def __run(self: ConnectSpotWebsocketBase, event: asyncio.Event) -> None:
        """
        This function establishes the websocket connection and runs until
        some error occurs.

        :param event: Event used to control the information flow
        :type event: asyncio.Event
        """
        self._last_ping = time()
        self.ws_conn_details = (
            None if not self.__is_auth else await self.__client.get_ws_token()
        )
        LOG.debug("Websocket token: %s", self.ws_conn_details)

        async with websockets.connect(  # pylint: disable=no-member
            f"wss://{self.__ws_endpoint}",
            extra_headers={"User-Agent": "python-kraken-sdk"},
            ping_interval=30,
        ) as socket:
            LOG.info("Websocket connected!")
            self.socket = socket

            if not event.is_set():
                await self.send_ping()
                event.set()
            self.__reconnect_num = 0

            while self.keep_alive:
                if time() - self._last_ping > self.PING_INTERVAL:
                    await self.send_ping()
                try:
                    _message = await asyncio.wait_for(self.socket.recv(), timeout=10)
                except TimeoutError:  # important
                    await self.send_ping()
                except asyncio.CancelledError:
                    LOG.exception("asyncio.CancelledError")
                    self.keep_alive = False
                    await self.__callback({"error": "asyncio.CancelledError"})
                else:
                    try:
                        message: dict = json.loads(_message)
                    except ValueError:
                        LOG.warning(_message)
                    else:
                        LOG.debug(message)
                        self._manage_subscriptions(message=message)
                        await self.__callback(message)

    async def __run_forever(self: ConnectSpotWebsocketBase) -> None:
        """This function ensures the reconnects."""
        self.keep_alive = True
        self.exception_occur = False
        try:
            while self.keep_alive:
                await self.__reconnect()
        except MaxReconnectError:
            await self.__callback(
                {"error": "kraken.exceptions.MaxReconnectError"},
            )
            self.exception_occur = True
        except Exception as exc:
            traceback_: str = traceback.format_exc()
            LOG.exception(
                "%s: %s",
                exc,
                traceback_,
            )
            await self.__callback({"error": traceback_})
            self.exception_occur = True

    async def close_connection(self: ConnectSpotWebsocketBase) -> None:
        """Closes the websocket connection and thus forces a reconnect"""
        await self.socket.close()

    async def __reconnect(self: ConnectSpotWebsocketBase) -> None:
        """
        Handles the reconnect - before starting the connection and after an
        error.

        :raises KrakenException.MaxReconnectError: If there are to many
            reconnect retries
        """
        LOG.info("Websocket start connect/reconnect")

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            raise MaxReconnectError(
                "The Kraken Spot websocket client encountered to many reconnects!",
            )

        reconnect_wait: float = self.__get_reconnect_wait(self.__reconnect_num)
        LOG.debug(
            "asyncio sleep reconnect_wait=%.1f s reconnect_num=%d",
            reconnect_wait,
            self.__reconnect_num,
        )
        await asyncio.sleep(reconnect_wait)

        event: asyncio.Event = asyncio.Event()
        tasks: list[asyncio.Task] = [
            asyncio.create_task(self._recover_subscriptions(event)),
            asyncio.create_task(self.__run(event)),
        ]

        while self.keep_alive:
            finished, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_EXCEPTION,
            )
            exception_occur: bool = False
            for task in finished:
                if task.exception():
                    exception_occur = True
                    traceback.print_stack()
                    message: str = (
                        f"{task} got an exception {task.exception()}\n {task.get_stack()}"
                    )
                    LOG.warning(message)
                    for process in pending:
                        LOG.warning("pending %s", process)
                        try:
                            process.cancel()
                        except asyncio.CancelledError:
                            LOG.exception("asyncio.CancelledError")
                    await self.__callback({"error": message})
            if exception_occur:
                break
        LOG.warning("Connection closed")

    def __get_reconnect_wait(
        self: ConnectSpotWebsocketBase,
        attempts: int,
    ) -> float | Any:  # noqa: ANN401
        """
        Get some random wait time that increases by any attempt.

        :param attempts: Number of reconnects that failed
        :type attempts: int
        :return: Wait time
        :rtype: float | Any
        """
        return round(
            random() * min(60 * 3, (2**attempts) - 1) + 1,  # noqa: S311 # nosec: B311
        )

    # --------------------------------------------------------------------------
    # Functions to overload

    async def send_ping(self: ConnectSpotWebsocketBase) -> None:
        """Function that is to be overloaded.

        Has to implement the ping to Kraken.
        """
        raise NotImplementedError(  # coverage: disable
            "This function must be overloaded.",
        )

    def _manage_subscriptions(
        self: ConnectSpotWebsocketBase,
        message: dict | list,
    ) -> None:
        """Function that is to be overloaded.

        Has to manage incoming messages about subscriptions - and then trigger
        the local management of new un-/subscriptions.
        """
        raise NotImplementedError(  # coverage: disable
            "This function must be overloaded.",
        )

    async def _recover_subscriptions(
        self: ConnectSpotWebsocketBase,
        event: asyncio.Event,
    ) -> None:
        """Function that is to be overloaded.

        Is responsible for recovering subscriptions if the connection was
        closed.
        """
        raise NotImplementedError(  # coverage: disable
            "This function must be overloaded.",
        )


class ConnectSpotWebsocket(ConnectSpotWebsocketBase):
    """
    This class extends the
    :class:`kraken.spot.websocket.connectors.ConnectSpotWebsocketBase` and can
    be instantiated to create and maintain a websocket connection using the
    Kraken Websocket API v2.

    **This is an internal class and should not be used outside.**

    :param client: The websocket client that wants to connect
    :type client: :class:`kraken.spot.SpotWSClientBase`
    :param endpoint: The websocket endpoint
    :type endpoint: str
    :param callback: Callback function that receives the websocket messages
    :type callback: function
    :param is_auth: If the websocket connects to endpoints that require
        authentication (default: ``False``)
    :type is_auth: bool, optional
    """

    def __init__(
        self: ConnectSpotWebsocket,
        client: SpotWSClientBase,
        endpoint: str,
        callback: Callable | None,
        *,
        is_auth: bool = False,
    ) -> None:
        super().__init__(
            client=client,
            endpoint=endpoint,
            callback=callback,
            is_auth=is_auth,
        )

    async def send_ping(self: ConnectSpotWebsocket) -> None:
        """Sends ping to Kraken"""
        await self.socket.send(json.dumps({"method": "ping"}))
        self._last_ping = time()

    async def _recover_subscriptions(
        self: ConnectSpotWebsocket,
        event: asyncio.Event,
    ) -> None:
        """
        Executes the subscribe function for all subscriptions that were  tracked
        locally. This function is called when the connection was closed to
        recover the subscriptions.

        :param event: Event to wait for (so this is only executed when
            it is set to ``True`` - which is when the connection is ready)
        :type event: asyncio.Event
        """
        log_msg: str = (
            f'Recover {"authenticated" if self.is_auth else "public"} subscriptions {self._subscriptions}'
        )
        LOG.info("%s: waiting", log_msg)
        await event.wait()

        for subscription in self._subscriptions:
            await self.client.subscribe(params=subscription)
            LOG.info("%s: OK", subscription)

        LOG.info("%s: done", log_msg)

    def _manage_subscriptions(self: ConnectSpotWebsocket, message: dict) -> None:  # type: ignore[override]
        """
        Checks if the message contains events about un-/subscriptions
        to add or remove these from the list of current tracked subscriptions.

        :param message: The message to check for subscriptions
        :type message: dict
        """
        if message.get("method") == "subscribe":
            if message.get("success") and message.get("result"):
                message = self.__transform_subscription(subscription=message)
                self.__append_subscription(subscription=message["result"])
            else:
                LOG.warning(message)

        elif message.get("method") == "unsubscribe":
            if message.get("success") and message.get("result"):
                message = self.__transform_subscription(subscription=message)
                self.__remove_subscription(subscription=message["result"])
            else:
                LOG.warning(message)

    def __append_subscription(self: ConnectSpotWebsocket, subscription: dict) -> None:
        """
        Appends a subscription to the local list of tracked subscriptions.

        :param subscription: The subscription to append
        :type subscription: dict
        """
        self.__remove_subscription(subscription=subscription)
        self._subscriptions.append(subscription)

    def __remove_subscription(self: ConnectSpotWebsocket, subscription: dict) -> None:
        """
        Removes a subscription from the list of locally tracked subscriptions.

        :param subscription: The subscription to remove.
        :type subscription: dict
        """
        for position, sub in enumerate(self._subscriptions):
            if sub == subscription or (
                subscription.get("channel", False) == sub.get("channel", False)
                and subscription.get("symbol", False) == sub.get("symbol", False)
            ):
                del self._subscriptions[position]
                return

    def __transform_subscription(
        self: ConnectSpotWebsocket,
        subscription: dict,
    ) -> dict:
        """
        Returns a dictionary that can be used to subscribe to a websocket feed.
        This function is most likely used to parse incoming un-/subscription
        messages.

        :param subscription: The raw un-/subscription confirmation
        :type subscription: dict
        :return: The "corrected" subscription
        :rtype: dict
        """
        # Without deepcopy, the passed message will be modified, which is *not*
        # intended.
        subscription_copy: dict = deepcopy(subscription)
        channel: Final[str] = subscription["result"].get("channel", "")

        match channel:
            case "book" | "ticker" | "ohlc" | "trade":
                # Subscriptions for specific symbols must contain the 'symbols'
                # key with a value of type list[str]. The python-kraken-sdk is
                # caching active subscriptions from that moment, the successful
                # response arrives. These responses must be parsed to use them
                # to resubscribe on connection losses.
                if not isinstance(
                    subscription["result"].get("symbol"),
                    list,
                ):
                    subscription_copy["result"]["symbol"] = [
                        subscription_copy["result"]["symbol"],
                    ]
            case "executions":
                # Kraken somehow responds with this key - but this is not
                # accepted when subscribing (Dec 2023).
                if (
                    subscription_copy["method"] in {"subscribe", "unsubscribe"}
                    and "maxratecount" in subscription["result"]
                ):
                    del subscription_copy["result"]["maxratecount"]

        # Sometimes Kraken responds with hints about deprecation - we don't want
        # to save those data as resubscribing would fail for those cases.
        if "warnings" in subscription["result"]:
            del subscription_copy["result"]["warnings"]

        return subscription_copy


__all__ = [
    "ConnectSpotWebsocketBase",
    "ConnectSpotWebsocket",
]
