# Configuration file for the Sphinx documentation builder.

project = 'MoneySmarts'
copyright = '2025, MoneySmarts Team'
author = 'MoneySmarts Team'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'

# Add moneySmarts to the Python path for autodoc
import os
import sys
sys.path.insert(0, os.path.abspath('../../moneySmarts'))

