# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

"""This module is the configuration for the Sphinx documentation building process"""
# pylint: disable=invalid-name

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Python Kraken SDK"  #
copyright = "2023, Benjamin Thomas Schwertfeger"  # pylint: disable=redefined-builtin
author = "Benjamin Thomas Schwertfeger"


sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    # "sphinx_reference_rename",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# sphinx_reference_rename_mapping = {
#     "kraken.spot.user.user.UserClient": "kraken.Spot.User",
# }


def setup(app):
    """Run during the Sphinx building process"""
    # from kraken.spot.user.user import UserClient

    # UserClient.__module__ = "kraken.Spot.User"
    # kraken.spot.user.user.UserClient.__name__ = "kraken.Spot.User"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
# html_theme_options = {"rightsidebar": "true", "relbarbgcolor": "black"}
