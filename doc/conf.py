# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# pylint: disable=invalid-name

"""
This module is the configuration for the Sphinx documentation building process.
"""

import sys
from pathlib import Path
from shutil import copyfile
from typing import Any

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "python-kraken-sdk"
copyright = "2023, Benjamin Thomas Schwertfeger"  # noqa: A001 # pylint: disable=redefined-builtin
author = "Benjamin Thomas Schwertfeger"

# Add the package to sys.path:
sys.path.insert(0, str(Path("..").resolve() / "src"))

rst_epilog = ""
# Read link all targets from file
with Path("links.rst").open(encoding="utf-8") as f:
    rst_epilog += f.read()


def setup(app: Any) -> None:  # noqa: ARG001,ANN401
    """Setup function to modify doc building"""
    copyfile(
        Path("..") / "examples" / "market_client_example.ipynb",
        Path("03_examples") / "market_client_example.ipynb",
    )


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "nbsphinx",
    "sphinx_click",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "IPython.sphinxext.ipython_console_highlighting",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "links.rst",
    "**.ipynb_checkpoints",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"  # "sphinx_book_theme"  # "sphinx_rtd_theme"
# html_static_path = ["_static"] # for images
html_context = {
    "display_github": True,
    "github_user": "btschwertfeger",
    "github_repo": "python-kraken-sdk",
    "github_version": "master/doc/",
}
html_theme_options = {
    # "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#336790",
        "color-brand-content": "#336790",
    },
    "dark_css_variables": {
        "color-brand-primary": "#E5B62F",
        "color-brand-content": "#E5B62F",
    },
    "source_repository": "https://github.com/btschwertfeger/python-kraken-sdk/",
    "source_branch": "master",
    "source_directory": "doc/",
}
