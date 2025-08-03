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

python-kraken-sdk
=================

|GitHub badge| |License badge| |PyVersions badge| |Downloads badge|
|CI/CD badge| |codecov badge| |Typing badge|
|OSSF Scorecard| |OSSF Best Practices|
|Release date badge| |Release version badge| |DOI badge|


**This is the documentation of the unofficial Python SDK to interact with the
Kraken Crypto Asset Exchange.**

*Payward Ltd. and Kraken are in no way associated with the authors of this
package and documentation. Please note that this project is independent and not
endorsed by Kraken or Payward Ltd. Users should be aware that they are using
third-party software, and the authors of this project are not responsible for
any issues, losses, or risks associated with its usage.*

This documentation refers to the `python-kraken-sdk`_ and serves to simplify the
application of trading strategies, in which as far as possible all interaction
possibilities with the crypto asset exchange Kraken are implemented, tested
and documented.

- Gladly open an issue on GitHub on make if something is incorrect or missing
  (`python-kraken-sdk/issues`_).
- The output in the examples may differ, as these are only intended as examples
  and may change in the future.
- If a certain endpoint is not reachable, the function
  :func:`kraken.spot.SpotClient.request` or
  :func:`kraken.futures.FuturesClient.request`,
  which is also available in all derived REST clients, can be used to reach an
  endpoint with the appropriate parameters. Here private content can also be
  accessed, provided that either the base class or one of the clients has been
  initialized with valid credentials.
- For Futures there is the websocket client
  :class:`kraken.futures.FuturesWSClient` and for Spot
  :class:`kraken.spot.SpotWSClient`.


Disclaimer
----------

There is no guarantee that this software will work flawlessly at this or later
times. Of course, no responsibility is taken for possible profits or losses.
This software probably has some errors in it, so use it at your own risk. Also
no one should be motivated or tempted to invest assets in speculative forms of
investment. By using this software you release the author(s) from any liability
regarding the use of this software.


Features
--------

General:

- Command-line interface
- Access both public and private, REST and websocket endpoints
- Responsive error handling and custom exceptions
- Extensive examples
- Tested using the `pytest <https://docs.pytest.org/en/7.3.x/>`_ framework
- Releases are permanently archived at `Zenodo <https://zenodo.org/badge/latestdoi/510751854>`_

Available Clients:

- Spot REST Clients (sync and async)
- Spot Websocket Client (Websocket API v2)
- Spot Orderbook Client (Websocket API v2)
- Futures REST Clients (sync and async)
- Futures Websocket Client

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
- Always keep an eye on https://status.kraken.com/ when encountering
  connectivity problems.
- Feel free to open an issue at `python-kraken-sdk/issues`_.

References
----------

- https://python-kraken-sdk.readthedocs.io/en/stable
- https://docs.kraken.com/api/
- https://docs.kraken.com/api/docs/guides/global-intro
- https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API
