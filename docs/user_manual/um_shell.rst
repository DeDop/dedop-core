============
DeDop Shell
============

Overview
========

DeDop Shell comprises a single command-line executable, which is called ``dedop`` and is available after installing
the DeDop Shell on your computer. With this tool, users can have a complete interaction with the input data, processor,
configuration, and finally the output products. If you have not done so, see section :doc:`um_setup` to install and
initialize DeDop Shell.

In this section, you will find a complete manual on how to use DeDop Shell. This can be sub-divided into the following
parts:

- :ref:`Workspace Management <workspace_manag>`
- :ref:`Source File Management <source_file_manag>`
- :ref:`Processor Configuration Management <config_manag>`
- :ref:`Running the Processor <run_proc>`
- :ref:`Analyse the Results <analyse_results>`


.. _workspace_manag:

Workspace Management
====================

Add a new workspace
--------------------

When DeDop Shell runs for the first time, there is no workspace available. An automatic creation of default workspace can
be triggered by running ``dedop input add some/path/to/your/L1A.nc`` or ``dedop run`` command as described
:ref:`here <processing_l1a_l1b>`.

To add a new workspace is by running the following command::

   $ dedop w add workspace_name

Upon successful operation, the following responses shall be returned::

   $ created workspace "workspace_name"
   $ current workspace is "workspace_name"

This means that the new workspace has been successfully created and made the current workspace, which means that, unless
explicitly changed, whatever operations being performed after this will happen inside this workspace.

Remove a workspace
-------------------

To remove a workspace, run one of the following commands::

   $ dedop w remove                   # CASE 1
   $ dedop w remove workspace_name    # CASE 2

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

   $ dedop w copy                                       # CASE 1
   $ dedop w copy workspace_to_be_copied                # CASE 2
   $ dedop w copy workspace_to_be_copied new_workspace  # CASE 3

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

   $ dedop w rename new_workspace_name                           # CASE 1
   $ dedop w rename workspace_to_be_renamed new_workspace_name   # CASE 2

In **CASE 1**, the current workspace will be renamed to ``new_workspace_name``. The current workspace will be automatically
changed after the renaming.

In **CASE 2**, the specified workspace will be renamed to ``new_workspace_name``. There is **NO** change on the current workspace.

``rename`` has an alias ``rn``.

Get current workspace
----------------------

It is sometimes useful to know in which workspace we are working on at the moment. To get that information, run the following::

   $ dedop w current

If there is a current workspace, the name of the current workspace will be returned. Otherwise, ``no current workspace``
will be returned.

``current`` has an alias ``cur``.

List workspaces
---------------

To list available workspaces, run the following command::

   dedop w list

``list`` has an alias ``ls``.

.. _source_file_manag:

Source File Management
======================

After creating a workspace, the next step is to manage the L1A source files.

Add new L1A source file
------------------------

To add a new L1A file(s) into this workspace, run the following command::

   $ dedop i add /path/to/file1 /path/to/file2 /path/to/file3

What this command does is copying those files into the current workspace directory. When successful, those files will be
located inside ``inputs`` directory under the current workspace directory. Every workspace will have its own ``inputs``
directory, which in the end can be used as a source file for running multiple processes with different configurations.

Remove L1A source file
-----------------------

To remove the previously-added L1A file(s), run one of the following commands::

   $ dedop i remove                                           # CASE 1
   $ dedop i remove file_name1 file_name2                     # CASE 2
   $ dedop i remove -w workspace_name                         # CASE 3
   $ dedop i remove -w workspace_name file_name1 file_name2   # CASE 4

In all cases, a confirmation prompt will appear to really ensure that this action is intentional. To disable this prompt,
use the optional argument ``--quiet`` (eg. ``dedop i remove --quiet``).

In **CASE 1**, all previously-added source files in the current workspace will be removed.

In **CASE 2**, the specified files in the current workspace will be removed.

In **CASE 3**, all previously-added source in the specified workspace will be removed.

In **CASE 4**, the specified files in the specified workspace will be removed.

``remove`` has an alias ``rm``.

List all L1A source files
--------------------------

