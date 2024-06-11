.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

.. _section-examples:

Usage Examples
==============

The python-kraken-sdk provides lots of functions to easily access most of the
REST and websocket endpoints of the Kraken Cryptocurrency Exchange API. Since
these endpoints and their parameters may change, all implemented endpoints are
tested on a regular basis.

If certain parameters or settings are not available, or specific endpoints are
hidden and not implemented, it is always possible to execute requests to the
endpoints directly using the ``request`` method provided by all clients. This
is demonstrated below.

.. code-block:: python
    :linenos:
    :caption: Usage of the basic request method

    from kraken.spot import KrakenSpotBaseAPI

    client = KrakenSpotBaseAPI(key="<your-api-key>", secret="<your-secret-key>")
    print(client.request(method="POST", uri="/0/private/Balance"))

The repository of the `python-kraken-sdk`_ provides some example scripts that
demonstrate some of the implemented methods. Please see the sections listed
below.

.. toctree::
    :maxdepth: 2

    rest_ws_samples/spot_rest_examples.rst
    rest_ws_samples/spot_ws_examples.rst
    market_client_example.ipynb
    rest_ws_samples/futures_ws_examples.rst
    rest_ws_samples/futures_rest_examples.rst

Third-party projects that use the SDK are listed below.

* https://github.com/btschwertfeger/kraken-rebalance-bot
