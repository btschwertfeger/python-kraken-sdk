#!make
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

PYTHON := python

PYTEST := $(PYTHON) -m pytest
PYTEST_OPTS := -vv --junit-xml=pytest.xml
PYTEST_COV_OPTS := $(PYTEST_OPTS) --cov --cov-report=xml:coverage.xml --cov-report=term
TEST_DIR := tests

.PHONY := build dev install test tests coverage doc doctest clean changelog pre-commit

help:
	@grep "^##" Makefile | sed -e "s/##//"

## ======= B U I L D I N G =======
## build		Builds the python-kraken-sdk
##
build:
	$(PYTHON) -m build .

rebuild: clean build

## dev		Installs the extended package in edit mode
##
dev:
	$(PYTHON) -m pip install -e ".[dev]"

## doc		Build the documentation
##
doc:
	cd docs && make html

## ======= I N S T A L L A T I O N =======
## install	Install the package
##
install:
	$(PYTHON) -m pip install .

## ======= T E S T I N G =======
## test		Run the unit tests
##
test:
	$(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)

tests: test

test-wip:
	$(PYTEST) -m "wip" -vv $(TEST_DIR)

coverage:
	$(PYTEST) $(PYTEST_COV_OPTS) $(TEST_DIR)

## doctest	Run the documentation tests
##
doctest:
	cd docs && make doctest

## ======= M I S C E L A N I O U S =======
## pre-commit	Run the pre-commit targets
##
pre-commit:
	@pre-commit run -a

## changelog	Generate the changelog
##
changelog:
	docker run -it --rm \
		-v $(PWD):/usr/local/src/your-app \
		githubchangeloggenerator/github-changelog-generator \
		--user btschwertfeger \
		--project python-kraken-sdk \
		--token $(GHTOKEN)  \
		--breaking-labels Breaking \
		--enhancement-labels Feature \
		--release-branch master \
		--pr-label "Uncategorized merged pull requests:"

## clean		Clean the workspace
##
clean:
	rm -rf .pytest_cache build/ dist/ \
		python_kraken_sdk.egg-info \
		docs/_build \
		.vscode \
		.mypy_cache

	rm -f .coverage coverage.xml pytest.xml mypy.xml \
		kraken/_version.py \
		*.log *.csv *.zip \
		tests/*.zip tests/.csv \
		python_kraken_sdk-*.whl

	find tests -name "__pycache__" | xargs rm -rf
	find kraken -name "__pycache__" | xargs rm -rf
	find examples -name "__pycache__" | xargs rm -rf