To list all source files that have been added, run one of the following commands::

   $ dedop i list                     # CASE 1
   $ dedop i list -w other_workspace  # CASE 2
   $ dedop i list L1A*                # CASE 3

In **CASE 1**, the tool will return a list of all source files in the current workspace.

In **CASE 2**, the tool will return a list of all source files in the specified workspace.

In **CASE 3**, the tool will return a list of all source files that match the given regex ``L1A*``.

``list`` has an alias ``ls``.

.. _config_manag:

Processor Configuration Management
==================================

The next step before running an actual process is to manage the configurations.

Add a new configuration
------------------------

To add a new configuration, run one of the following commands::

   $ dedop c add new_config_name                     # CASE 1
   $ dedop c add -w other_workspace new_config_name  # CASE 2
   $ dedop c add --cryosat-adapted new_config_name   # CASE 3

In all cases, a new folder named ``new_config_name`` is created under a workspace and it consists of three default configuration
files ``CHD.json``, ``CNF.json``, and ``CST.json``. The generated configurations are by default for ``Sentinel-3`` processing
unless when ``--cryosat-adapted`` is specified.

In **CASE 1**, a new configuration will be created under the current workspace directory.

In **CASE 2**, a new configuration will be created under the specified workspace directory.

In **CASE 3**, a new configuration suited for Adapted Cryosat-2 FBR data will be created under the current workspace directory.

Remove a configuration
-----------------------

To remove a configuration, run one of the following commands::

   $ dedop c remove                                  # CASE 1
   $ dedop c remove config_name                      # CASE 2
   $ dedop c remove -w other_workspace config_name   # CASE 3

In all cases, a confirmation prompt will appear to really ensure that this action is intentional. To disable this prompt,
use the optional argument ``--yes`` (eg. ``dedop c remove --yes``). Removing a configuration means deleting a configuration
folder including its contents (all the CHD, CNF, and CST files).

In **CASE 1**, the current configuration in the current workspace will be removed. It will then change the current configuration
to the next configuration. When none left, it will go into a state where there are no current configurations.

In **CASE 2**, the specified configuration in the current workspace will be removed. There is no change of current configuration
if it does not involve current configuration.

In **CASE 3**, the specified configuration inside a specified workspace will be removed.

``remove`` has an alias ``rm``.

Modify a configuration
-----------------------

To modify a configuration, run one of the following commands::

   $ dedop c edit                                 # CASE 1
   $ dedop c edit config_name                     # CASE 2
   $ dedop c edit -w other_workspace config_name  # CASE 3

In all cases, it will launch a text editor and open all three configuration files. The text editor to be launched is OS-dependent
and it is configurable on the :ref:`Tool Configuration <tool_config>` with the key name :ref:`launch_editor_command <tool_config_parameters>`.

In **CASE 1**, the text editor will open all the configuration files of the current configuration under the current workspace.

In **CASE 2**, the text editor will open all the configuration files of the specified configuration under the current workspace.

In **CASE 3**, the text editor will open all the configuration files of the specified configuration under the specified workspace.

When you are finished, just save the files and close the editor.

``edit`` has an alias ``ed``.

Copy a configuration
---------------------

To copy a configuration, run one of the following commands::

   $ dedop c copy                                                               # CASE 1
   $ dedop c copy config_name_to_be_copied                                      # CASE 2
   $ dedop c copy config_name_to_be_copied new_config_name                      # CASE 3
   $ dedop c copy -w other_workspace config_name_to_be_copied new_config_name   # CASE 4

In **CASE 1**, neither the configuration to be copied nor the new configuration name is specified, so in this case a new
name with the format of ``current_config_name + _copy_ + unique_number`` is created. The unique number will be incremented
until a unique combination is constructed. For example, for a current config ``config1``, it will create a new config
named ``config1_copy``, ``config1_copy_2``, ``config1_copy_3``, and so on.

In **CASE 2**, the configuration to be copied is specified, but not the name of the new config. It will then follow the
same rule as in **CASE 1**, by creating a new config with a name that is of format
``current_config_name + _copy_ + unique_number``.

In **CASE 3**, the specified configuration will be copied as ``new_config_name`` inside the current workspace

