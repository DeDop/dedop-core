[![Build Status](https://travis-ci.org/DeDop/dedop-core.svg?branch=master)](https://travis-ci.org/DeDop/dedop-core)
[![Build status](https://ci.appveyor.com/api/projects/status/2461996aau28tsm9/branch/master?svg=true)](https://ci.appveyor.com/project/hans-permana/dedop-core/branch/master)
[![codecov](https://codecov.io/gh/DeDop/dedop-core/branch/master/graph/badge.svg)](https://codecov.io/gh/DeDop/dedop-core)
[![Documentation Status](https://readthedocs.org/projects/dedop-core/badge/?version=latest)](http://dedop-core.readthedocs.io/en/latest/?badge=latest)


# DeDop³

DeDop is a User Configurable Tool for Processing Delay Doppler Altimeter Data.
"DeDop" stands for Delay Doppler (Altimeter) Processor.

For more information about the project please visit [www.dedop.org](http://www.dedop.org/).
For more information about the software have a look into
the [DeDop User Manual](http://dedop.readthedocs.io/en/latest/user_manual.html).

## Contents

* `setup.py` - main build script to be run with Python 3.5
* `dedop/` - main package and production code
* `test/` - test package and test code
* `docs/` - documentation in Sphinx/RST format
* `notebooks/` - some IPython notebooks demonstrating the use of the DeDop Python API

## Installation using installer (recommended)

Instructions on how to get the installer and how to install are available [here](https://github.com/DeDop/dedop-installer#install-dedop-core).

## Installation from Sources

### Using Conda

We recommend installing DeDop into an isolated Python 3 environment,
because this approach avoids clashes with existing versions of DeDop's 3rd-party module requirements.
We recommend using Conda ([Miniconda](http://conda.pydata.org/miniconda.html)
or [Anaconda](https://www.continuum.io/downloads)) which will usually also avoid platform-specific
issues caused by module native binaries.

Creating an isolated environment for DeDop. This will require around 2.2 GB disk space on Linux/Darwin
and and 1.2 GB on Windows. To create a new DeDop environment `dedop` in your Anaconda/Miniconda installation directory,
type:

    $ conda env create --file environment.yml

If you want the environment to be installed in another location, e.g. due to disk space limitations, type:

    $ conda env create --file environment.yml --prefix some/other/location/for/dedop

Next step is to activate the new environment. On Linux/Darwin type:

    $ source activate dedop

In case you used another location use it instead of the name `dedop`.
Windows users can omit the `source` command and just type

    > activate dedop

You can now safely install and run DeDop sources into the new `dedop` environment.

    (dedop) $ python setup.py develop

To permanently install DeDop into the Python environment (not recommended while in development mode!), type:

    (dedop) $ python setup.py install

### Using Standard Python

DeDop requires Python 3.5+.

DeDop can be run from sources directly, once the following module requirements are resolved:

* `numpy`
* `scipy`
* `netcdf4`
* `numexpr`
* `pyproj`

If you like to perform L1B product analysis tasks with DeDop using an IPython Notebook, then also install:

* `jupyter`
* `ipywidgets`
* `matplotlib`
* `bokeh`

The most up-to-date and complete list of module requirements is found in the project's `environment.yml` file.

To install and run DeDop from sources directly, type:

    $ python setup.py develop

To permanently install DeDop into Python (not recommended while in development mode!), type:

    $ python setup.py install

## Getting started

### Command Line Interface

To test the installation from source, first run the DeDop command-line interface. Type

    $ dedop -h
    
More examples are available here http://dedop-core.readthedocs.io/en/latest/manual.html#examples
    
### Web API

This is required by dedop-studio. To start the web API, type:

    $ dedop-webapi start
    
A random port number will be assigned unless explicitly specified on the command like so:
    
    $ dedop-webapi --port 2999 start
    
To check if the wbe API has started successfully, open your browser and enter the web API URL. The following response should be displayed:
    
    {"status": "ok", "content": {"name": "dedop-webapi", "version": "1.0.0", "timestamp": "2017-05-16"}}

To stop, go to **[host_name]:[port_number]/exit** on the browser. For example:

    127.0.0.1:2999/exit

## License

DeDop is distributed under the terms and conditions of the [MIT license](https://opensource.org/licenses/MIT).
