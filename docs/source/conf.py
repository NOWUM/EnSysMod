# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import json
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import os
import pathlib
import sys

from fastapi.openapi.utils import get_openapi

import ensysmod
from ensysmod.app import app

sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

# If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'EnSysMod'
copyright = '2021, NOWUM'
author = 'NOWUM'

# The full version, including alpha/beta/rc tags
release = ensysmod.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.openapi',
    'sphinxcontrib.autodoc_pydantic',
]

# configure for edit_on_github-Button
html_context = {
    'display_github': True,
    'github_user': 'NOWUM',
    'github_repo': 'ensysmod',
    'github_version': 'main/docs/source/',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# -- Automatically generate Rest-Endpoints in Sphinx
generated_dir = './generated'
if not os.path.exists(generated_dir):
    os.makedirs(generated_dir)
with open(f"{generated_dir}/openapi.json", 'w') as f:
    json.dump(get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    ), f)

# Pydantic schema generation configuration
# see https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html#model
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_members = False
