# Changelog

## [Unreleased](https://github.com/btschwertfeger/python-kraken-sdk/tree/HEAD)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v1.1.0...HEAD)

**Breaking changes:**

- \(inconsistent spelling/typo\) recend --\> recent in kraken.spot [\#77](https://github.com/btschwertfeger/python-kraken-sdk/issues/77)
- Add API rate limit exception; extend test doc strings [\#79](https://github.com/btschwertfeger/python-kraken-sdk/pull/79) ([btschwertfeger](https://github.com/btschwertfeger))
- Fix bug/typo: "recend" -\> recent throughout kraken.spot [\#76](https://github.com/btschwertfeger/python-kraken-sdk/pull/76) ([jcr-jeff](https://github.com/jcr-jeff))

**Implemented enhancements:**

- Enable trading on Futures subaccount [\#72](https://github.com/btschwertfeger/python-kraken-sdk/issues/72)
- Check if trading is enabled for Futures subaccount [\#71](https://github.com/btschwertfeger/python-kraken-sdk/issues/71)
- Add Futures user endpoints: `check_trading_enabled_on_subaccount` and `set_trading_on_subaccount` [\#80](https://github.com/btschwertfeger/python-kraken-sdk/pull/80) ([btschwertfeger](https://github.com/btschwertfeger))

**Fixed bugs:**

- Release workflow skips the PyPI publish [\#67](https://github.com/btschwertfeger/python-kraken-sdk/issues/67)
- Fixed bug where `spot.user.get_balances` floats to periodic X.9999... [\#78](https://github.com/btschwertfeger/python-kraken-sdk/pull/78) ([btschwertfeger](https://github.com/btschwertfeger))
- Fix PyPI upload job + extend disclaimer [\#70](https://github.com/btschwertfeger/python-kraken-sdk/pull/70) ([btschwertfeger](https://github.com/btschwertfeger))
- Fix and extend release workflow [\#68](https://github.com/btschwertfeger/python-kraken-sdk/pull/68) ([btschwertfeger](https://github.com/btschwertfeger))

**Merged pull requests:**

- Split the unit tests into individual files [\#75](https://github.com/btschwertfeger/python-kraken-sdk/pull/75) ([btschwertfeger](https://github.com/btschwertfeger))
- Removed matrix from CodeQL job [\#74](https://github.com/btschwertfeger/python-kraken-sdk/pull/74) ([btschwertfeger](https://github.com/btschwertfeger))
- Add a Changelog [\#73](https://github.com/btschwertfeger/python-kraken-sdk/pull/73) ([btschwertfeger](https://github.com/btschwertfeger))

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

**Merged pull requests:**

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

**Merged pull requests:**

- examples now use os.getenv instead of python-dotenv [\#34](https://github.com/btschwertfeger/python-kraken-sdk/pull/34) ([btschwertfeger](https://github.com/btschwertfeger))
- Release v1.0.1 [\#44](https://github.com/btschwertfeger/python-kraken-sdk/pull/44) ([btschwertfeger](https://github.com/btschwertfeger))

## [v1.0.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v1.0.0) (2023-03-04)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.8.0...v1.0.0)

**Implemented enhancements:**

- Extended CI/CD [\#31](https://github.com/btschwertfeger/python-kraken-sdk/pull/31) ([btschwertfeger](https://github.com/btschwertfeger))

**Merged pull requests:**

- Extend unittests [\#32](https://github.com/btschwertfeger/python-kraken-sdk/pull/32) ([btschwertfeger](https://github.com/btschwertfeger))
- Add unit tests \#2 [\#30](https://github.com/btschwertfeger/python-kraken-sdk/pull/30) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.8.0](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.8.0) (2023-02-18)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.7...v0.8.0)

**Merged pull requests:**

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

**Merged pull requests:**

- Add exceptions [\#28](https://github.com/btschwertfeger/python-kraken-sdk/pull/28) ([btschwertfeger](https://github.com/btschwertfeger))
- Create CODE_OF_CONDUCT.md [\#27](https://github.com/btschwertfeger/python-kraken-sdk/pull/27) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.7.2](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.2) (2022-11-24)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7.1...v0.7.2)

## [v0.7.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7.1) (2022-11-23)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.7...v0.7.1)

**Implemented enhancements:**

- add futures websocket endpoints [\#21](https://github.com/btschwertfeger/python-kraken-sdk/issues/21)

**Merged pull requests:**

- Optimized websocket clients [\#26](https://github.com/btschwertfeger/python-kraken-sdk/pull/26) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.7](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.7) (2022-11-22)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.6.1...v0.7)

**Implemented enhancements:**

- add futures trade endpoints [\#20](https://github.com/btschwertfeger/python-kraken-sdk/issues/20)

**Merged pull requests:**

- Add testing [\#25](https://github.com/btschwertfeger/python-kraken-sdk/pull/25) ([btschwertfeger](https://github.com/btschwertfeger))
- implemented Futures WS Client; adjust spot ws client [\#24](https://github.com/btschwertfeger/python-kraken-sdk/pull/24) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.6.1](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.6.1) (2022-11-20)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.4.2...v0.6.1)

**Merged pull requests:**

- Add futures clients [\#23](https://github.com/btschwertfeger/python-kraken-sdk/pull/23) ([btschwertfeger](https://github.com/btschwertfeger))

## [v0.5.4.2](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5.4.2) (2022-11-09)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.4...v0.5.4.2)

## [v0.5.4](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5.4) (2022-10-13)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.2...v0.5.4)

## [v0.5.2](https://github.com/btschwertfeger/python-kraken-sdk/tree/v0.5.2) (2022-09-18)

[Full Changelog](https://github.com/btschwertfeger/python-kraken-sdk/compare/v0.5.1...v0.5.2)

**Implemented enhancements:**

- Add futures market endpoints [\#19](https://github.com/btschwertfeger/python-kraken-sdk/issues/19)

**Merged pull requests:**

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

**Merged pull requests:**

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