In **CASE 4**, the specified configuration will be copied as ``new_config_name`` inside the specified workspace

As in workspace management, copying a configuration does **NOT** automatically change the current configuration.

``copy`` has an alias ``cp``.

Rename a configuration
-----------------------

To rename a configuration, run one of the following commands::

   $ dedop c rename new_config_name                                          # CASE 1
   $ dedop c rename config_to_be_renamed new_config_name                     # CASE 2
   $ dedop c rename -w other_workspace config_to_be_renamed new_config_name  # CASE 3

In **CASE 1**, the current config name will be renamed to ``new_config_name``. The current configuration will also be
changed to ``new_config_name``.

In **CASE 2**, the specified config name in the current workspace will be renamed to ``new_config_name``.

In **CASE 3**, the specified config name in the specified workspace will be renamed to ``new_config_name``.

``rename`` has an alias ``rn``.

Show configuration info
------------------------

To display information about the configuration such as current configuration path, list of files, as well as the file sizes,
run the following command::

   $ dedop c info                                 # CASE 1
   $ dedop c info other_config                    # CASE 2
   $ dedop c info -w other_workspace config_name  # CASE 3

In **CASE 1**, information for the current configuration in the current workspace will be displayed.

In **CASE 2**, information for the specified configuration in the current workspace will be displayed.

In **CASE 3**, information for the specified configuration in the specified workspace will be displayed.

``info`` has an alias ``i``.

Get current configuration
--------------------------

To get the current configuration name, run the following::

   $ dedop c current

If there is a current configuration, the name of the current configuration will be returned. Otherwise,
``no current DDP configuration`` will be returned.

It is also possible to get the current configuration in the other workspace by adding this parameter
``-w other_workspace_name`` in the command.

``current`` has an alias ``cur``.

List configurations
--------------------

To list available configurations, run one of the following commands::

   $ dedop c list

As before, to list available configurations in the other workspace, just add ``-w other_workspace_name`` in the command.

``list`` has an alias ``ls``.

Upgrade configurations
-----------------------

A new version of DeDop Core sometimes comes with new versions of configuration files. In order to update your configurations,
run the following command::

   $ dedop c upgrade

Failure to use the latest version of configurations may result in processing errors.

``upgrade`` has an alias ``up``.

Show configuration version
---------------------------

To display the current configuration version, run the following command::

   $ dedop c version

``version`` has an alias ``v``.

.. _run_proc:

Running the Processor
=====================

Once the L1A source files have been added and configurations have been created, it is time to run the processing. To
do that, use the following command::

   $ dedop run

This command calls a processor to process L1A files to L1B (and possible L1BS). More information on how the processor
works, go to :ref:`here <processor_info_not_yet_exists>`. By default, the command above will process every single L1A files
inside the ``inputs`` directory under the current workspace, unless ``--inputs [L1A_FILE [L1A_FILE ...]]`` flag is specified.

The default behaviour is that the current configuration is used for processing. However, when ``--all-configs``
flag is set, it will process the input files with all available configurations in the current workspace, producing an
output for each configuration. The output products will be located inside ``outputs`` directory under each configuration
directory. To specify other locations for the outputs, the flag ``--output DIR`` can be used.

When the flag ``--skip-l1bs`` is added to the command above, the process will generate only L1B files.


.. _analyse_results:

Analyse the Results
====================

After the processing has been finished, we can now compare the L1B outputs in an interactive Jupyter Notebook::

    $ dedop output compare -C default L1B_myconf.nc L1B_default.nc

When you pass just file *names* to the ``dedop output compare`` command, DeDop must know to which configurations they
refer to. The first filename corresponds to the *current* DDP configuration or the one given by the ``-c`` option.
The second filename corresponds to a DDP configuration given by the ``-C`` (upper case!) option.
You can also pass file *paths* to the ``dedop output compare`` command in which case the configuration names are ignored.

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

.. _tool_config_parameters:

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


.. _command_ref:

Command Reference
=================

The following examples shall help you understand the basic concepts behind the various ``dedop`` commands.

.. argparse::
   :module: dedop.cli.main
   :func: _make_dedop_parser
   :prog: dedop