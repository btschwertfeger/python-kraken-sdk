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

.. _section-examples:

Usage Examples
==============

The python-kraken-sdk provides lots of functions to easily access most of the
REST and websocket endpoints of the Kraken Crypto Asset Exchange API. Since
these endpoints and their parameters may change, all implemented endpoints are
tested on a regular basis.

The repository of the `python-kraken-sdk`_ provides some example scripts that
demonstrate some of the implemented methods. Please see the sections listed
below.

Projects that use the SDK are listed below:

* https://github.com/btschwertfeger/infinity-grid
* https://github.com/btschwertfeger/kraken-rebalance-bot

.. toctree::
    :maxdepth: 2

    rest_examples/spot_rest_examples.rst
    rest_examples/spot_ws_examples.rst
    rest_examples/xstocks_rest_examples.rst
    market_client_example.ipynb
    rest_examples/futures_ws_examples.rst
    rest_examples/futures_rest_examples.rst
