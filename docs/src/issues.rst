.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

Known Issues
============

Issues listed here: `python-kraken-sdk/issues`_

Futures Trading
---------------

- Kraken's API doesn't seem to know the ``trailing_stop`` order type and raises
  an error if this type is part of an order. This order type is documented here
  https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order

  .. code-block:: python
    :linenos:
    :caption: ``trailing_stop`` order type not working in Kraken Futures

    from kraken.futures import Trade

    Trade(key="api-key", secret="secret-key").create_order(
        orderType="trailing_stop",
        size=10,
        side="buy",
        symbol="PI_XBTUSD",
        limitPrice=12000,
        triggerSignal="mark",
        trailingStopDeviationUnit="PERCENT",
        trailingStopMaxDeviation=10,
    )
    """ Output:
    {
        "status": "BAD_REQUEST",
        "result": "error",
        "errors": [{
            "code": 11,
            "message": "invalid order type"
        }],
        "serverTime":"2023-04-07T19:26:41.299Z"
    }
    """"
