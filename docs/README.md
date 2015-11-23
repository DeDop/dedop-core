This directory `docs` is the DeDop documentation folder. 
Documentation is build from `\*.rst` files using *Sphinx*.
`index.rst` is the main documentation page.

To install Sphinx run:

     > pip install Sphinx

To build the DeDop documentation run:

     > cd dedop/docs
     > make html

or to force regeneration of docs, run:

     > cd dedop
     > sphinx-build -E -a -b html docs docs/_build/html

Then find the html documentation in `dedop/docs/_build/html`

More info:

* Sphinx Tutorial: http://sphinx-doc.org/tutorial.html
* RST Primer: http://sphinx-doc.org/rest.html#rst-primer