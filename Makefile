

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

##
##
doc:
	cd docs && make html

##		Clean the workspace
##
clean:
	rm -rf .pytest_cache build/ dist/ python_kraken_sdk.egg-info docs/_build
	rm -f .coverage kraken/_version.py *.log *.csv *.zip tests/*.zip tests/.csv
	find tests -name "__pycache__" | xargs rm -rf
	find kraken -name "__pycache__" | xargs rm -rf
	find examples -name "__pycache__" | xargs rm -rf
