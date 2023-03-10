# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'qutip_qtrl'
copyright = '2011-2023, QuTiP Community'
author = 'QuTiP Community'


def qutip_qtrl_version():
    """ Retrieve the qutip-qtrl version from ``../../VERSION``.
    """
    src_folder_root = pathlib.Path(__file__).absolute().parent.parent.parent
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
