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

Spot Trading Bot Templates
--------------------------

The templates presented below serve as starting points for the development of
a trading algorithms for Spot trading on the crypto asset exchange `Kraken`_
using the `python-kraken-sdk`_.

The trading strategy can be implemented using the ``TradingBot`` class. This
class has access to all REST clients and receives all messages that are sent by
the subscribed websocket feeds via the ``on_message`` function.

.. literalinclude:: ../../../examples/spot_trading_bot_template.py
   :language: python
   :linenos:
   :caption: Template to build a trading bot using the Kraken Spot Websocket API v2
