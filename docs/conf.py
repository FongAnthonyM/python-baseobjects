#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sphinx configuration for baseobjects.

This configuration enables extensive API documentation using autodoc and
autosummary, better type and Google/NumPy style docstring parsing via
Napoleon, and several convenience extensions like viewcode, intersphinx,
and todo.
"""
# Imports #
# Standard Libraries #
from datetime import datetime
import os
import sys

# Ensure src is on sys.path for autodoc
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if os.path.isdir(SRC) and SRC not in sys.path:
    sys.path.insert(0, SRC)

# Project Information #
project = "baseobjects"
author = "Anthony Fong"
copyright = f"{datetime.now().year}, {author}"

# General configuration #
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_click",
]

# Autodoc / Autosummary
autodoc_typehints = "description"
autosummary_generate = True
add_module_names = False
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_attr_annotations = True

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# HTML output
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
}

todo_include_todos = True
