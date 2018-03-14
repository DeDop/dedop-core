

.. _quick_start:

===========
Quick Start
===========

This chapter is a tutorial for users new to the DeDop Shell.

Refer to :doc:`user_manual/um_setup` for installing DeDop.

Using DeDop Shell
=================

In the new terminal window, type::

    $ dedop -h

to list the available DeDop sub-commands. You can get help on sub-commands as well::

    $ dedop run -h


.. _processing_l1a_l1b:

----------------------
Processing L1A to L1B
----------------------

To perform L1A to L1B processing using the Delay Doppler Processor (DDP) you need to add one or more L1A
input files to your current DeDop *workspace*. For example, download
`Amazon <http://dedop.org/data/resources/Amazon/CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL.nc>`_
or `Iceberg <http://dedop.org/data/resources/Icebergs/CS_LTA__SIR1SAR_FR_20130303T030418_20130303T030503_C001.DBL.nc>`_
L1A data. And then, add the file(s) to your dedop workspace::

    $ dedop input add some/path/to/CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL.nc
    created workspace "default"
    current workspace is "default"
    adding inputs: done
    one input added

From the output, you can see that a new workspace named ``default`` and a new DDP configuration also named ``default``
Now run the processor with default settings::

    $ dedop run
    created DDP configuration "default" in workspace "default"
    current DDP configuration is "default"
    processing ~/.dedop/workspaces/default/inputs/CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL.nc using "default"
    processing: [##########------------------------------] 25%
    ...
    processing took 0:05:03.159575

If the command succeeded, the L1B output files can be found in ``workspaces/default/configs/default/outputs``,
which is by default located in the DeDop user data directory. On Unixes and Darwin (OS) this directory
is ``~/.dedop`` while on Windows it is ``C:/Users/<username>/.dedop``. The location of your workspaces directory
can be changed by configuration. Please refer to the :ref:`tool_config_parameters`.

If the processor run was successful you can inspect the generated L1B file::

    $ dedop output inspect L1B_default.nc

This command should open up a web browser window that displays an interactive *Jupyter Notebook*.
Also a second terminal window should have opened up. This hosts the Jupyter Notebook server process.
Just close the terminal window, if you no longer require the Notebook.

If you like to perform your analysis in batch mode rather than using the interactive Notebook,
you can do so by writing your own analysis script in Python. An example is given in DeDop's
source code repository: `inspect-script.py <https://github.com/DeDop/dedop/blob/master/inspect-script.py>`_.

This script can by run with the Python interpreter bundled with the dedop installation. To generate a multi page PDF use an
output filename that has the ``.pdf`` extension::

    $ python inspect-script.py some/path/L1B_default.nc inspect-out.pdf

To generate a directory of figure images, run the script with a directory name or with ``dir`` as 3rd argument::

    $ python inspect-script.py some/path/L1B_default.nc inspect-out dir


------------------------------------
Changing the processor configuration
------------------------------------

From the last steps above, the current DDP configuration should be still ``default``. Verify::

    $ dedop status
    configuration location:     ~/.dedop/config.py
    workspaces location:        ~/.dedop/workspaces
    workspaces total size:      150 MiB
    workspace names:            default
    current workspace:          default
    current DDP configuration:  default


We will now create a new configuration ``myconf``, type::

    $ dedop config add myconf
    created DDP configuration "myconf" in workspace "default"
    current DDP configuration is "myconf"

From the output, you can see that a new DDP configuration named ``myconf`` has been created and is now the current one.
To modify the configuration, type::

    $ dedop config edit

Now three DDP configuration files should have been opened in your default text editor.
Their format is JSON. You may change any DDP configuration settings now, for example, in the ``CHD.json``
(the *characterisation definition file*) change the value of the parameter ``uso_freq_nom_chd`` from its
default value ``10e6`` to ``7.5e6``::

   "uso_freq_nom_chd": {
        "value": 7.5e6,
        "description": "USO nominal frequency",
        "units": "Hz"
   },

Save the configuration file in your text editor.

Now run the processor with the modified DDP configuration ``myconf``::

    $ dedop run

We can now compare the L1B outputs in an interactive Jupyter Notebook::

    $ dedop output compare -C default L1B_myconf.nc L1B_default.nc

When you pass just file *names* to the ``dedop output compare`` command, DeDop must know to which configurations they
refer to. The first filename corresponds to the *current* DDP configuration or the one given by the ``-c`` option.
The second filename corresponds to a DDP configuration given by the ``-C`` (upper case!) option.
You can also pass file *paths* to the ``dedop output compare`` command in which case the configuration names are ignored.

Again, if you like to perform your analysis in batch mode, you can do so by writing your own comparison analysis script
in Python. An example is given in DeDop's source code repository:
`compare-script.py <https://github.com/DeDop/dedop/blob/master/compare-script.py>`_.

This script can be run with the Python interpreter bundled with the dedop installation. To generate a multi page PDF use an
output filename that has the ``.pdf`` extension::

    $ python compare-script.py some/path/L1B_myconf.nc some/other/path/L1B_default.nc compare-out.pdf

To generate a directory of figure images, run the script with a directory name or with ``dir`` as 4th argument::

    $ python compare-script.py some/path/L1B_myconf.nc some/other/path/L1B_default.nc compare-out dir

