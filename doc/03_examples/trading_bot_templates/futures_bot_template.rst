.. -*- mode: rst; coding: utf-8 -*-
..
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. https://github.com/btschwertfeger
..
.. SPDX-License-Identifier: Apache-2.0
..

Futures Trading Bot Template
----------------------------

The template presented below serves as a starting point for the development of
a trading algorithm for trading futures contracts on the crypto asset exchange
`Kraken`_ using the `python-kraken-sdk`_.

The trading strategy can be implemented in the ``TradingBot`` class. This class
has access to all REST clients and receives all messages that are sent via the
subscribed websocket feeds via the ``on_message`` function.

.. literalinclude:: ../../../examples/futures_trading_bot_template.py
   :language: python
   :linenos:
   :caption: Template to build a trading bot using the Kraken Futures Websocket API
