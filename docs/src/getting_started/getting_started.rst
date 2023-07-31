.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

Getting Started
===============

1. Install the Python module

.. code-block:: bash

    python3 -m pip install python-kraken-sdk


2. Register at Kraken and generate API Keys

- Spot Trading: https://www.kraken.com/u/security/api
- Futures Trading: https://futures.kraken.com/trade/settings/api
- Futures Sandbox: https://demo-futures.kraken.com/settings/api

3. Start using the provided example scripts

The examples can be found within the repository of the `python-kraken-sdk`_ and
obviously in this documentation. For trading algorithms templates see the
:ref:`section-trading-bot-templates` section.

4. Error handling

If any unexpected behavior occurs, please check **your API permissions**,
**rate limits**, update the `python-kraken-sdk`_, see the
:ref:`section-troubleshooting` section, and if the error persists please open an
issue at `python-kraken-sdk/issues`_.
