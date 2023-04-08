.. This is the introduction

Introduction
=============

|GitHub badge| |License badge| |PyVersions badge| |Downloads badge|
|CodeQL badge| |CI/CD badge| |codecov badge|
|Release date badge| |Release version badge| |DOI badge|

|Docs stable| |Docs latest|

**This is the documentation of the unofficial Python SDK to interact with the Kraken cryptocurrency exchange. Payward Ltd. and Kraken are in
no way associated with the authors of this module and documentation.**

This documentation refers to the `python-kraken-sdk`_ and serves to simplify the application of trading strategies,
in which as far as possible all interaction possibilities with the cryptocurrency exchange Kraken are implemented, tested and documented.

- Gladly open an issue on github on make if something is incorrect or missing (`python-kraken-sdk/issues`_).
- The ouput in the examples may differ, as these are only intended as examples and may change in the future.
- If a certain endpoint is not reachable, the function :func:`kraken.base_api.KrakenBaseSpotAPI._request` or :func:`kraken.base_api.KrakenBaseFuturesAPI._request`,
  which is also available in all derived REST clients, can be used to reach an endpoint with the appropriate parameters. Here private content can also be accessed,
  provided that either the base class or one of the clients has been initialized with valid credentials.


Disclaimer
-------------

There is no guarantee that this software will work flawlessly at this or later times. Of course,
no responsibility is taken for possible profits or losses. This software probably has some errors in it, so use it at your own risk.
Also no one should be motivated or tempted to invest assets in speculative forms of investment. By using this software you release the author(s)
from any liability regarding the use of this software.


Features
-----------

Clients:

- Spot REST Clients
- Spot Websocket Client
- Futures REST Clients
- Futures Websocket Client

General:

- access both public and private endpoints
- responsive error handling, custom exceptions and logging
- extensive examples
- coding standards like snake case are not always followed to maintain the parameter naming convention of the Kraken API

Important Notice
-----------------
**ONLY tagged releases are availabe at PyPI**. The content of the master branch may not match with the content of the latest release. So please have a look at the release specific READMEs and changelogs.

.. _section-troubleshooting:

Troubleshooting
------------------
- Check if you downloaded and installed the **latest version** of the python-kraken-sdk.
- Check the **permissions of your API keys** and the required permissions on the respective endpoints.
- If you get some cloudflare or **rate limit errors**, please check your Kraken Tier level and maybe apply for a higher rank if required.
- **Use different API keys for different algorithms**, because the nonce calculation is based on timestamps and a sent nonce must always be the highest nonce ever sent of that API key. Having multiple algorithms using the same keys will result in invalid nonce errors.
- Feel free to open an issue at `python-kraken-sdk/issues`_.


References
-------------
- https://docs.kraken.com/rest
- https://docs.kraken.com/websockets
- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API
