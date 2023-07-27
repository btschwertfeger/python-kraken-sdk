#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
This module provides the Spot websocket client (Websocket API V2 as
documented in - https://docs.kraken.com/websockets-v2).
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Callable, List, Optional

from kraken.base_api import defined
from kraken.exceptions import KrakenException
from kraken.spot.websocket import KrakenSpotWSClientBase


class KrakenSpotWSClientV2(KrakenSpotWSClientBase):
    """
    Class to access public and private/authenticated websocket connections.

    **This client only supports the Kraken Websocket API v2.**

    - https://docs.kraken.com/websockets-v2

    … please use :class:`KrakenSpotWSClient` for accessing the Kraken's
    Websocket API v1.

    This class holds up to two websocket connections, one private
    and one public. The core functionalities are un-/subscribing to websocket
    feeds and sending messages.
    See :func:`kraken.spot.KrakenSpotWSClientV2.subscribe` and
    :func:`kraken.spot.KrakenSpotWSClientV2.send_message` for more information.

    When accessing private endpoints that need authentication make sure,
    that the ``Access WebSockets API`` API key permission is set in the user's
    account. To place or cancel orders, querying ledger information or accessing
    live portfolio changes (fills, new orders, ...) there are separate
    permissions that must be enabled if required.

    :param key: API Key for the Kraken Spot API (default: ``""``)
    :type key: str, optional
    :param secret: Secret API Key for the Kraken Spot API (default: ``""``)
    :type secret: str, optional
    :param url: Set a specific URL to access the Kraken REST API
    :type url: str, optional
    :param no_public: Disables public connection (default: ``False``).
        If not set or set to ``False``, the client will create a public and
        a private connection per default. If only a private connection is
        required, this parameter should be set to ``True``.
    :param beta: Use the beta websocket channels (maybe not supported anymore,
        default: ``False``)
    :type beta: bool

    .. code-block:: python
        :linenos:
        :caption: HowTo: Use the Kraken Spot websocket client (v2)

        import asyncio
        from kraken.spot import KrakenSpotWSClientV2


        class Client(KrakenSpotWSClientV2):

            async def on_message(self, message):
                print(message)


        async def main():

            client = Client()         # unauthenticated
            client_auth = Client(     # authenticated
                key="kraken-api-key",
                secret="kraken-secret-key"
            )

            # subscribe to the desired feeds:
            await client.subscribe(
                params={"channel": "ticker", "symbol": ["BTC/USD"]}
            )
            # from now on the on_message function receives the ticker feed

            while not client.exception_occur:
                await asyncio.sleep(6)

        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass

    .. code-block:: python
        :linenos:
        :caption: HowTo: Use the websocket client (v2) as instance

        import asyncio
        from kraken.spot import KrakenSpotWSClientV2


        async def main():
            async def on_message(message):
                print(message)

            client = KrakenSpotWSClientV2(callback=on_message)
            await client.subscribe(
                params={"channel": "ticker", "symbol": ["BTC/USD"]}
            )

            while not client.exception_occur:
                await asyncio.sleep(10)


        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass


    .. code-block:: python
        :linenos:
        :caption: HowTo: Use the websocket client (v2) as context manager

        import asyncio
        from kraken.spot import KrakenSpotWSClientV2

        async def on_message(message):
            print(message)

        async def main():
            async with KrakenSpotWSClientV2(
                key="api-key",
                secret="secret-key",
                callback=on_message
            ) as session:
                await session.subscribe(
                    params={"channel": "ticker", "symbol": ["BTC/USD"]}
                )

            while True
                await asyncio.sleep(6)


        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass
    """

    def __init__(
        self: KrakenSpotWSClientV2,
        key: str = "",
        secret: str = "",
        callback: Optional[Callable] = None,
        no_public: bool = False,
        beta: bool = False,
    ):
        super().__init__(
            key=key,
            secret=secret,
            callback=callback,
            no_public=no_public,
            beta=beta,
            api_version="v2",
        )

    async def send_message(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2,
        message: dict,
        raw: bool = False,
    ) -> None:
        """
        Sends a message via the websocket connection. For private messages
        the authentication token will be assigned automatically if
        ``raw=False``.

        The user can specify a ``req_d`` within the message to identify
        corresponding responses via websocket feed.

        :param message: The information to send
        :type message: dict
        :param raw: If set to ``True`` the ``message`` will be sent directly.
        :type raw: bool, optional

        The following examples demonstrate how to use the
        :func:`kraken.spot.KrakenSpotWSClientV2.send_message` function. The
        client must be instantiated as described in
        :class:`kraken.spot.KrakenSpotWSClientV2` where ``client`` uses
        public connections (without authentication) and ``client_auth`` must
        be instantiated using valid credentials since only this way placing or
        canceling orders can be done.

        **Please note that the send_message function will automatically
        pass the authentication token (except for the case if** ``raw=True``
        **).**

        **Placing orders** using an authenticated websocket connection can be
        easily done as shown in the example below. See
        https://docs.kraken.com/websockets-v2/#add-order to retrieve more
        information about the available parameters.

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Place a new order

            >>> await client_auth.send_message(
            ...     message={
            ...         "method": "add_order",
            ...         "params": {
            ...             "limit_price": 1234.56,
            ...             "order_type": "limit",
            ...             "order_userref": 123456789,
            ...             "order_qty": 1.0,
            ...             "side": "buy",
            ...             "symbol": "BTC/USD",
            ...         },
            ...     }
            ... )

        **Placing orders as batch** can be done by passing ``batch_add`` as
        method. Its parameters and limitations are described in
        https://docs.kraken.com/websockets-v2/#batch-add.

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Placing orders as batch

            >>> await client_auth.send_message(
            ...     message={
            ...         "method": "batch_add",
            ...         "params": {
            ...             "orders": [
            ...                 {
            ...                     "limit_price": 1000.23,
            ...                     "order_qty": 1,
            ...                     "order_type": "limit",
            ...                     "order_userref": 123456789,
            ...                     "side": "buy",
            ...                 },
            ...                 {
            ...                     "limit_price": 500.21,
            ...                     "order_qty": 2.12345,
            ...                     "order_type": "limit",
            ...                     "order_userref": 212345679,
            ...                     "side": "sell",
            ...                     "stp_type": "cancel_both",
            ...                 },
            ...             ],
            ...             "symbol": "BTC/USD",
            ...             "validate": True,
            ...         },
            ...     }
            ... )

        **Cancel orders as batch** is available using the ``batch_cancel``
        method as described in
        https://docs.kraken.com/websockets-v2/#batch-cancel.

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Cancel orders as batch

            >>> await client_auth.send_message(
            ...     message={
            ...         "method": "batch_cancel",
            ...         "params": {
            ...             "orders": [
            ...                 "123456789",
            ...                 "212345679",
            ...                 "ORDER-ID123-4567890"
            ...             ],
            ...         },
            ...     }
            ... )

        **Cancel all orders** can be used as the name suggests - to cancel
        all open orders (see
        https://docs.kraken.com/websockets-v2/#cancel-all-orders).

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Cancel all orders

            >>> await client_auth.send_message(
            ...     message={
            ...         "method": "cancel_all",
            ...     }
            ... )

        **Death Man's Switch** is a useful utility to reduce the risk of losses
        due to network fuckups since it will cancel all orders if the call
        was not received by Kraken within a certain amount of time. See
        https://docs.kraken.com/websockets-v2/#cancel-all-orders-after for more
        information.

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Death Man's Switch / cancel_all_orders_after

            >>> await client_auth.send_message(
            ...     message={
            ...         "method": "cancel_all_orders_after",
            ...         "params": {"timeout": 60},
            ...     }
            ... )

        **Canceling orders** is a common task during trading and can be done
        as described in https://docs.kraken.com/websockets-v2/#cancel-order.

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Cancel order(s)

            >>> await client_auth.send_message(
            ...     message={
            ...         "method": "cancel_order",
            ...         "params": {
            ...             "order_id": ["ORDER-ID123-456789", "ORDER-ID123-987654"],
            ...         },
            ...     }
            ... )

        **Editing orders** can be done as shown in the example below. See
        https://docs.kraken.com/websockets-v2/#edit-order for more information.

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Cancel order(s)

            >>> await client_auth.send_message(
            ...     message={
            ...         "method": "edit_order",
            ...         "params": {
            ...             "order_id": "ORDER-ID123-456789",
            ...             "order_qty": 2.5,
            ...             "symbol": "BTC/USD",
            ...         },
            ...     }
            ... )

        **Subscribing** to websocket feeds can be done using the send_message
        function but it is recommended to use
        :func:`kraken.spot.KrakenSpotWSClientV2.subscribe` instead.

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Subscribe to a websocket feed

            >>> await client.send_message(
            ...     message={
            ...         "method": "subscribe",
            ...         "params": {"channel": "book", "snapshot": False, "symbol": ["BTC/USD"]},
            ...     }
            ... )
        """
        if not isinstance(message, dict):
            raise TypeError("The ``message`` must be type dict!")

        if not message.get("method") or not isinstance(message["method"], str):
            raise TypeError(
                "The message must contain the ``method`` key with a valid string!"
            )

        # includes also unsubscribe
        if "subscribe" in message["method"]:
            if not message.get("params") or not isinstance(message["params"], dict):
                raise TypeError(
                    "The message must contain the ``params`` key with a value"
                    " as type dict!"
                )
            if not message["params"].get("channel") or not isinstance(
                message["params"]["channel"], str
            ):
                raise TypeError(
                    "The message must contain the ``params`` key that points to"
                    " a dictionary containing the ``channel`` key with a valid"
                    " string!"
                )

        # ----------------------------------------------------------------------

        private: bool = (message["method"] in self.private_methods) or (
            "subscribe" in message["method"]
            and message["params"]
            and message["params"]["channel"] in self.private_channel_names
        )
        if private and not self._is_auth:
            raise KrakenException.KrakenAuthenticationError()

        retries: int = 0
        socket: Any = self._get_socket(private=private)
        while not socket and retries < 12:
            retries += 1
            socket = self._get_socket(private=private)
            await asyncio.sleep(0.4)

        if retries == 12 and not socket:
            raise TimeoutError("Could not get the desired websocket connection!")

        # ----------------------------------------------------------------------

        if raw:
            await socket.send(json.dumps(message))
            return

        # ----------------------------------------------------------------------

        if not message.get("params") and message["method"] in self.private_methods:
            message["params"] = {}

        if private:
            message["params"]["token"] = self._priv_conn.ws_conn_details["token"]

        await socket.send(json.dumps(message))

    async def subscribe(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2, params: dict, req_id: Optional[int] = None
    ) -> None:
        """
        Subscribe to a channel/feed

        Success or failures are sent over the websocket connection and can be
        received via the on_message or callback function.

        When accessing private endpoints and subscription feeds that need
        authentication make sure that the ``Access WebSockets API`` API key
        permission is set in the users Kraken account.

        - https://docs.kraken.com/websockets-v2/#subscribe

        See https://docs.kraken.com/websockets-v2/#channels for all channels.

        **Please note** that this function automatically assigns the ``method``
        key and sets its value to ``subscribe``. The authentication token is
        also assigned automatically, so only the ``params`` are needed here.

        :param params: The subscription message
        :type params: dict
        :param req_id: Identification number that will be added to the
            response message sent by the websocket feed.
        :type req_id: int, optional
        Initialize your client as described in
        :class:`kraken.spot.KrakenSpotWSClientV2` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Subscribe to a websocket feed

            >>> await client.subscribe(
            ...     params={"channel": "ticker", "symbol": ["BTC/USD"]}
            ... )

        """
        payload: dict = {"method": "subscribe"}
        if defined(req_id):
            payload["req_id"] = req_id

        payload["params"] = params

        await self.send_message(message=payload)

    async def unsubscribe(  # pylint: disable=arguments-differ
        self: KrakenSpotWSClientV2, params: dict, req_id: Optional[int] = None
    ) -> None:
        """
        Unsubscribe from a channel/feed

        Success or failures are sent via the websocket connection and can be
        received via the on_message or callback function.

        When accessing private endpoints and subscription feeds that need
        authentication make sure, that the ``Access WebSockets API`` API key
        permission is set in the users Kraken account.

        - https://docs.kraken.com/websockets-v2/#unsubscribe

        :param params: The unsubscription message (only the params part)
        :type params: dict

        Initialize your client as described in
        :class:`kraken.spot.KrakenSpotWSClientV2` to run the following example:

        .. code-block:: python
            :linenos:
            :caption: Spot Websocket v2: Unsubscribe from a websocket feed

            >>> await client.unsubscribe(
            ...     params={"channel": "ticker", "symbol": ["BTC/USD"]}
            ... )
        """
        payload: dict = {"method": "unsubscribe"}
        if defined(req_id):
            payload["req_id"] = req_id

        payload["params"] = params

        await self.send_message(message=payload)

    @property
    def public_channel_names(self: KrakenSpotWSClientV2) -> List[str]:
        """
        Returns the list of valid values for ``channel`` when un-/subscribing
        from/to public feeds without authentication.

        See https://docs.kraken.com/websockets-v2/#channels for all channels.

        The available public channels are listed below:

        - `book <https://docs.kraken.com/websockets-v2/#book>`_
        - `instrument <https://docs.kraken.com/websockets-v2/#instrument>`_
        - `ohlc <https://docs.kraken.com/websockets-v2/#open-high-low-and-close-ohlc>`_
        - `ticker <https://docs.kraken.com/websockets-v2/#ticker>`_
        - `trade <https://docs.kraken.com/websockets-v2/#trade>`_

        :return: List of available public channel names
        :rtype: list[str]
        """
        return ["book", "instrument", "ohlc", "ticker", "trade"]

    @property
    def private_channel_names(self: KrakenSpotWSClientV2) -> List[str]:
        """
        Returns the list of valid values for ``channel`` when un-/subscribing
        from/to private feeds that need authentication.

        See https://docs.kraken.com/websockets-v2/#channels for all channels.

        Currently there is only one private channel (June 2023):

        - `executions <https://docs.kraken.com/websockets-v2/#executions>`_

        :return: List of available private channel names
        :rtype: list[str]
        """
        return ["executions"]

    @property
    def private_methods(self: KrakenSpotWSClientV2) -> List[str]:
        """
        Returns the list of available methods - parameters are  similar to the
        REST API trade methods.

        The available methods and their documentation are listed below (as of
        June 2023):

        - `add_order <https://docs.kraken.com/websockets-v2/#add-order>`_
        - `batch_order <https://docs.kraken.com/websockets-v2/#batch-add>`_
        - `batch_cancel <https://docs.kraken.com/websockets-v2/#batch-cancel>`_
        - `cancel_all <https://docs.kraken.com/websockets-v2/#cancel-all-orders>`_
        - `cancel_all_orders_after <https://docs.kraken.com/websockets-v2/#cancel-all-orders-after>`_
        - `cancel_order <https://docs.kraken.com/websockets-v2/#cancel-order>`_
        - `edit_order <https://docs.kraken.com/websockets-v2/#edit-order>`_

        :return: List of available methods
        :rtype: list[str]
        """
        return [
            "add_order",
            "batch_add",
            "batch_cancel",
            "cancel_all",
            "cancel_all_orders_after",
            "cancel_order",
            "edit_order",
        ]


__all__ = ["KrakenSpotWSClientV2"]
