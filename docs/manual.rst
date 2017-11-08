======
Manual
======

The DeDop tool set currently comprises only the *DeDop Shell* - a command-line interface to the
Delay Doppler Processor (DDP).


.. _workspace_manag:

Workspace Management
====================

**Workspace** in DeDop Shell refers to a space in the file system in which all the requires parts for processing are located.
They include input files, configurations, output files, as well as the Jupyter notebooks. It is possible to have multiple
workspaces and by default they are located under ``$USER_DIR/.dedop/workspaces``.
For example::

   C:\\Users\\dummy_user\\.dedop\\workspaces  # Windows
   /home/dummy_user/.dedop/workspaces         # Linux
   /Users/dummy_user/.dedop/workspaces        # MacOS

Add a new workspace
--------------------

When DeDop Shell runs for the first time, there is no workspace available. An automatic creation of default workspace can
be triggered by running ``dedop input add some/path/to/your/L1A.nc`` or ``dedop run`` command as described
:ref:`here <processing_l1a_l1b>`.

Another (more recommended) way to add a new workspace is by running the following command::

   dedop w add workspace_name

Upon successful operation, the following responses shall be returned::

   created workspace "workspace_name"
   current workspace is "workspace_name"

This means that the new workspace has been successfully created and made the current workspace, which means that, unless
explicitly changed, whatever operations being performed after this will happen inside this workspace.

Remove a workspace
-------------------

To remove a workspace, run one of the following commands::

   dedop w remove                   # CASE 1
   dedop w remove workspace_name    # CASE 2

In both cases, a confirmation prompt will appear to really ensure that this action is intentional. To disable this prompt,
use the optional argument ``--yes`` (eg. ``dedop w remove --yes``).

In **CASE 1**, the tool will remove the current workspace. It will then change the current workspace to the next workspace.
When no more workspaces exist, it will just be assumed that there is no current workspace.

In **CASE 2**, the tool will remove the specified workspace. If the specified name is also the current workspace name, the
above scenario will be in effect.

``remove`` has an alias ``rm``.

Copy a workspace
-----------------

To copy a workspace, run one of the following commands::

   dedop w copy                                       # CASE 1
   dedop w copy workspace_to_be_copied                # CASE 2
   dedop w copy workspace_to_be_copied new_workspace  # CASE 3

In **CASE 1**, without specifying which workspace to be copied, it will default to the current workspace. The new workspace
name is also not specified, so in this case a new name with the format of ``current_workspace_name + _ + unique_number``
is created. The unique number will be incremented until a unique combination is constructed. For example, for a current
workspace ``workspace1``, it will create a new workspace named ``workspace1_1``.

In **CASE 2**, the workspace to be copied is specified, but not the name of the new workspace. It will then follow the
same rule as in **CASE 1**, by creating a new workspace with a name that is of format ``workspace_to_be_copied + _ + unique_number``.

In **CASE 3**, both the workspace to be copied and the name of the new workspace are specified. It is very clear that
it will copy the specified workspace to a new workspace with the specified name.

One thing that is worth mentioning is that copying a workspace does not automatically change the current workspace.

``copy`` has an alias ``cp``.

Rename a workspace
------------------

To rename a workspace, run one of the following commands::

   dedop w rename new_workspace_name                           # CASE 1
   dedop w rename workspace_to_be_renamed new_workspace_name   # CASE 2

In **CASE 1**, the current workspace will be renamed to ``new_workspace_name``. The current workspace will be automatically
changed after the renaming.

In **CASE 2**, the specified workspace will be renamed to ``new_workspace_name``. There is **NO** change on the current workspace.

``rename`` has an alias ``rn``.

Get current workspace
----------------------

It is sometimes useful to know in which workspace we are working on at the moment. To get that information, run the following::

   dedop w current

If there is a current workspace, the name of the current workspace will be returned. Otherwise, ``no current workspace``
will be returned.

``current`` has an alias ``cur``.

List workspaces
---------------

To list available workspaces, run the following command::

   dedop w list

``list`` has an alias ``ls``.

.. _source_file_manag:

L1A Source File Management
==========================

TODO

.. _config_manag:

Processor Configuration Management
==================================

TODO

.. _run_proc:

Running the Processor
=====================

TODO

.. _analyse_l1b:

Analysing L1B Results
=====================

TODO

.. _command_ref:

Command Reference
=================

TODO

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