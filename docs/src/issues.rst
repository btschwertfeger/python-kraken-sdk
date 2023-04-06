Known Issues
============

- :func:`kraken.spot.Trading.cancel_order`: The Kraken docs say that multiple orders can be cancelled - this does not work.
- :func:`kraken.spot.Trading.cancel_order_batch`: Always return error - event the example in the official Kraken documentation returns the same error (https://github.com/btschwertfeger/Python-Kraken-SDK/issues/65)
