# Self review checklist ✅

Before creating a pull request you should check the following requirements that
must be addressed before a PR will be accepted.

- [ ] **All** pre-commit hooks must run through - successfully.
- [ ] Make sure that the changes confirm the coding style of the
      [python-kraken-sdk](https://github.com/btschwertfeger/python-kraken-sdk).
      Most issues will be resolve through the pre-commit hooks.
- [ ] Also take care to follow the community guidelines and the [Code of
      Conduct](./CODE_OF_CONDUCT.md).
- [ ] Self-review your changes to detect typos, syntax errors, and any kind of
      unwanted behavior.
- [ ] If you changed the source code you have to **ensure that all unit tests
      run through**. If you added a new function you also have to **write a
      test** for that. Also make sure to **follow the doc string style** of the
      package and **provide at least one working example** within a function doc
      string. This is important since doc strings will be reflected within the
      documentation.
- [ ] Take your time to prepare your code before creating a PR. A good PR will
      save a lot of time for everyone.
- [ ] There are several workflows/actions within this repository. Relevant
      workflows must be run successfully within your fork. Actions must be
      enabled within the fork, so that workflows can run within the context of a
      PR. [cicd.yaml](./workflows/cicd.yaml) can be used to run all actions at
      once - but requires having API keys for Spot, Futures and the Futures demo
      environment.
