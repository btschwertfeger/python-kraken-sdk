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

Known Issues
============

Issues listed here: `python-kraken-sdk/issues`_

Futures Trading
---------------

- The Kraken API returns 500 - INTERNAL_SERVER_ERROR for some endpoints if
  ``order_id`` or ``orderId``, ``cliOrdId`` seems to work in all cases.
- Kraken's API doesn't seem to know the ``trailing_stop`` order type and raises
  an error if this type is part of an order. This order type is documented here
  https://docs.kraken.com/api/docs/futures-api/trading/send-order

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
