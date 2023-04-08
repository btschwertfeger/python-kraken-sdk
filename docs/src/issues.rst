Known Issues
============

Spot Trading
------------

- :func:`kraken.spot.Trading.cancel_order_batch`: This endpoint is broken - Even the provided example in the official Kraken documentation does not work (https://github.com/btschwertfeger/Python-Kraken-SDK/issues/65)

Futures Trading
---------------

- Krakens API doesnt seem to know the ``trailing_stop`` order type and raises an error if this is type
  is part of an order. This order type is documented here https://docs.futures.kraken.com/#http-api-trading-v3-api-order-management-send-order

  .. code-block:: python
    :linenos:
    :caption: ``trailing_stop`` order type not working in Kraken Futures

    from kraken.futures import Trade

    Trade(key="api-key", secret="secreet-key").create_order(
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
