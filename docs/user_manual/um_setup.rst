======
Setup
======

DeDop Core Installation
========================

From Binaries
--------------

DeDop Core is distributed as pre-compiled binaries which can be retrieved from `here <https://github.com/DeDop/dedop-core/releases/tag/v1.3.0>`_.
For the windows Windows platforms there is a dedicated installer executable. For MacOS and Unix a shell script file is
provided. All platform distributions have a bundled Python interpreter, which makes it rather large in size
(roughly 300-400 MB). As mentioned before, this package also contains DeDop processor and DeDop webapi. To install DeDop
Core in Windows, double click the ``exe`` file.

In MacOS, run the following commands::

    chmod u+x DeDop-core-1.x.x-MacOSX-x86_64.sh
    ./DeDop-core-1.x.x-MacOSX-x86_64.sh

In Unix, run the following commands::

    chmod u+x DeDop-core-1.x.x-Linux-x86_64.sh
    ./DeDop-core-1.x.x-Linux-x86_64.sh

During installation, you will be requested the installation location as well as a preference to add this location to
your PATH. When unsure, just follow the default (no).

Run the following command to start DeDop Shell::

    <dedop_core_installation_dir>\Scripts\dedop-shell.bat   # Windows
    <dedop_core_installation_dir>/bin/dedop-shell.command   # MacOS
    <dedop_core_installation_dir>/bin/dedop-shell.sh        # Unix

From Source
------------

DeDop is programmed in Python so you first need to setup a suitable Python environment.
We recommend using a `Miniconda <http://conda.pydata.org/miniconda.html>`_ Python3 environment to create an isolated
environment that is independent from the default Python in your machine. Refer to `this page <https://conda.io/docs/user-guide/install/index.html>`_
for the instruction on how to install Miniconda on your machine. It is recommended to install Miniconda with Python 3.x
since DeDop Core uses Python 3.

To install DeDop Core from source, first you need to checkout the DeDop Core GitHub repository::

    git clone https://github.com/DeDop/dedop-core.git

Step into the newly created source directory::

    cd dedop-core

After installing Miniconda, open a terminal window and create ``dedop`` environment with all the required
dependencies as listed in `environment.yml` by typing::

    <miniconda_installation_dir>/bin/conda env create --file environment.yml

To activate this environment, type::

    source <miniconda_installation_dir>/bin/activate dedop      # Linux, MacOS
    <miniconda_installation_dir>\Scripts\activate dedop         # Windows

Install DeDop in the Python environment `dedop`::

    python setup.py install

After the installation is finished, start DeDop Shell by typing::

    dedop --help

If you plan to run DeDop Studio, please run the following command::

    dedop-webapi --version

This is necessary to trigger the creation of `~/.dedop/<version_num>/dedop-location` file. In the installation from binary,
this is not required because at the end of the installation, this file is automatically created.


DeDop Studio Installation
==========================

As illustrated in :ref:`this diagram<dedop_diagram>`, DeDop Studio is dependent on DeDop Core in performing any processing
tasks. For this reason, make sure that DeDop Core has been installed in your computer before performing DeDop Studio
installation. Failure to do that will result in the DeDop studio failing to startup.

From Binaries
--------------

DeDop is distributed as pre-compiled binaries which can be retrieved from
`DeDop Studio release page <https://github.com/DeDop/dedop-studio/releases/tag/v1.3.0>`_.
For the windows Windows platforms there is an easy one-click installer executable. For MacOS, the installer is available
as dmg file and zip file, while for Unix, the installer is available as tar.gz, zip, and AppImage files. All DeDop Studio
installers (except  the Unix tar.gz and zip files) are light-weight and executed by double clicking them. They don’t
require any extra user input.

Please note that in Windows, you may need to accept the warning at the beginning in regards to installing a third-party
software. Similarly in MacOS, you may need to allow installation of apps downloaded from `App Store and identified developers`.
More information about it can be found `in Gatekeeper page <https://support.apple.com/en-us/HT202491>`_.

After the installation has been completed, you will find an executable file named `DeDop-Studio`, which you can search using
start menu (Windows) or Spotlight (MacOS).

From Source
------------

---------------
Pre-requisites
---------------

The following software needs to be installed on your machine before you can start installing DeDop Studio from source:

    - nodejs v6.9.1
    - npm v3.10.8 (comes with nodejs)

Go to `here <https://nodejs.org/en/download/releases/>`_ for downloading nodejs and
`here <https://nodejs.org/en/download/package-manager/>`_ for the installation guide.

---------------
How-to-install
---------------

Clone dedop-studio repository::

    git clone https://github.com/DeDop/dedop-studio.git

Do npm install::

    cd dedop-studio
    npm install

Create a `dedop-config.js` inside `dedop-studio` directory and put the location of ``dedop-webapi.exe`` (Windows) or
``dedop-webapi`` (MacOS and Linux) under ``webAPIConfig`` field. The location of ``dedop-webapi`` will be where the
dedop environment is, eg.::

    <miniconda_installation_dir>\envs\dedop\Scripts\dedop-webapi.exe    # Windows with DeDop Core installation from source
    <miniconda_installation_dir>/envs/dedop/bin/dedop-webapi            # MacOS & Unix with DeDop Core installation from source

    <dedop-core_installation_dir>\Scripts\dedop-webapi.exe              # Windows with DeDop Core installation from binary
    <dedop-core_installation_dir>/bin/dedop-webapi                      # MacOS & Unix with DeDop Core installation from binary


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

