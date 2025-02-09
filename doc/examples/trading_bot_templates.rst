.. -*- mode: rst; coding: utf-8 -*-
..
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. All rights reserved.
.. https://github.com/btschwertfeger
..

.. _section-trading-bot-templates:

Trading Bot Templates
=====================

The `python-kraken-sdk`_ is perfectly suited to develop automated trading
algorithms. To facilitate the start here directly for Spot trading as well as
for the Futures enthusiasts, templates are provided which can serve as the basis
for dynamic trading algorithms. In both cases websockets are used to capture the
live data. In addition REST clients are integrated, so that their endpoints can
also be reached at any time.

For questions, feedback, additions, suggestions or problems
`python-kraken-sdk/discussions`_ or `python-kraken-sdk/issues`_ may be helpful.

.. toctree::
    :maxdepth: 2

    trading_bot_templates/spot_bot_templates.rst
    trading_bot_templates/spot_orderbook.rst
    trading_bot_templates/futures_bot_template.rst
