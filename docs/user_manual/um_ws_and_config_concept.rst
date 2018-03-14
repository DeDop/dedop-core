===================================
Workspace and Configuration Concept
===================================

Workspace
==========

**Workspace** in DeDop Shell refers to a space in the file system in which all the requires parts for processing are located.
They include source files, configurations, output files, as well as the Jupyter notebooks. It is possible to have multiple
workspaces and by default they are located under ``$USER_DIR/.dedop/workspaces``.
For example::

   C:\\Users\\dummy_user\\.dedop\\workspaces  # Windows
   /home/dummy_user/.dedop/workspaces         # Linux
   /Users/dummy_user/.dedop/workspaces        # MacOS

When DeDop Shell runs for the first time, there is no workspace available. An automatic creation of default workspace can
be triggered by running ``dedop input add some/path/to/your/L1A.nc`` or ``dedop run`` command as described
:ref:`here <processing_l1a_l1b>`.

Another (more recommended) way to add a new workspace is by running the following command::

   $ dedop w add workspace_name

Upon successful operation, the following responses shall be returned::

   created workspace "workspace_name"
   current workspace is "workspace_name"

This means that the new workspace has been successfully created and made the current workspace, which means that, unless
explicitly changed, whatever operations being performed after this will happen inside this workspace.

Inside ``workspaces`` directory, there is a file called ``.current``, inside which the name of the current workspace can
be found. When there is no current workspace (eg. because there is no more workspace after a deletion), this file will
be empty.

More information and example on workspace management operations, please go to :ref:`here <workspace_manag>`.

Configuration
==============

**DeDop configuration** refers to a set of configurations (Configuration, Characterization, Constants), which in the file
system are stored as CNF.json, CHD.json, and CST.json. Most of the time, users will need to modify only the **Configuration**
(CNF.json).
A configuration is represented by a directory with a name of the configuration name and is located under ``configs``
directory inside a workspace directory. It is possible to have multiple configurations under each workspace and it is
recommended to have a new configuration for different set of configuration values because in the end the generated output
products have a one-to-one relationship with the configuration. This enables a particular output to be easily reproduced
in the future, if required.

As in ``workspaces`` directory, there is a ``.current`` file inside ``configs`` directory. It works following exactly the same
concept: this file has the information on what is the current configuration. In the case of no current configuration,
this file will be empty.

More information and example on configuration management operations, please go to :ref:`here <config_manag>`.