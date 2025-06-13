.. -*- mode: rst; coding: utf-8 -*-
..
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. https://github.com/btschwertfeger
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..     http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..

Futures Trading Bot Template
----------------------------

The template presented below serves as a starting point for the development of
a trading algorithm for trading futures contracts on the cryptocurrency exchange
`Kraken`_ using the `python-kraken-sdk`_.

The trading strategy can be implemented in the ``TradingBot`` class. This class
has access to all REST clients and receives all messages that are sent via the
subscribed websocket feeds via the ``on_message`` function.

.. literalinclude:: ../../../examples/futures_trading_bot_template.py
   :language: python
   :linenos:
   :caption: Template to build a trading bot using the Kraken Futures Websocket API
