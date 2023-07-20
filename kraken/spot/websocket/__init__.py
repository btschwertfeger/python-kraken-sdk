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
from typing import Any, Callable, List, Optional, Union

import websockets

from kraken.base_api import KrakenBaseSpotAPI
from kraken.exceptions import KrakenException


class KrakenSpotWSClientBase(KrakenBaseSpotAPI):
    """
    todo: write doc
    """

    LOG: logging.Logger = logging.getLogger(__name__)

    PROD_ENV_URL: str = "ws.kraken.com"
    AUTH_PROD_ENV_URL: str = "ws-auth.kraken.com"
    BETA_ENV_URL: str = "beta-ws.kraken.com"
    AUTH_BETA_ENV_URL: str = "beta-ws-auth.kraken.com"

    def __init__(
        self: "KrakenSpotWSClientBase",
        key: str = "",
        secret: str = "",
        callback: Optional[Callable] = None,
        no_public: bool = False,
        beta: bool = False,
        api_version: str = "v2",
    ) -> None:
        super().__init__(key=key, secret=secret, sandbox=beta)
        self.__setup_api_version(version=api_version)

        self._is_auth: bool = bool(key and secret)
        self.__callback: Optional[Callable] = callback
        self.exception_occur: bool = False

        self._pub_conn: Optional[ConnectSpotWebsocket] = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.PROD_ENV_URL if not beta else self.BETA_ENV_URL,
                is_auth=False,
                callback=self.on_message,
            )
            if not no_public
            else None
        )

        self._priv_conn: Optional[ConnectSpotWebsocket] = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.AUTH_PROD_ENV_URL if not beta else self.AUTH_BETA_ENV_URL,
                is_auth=True,
                callback=self.on_message,
            )
            if self._is_auth
            else None
        )

    # --------------------------------------------------------------------------
    # Internals
    def __setup_api_version(self: "KrakenSpotWSClientBase", version: str) -> None:
        """
        Set up functions and attributes based on the API version.

        :param version: The Websocket API version to use (one of ``v1``, ``v2``)
        :type version: str
        """
        if version == "v1":
            return

        if version == "v2":
            # pylint: disable=invalid-name
            self.PROD_ENV_URL += "/v2"
            self.AUTH_PROD_ENV_URL += "/v2"
            self.BETA_ENV_URL += "/v2"
            self.AUTH_BETA_ENV_URL += "/v2"
            return

        raise ValueError("Version must be one of ``v1``, ``v2``")

    async def on_message(
        self: "KrakenSpotWSClientBase", msg: Union[dict, list]
    ) -> None:
        """
        Calls the defined callback function (if defined) or overload this
        function.

        Can be overloaded as described in :class:`kraken.spot.KrakenSpotWSClient`
        and :class:`kraken.spot.KrakenSpotWSClientV2`.

        :param msg: The message received sent by Kraken via the websocket connection
        :type msg: dict | list
        """
        if self.__callback is not None:
            await self.__callback(msg)
        else:
            self.LOG.warning(
                """
                Received message but no callback is defined! Either use a
                callback when initializing the websocket client or overload
                its ``on_message`` function.
            """
            )
            print(msg)

    async def __aenter__(self: "KrakenSpotWSClientBase") -> "KrakenSpotWSClientBase":
        """Entrypoint for use as context manager"""
        return self

    async def __aexit__(
        self: "KrakenSpotWSClientBase", *exc: tuple, **kwargs: dict
    ) -> None:
        """Exit if used as context manager"""

    def get_ws_token(self: "KrakenSpotWSClientBase") -> dict:
        """
        Get the authentication token to establish the authenticated
        websocket connection.

        - https://docs.kraken.com/rest/#tag/Websockets-Authentication

        :returns: The authentication token
        :rtype: dict
        """
        return self._request(  # type: ignore[return-value]
            "POST", "/private/GetWebSocketsToken"
        )

    def _get_socket(self: "KrakenSpotWSClientBase", private: bool) -> Any:
        """
        Returns the socket or ``None`` if not connected.

        :param private: Return the socket of the public or private connection
        :type private: bool
        :return: The socket
        :rtype: Any
        """
        if private:
            return self._priv_conn.socket
        return self._pub_conn.socket

    @property
    def active_public_subscriptions(
        self: "KrakenSpotWSClientBase",
    ) -> Union[List[dict], Any]:
        """
        Returns the active public subscriptions

        :return: List of active public subscriptions
        :rtype: list[dict] | Any
        :raises ConnectionError: If there is no active public connection.
        """
        if self._pub_conn is not None:
            return self._pub_conn.subscriptions
        raise ConnectionError("Public connection does not exist!")

    @property
    def active_private_subscriptions(
        self: "KrakenSpotWSClientBase",
    ) -> Union[List[dict], Any]:
        """
        Returns the active private subscriptions

        :return: List of active private subscriptions
        :rtype: list[dict] | Any
        :raises ConnectionError: If there is no active private connection
        """
        if self._priv_conn is not None:
            return self._priv_conn.subscriptions
        raise ConnectionError("Private connection does not exist!")

    # --------------------------------------------------------------------------
    # Functions and attributes to overload

    async def send_message(
        self: "KrakenSpotWSClientBase", *args: Any, **kwargs: Any
    ) -> None:
        """
        This functions must be overloaded and should be used to send messages
        via the websocket connection(s).
        """
        raise NotImplementedError("Must be overloaded!")

    async def subscribe(
        self: "KrakenSpotWSClientBase", *args: Any, **kwargs: Any
    ) -> None:
        """
        This function must be overloaded and should be used to subscribe
        to websocket channels/feeds.
        """
        raise NotImplementedError("Must be overloaded!")

    async def unsubscribe(
        self: "KrakenSpotWSClientBase", *args: Any, **kwargs: Any
    ) -> None:
        """
        This function must be overloaded and should be used to unsubscribe
        from websocket channels/feeds.
        """
        raise NotImplementedError("Must be overloaded!")

    @property
    def public_channel_names(self: "KrakenSpotWSClientBase") -> List[str]:
        """
        This function must be overloaded and return a list of names that can be
        subscribed to (for unauthenticated connections).
        """
        raise NotImplementedError("Must be overloaded!")

    @property
    def private_channel_names(self: "KrakenSpotWSClientBase") -> List[str]:
        """
        This function must be overloaded and return a list of names that can be
        subscribed to (for authenticated connections).
        """
        raise NotImplementedError("Must be overloaded!")


