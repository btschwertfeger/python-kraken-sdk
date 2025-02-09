.. -*- mode: rst; coding: utf-8 -*-
..
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. All rights reserved.
.. https://github.com/btschwertfeger
..

.. _section-examples:

Usage Examples
==============

The python-kraken-sdk provides lots of functions to easily access most of the
REST and websocket endpoints of the Kraken Cryptocurrency Exchange API. Since
these endpoints and their parameters may change, all implemented endpoints are
tested on a regular basis.

The repository of the `python-kraken-sdk`_ provides some example scripts that
demonstrate some of the implemented methods. Please see the sections listed
below.

Projects that use the SDK are listed below:

* https://github.com/btschwertfeger/kraken-infinity-grid
* https://github.com/btschwertfeger/kraken-rebalance-bot

.. toctree::
    :maxdepth: 2

    rest_ws_samples/spot_rest_examples.rst
    rest_ws_samples/spot_ws_examples.rst
    market_client_example.ipynb
    rest_ws_samples/futures_ws_examples.rst
    rest_ws_samples/futures_rest_examples.rst
