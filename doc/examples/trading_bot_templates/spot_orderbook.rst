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

Maintain a valid Spot Orderbook
-------------------------------

The following examples demonstrate how to use the python-kraken-sdk to retrieve
valid realtime orderbooks. The current implementation of the
:class:`kraken.spot.SpotOrderBookClient` uses the websocket API v2.

.. literalinclude:: ../../../examples/spot_orderbook.py
   :language: python
   :linenos:
   :caption: Sample on how to maintain a valid orderbook w/ websocket API

References:
- https://gist.github.com/btschwertfeger/6eea0eeff193f7cd1b262cfce4f0eb51
