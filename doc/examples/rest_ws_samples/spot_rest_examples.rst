.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

.. _section-spot-rest-examples:

Spot REST
---------

The examples presented below serve to demonstrate the usage of the Spot
REST clients provided by `python-kraken-sdk`_ to access `Kraken`_'s REST API.

For questions, feedback, additions, suggestions for improvement or problems
`python-kraken-sdk/discussions`_ or `python-kraken-sdk/issues`_ may be helpful.

See https://docs.kraken.com/api/docs/guides/global-intro for information about
the available endpoints and their usage.

The Spot client provides access to all un-and authenticated endpoints of
Kraken's Spot and NFT API.

.. code-block:: python
   :linenos:
   :caption: Example: Spot Client Usage (1)

   from kraken.spot import SpotClient

   client = SpotClient(key="<your-api-key>", secret="<your-secret-key>")
   print(client.request("POST", "/0/private/Balance"))

The async Spot client allows for asynchronous access to Kraken's Spot and NFT
API endpoints. Below are two examples demonstrating its usage.

Using SpotAsyncClient without a context manager; In this example, the client is
manually closed after the request is made.

.. code-block:: python
   :linenos:
   :caption: Example: Spot Client Usage (2)

   import asyncio
   from kraken.spot import SpotAsyncClient

   async def main():
      client = SpotAsyncClient(key="<your-api-key>", secret="<your-secret-key>")
      try:
         response = await client.request("POST", "/0/private/Balance")
         print(response)
      finally:
         await client.async_close()

   asyncio.run(main())

Using SpotAsyncClient as context manager; This example demonstrates the use of
the context manager, which ensures the client is automatically closed after the
request is completed.

.. code-block:: python
   :linenos:
   :caption: Example: Spot Client Usage (3)

   import asyncio
   from kraken.spot import SpotAsyncClient

   async def main():
      async with SpotAsyncClient(key="<your-api-key>", secret="<your-secret-key>")as client:
         response = await client.request("POST", "/0/private/Balance")
         print(response)

   asyncio.run(main())

The following legacy examples are not maintained on a regular basis. They serve
only for demonstration purposes - make sure to checkout the documentation of the
individual functions.

.. literalinclude:: ../../../examples/spot_examples.py
   :language: python
   :linenos:
   :caption: Example usage of Spot REST clients
