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

.. _section-xstocks-rest-examples:

xStocks REST
------------

The examples presented below serve to demonstrate the usage of the Spot
REST clients provided by `python-kraken-sdk`_ to access `Kraken`_'s REST API for
trading xStocks.

For questions, feedback, additions, suggestions for improvement or problems
`python-kraken-sdk/discussions`_ or `python-kraken-sdk/issues`_ may be helpful.

See https://docs.kraken.com/api/docs/guides/global-intro for information about
the available endpoints and their usage.

.. literalinclude:: ../../../examples/xstocks_examples.py
   :language: python
   :linenos:
   :caption: Example usage of Spot REST client for xStocks
