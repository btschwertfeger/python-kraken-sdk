#!make
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger

PYTHON := python

.PHONY := build dev install test tests doc doctests clean

help:
	@grep "^##" Makefile | sed -e "s/##//"

## ======= B U I L D I N G =======
## build		Builds the python-kraken-sdk
##
build:
	$(PYTHON) -m pip wheel -w dist --no-deps .

rebuild: clean build

## dev		Installs the package in edit mode
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
## test		Run the unittests
##
test:
	$(PYTHON) -m pytest -v tests/

tests: test

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
		-v "$(pwd)":/usr/local/src/pksdk \
		githubchangeloggenerator/github-changelog-generator \
		-u btschwertfeger \
		-p python-kraken-sdk \
		-t $(GHTOKEN)  \
		--breaking-labels Breaking \
		--enhancement-labels Feature

## clean		Clean the workspace
##
clean:
	rm -rf .pytest_cache build/ dist/ \
		python_kraken_sdk.egg-info \
		docs/_build \
		.vscode
	rm -f .coverage coverage.xml \
		kraken/_version.py \
		*.log *.csv *.zip \
		tests/*.zip tests/.csv

	find tests -name "__pycache__" | xargs rm -rf
	find kraken -name "__pycache__" | xargs rm -rf
	find examples -name "__pycache__" | xargs rm -rf
