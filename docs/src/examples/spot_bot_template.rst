.. The futures trading bot

Spot Trading Bot Example
------------------------

The templates presented below serves as a starting point for the development of
a trading algorithm for Spot trading on the cryptocurrency platform Kraken using
the `python-kraken-sdk`_.

The ``ManagedBot`` class is a helper class that instantiates the trading
strategy. The trading strategy can be implemented using the ``TradingBot``
class. This class has access to all REST clients and receives all messages that
are sent via the subscribed websocket feeds via the ``on_message`` function.

.. literalinclude:: ../../../examples/spot_trading_bot_template_v2.py
   :language: python
   :linenos:
   :caption: Template to build a trading bot using the Kraken Spot Websocket API v2

.. literalinclude:: ../../../examples/spot_trading_bot_template_v1.py
   :language: python
   :linenos:
   :caption: Template to build a trading bot using the Kraken Spot Websocket API v1
