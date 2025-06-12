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
