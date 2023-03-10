# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import pathlib
import sys
sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'qutip_qtrl'
copyright = '2011-2023, QuTiP Community'
author = 'QuTiP Community'


def qutip_qtrl_version():
    """ Retrieve the qutip-qtrl version from ``../../VERSION``.
    """
    src_folder_root = pathlib.Path(__file__).absolute().parent.parent
    version = src_folder_root.joinpath(
        "VERSION"
    ).read_text().strip()
    return version


# The full version, including alpha/beta/rc tags.
release = qutip_qtrl_version()
# The short X.Y version.
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.mathjax',
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'numpydoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.viewcode',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinxcontrib.bibtex',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for numpydoc ---------------------------------------

numpydoc_show_class_members = False
napoleon_numpy_docstring = True
napoleon_use_admonition_for_notes = True

# -- Options for api doc ---------------------------------------

# autosummary_generate can be turned on to automatically generate files in the
# apidoc folder. This is particularly useful for modules with lots of
# functions/classes. However, pay attention that some api docs files are
# adjusted manually for better illustration and should not be overwritten.
autosummary_generate = False
autosummary_imported_members = True

# -- Options for biblatex ---------------------------------------

bibtex_bibfiles = ['references.bib']
bibtex_default_style = 'unsrt'

# -- Options for intersphinx ---------------------------------------

intersphinx_mapping = {
    'qutip': ('https://qutip.org/docs/latest/', None),
}
