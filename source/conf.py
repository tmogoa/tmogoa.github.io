# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "tmogoa"
copyright = "2026, Tony Mogoa"
author = "Tony Mogoa"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxext.opengraph',
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_title = "tmogoa"
html_theme = "shibuya"
html_static_path = ["_static"]

ogp_use_first_image = True
ogp_site_url = 'https://tmogoa.github.io/'
ogp_description_length = 200
ogp_type = "article"
