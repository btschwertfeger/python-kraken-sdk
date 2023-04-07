Known Issues
============

- :func:`kraken.spot.Trading.cancel_order`: The Kraken docs say that multiple orders can be cancelled - this does not work.
- :func:`kraken.spot.Trading.cancel_order_batch`: This endpoint is broken - Even the provided example in the official Kraken documentation does not work (https://github.com/btschwertfeger/Python-Kraken-SDK/issues/65)
