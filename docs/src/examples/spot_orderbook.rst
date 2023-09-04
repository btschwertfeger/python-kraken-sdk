.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

.. The spot orderbook

Maintain a valid Spot order book
--------------------------------

The following examples demonstrate how to use the python-kraken-sdk to retrieve
valid realtime orderbooks. The current implementation of the
:class:`kraken.spot.OrderbookClientV2` uses the websocket API v2 and
:class:`kraken.spot.OrderbookClientV1` provides the legacy support for websocket
API v2.

.. literalinclude:: ../../../examples/spot_orderbook_v2.py
   :language: python
   :linenos:
   :caption: Sample on how to maintain a valid orderbook w/ websocket API v2


.. literalinclude:: ../../../examples/spot_orderbook_v1.py
   :language: python
   :linenos:
   :caption: Sample on how to maintain a valid orderbook w/ websocket API v1


References:
- https://gist.github.com/btschwertfeger/6eea0eeff193f7cd1b262cfce4f0eb51
