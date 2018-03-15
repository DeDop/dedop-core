

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
which is by default located in the DeDop user data directory. On Unix and MacOS this directory
is ``~/.dedop`` while on Windows it is ``C:/Users/<username>/.dedop``. The location of your workspaces directory
can be changed by configuration. Please refer to the :ref:`tool_config_parameters`.

If the processor run was successful you can observe new L1B and L1BS files::

    $ dedop output ls
    2 outputs created with config "default" in workspace "default":
      1: L1BS_CS_LTA__SIR1SAR_FR_20130303T030418_20130303T030503_C001.DBL_default.nc
      2: L1B_CS_LTA__SIR1SAR_FR_20130303T030418_20130303T030503_C001.DBL_default.nc

To inspect and interact with the generated L1B file::

    $ dedop output inspect L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc
    wrote notebook file "C:\Users\dedop-user\.dedop\workspaces\default\notebooks\inspect-L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc.ipynb"
    calling: start "DeDop - inspect - [...AR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc]" /Min "C:\Users\dedop-user\.dedop\temp\dedop-notebook-server.bat"
    A terminal window titled "DeDop - inspect - [...AR_FR..." has been opened.
    Close that window or press CTRL+C within it to terminate the Notebook session.

**NOTE**: the command above was executed in Windows machine. Command output in Unix or MacOS maybe different but comparable.

This command should open up a web browser window that displays an interactive *Jupyter Notebook*.
Also a second terminal window should have opened up. This hosts the Jupyter Notebook server process.
If you are not familiar with Jupyter Notebook, read the introduction `here <https://jupyter-notebook.readthedocs.io/en/stable/ui_components.html#>`_.
Try to run the commands in the Notebook by selecting **Cell > Run All**. Here is a `sample inspect Notebook <https://github.com/DeDop/dedop-core/blob/master/docs/notebooks/inspect-L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc-1.ipynb>`_
to show how it looks like for a successful run of ``inspect`` notebook (some graphics may not be able
to be displayed by GitHub).
When you are done with the Notebook, simply close the Notebook tab in the browser as well as the second terminal window.

If you like to perform your analysis in batch mode rather than using the interactive Notebook,
you can do so by writing your own analysis script in Python. An example is given in DeDop's
source code repository: `inspect-script.py <https://github.com/DeDop/dedop/blob/master/inspect-script.py>`_.

This script can by run with the Python interpreter bundled with the DeDop Core installation. To generate a multi page PDF,
with all the figures use an output filename that has the ``.pdf`` extension::

    $ python inspect-script.py "C:\Users\dedop-user\.dedop\workspaces\default\configs\default\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc" inspect-out.pdf

To generate a directory of figure images, run the script with a directory name or with ``dir`` as 3rd argument::

    $ python inspect-script.py "C:\Users\dedop-user\.dedop\workspaces\default\configs\default\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc" inspect-out dir


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

    $ dedop output compare -C default L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_myconf.nc L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc
    wrote notebook file "C:\Users\dedop-user\.dedop\workspaces\default\notebooks\compare-L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_myconf.nc-L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc-1.ipynb"
    calling: start "DeDop - compare - [...1T034235_C001.DBL_myconf.nc] [...T034235_C001.DBL_default.nc]" /Min "C:\Users\dedop-user\.dedop\temp\dedop-notebook-server.bat"
    A terminal window titled "DeDop - compare - [...1T034..." has been opened.
    Close that window or press CTRL+C within it to terminate the Notebook session.

When you pass just file *names* to the ``dedop output compare`` command, DeDop must know to which configurations they
refer to. The first filename corresponds to the *current* DDP configuration or the one given by the ``-c`` option.
The second filename corresponds to a DDP configuration given by the ``-C`` (upper case!) option.
Here is a `sample compare Notebook <https://github.com/DeDop/dedop-core/blob/master/docs/notebooks/compare-L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_myconf.nc-L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc-1.ipynb>`_
to show how it looks like for a successful run of ``compare`` notebook (some graphics may not be able
to be displayed by GitHub).

Instead of specifying the configuration name, you can also pass any two L1B *file paths* to the ``dedop output compare`` command::

    $ dedop output compare "C:\Users\dedop-user\.dedop\workspaces\default\configs\default\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc" "C:\Users\dedop-user\.dedop\workspaces\default\configs\myconf\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_myconf.nc"

Again, if you like to perform your analysis in batch mode, you can do so by writing your own comparison analysis script
in Python. An example is given in DeDop's source code repository:
`compare-script.py <https://github.com/DeDop/dedop/blob/master/compare-script.py>`_.

This script can be run with the Python interpreter bundled with the DeDop Core installation. To generate a multi page PDF use an
output filename that has the ``.pdf`` extension::

    $ python compare-script.py "C:\Users\dedop-user\.dedop\workspaces\default\configs\default\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc" "C:\Users\dedop-user\.dedop\workspaces\default\configs\myconf\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_myconf.nc" compare-out.pdf

To generate a directory of figure images, run the script with a directory name or with ``dir`` as 4th argument::

    $ python compare-script.py "C:\Users\dedop-user\.dedop\workspaces\default\configs\default\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_default.nc" "C:\Users\dedop-user\.dedop\workspaces\default\configs\myconf\outputs\L1B_CS_LTA__SIR1SAR_FR_20150331T034023_20150331T034235_C001.DBL_myconf.nc" compare-out dir

