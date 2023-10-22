.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

.. The spot trading bot templates

Spot Trading Bot Templates
--------------------------

The templates presented below serve as starting points for the development of
a trading algorithms for Spot trading on the cryptocurrency exchange `Kraken`_
using the `python-kraken-sdk`_.

The trading strategy can be implemented using the ``TradingBot`` class. This
class has access to all REST clients and receives all messages that are sent by
the subscribed websocket feeds via the ``on_message`` function.

.. literalinclude:: ../../../../examples/spot_trading_bot_template_v2.py
   :language: python
   :linenos:
   :caption: Template to build a trading bot using the Kraken Spot Websocket API v2

.. literalinclude:: ../../../../examples/spot_trading_bot_template_v1.py
   :language: python
   :linenos:
   :caption: Template to build a trading bot using the Kraken Spot Websocket API v1
