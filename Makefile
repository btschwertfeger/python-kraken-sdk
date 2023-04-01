

VENV := venv
GLOBAL_PYTHON := $(shell which python3)
PYTHON := $(VENV)/bin/python

.PHONY := build dev install test test_upload live_upload clean

##		Builds the python-kraken-sdk
##
build:
	$(PYTHON) -m build .

##		Installs the local python-kraken-sdk
##		in edit mode
##
dev:
	$(PYTHON) -m pip install -e .

##		Installs python dependencies
##
install:
	$(PYTHON) -m pip install build setuptools_scm

##		Run the unittests
##
test:

##		Upload to testpypi
##
test_upload:
	twine upload -r testpypi dist/*

##		Upload to PyPI
##
live_upload:
	twine upload dist/*

##		Clean the workspace
##
clean:
	rm -rf .pytest_cache build/ dist/ python_kraken_sdk.egg-info
	rm -f .coverage kraken/_version.py
