======
Manual
======

The DeDop software manual has not yet been written. While it is being prepared, please refer to the :doc:`quickstart`,
which should give you a first impression how the DeDop Shell is used.

Please note that all DeDop Shell commands and also its sub-commands have a ``--help``, or shorter ``-h``, option that
you can use for getting more information.

.. _tool_config:

Tool Configuration
==================

Configuration File
------------------

When DeDop is run for the first time it will create a file ``config.py`` in the directory ``.dedop`` of the
current user's home directory. All DeDop tools use this file to read special software configuration parameters.

This is not to be confused with the *processor configurations* referred to in the dedicated section above.

**Unixes and Darwin**: On Unixes and Darwin (OS X), the full path to the DeDop tools configuration file is usually::

    /home/<username>/.dedop/config.py

where ``/home/<username>`` is also given by ``~`` or ``$HOME`` in a terminal or shell.


**Windows**: On Windows 7+, the full path to the DeDop tools configuration file is usually::

    C:/Users/<username>/.dedop/config.py

where ``C:/Users/<username>`` is also given by ``%USERPROFILE%`` on the Windows command-prompt.

To force writing a new DeDop tools configuration file use::

    $ dedop --new-conf

This may be useful after DeDop software updates. It will ensure that you get the latest configuration parameters
supported by a given DeDop version.

Configuration Parameters
------------------------

Given here are the current DeDop tools configuration parameters:

===================================  =====================================================   ===========================
Parameter name                       Description                                             Default value
===================================  =====================================================   ===========================
``workspaces_dir``                   Path where the DeDop Shell stores your workspaces.      ``'~/.dedop/workspaces'``
``launch_notebook_command``          An OS-specific shell command string used to launch a    *OS-specific*
                                     new Jupyter notebook server.
``launch_notebook_in_new_terminal``  Whether launching the notebook creates a new terminal   ``False``
                                     window.
``launch_editor_command``            An OS-specific shell command string used to launch a    *OS-specific*
                                     text editor for the processor configuration files.
===================================  =====================================================   ===========================


.. _cli_examples:

Examples
========

The following examples shall help you understand the basic concepts behind the various ``dedop`` commands.

.. argparse::
   :module: dedop.cli.main
   :func: _make_dedop_parser
   :prog: dedop