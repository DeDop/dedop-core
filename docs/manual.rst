======
Manual
======

The DeDop tool currently comprises only the DeDop Shell - a command-line interface to the DPP.

Quick Start
===========

Getting help on the DeDop Shell::

    $ dedop -h

You can get help on sub-commands as well::

    $ dedop run -h

Adding L1A input file(s)::

    $ dedop input add EOData/L1A.nc
    created workspace "default"
    current workspace is "default"
    adding inputs: done
    one input added

Editing the processor configuration::

    $ dedop config edit
    created configuration "default" in workspace "default"
    current configuration is "default"

The ``dedop config edit`` command should open three processor configuration files in your default text editor.
Their format is JSON. You may change settings now and save them.

Finally run the processor::

    $ dedop run

If the command succeeds, the L1B output files can be found in ``~/.dedop/workspaces/default/configs/default/outputs``
where ``~`` points to the current user's home directory.

Workspace Management
====================

TODO

Processor Configuration Management
==================================

TODO

Running the Processor
=====================

TODO

Command Reference
=================

TODO
