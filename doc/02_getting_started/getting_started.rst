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

Getting Started
===============

1. Install the Python module

.. code-block:: bash

    python3 -m pip install python-kraken-sdk


2. Register at Kraken and generate API Keys

- Spot Trading: https://pro.kraken.com/app/settings/api
- Futures Trading: https://futures.kraken.com/trade/settings/api
- Futures Sandbox: https://demo-futures.kraken.com/settings/api

3. Start using the provided example scripts

Examples can be found within the repository of the `python-kraken-sdk`_ and
obviously in this documentation. See the :ref:`section-examples` section for
basic usage examples and :ref:`section-trading-bot-templates` to get impressed
by orderbook clients, as well as boilerplates for trading bots using the SDK.

4. Error handling

If any unexpected behavior occurs, please check **your API permissions**,
**rate limits**, update the `python-kraken-sdk`_, see the
:ref:`section-troubleshooting` section, and if the error persists please open an
issue at `python-kraken-sdk/issues`_.
