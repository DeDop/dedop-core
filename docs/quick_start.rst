
.. _quick_start:

===========
Quick Start
===========

The DeDop tool set currently comprises only the *DeDop Shell* - a command-line interface to the DPP.

This section is a tutorial for users new to the DeDop Shell.

If you haven't installed DeDop yet, please refer to :doc:`installation`.

During installation, a new menu entry or desktop shortcut named **DeDop Shell** should have been created.
If you open it, a new terminal window should open up. Type::

    $ dedop -h

to list the available DeDop sub-commands. You can get help on sub-commands as well::

    $ dedop run -h

To perform L1A to L1B processing using the Delay Doppler Processor (DDP) you need to add one or more L1A
input files to your current DeDop *workspace*::

    $ dedop input add EOData/L1A.nc
    created workspace "default"
    current workspace is "default"
    adding inputs: done
    one input added

From the output, you can see that a new workspace named ``default`` has been created.
The following command lets you edit the current DDP configuration::

    $ dedop config edit
    created configuration "default" in workspace "default"
    current configuration is "default"

From the output, you can see that a new processor configuration named ``default`` has been created.
The ``dedop config edit`` command should open three processor configuration files in your default text editor.
Their format is JSON. You may change any processor configuration settings now and save them.

Finally run the processor::

    $ dedop run

If the command succeeds, the L1B output files can be found in ``workspaces/default/configs/default/outputs``
which is by default located in the DeDop user data directory. On Unixes and Darwin (OS) this directory
is ``~/.dedop`` while on Windows it is ``C:/Users/<username>/.dedop``. The location of your workspaces directory
can be changed by configuration. Please refer to the :doc:`manual`.

If the processor run was successful you can inspect the generated L1B file::

    $ dedop output inspect L1B.nc

This command should open up a web browser window that displays a an interactive *Jupyter Notebook*.
Also a second terminal window should have opened up. This hosts the Jupyter Notebook server process.
Just close the terminal window, if you no longer require the notebook.