class ConnectSpotWebsocket:
    """
    This class is only usd by :class:`kraken.spot.KrakenSpotWSClientBase`
    to establish and handle a websocket connection.

    :param client: The websocket client that wants to connect
    :type client: :class:`kraken.spot.KrakenSpotWSClientBase`
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

        self.__last_ping: Optional[Union[int, float]] = None
        self.socket: Optional[Any] = None
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
                if time() - self.__last_ping > 10:
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
            await self.__callback({"error": "KrakenSpotWSClient: exception_occur"})
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

    def __get_reconnect_wait(
        self: "ConnectSpotWebsocket", attempts: int
    ) -> Union[float, Any]:
        return round(random() * min(60 * 3, (2**attempts) - 1) + 1)

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

    # --------------------------------------------------------------------------
    # todo: where to put these functions?:
    async def send_ping(self: "ConnectSpotWebsocket") -> None:
        """Sends ping to Kraken"""
        await self.socket.send(
            json.dumps(
                {
                    "event": "ping",
                    "reqid": int(time() * 1000),
                }
            )
        )
        self.__last_ping = time()

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
                and sub["subscription"]["name"] in self.__client.private_channel_names
            ):
                cpy["subscription"]["token"] = self.ws_conn_details["token"]
                private = True
            await self.__client.send_message(cpy, private=private)
            self.LOG.info(f"{sub} OK")

        self.LOG.info(
            f'Recovering {"auth" if self.__is_auth else "public"} subscriptions {self.__subscriptions} done.'
        )

    def __build_subscription(self: "ConnectSpotWebsocket", msg: dict) -> dict:
        sub: dict = {"event": "subscribe"}

        if not "subscription" in msg or "name" not in msg["subscription"]:
            raise ValueError("Cannot remove subscription with missing attributes.")
        if (
            msg["subscription"]["name"] in self.__client.public_channel_names
        ):  # public endpoint
            if "pair" in msg:
                sub["pair"] = (
                    msg["pair"] if isinstance(msg["pair"], list) else [msg["pair"]]
                )
            sub["subscription"] = msg["subscription"]
        elif (
            msg["subscription"]["name"] in self.__client.private_channel_names
        ):  # private endpoint
            sub["subscription"] = {"name": msg["subscription"]["name"]}
        else:
            self.LOG.warning(
                "Feed not implemented. Please contact the python-kraken-sdk package author."
            )
        return sub
