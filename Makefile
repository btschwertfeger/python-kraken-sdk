#!make
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

PYTHON := python
PYTEST := $(PYTHON) -m pytest
PYTEST_OPTS := -vv --junit-xml=pytest.xml
PYTEST_COV_OPTS := $(PYTEST_OPTS) --cov --cov-report=xml:coverage.xml --cov-report=term
TEST_DIR := tests

.PHONY: help
help:
	@grep "^##" Makefile | sed -e "s/##//"

## ======= B U I L D I N G =======
## build		Builds the python-kraken-sdk
##
.PHONY: build
build:
	$(PYTHON) -m build .
.PHONY: rebuild
rebuild: clean build

## doc		Build the documentation
##
.PHONY: doc
doc:
	cd docs && make html

## ======= I N S T A L L A T I O N =======
## install	Install the package
##
.PHONY: install
install:
	$(PYTHON) -m pip install .

## dev		Installs the extended package in edit mode
##
.PHONY: dev
dev:
	$(PYTHON) -m pip install -e ".[dev]"

## ======= T E S T I N G =======
## test		Run the unit tests
##
.PHONY: test
test:
	@rm *.log || true
	$(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)

.PHONY: tests
tests: test

## test-wip		Run tests marked as 'wip'
##
.PHONY: test-wip
test-wip:
	@rm *.log || true
	$(PYTEST) -m "wip" -vv $(TEST_DIR)

## coverage		Run all tests and generate the coverage report
##
.PHONY: coverage
coverage:
	@rm *.log || true
	$(PYTEST) $(PYTEST_COV_OPTS) $(TEST_DIR)

## doctest	Run the documentation related tests
##
.PHONY: doctest
doctest:
	cd docs && make doctest

## ======= M I S C E L A N I O U S =======
## pre-commit	Run the pre-commit targets
##
.PHONY: pre-commit
pre-commit:
	@pre-commit run -a

## ruff 	Run ruff without fix
.PHONY: ruff
ruff:
	ruff check .

## ruff-fix 	Run ruff with fix
##
.PHONY: ruff-fix
ruff-fix:
	ruff check . --fix

## changelog	Generate the changelog
##
.PHONY: changelog
changelog:
	docker run -it --rm \
		-v $(PWD):/usr/local/src/your-app \
		githubchangeloggenerator/github-changelog-generator \
		--user btschwertfeger \
		--project python-kraken-sdk \
		--token $(GHTOKEN)  \
		--breaking-labels Breaking \
		--enhancement-labels Feature,enhancement \
		--release-branch master \
		--pr-label "Uncategorized merged pull requests:"

## clean		Clean the workspace
##
.PHONY: clean
clean:
	rm -rf .pytest_cache build/ dist/ \
		python_kraken_sdk.egg-info \
		docs/_build \
		.vscode \
		.cache \
		.mypy_cache \
		.ruff_cache

	rm -f .coverage coverage.xml pytest.xml mypy.xml \
		kraken/_version.py \
		*.log *.csv *.zip \
		tests/*.zip tests/.csv \
		python_kraken_sdk-*.whl

	find tests -name "__pycache__" | xargs rm -rf
	find kraken -name "__pycache__" | xargs rm -rf
	find examples -name "__pycache__" | xargs rm -rf
