.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

Base Clients and Internals
==========================

The following classes and data structures are listed for completeness. Please
avoid using them since these are internals and may change without any warning.

They are the base classes for Spot and Futures REST and websocket clients.

.. autoclass:: kraken.base_api.SpotClient
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.base_api.SpotAsyncClient
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.base_api.FuturesClient
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.base_api.FuturesAsyncClient
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.spot.websocket.SpotWSClientBase
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: kraken.spot.websocket.connectors.ConnectSpotWebsocket
   :members:
   :show-inheritance:
   :inherited-members:
