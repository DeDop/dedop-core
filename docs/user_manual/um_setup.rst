======
Setup
======

DeDop Shell Installation
=========================

From Binaries
--------------

DeDop is distributed as pre-compiled binaries which can be retrieved from `here <https://github.com/DeDop/dedop-core/releases/tag/v1.2.0>`_.
For the windows Windows platforms there is a dedicated installer executable. For Mac OS and Unixes a ZIP file is provided.
All platform distributions have a bundled Python interpreter, that's also the reason why they are quite large in size
(roughly 300 megabytes). As mentioned before, this package also contains DeDop processor and DeDop webapi.

After installing (on Windows) / unpacking (on Unixes) you find an executable file named `dedop-shell` in the
installation's root directory. Running it brings up the *DeDop Shell*.

From Source
------------

DeDop is programmed in Python so you first need to setup a suitable Python environment.
We recommend using a `Miniconda <http://conda.pydata.org/miniconda.html>`_ Python3 environment, so
you don't need to install the DeDop library dependencies in your default Python.

First, checkout the DeDop source code from GitHub::

    git clone https://github.com/DeDop/dedop-core.git

Step into the newly created source directory::

    cd dedop-core

After installing Miniconda, open a terminal window and create an isolated Python environment with all the required
dependencies as listed in `environment.yml` and *activate* it. Type::

    conda env create --file environment.yml
    source activate dedop  # Linux, MacOS
    activate dedop         # Windows

Install DeDop in the Python environment `dedop`::

    python setup.py develop

After installing from source, you should be able to run the DeDop Shell, try::

    dedop --help

If you plan to run DeDop Studio, please run the following command::

    dedop-webapi

This is necessary to trigger the creation of `~/.dedop/<version_num>/dedop-location` file. In the installation from binary,
this is not required because at the end of the installation, this file is automatically created.


DeDop Studio Installation
==========================

As illustrated in :ref:`this diagram<dedop_diagram>`, DeDop studio is dependent on DeDop core in performing any processing duties.
For this reason, make sure that DeDop core has been installed in your computer before performing DeDop studio installation.
Failure to do that will result in the DeDop studio failing to startup.

From Binaries
--------------

DeDop is distributed as pre-compiled binaries which can be retrieved from
`DeDop Studio release page <https://github.com/DeDop/dedop-studio/releases/tag/v1.2.0>`_.
For the windows Windows platforms there is an easy one-click installer executable. For Mac OS, the installer is available
as dmg file and zip file, while for Unix, the installer is availble as tar.gz, zip, and AppImage files. Please make sure that
you have already installed DeDop-core before starting the DeDop-studio installation. More information about this can be found
:ref:`in this section <studio_intro>`.

Please note that in Windows, you may need to accept the warning at the beginning in regards to installing a third-party software.
Similarly in MacOS, you may need to enable an installation of third-party software: More information about it can be found
`in Gatekeeper page <https://support.apple.com/en-us/HT202491>`_.

After the installation has been completed, you will find an executable file named `DeDop-Studio`, which you can search using
start menu (Windows) or Spotlight (MacOS).

From Source
------------

Pre-requisites
---------------
- nodejs v6.9.1
- npm v3.10.8
- git
- dedop-core

How-to-install
---------------

First of all, clone the dedop-core repository::

    git clone https://github.com/DeDop/dedop-studio.git

Do npm install::

    cd dedop-studio
    npm install

Create a `dedop-config.js` and put the location of ``dedop-webapi.exe`` (Windows) or ``dedop-webapi`` (MacOS and Linux) under ``webAPIConfig`` field.
More information about the can be found in ``dedop-config.template.js``. Sample values for ``webAPIConfig`` in different OS's are
provided here::

    # Windows
    webAPIConfig: {
      command: "C:\\Miniconda3\\envs\\dedop\\Scripts\\dedop-webapi.exe",
      servicePort: 2999,
      processOptions: {}
    }

    # MacOS
    webAPIConfig: {
      command: "/Users/userName/miniconda3/envs/dedop/bin/dedop-webapi",
      servicePort: 2999,
      processOptions: {}
    }

    # Linux
    webAPIConfig: {
      command: "/home/userName/miniconda3/envs/dedop/bin/dedop-webapi",
      servicePort: 2999,
      processOptions: {}
    }

Compile::

  npm run compile

Start::

  npm start

