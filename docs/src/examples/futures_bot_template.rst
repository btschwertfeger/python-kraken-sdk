.. The futures trading bot

Futures Trading Bot Example
----------------------------

The template presented below serves as a starting point for the development of a trading algorithm for
trading futures contracts on the cryptocurrency platform Kraken using the
`python-kraken-sdk`_.

The ``ManagedBot`` class is a helper class that instantiates the trading strategy. The trading strategy
can be implemented in the ``TradingBot`` class. This class has access to all REST clients and gets
gets via the ``on_message`` method all messages that are sent via the subscribed websocket feeds.

This is the starting point from which a strategy can be implemented and applied.

.. literalinclude:: ../../../examples/futures_trading_bot_template.py
   :language: python
   :linenos:
