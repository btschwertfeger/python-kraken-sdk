# -*- mode: make; coding: utf-8 -*-
#!make
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

UV ?= uv
PYTHON := python
PYTEST := $(UV) run pytest
PYTEST_OPTS := -vv --junit-xml=pytest.xml
PYTEST_COV_OPTS := $(PYTEST_OPTS) --cov=kraken --cov-report=xml:coverage.xml --cov-report=term
TEST_DIR := tests

## ======= M A K E F I L E - T A R G E T S =====================================
## help           Show this help message
##
.PHONY: help
help:
	@grep "^##" Makefile | sed -e "s/##//"

## ======= B U I L D I N G =====================================================
## build		Builds the package
##
.PHONY: build
build: check-uv
	$(UV) build .

## rebuild 	Rebuild the package
##
.PHONY: rebuild
rebuild: clean build

## doc		Build the documentation
##
.PHONY: doc
doc:
	cd doc && make html

## ======= I N S T A L L A T I O N =============================================
## install	Install the package
##
.PHONY: install
install: check-uv
	$(UV) pip install .

## dev		Installs the extended package in edit mode
##
.PHONY: dev
dev: check-uv
	$(UV) pip install -e . -r requirements-dev.txt -r doc/requirements.txt

## ======= T E S T I N G =======================================================
## test		Run the unit tests
##
.PHONY: test
test:
	@rm .cache/tests/*.log || true
	$(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)

.PHONY: tests
tests: test

## retest         Run tests that failed in the last run
##
.PHONY: retest
retest:
	@rm .cache/tests/*.log || true
	$(PYTEST) $(PYTEST_OPTS) --lf $(TEST_DIR)

## wip		Run tests marked as 'wip'
##
.PHONY: wip
wip:
	@rm .cache/tests/*.log || true
	$(PYTEST) -m "wip" -vv $(TEST_DIR)

## coverage       Run all tests and generate the coverage report
##
.PHONY: coverage
coverage:
	@rm .cache/tests/*.log || true
	$(PYTEST) $(PYTEST_COV_OPTS) $(TEST_DIR)

## doctest	Run the documentation related tests
##
.PHONY: doctest
doctest:
	cd docs && make doctest

## ======= M I S C E L A N I O U S =============================================
## pre-commit	Run the pre-commit targets
##
.PHONY: pre-commit
pre-commit:
	@pre-commit run -a

## ruff           Run ruff without fix
##
.PHONY: ruff
ruff:
	$(UVX) ruff check --preview .

## ruff-fix 	Run ruff with fix
##
.PHONY: ruff-fix
ruff-fix:
	$(UVX) ruff check --fix --preview .

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
		--no-issues \
		--no-issues-wo-labels \
		--enhancement-labels Feature,enhancement \
		--release-branch master \
		--pr-label "Uncategorized merged pull requests:"

## clean		Clean the workspace
##
.PHONY: clean
clean:
	rm -rf .cache \
		.vscode \
		dist/ \
		doc/_build \
		src/python_kraken_sdk.egg-info \
	    build/

	rm -f .coverage \
		*.csv \
		*.log \
		*.zip \
		coverage.xml \
		src/kraken/_version.py \
		mypy.xml \
		pytest.xml \
		tests/*.zip

	find tests -name "__pycache__" | xargs rm -rf
	find src -name "__pycache__" | xargs rm -rf
	find examples -name "__pycache__" | xargs rm -rf

## check-uv       Check if uv is installed
##
.PHONY: check-uv
check-uv:
	@if ! command -v $(UV) >/dev/null; then \
		echo "Error: uv is not installed. Please visit https://github.com/astral-sh/uv for installation instructions."; \
		exit 1; \
	fi
