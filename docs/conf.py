# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# pylint: disable=invalid-name

"""This module is the configuration for the Sphinx documentation building process"""

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "python-kraken-sdk"
copyright = "2023, Benjamin Thomas Schwertfeger"  # ruff: noqa: A001
author = "Benjamin Thomas Schwertfeger"

# to import the package
sys.path.insert(0, os.path.abspath(".."))

# import links
rst_epilog = ""
# Read link all targets from file
with open("links.rst", encoding="utf-8") as f:
    rst_epilog += f.read()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "links.rst"]


def setup(app):
    """Run during the Sphinx building process"""


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_context = {
    "display_github": True,
    "github_user": "btschwertfeger",
    "github_repo": "python-kraken-sdk",
    "github_version": "master/docs/",
}
# html_theme_options = {"rightsidebar": "true", "relbarbgcolor": "black"}
