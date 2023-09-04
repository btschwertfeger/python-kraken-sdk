.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

The Base Clients and Internals
==============================

The following classes and data structures are listed for completeness. Please
avoid using them, since these are internals and may change without any warning.

They are the base classes for Spot and Futures REST and websocket clients.

.. autoclass:: kraken.base_api.KrakenSpotBaseAPI
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.base_api.KrakenFuturesBaseAPI
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.spot.websocket.KrakenSpotWSClientBase
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.spot.websocket.connectors.ConnectSpotWebsocketV1
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.spot.websocket.connectors.ConnectSpotWebsocketV2
   :members:
   :show-inheritance:
   :inherited-members:
