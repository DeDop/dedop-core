=======================
Manual for DeDop Studio
=======================

The DeDop tool set currently comprises the *DeDop Shell* - a command-line interface to the
Delay Doppler Processor (DDP) - and *DeDop Studio* - a graphical user interface to the
Delay Doppler Processor (DDP). In this section, you will find the manual for DeDop Studio.
For the manual of DeDop Shell go to :doc:`manual_shell`.


.. _workspace_manag_studio:

Workspace Management
====================

**Workspace** in DeDop Shell refers to a space in the file system in which all the requires parts for processing are located.
They include source files, configurations, output files, as well as the Jupyter notebooks. It is possible to have multiple
workspaces and by default they are located under ``$USER_DIR/.dedop/workspaces``.
For example::

   C:\\Users\\dummy_user\\.dedop\\workspaces  # Windows
   /home/dummy_user/.dedop/workspaces         # Linux
   /Users/dummy_user/.dedop/workspaces        # MacOS

Add a new workspace
--------------------


Remove a workspace
-------------------


Copy a workspace
-----------------


Rename a workspace
------------------


Get current workspace
----------------------


List workspaces
---------------


.. _source_file_manag_studio:

L1A Source File Management
==========================


Add new L1A source file
------------------------


Remove L1A source file
-----------------------


List all L1A source files
--------------------------


.. _config_manag_studio:

Processor Configuration Management
==================================


Add a new configuration
------------------------


Remove a configuration
-----------------------


Modify a configuration
-----------------------


Copy a configuration
---------------------


Rename a configuration
-----------------------


Show configuration info
------------------------


Get current configuration
--------------------------


List configurations
--------------------


Upgrade configurations
-----------------------


Show configuration version
---------------------------


.. _run_proc_studio:

Running the Processor
=====================


.. _analyse_l1b_studio:

Analysing L1B Results
=====================


.. _tool_config_studio:
