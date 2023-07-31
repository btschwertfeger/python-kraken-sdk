.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

.. The spot orderbook

Maintain a valid Spot order book
--------------------------------

The following example demonstrate how to use the python-kraken-sdk to retrieve a
valid realtime orderbook. The current implementation of the
:class:`kraken.spot.OrderbookClient` uses the Kraken Spot API v1 but will be
updated soon to use the websocket API v2.

References:
- https://gist.github.com/btschwertfeger/6eea0eeff193f7cd1b262cfce4f0eb51


.. literalinclude:: ../../../examples/spot_orderbook.py
   :language: python
   :linenos:
   :caption: Sample on how to maintain a valid orderbook using the python-kraken-sdk
