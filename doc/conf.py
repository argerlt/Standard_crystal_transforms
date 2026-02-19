# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from datetime import datetime
import inspect
import os
import re
import sys

from numpydoc.docscrape_sphinx import SphinxDocString

project = 'A Crystal Transforms Standard'
copyright = '2026, Gerlt et al'
author = 'Gerlt et al'
release = '0.1.0'

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath("."))
sys.path.append("../")

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    # Suppress warnings from Sphinx regarding "duplicate source files":
    # https://github.com/executablebooks/MyST-NB/issues/363#issuecomment-1682540222
    "examples/*/*.ipynb",
    "examples/*/*.py",
]


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.imgconverter",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "numpydoc",  # Must be loaded after autodoc
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# HTML theming: pydata-sphinx-theme
# https://pydata-sphinx-theme.readthedocs.io
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/pyxem/orix",
    "header_links_before_dropdown": 6,
    "logo": {"alt_text": project, "text": project},
    "navigation_with_keys": True,
    "show_toc_level": 2,
    "use_edit_page_button": True,
}
html_context = {
    "github_user": "pyxem",
    "github_repo": "orix",
    "github_version": "develop",
    "doc_path": "doc",
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Syntax highlighting
pygments_style = "friendly"

# -- matplotlib.sphinxext.plot_directive
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html
plot_formats = ["png"]
plot_html_show_source_link = False
plot_html_show_formats = False
plot_include_source = True


def _str_examples(self):
    examples_str = "\n".join(self["Examples"])
    if (
        self.use_plots
        and (
            re.search(r"\b(.plot)\b", examples_str)
            or re.search(r"\b(.plot_map)\b", examples_str)
            or re.search(r"\b(.imshow)\b", examples_str)
        )
        and "plot::" not in examples_str
    ):
        out = []
        out += self._str_header("Examples")
        out += [".. plot::", ""]
        out += self._str_indent(self["Examples"])
        out += [""]
        return out
    else:
        return self._str_section("Examples")


SphinxDocString._str_examples = _str_examples


# -- Sphinx-Gallery
# https://sphinx-gallery.github.io
sphinx_gallery_conf = {
    "backreferences_dir": "reference/generated",
    "doc_module": ("orix",),
    "examples_dirs": "../examples",
    "filename_pattern": "^((?!sgskip).)*$",
    "gallery_dirs": "examples",
    "reference_url": {"orix": None},
    "run_stale_examples": False,
    "show_memory": True,
}
autosummary_generate = True


# Download example datasets prior to building the docs
print("[orix] Downloading example datasets (if not found in the cache)")
_ = data.sdss_ferrite_austenite(allow_download=True)
_ = data.sdss_austenite(allow_download=True)
_ = data.ti_orientations(allow_download=True)


def skip_member(app, what, name, obj, skip, options):
    """Exclude objects not defined within orix from the API reference.

    This ensures inherited members from Matplotlib axes extensions are
    excluded from the reference. We could exclude inherited members
    all together in the Sphinx Jinja2 template. But, this would mean
    classes such as Rotation would have to "overwrite" all methods and
    properties from Quaternion for these members to be listed in the
    API reference of Rotation. Instead, we allow inherited members, but
    try our best to skip members coming from outside orix here.
    """
    if what in ["attribute", "property"]:
        obj_module = inspect.getmodule(getattr(obj, "fget", None))
    else:
        obj_module = inspect.getmodule(obj)
    return "orix" not in getattr(obj_module, "__name__", [])


def setup(app):
    app.connect("autodoc-skip-member", skip_member)
