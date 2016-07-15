============
Installation
============

From Binaries
=============

DeDop is distributed as pre-compiled binaries which can be retrieved from the `here <ftp://isardsat-ACA@ftp.isardsat.co.uk/tool>`_.
For the windows Windows platforms there is a dedicated installer executable. For Mac OS and Unixes a ZIP file is provided.
All platform distributions have a bundled Python interpreter, that's also the reason why they are quite large in size
(roughly 300 megabytes).

After installing (on Windows) / unpacking (on Unixes) you find an executable file named `dedop-shell` in the
installation's root directory. Running it brings up the *DeDop Shell*.

From Source
===========

DeDop is programmed in Python so you first need to setup a suitable Python environment.
We recommend using a `Miniconda <http://conda.pydata.org/miniconda.html>`_ Python environment, so
you don't need to install the DeDop library dependencies in your default Python.

After installing Miniconda open a terminal window and create an isolated Python environment and *activate* it. Type::

    conda create -n dedop python=3
    source activate.sh dedop


Then install DeDop library requirements::

    conda install numpy scipy netCDF4

If you like to perfoam analysis tasks with DeDop, then also install::

    conda install -c IOOS basemap matplotlib jupyter

Then checkout the DeDop source code from GitHub::

    git clone https://github.com/DeDop/dedop.git

Step into the newly created directory and install dedop in the Python environment `dedop`::

    cd dedop
    python setup.py develop

After installing from source, you should be able to run the DeDop Shell, try::

    dedop --help





