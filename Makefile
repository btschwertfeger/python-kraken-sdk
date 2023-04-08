#!make
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger

VENV := venv
GLOBAL_PYTHON := $(shell which python3)
PYTHON := $(VENV)/bin/python

.PHONY := build dev install test test_upload live_upload clean

##		Builds the python-kraken-sdk
##
build:
	$(PYTHON) -m pip wheel -w dist --no-deps .

##		Installs the package in edit mode
##
dev:
	$(PYTHON) -m pip install -e .[dev]

##		Install the package
##
install:
	$(PYTHON) -m pip install .

##		Run the unittests
##
test:
	$(PYTHON) -m pytest tests/

##		Build the documentation
##
doc:
	cd docs && make html

##		Run the documentation tests
##
doctest:
	cd docs && make doctest

##		Pre-Commit
pre-commit:
	@pre-commit run -a

##		Clean the workspace
##
clean:
	rm -rf .pytest_cache build/ dist/ python_kraken_sdk.egg-info docs/_build
	rm -f .coverage kraken/_version.py *.log *.csv *.zip tests/*.zip tests/.csv

	find tests -name "__pycache__" | xargs rm -rf
	find kraken -name "__pycache__" | xargs rm -rf
	find examples -name "__pycache__" | xargs rm -rf
