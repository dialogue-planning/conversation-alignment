# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import pathlib

project = 'Conversation Alignment'
copyright = '2023, Natalie Nova, Rebecca De Venezia'
author = 'Natalie Nova, Rebecca De Venezia'
release = '2022'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
   'sphinx.ext.autodoc', # gets docstrings from Python code
   'sphinx.ext.autosummary', # auto-generates .rst files
   'sphinx.ext.napoleon', # allows for Google/numpy style docstrings
   'sphinx.ext.viewcode', # adds link to the source code in the docs
   "sphinx_rtd_theme"  # read the docs theme
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_static_path = ['_static']

# Source code dir relative to this file. You may also need to add other paths to the file (anything needed for imports) depending on how your project is structured.
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
sys.path.insert(0, (pathlib.Path(__file__).parents[2] / "beam_search").resolve().as_posix()) 
# Turn on sphinx.ext.autosummary and set autodoc options
autosummary_generate = True
autodoc_default_options = {
    'members':          True,
    'undoc-members':    True,
    'private-members':  True,
    'special-members':  False,
    'inherited-members':True,
    'show-inheritance': True
}
html_theme = "sphinx_rtd_theme"
add_module_names = False