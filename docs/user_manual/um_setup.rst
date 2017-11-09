======
Setup
======

Installation
=============

From Binaries
--------------

DeDop is distributed as pre-compiled binaries which can be retrieved from `here <https://github.com/DeDop/dedop/releases/tag/v0.5.3>`_.
For the windows Windows platforms there is a dedicated installer executable. For Mac OS and Unixes a ZIP file is provided.
All platform distributions have a bundled Python interpreter, that's also the reason why they are quite large in size
(roughly 300 megabytes).

After installing (on Windows) / unpacking (on Unixes) you find an executable file named `dedop-shell` in the
installation's root directory. Running it brings up the *DeDop Shell*.

From Source
------------

DeDop is programmed in Python so you first need to setup a suitable Python environment.
We recommend using a `Miniconda <http://conda.pydata.org/miniconda.html>`_ Python3 environment, so
you don't need to install the DeDop library dependencies in your default Python.

After installing Miniconda open a terminal window and create an isolated Python environment and *activate* it. Type::

    conda create -n dedop python=3.5
    source activate dedop


Then install the DeDop library requirements::

    conda install numpy scipy netcdf4 numexpr pyproj

If you like to perform analysis tasks with DeDop, then also install::

    conda install matplotlib bokeh jupyter ipywidgets

Then checkout the DeDop source code from GitHub::

    git clone https://github.com/DeDop/dedop-core.git

Step into the newly created source directory and install DeDop in the Python environment `dedop`::

    cd dedop-core
    python setup.py develop

After installing from source, you should be able to run the DeDop Shell, try::

    dedop --help

