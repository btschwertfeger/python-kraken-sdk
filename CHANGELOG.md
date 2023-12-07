# Changelog

## [Unreleased](https://github.com/btschwertfeger/python-kraken-sdk/tree/HEAD)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v2.0.0...HEAD)

**Implemented enhancements:**

- Add `start`, `end`, and `cursor` parameters to `kraken.spot.Funding.get_recent_withdraw_status` [\#176](https://github.com/btschwertfeger/python-kraken-sdk/issues/176)
- Add `withdraw_methods` and `withdraw_addresses` to `kraken.spot.Funding` [\#174](https://github.com/btschwertfeger/python-kraken-sdk/issues/174)
- Add `start`, `end`, and `cursor` parameters to `kraken.spot.Funding.get_recent_withdraw_status` [\#177](https://github.com/btschwertfeger/python-kraken-sdk/pull/177) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "Add `withdraw_methods` and `withdraw_addresses` to `kraken.spot.Funding`" [\#175](https://github.com/btschwertfeger/python-kraken-sdk/pull/175) ([btschwertfeger](https://github.com/btschwertfeger))

## [v2.0.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v2.0.0) (2023-10-22)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.6.2...v2.0.0)

**Breaking changes:**

- Extract the Kraken\* exception classes from `kraken.exceptions.KrakenException` [\#161](https://github.com/btschwertfeger/python-kraken-sdk/issues/161)
- Rename `KrakenBaseSpotAPI` to `KrakenSpotBaseAPI` and `KrakenBaseFuturesAPI` to `KrakenFuturesBaseAPI` [\#158](https://github.com/btschwertfeger/python-kraken-sdk/issues/158)
- Rename `kraken.spot.KrakenSpotWSClient` to `kraken.spot.KrakenSpotWSClientV1` [\#152](https://github.com/btschwertfeger/python-kraken-sdk/issues/152)
- Add the legacy OrderbookClient for Krakens websocket API v1 [\#150](https://github.com/btschwertfeger/python-kraken-sdk/issues/150)
- Drop Support for Python \< 3.11 [\#132](https://github.com/btschwertfeger/python-kraken-sdk/issues/132)
- Resolve "Extract the Kraken\* exception classes from `kraken.exceptions.KrakenException`" [\#162](https://github.com/btschwertfeger/python-kraken-sdk/pull/162) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "Rename `kraken.spot.KrakenSpotWSClient` to `kraken.spot.KrakenSpotWSClientV1`" [\#160](https://github.com/btschwertfeger/python-kraken-sdk/pull/160) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "Rename `KrakenBaseSpotAPI` to `KrakenSpotBaseAPI` and `KrakenBaseFuturesAPI` to `KrakenFuturesBaseAPI`" [\#159](https://github.com/btschwertfeger/python-kraken-sdk/pull/159) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "Drop Support for Python \< 3.11" [\#157](https://github.com/btschwertfeger/python-kraken-sdk/pull/157) ([btschwertfeger](https://github.com/btschwertfeger))

**Implemented enhancements:**

- Add `max_fee` parameter to `kraken.spot.Funding.withdraw_funds` [\#169](https://github.com/btschwertfeger/python-kraken-sdk/issues/169)
- Add `start`, `end`, and `cursor` parameters to `kraken.spot.Funding.get_recent_deposits_status` [\#168](https://github.com/btschwertfeger/python-kraken-sdk/issues/168)
- Add optional `extra_params` to any requesting function [\#154](https://github.com/btschwertfeger/python-kraken-sdk/issues/154)
- Resolve "Add `max_fee` parameter to `kraken.spot.Funding.withdraw_funds`" [\#171](https://github.com/btschwertfeger/python-kraken-sdk/pull/171) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "Add `start`, `end`, and `cursor` parameters to `kraken.spot.Funding.get_recent_deposits_status`" [\#170](https://github.com/btschwertfeger/python-kraken-sdk/pull/170) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "Add optional `extra_params` to any requesting function" [\#155](https://github.com/btschwertfeger/python-kraken-sdk/pull/155) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "150 add the legacy OrderbookClient for Krakens websocket API v1" [\#151](https://github.com/btschwertfeger/python-kraken-sdk/pull/151) ([btschwertfeger](https://github.com/btschwertfeger))

**Closed issues:**

- Use Apache 2.0 license instead of GNU GPLv3 [\#166](https://github.com/btschwertfeger/python-kraken-sdk/issues/166)
- Uniform the "msg" parameter [\#163](https://github.com/btschwertfeger/python-kraken-sdk/issues/163)

Uncategorized merged pull requests:

- Adjust docstrings and documentation [\#172](https://github.com/btschwertfeger/python-kraken-sdk/pull/172) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "Use Apache 2.0 license instead of GNU GPLv3" [\#167](https://github.com/btschwertfeger/python-kraken-sdk/pull/167) ([btschwertfeger](https://github.com/btschwertfeger))
- Apply hints suggested by the ruff linter [\#165](https://github.com/btschwertfeger/python-kraken-sdk/pull/165) ([btschwertfeger](https://github.com/btschwertfeger))
- Resolve "163 uniform the msg parameter" [\#164](https://github.com/btschwertfeger/python-kraken-sdk/pull/164) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.6.2](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.6.2) (2023-08-31)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.6.1...v1.6.2)

**Fixed bugs:**

- `kraken.spot.OrderbookClient` is not able to resubscribe to book feeds after connection lost [\#148](https://github.com/btschwertfeger/python-kraken-sdk/issues/148)

Uncategorized merged pull requests:

- Bump Pre-Commit hook versions and adjust typing [\#146](https://github.com/btschwertfeger/python-kraken-sdk/pull/146) ([btschwertfeger](https://github.com/btschwertfeger))
- Fix "`kraken.spot.OrderbookClient` is not able to resubscribe to book feeds after connection lost" [\#149](https://github.com/btschwertfeger/python-kraken-sdk/pull/149) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.6.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.6.1) (2023-08-07)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.6.0...v1.6.1)

**Fixed bugs:**

- Adjust logging and examples; add PyLint check [\#144](https://github.com/btschwertfeger/python-kraken-sdk/pull/144) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.6.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.6.0) (2023-08-01)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.5.0...v1.6.0)

**Breaking changes:**

- Integrate Websockets API v2 [\#130](https://github.com/btschwertfeger/python-kraken-sdk/issues/130)
- Integrate and apply ruff [\#142](https://github.com/btschwertfeger/python-kraken-sdk/pull/142) ([btschwertfeger](https://github.com/btschwertfeger))
- Let `kraken.spot.OrderbookClient` use Spot Websocket API v2 [\#139](https://github.com/btschwertfeger/python-kraken-sdk/pull/139) ([btschwertfeger](https://github.com/btschwertfeger))
- Integrate Kraken Websockets API v2; add `kraken.spot.KrakenSpotWebsocketClientV2`; internals [\#131](https://github.com/btschwertfeger/python-kraken-sdk/pull/131) ([btschwertfeger](https://github.com/btschwertfeger))

**Implemented enhancements:**

- Let `kraken.spot.OrderbookClient` use the Spot Websocket API v2 [\#133](https://github.com/btschwertfeger/python-kraken-sdk/issues/133)
- Add `/private/AccountTransfer` endpoint to `kraken.spot.User` [\#128](https://github.com/btschwertfeger/python-kraken-sdk/issues/128)
- Add `/private/AccountTransfer` endpoint -\> `kraken.spot.User.account_transfer` [\#129](https://github.com/btschwertfeger/python-kraken-sdk/pull/129) ([btschwertfeger](https://github.com/btschwertfeger))

**Closed issues:**

- Use ruff instead of pylint and friends [\#140](https://github.com/btschwertfeger/python-kraken-sdk/issues/140)
- The content of `.pylintrc` can be moved into `pyproject.toml` [\#136](https://github.com/btschwertfeger/python-kraken-sdk/issues/136)
- Build the package also on Windows within the CI [\#134](https://github.com/btschwertfeger/python-kraken-sdk/issues/134)

Uncategorized merged pull requests:

- Merge `.pylintrc` and `pyproject.toml` [\#137](https://github.com/btschwertfeger/python-kraken-sdk/pull/137) ([btschwertfeger](https://github.com/btschwertfeger))
- Enable Windows builds within the CI [\#135](https://github.com/btschwertfeger/python-kraken-sdk/pull/135) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.5.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.5.0) (2023-07-16)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.4.1...v1.5.0)

**Breaking changes:**

- `kraken.spot.OrderbookClient`: add timestamps to book's ask and bid values [\#124](https://github.com/btschwertfeger/python-kraken-sdk/pull/124) ([btschwertfeger](https://github.com/btschwertfeger))

Uncategorized merged pull requests:

- Adjust project properties [\#123](https://github.com/btschwertfeger/python-kraken-sdk/pull/123) ([btschwertfeger](https://github.com/btschwertfeger))
- Add "Question" issue template [\#122](https://github.com/btschwertfeger/python-kraken-sdk/pull/122) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.4.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.4.1) (2023-06-28)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.4.0...v1.4.1)

**Fixed bugs:**

- `kraken.spot.Market.get_recent_trades`: 'since' parameter does not work [\#119](https://github.com/btschwertfeger/python-kraken-sdk/issues/119)
- Fix `kraken.spot.Market.get_recent_trades` parameter 'since' [\#120](https://github.com/btschwertfeger/python-kraken-sdk/pull/120) ([btschwertfeger](https://github.com/btschwertfeger))

**Closed issues:**

- Create `.github/release.yaml` [\#108](https://github.com/btschwertfeger/python-kraken-sdk/issues/108)

## [v1.4.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.4.0) (2023-06-16)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.3.0...v1.4.0)

**Implemented enhancements:**

- Add the `truncate` parameter to `create_order` of the Spot websocket client [\#111](https://github.com/btschwertfeger/python-kraken-sdk/issues/111)
- Add a Spot Orderbook client that handles a realtime order book [\#104](https://github.com/btschwertfeger/python-kraken-sdk/issues/104)
- A the Spot order book client \(`kraken.spot.OrderbookClient`\) [\#106](https://github.com/btschwertfeger/python-kraken-sdk/pull/106) ([btschwertfeger](https://github.com/btschwertfeger))
- Add the `truncate` parameter to the Spot websocket clients' `create_order` and `cancel_order`+ `kraken.spot.Trade.edit_order` [\#113](https://github.com/btschwertfeger/python-kraken-sdk/pull/113) ([btschwertfeger](https://github.com/btschwertfeger))

**Fixed bugs:**

- user.get_trade_volume\(\) says it supports multiple currencies as a list, but it does not seem to. [\#115](https://github.com/btschwertfeger/python-kraken-sdk/issues/115)
- kraken.exceptions.KrakenException.KrakenInvalidNonceError: An invalid nonce was supplied. [\#114](https://github.com/btschwertfeger/python-kraken-sdk/issues/114)

Uncategorized merged pull requests:

- Update `/examples/spot_orderbook.py` [\#110](https://github.com/btschwertfeger/python-kraken-sdk/pull/110) ([btschwertfeger](https://github.com/btschwertfeger))
- Create `release.yaml` [\#116](https://github.com/btschwertfeger/python-kraken-sdk/pull/116) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.3.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.3.0) (2023-05-24)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.2.0...v1.3.0)

**Breaking changes:**

- Rename `kraken.futures.User.get_unwindqueue` to `kraken.futures.User.get_unwind_queue` [\#107](https://github.com/btschwertfeger/python-kraken-sdk/issues/107)
- Prepare release v1.3.0 [\#99](https://github.com/btschwertfeger/python-kraken-sdk/pull/99) ([btschwertfeger](https://github.com/btschwertfeger))
- Change `kraken.spot.User.get_balances` and add `kraken.spot.User.get_balance` [\#98](https://github.com/btschwertfeger/python-kraken-sdk/pull/98) ([btschwertfeger](https://github.com/btschwertfeger))
- Rename `get_tradeable_asset_pair` to `get_asset_pairs` and make the `pair` parameter optional [\#93](https://github.com/btschwertfeger/python-kraken-sdk/pull/93) ([btschwertfeger](https://github.com/btschwertfeger))
- Extend typing + add `KrakenUnknownMethodError` and `KrakenBadRequestError` + Fix \#65 [\#87](https://github.com/btschwertfeger/python-kraken-sdk/pull/87) ([btschwertfeger](https://github.com/btschwertfeger))

**Implemented enhancements:**

- `kraken.spot.Trade.create_order`: Ability to use floats as trade amounts or prices [\#94](https://github.com/btschwertfeger/python-kraken-sdk/issues/94)
- /public/AssetPairs would be nice. [\#90](https://github.com/btschwertfeger/python-kraken-sdk/issues/90)
- Improve caching [\#102](https://github.com/btschwertfeger/python-kraken-sdk/pull/102) ([btschwertfeger](https://github.com/btschwertfeger))
- Add the `truncate` parameter to `kraken.spot.Trade.create_order` [\#95](https://github.com/btschwertfeger/python-kraken-sdk/pull/95) ([btschwertfeger](https://github.com/btschwertfeger))

**Fixed bugs:**

- `kraken.spot.User(...).get_balances('ZUSD')` silently does the wrong thing. [\#88](https://github.com/btschwertfeger/python-kraken-sdk/issues/88)
- `kraken.spot.Trade.cancel_order_batch` endpoint in Spot trading does not work. `{'error': ['EAPI:Bad request']}` [\#65](https://github.com/btschwertfeger/python-kraken-sdk/issues/65)

**Closed issues:**

- Add a realtime Spot order book example [\#103](https://github.com/btschwertfeger/python-kraken-sdk/issues/103)
- `kraken.spot.Trade.create_order`: documentatoin for txid outdated. [\#96](https://github.com/btschwertfeger/python-kraken-sdk/issues/96)
- Create `CONTRIBUTING.md` [\#91](https://github.com/btschwertfeger/python-kraken-sdk/issues/91)
- Extend the typing - using mypy [\#84](https://github.com/btschwertfeger/python-kraken-sdk/issues/84)

Uncategorized merged pull requests:

- Create a contribution guideline [\#92](https://github.com/btschwertfeger/python-kraken-sdk/pull/92) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.2.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.2.0) (2023-05-09)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.1.0...v1.2.0)

**Breaking changes:**

- \(inconsistent spelling/typo\) recend --\> recent in kraken.spot [\#77](https://github.com/btschwertfeger/python-kraken-sdk/issues/77)
- Add API rate limit exception; extend test doc strings [\#79](https://github.com/btschwertfeger/python-kraken-sdk/pull/79) ([btschwertfeger](https://github.com/btschwertfeger))
- Fix bug/typo: "recend" -\> recent throughout kraken.spot [\#76](https://github.com/btschwertfeger/python-kraken-sdk/pull/76) ([jcr-jeff](https://github.com/jcr-jeff))

**Implemented enhancements:**

- Let clients be used as context manager [\#81](https://github.com/btschwertfeger/python-kraken-sdk/issues/81)
- Enable trading on Futures subaccount [\#72](https://github.com/btschwertfeger/python-kraken-sdk/issues/72)
- Check if trading is enabled for Futures subaccount [\#71](https://github.com/btschwertfeger/python-kraken-sdk/issues/71)
- Optionally disable the custom KrakenErrors [\#69](https://github.com/btschwertfeger/python-kraken-sdk/issues/69)
- Let REST and websocket clients be used as context manager [\#83](https://github.com/btschwertfeger/python-kraken-sdk/pull/83) ([btschwertfeger](https://github.com/btschwertfeger))
- Disable custom Kraken exceptions \(optional\) [\#82](https://github.com/btschwertfeger/python-kraken-sdk/pull/82) ([btschwertfeger](https://github.com/btschwertfeger))
- Add Futures user endpoints: `check_trading_enabled_on_subaccount` and `set_trading_on_subaccount` [\#80](https://github.com/btschwertfeger/python-kraken-sdk/pull/80) ([btschwertfeger](https://github.com/btschwertfeger))

**Fixed bugs:**

- Release workflow skips the PyPI publish [\#67](https://github.com/btschwertfeger/python-kraken-sdk/issues/67)
- Fix PyPI upload job + extend disclaimer [\#70](https://github.com/btschwertfeger/python-kraken-sdk/pull/70) ([btschwertfeger](https://github.com/btschwertfeger))
- Fix and extend release workflow [\#68](https://github.com/btschwertfeger/python-kraken-sdk/pull/68) ([btschwertfeger](https://github.com/btschwertfeger))
- Fixed bug where `spot.user.get_balances` floats to periodic X.9999... [\#78](https://github.com/btschwertfeger/python-kraken-sdk/pull/78) ([btschwertfeger](https://github.com/btschwertfeger))

Uncategorized merged pull requests:

- Split the unit tests into individual files [\#75](https://github.com/btschwertfeger/python-kraken-sdk/pull/75) ([btschwertfeger](https://github.com/btschwertfeger))
- Removed matrix from CodeQL job [\#74](https://github.com/btschwertfeger/python-kraken-sdk/pull/74) ([btschwertfeger](https://github.com/btschwertfeger))
- Add a Changelog [\#73](https://github.com/btschwertfeger/python-kraken-sdk/pull/73) ([btschwertfeger](https://github.com/btschwertfeger))
- Updated changelog to match v1.2.0 [\#86](https://github.com/btschwertfeger/python-kraken-sdk/pull/86) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.1.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.1.0) (2023-04-08)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.0.1...v1.1.0)

**Breaking changes:**

- Move `kraken.exceptions.exceptions.KrakenExceptions` to `kraken.exceptions.KrakenException` [\#66](https://github.com/btschwertfeger/python-kraken-sdk/issues/66)
- Remove the unnecessary `client` module when importing the clients [\#57](https://github.com/btschwertfeger/python-kraken-sdk/issues/57)

**Implemented enhancements:**

- Add `trailingStopDeviationUnit` and `trailingStopMaxDeviation` to the Futures `create_order` method [\#64](https://github.com/btschwertfeger/python-kraken-sdk/issues/64)
- Create a documentation for the package [\#58](https://github.com/btschwertfeger/python-kraken-sdk/issues/58)
- Publish to production PyPI if a new release was created via Github UI [\#51](https://github.com/btschwertfeger/python-kraken-sdk/issues/51)
- Upload development releases to test.pypi.org within the CI [\#50](https://github.com/btschwertfeger/python-kraken-sdk/issues/50)
- Use reusable workflows [\#49](https://github.com/btschwertfeger/python-kraken-sdk/issues/49)
- Rework workflows for CI/CD [\#53](https://github.com/btschwertfeger/python-kraken-sdk/pull/53) ([btschwertfeger](https://github.com/btschwertfeger))
- Removed raising exception when currency not found in portfolio [\#47](https://github.com/btschwertfeger/python-kraken-sdk/pull/47) ([btschwertfeger](https://github.com/btschwertfeger))

**Fixed bugs:**

- Cannot access private historical events of the Futures Market client [\#62](https://github.com/btschwertfeger/python-kraken-sdk/issues/62)
- Avoid raising ValueError in `get_balance` if currency is not found in the portfolio [\#46](https://github.com/btschwertfeger/python-kraken-sdk/issues/46)

**Closed issues:**

- Change the default value of the futures dead mans switch to zero [\#63](https://github.com/btschwertfeger/python-kraken-sdk/issues/63)
- Create a workflow that builds the documentation [\#60](https://github.com/btschwertfeger/python-kraken-sdk/issues/60)
- Extend the docstrings with parameter description and examples [\#55](https://github.com/btschwertfeger/python-kraken-sdk/issues/55)
- Add a workflow or jobs that run all tests before a merge is done [\#54](https://github.com/btschwertfeger/python-kraken-sdk/issues/54)
- Move from setup.py to pyroject.toml [\#45](https://github.com/btschwertfeger/python-kraken-sdk/issues/45)

Uncategorized merged pull requests:

- Prepare Release v1.1.0 [\#61](https://github.com/btschwertfeger/python-kraken-sdk/pull/61) ([btschwertfeger](https://github.com/btschwertfeger))
- 57 remove the unnecessary `client` when importing clients [\#59](https://github.com/btschwertfeger/python-kraken-sdk/pull/59) ([btschwertfeger](https://github.com/btschwertfeger))
- 54 add a workflow or jobs that run all tests before a merge is done [\#56](https://github.com/btschwertfeger/python-kraken-sdk/pull/56) ([btschwertfeger](https://github.com/btschwertfeger))
- Moved from setup.py only to pyproject.toml [\#52](https://github.com/btschwertfeger/python-kraken-sdk/pull/52) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.0.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.0.1) (2023-03-27)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.0.0...v1.0.1)

**Implemented enhancements:**

- Use workflow_dispatch to only trigger tests \< python3.11 if really wanted [\#42](https://github.com/btschwertfeger/python-kraken-sdk/issues/42)
- Add subaccount Spot REST Endpoints [\#36](https://github.com/btschwertfeger/python-kraken-sdk/issues/36)
- Use workflow_dispatch to only trigger tests with python\<python3.11 manually [\#43](https://github.com/btschwertfeger/python-kraken-sdk/pull/43) ([btschwertfeger](https://github.com/btschwertfeger))
- Apply pre-commit and adjust workflows [\#35](https://github.com/btschwertfeger/python-kraken-sdk/pull/35) ([btschwertfeger](https://github.com/btschwertfeger))

**Fixed bugs:**

- Pull request workflows fail in test stage [\#41](https://github.com/btschwertfeger/python-kraken-sdk/issues/41)
- Missing consolidate_trades paramater in Spot REST in User get_orders_info [\#39](https://github.com/btschwertfeger/python-kraken-sdk/issues/39)
- Missing reduce_only parameter in Spot REST create_order [\#38](https://github.com/btschwertfeger/python-kraken-sdk/issues/38)
- Status methods does not require the asset anymore [\#37](https://github.com/btschwertfeger/python-kraken-sdk/issues/37)
- Apply kraken api changelog until mar 27 2023 [\#40](https://github.com/btschwertfeger/python-kraken-sdk/pull/40) ([btschwertfeger](https://github.com/btschwertfeger))

**Closed issues:**

- Missing package \(dotenv\) in requirements.txt [\#33](https://github.com/btschwertfeger/python-kraken-sdk/issues/33)

Uncategorized merged pull requests:

- examples now use os.getenv instead of python-dotenv [\#34](https://github.com/btschwertfeger/python-kraken-sdk/pull/34) ([btschwertfeger](https://github.com/btschwertfeger))
- Release v1.0.1 [\#44](https://github.com/btschwertfeger/python-kraken-sdk/pull/44) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.0.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.0.0) (2023-03-04)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.8.0...v1.0.0)

**Implemented enhancements:**

- Extended CI/CD [\#31](https://github.com/btschwertfeger/python-kraken-sdk/pull/31) ([btschwertfeger](https://github.com/btschwertfeger))

Uncategorized merged pull requests:

- Extend unittests [\#32](https://github.com/btschwertfeger/python-kraken-sdk/pull/32) ([btschwertfeger](https://github.com/btschwertfeger))
- Add unit tests \#2 [\#30](https://github.com/btschwertfeger/python-kraken-sdk/pull/30) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.8.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.8.0) (2023-02-18)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.7...v0.8.0)

Uncategorized merged pull requests:

- Add unit tests [\#29](https://github.com/btschwertfeger/python-kraken-sdk/pull/29) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.7.7](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.7) (2022-12-29)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.6...v0.7.7)

## [v0.7.6](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.6) (2022-12-01)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.4...v0.7.6)

## [v0.7.4](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.4) (2022-11-29)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.5...v0.7.4)

## [v0.7.5](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.5) (2022-11-27)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.3...v0.7.5)

## [v0.7.3](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.3) (2022-11-26)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.2...v0.7.3)

Uncategorized merged pull requests:

- Add exceptions [\#28](https://github.com/btschwertfeger/python-kraken-sdk/pull/28) ([btschwertfeger](https://github.com/btschwertfeger))
- Create CODE_OF_CONDUCT.md [\#27](https://github.com/btschwertfeger/python-kraken-sdk/pull/27) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.7.2](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.2) (2022-11-24)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.1...v0.7.2)

## [v0.7.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.1) (2022-11-23)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7...v0.7.1)

**Implemented enhancements:**

- add futures websocket endpoints [\#21](https://github.com/btschwertfeger/python-kraken-sdk/issues/21)

Uncategorized merged pull requests:

- Optimized websocket clients [\#26](https://github.com/btschwertfeger/python-kraken-sdk/pull/26) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.7](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7) (2022-11-22)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.6.1...v0.7)

**Implemented enhancements:**

- add futures trade endpoints [\#20](https://github.com/btschwertfeger/python-kraken-sdk/issues/20)

Uncategorized merged pull requests:

- Add testing [\#25](https://github.com/btschwertfeger/python-kraken-sdk/pull/25) ([btschwertfeger](https://github.com/btschwertfeger))
- implemented Futures WS Client; adjust spot ws client [\#24](https://github.com/btschwertfeger/python-kraken-sdk/pull/24) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.6.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.6.1) (2022-11-20)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.4.2...v0.6.1)

Uncategorized merged pull requests:

- Add futures clients [\#23](https://github.com/btschwertfeger/python-kraken-sdk/pull/23) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.5.4.2](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5.4.2) (2022-11-09)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.4...v0.5.4.2)

## [v0.5.4](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5.4) (2022-10-13)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.2...v0.5.4)

## [v0.5.2](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5.2) (2022-09-18)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.1...v0.5.2)

**Implemented enhancements:**

- Add futures market endpoints [\#19](https://github.com/btschwertfeger/python-kraken-sdk/issues/19)

Uncategorized merged pull requests:

- 19 add futures market endpoints [\#22](https://github.com/btschwertfeger/python-kraken-sdk/pull/22) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.5.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5.1) (2022-07-13)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5...v0.5.1)

## [v0.5](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5) (2022-07-13)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/f73882d2a9edf4d59597d4909300551e42a06020...v0.5)

**Implemented enhancements:**

- Add examples to all clients [\#12](https://github.com/btschwertfeger/python-kraken-sdk/issues/12)
- Add Websockets private and public endpoints [\#9](https://github.com/btschwertfeger/python-kraken-sdk/issues/9)
- Add Kraken Websockets-Authentication [\#4](https://github.com/btschwertfeger/python-kraken-sdk/issues/4)
- Add Kraken Staking endpoints [\#3](https://github.com/btschwertfeger/python-kraken-sdk/issues/3)
- Add Kraken Funding endpoints [\#2](https://github.com/btschwertfeger/python-kraken-sdk/issues/2)
- Add Kraken Trading endpints [\#1](https://github.com/btschwertfeger/python-kraken-sdk/issues/1)

**Closed issues:**

- Add setup files for publishing package [\#17](https://github.com/btschwertfeger/python-kraken-sdk/issues/17)
- Create README [\#14](https://github.com/btschwertfeger/python-kraken-sdk/issues/14)

Uncategorized merged pull requests:

- 17 add setup files for publishing package [\#18](https://github.com/btschwertfeger/python-kraken-sdk/pull/18) ([btschwertfeger](https://github.com/btschwertfeger))
- added README.md now ... [\#16](https://github.com/btschwertfeger/python-kraken-sdk/pull/16) ([btschwertfeger](https://github.com/btschwertfeger))
- added README.md [\#15](https://github.com/btschwertfeger/python-kraken-sdk/pull/15) ([btschwertfeger](https://github.com/btschwertfeger))
- 12 add examples to all clients [\#13](https://github.com/btschwertfeger/python-kraken-sdk/pull/13) ([btschwertfeger](https://github.com/btschwertfeger))
- 9 integrated websockets private and public endpoints [\#11](https://github.com/btschwertfeger/python-kraken-sdk/pull/11) ([btschwertfeger](https://github.com/btschwertfeger))
- added websocket clients and authentication [\#8](https://github.com/btschwertfeger/python-kraken-sdk/pull/8) ([btschwertfeger](https://github.com/btschwertfeger))
- added private staking endpoints [\#7](https://github.com/btschwertfeger/python-kraken-sdk/pull/7) ([btschwertfeger](https://github.com/btschwertfeger))
- added private funding endpoints [\#6](https://github.com/btschwertfeger/python-kraken-sdk/pull/6) ([btschwertfeger](https://github.com/btschwertfeger))
- added private trade endpoints [\#5](https://github.com/btschwertfeger/python-kraken-sdk/pull/5) ([btschwertfeger](https://github.com/btschwertfeger))

\* _This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)_
