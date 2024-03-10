.. -*- coding: utf-8 -*-
.. Copyright (C) 2023 Benjamin Thomas Schwertfeger
.. GitHub: https://github.com/btschwertfeger

Introduction
=============

|GitHub badge| |License badge| |PyVersions badge| |Downloads badge|
|CI/CD badge| |codecov badge| |Typing badge|
|Release date badge| |Release version badge| |DOI badge|


**This is the documentation of the unofficial Python SDK to interact with the
Kraken cryptocurrency exchange.**

*Payward Ltd. and Kraken are in no way associated with the authors of this
package and documentation. Please note that this project is independent and not
endorsed by Kraken or Payward Ltd. Users should be aware that they are using
third-party software, and the authors of this project are not responsible for
any issues, losses, or risks associated with its usage.*

This documentation refers to the `python-kraken-sdk`_ and serves to simplify the
application of trading strategies, in which as far as possible all interaction
possibilities with the cryptocurrency exchange Kraken are implemented, tested
and documented.

- Gladly open an issue on GitHub on make if something is incorrect or missing
  (`python-kraken-sdk/issues`_).
- The output in the examples may differ, as these are only intended as examples
  and may change in the future.
- If a certain endpoint is not reachable, the function
  :func:`kraken.base_api.KrakenSpotBaseAPI._request` or
  :func:`kraken.base_api.KrakenFuturesBaseAPI._request`,
  which is also available in all derived REST clients, can be used to reach an
  endpoint with the appropriate parameters. Here private content can also be
  accessed, provided that either the base class or one of the clients has been
  initialized with valid credentials.
- For Futures there is only one websocket client -
  :class:`kraken.futures.KrakenFuturesWSClient`. For Spot there are two:
  :class:`kraken.spot.KrakenSpotWSClientV1` (for API version 1) and
  :class:`kraken.spot.KrakenSpotWSClientV2` (for API version 2).


Disclaimer
-------------

There is no guarantee that this software will work flawlessly at this or later
times. Of course, no responsibility is taken for possible profits or losses.
This software probably has some errors in it, so use it at your own risk. Also
no one should be motivated or tempted to invest assets in speculative forms of
investment. By using this software you release the author(s) from any liability
regarding the use of this software.


Features
--------

Available Clients:

- Spot REST Clients
- Spot Websocket Clients (Websocket API v1 and v2)
- Spot Orderbook Clients (Websocket API v1 and v2)
- Futures REST Clients
- Futures Websocket Client

General:

- access both public and private, REST and websocket endpoints
- responsive error handling and custom exceptions
- extensive examples
- tested using the `pytest <https://docs.pytest.org/en/7.3.x/>`_ framework
- releases are permanently archived at `Zenodo <https://zenodo.org/badge/latestdoi/510751854>`_
- releases before v2.0.0 also support Python 3.7+


Important Notice
-----------------
**ONLY tagged releases are available at PyPI**. The content of the master branch
may not match with the content of the latest release. - Please have a look at
the release specific READMEs and changelogs.

It is also recommended to **pin the used version** to avoid unexpected behavior
on new releases.

.. _section-troubleshooting:

Troubleshooting
---------------
- Check if you downloaded and installed the **latest version** of the
  python-kraken-sdk.
- Check the **permissions of your API keys** and the required permissions on the
  respective endpoints.
- If you get some Cloudflare or **rate limit errors**, please check your
  `Kraken`_ Tier level and maybe apply for a higher rank if required.
- **Use different API keys for different algorithms**, because the nonce
  calculation is based on timestamps and a sent nonce must always be the highest
  nonce ever sent of that API key. Having multiple algorithms using the same
  keys will result in invalid nonce errors.
- Feel free to open an issue at `python-kraken-sdk/issues`_.


References
----------

- https://python-kraken-sdk.readthedocs.io/en/stable
- https://docs.kraken.com/rest
- https://docs.kraken.com/websockets
- https://docs.kraken.com/websockets-v2
- https://docs.futures.kraken.com
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API
