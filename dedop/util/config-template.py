###############################################################################
# This is a DeDop Tools configuration file.
#
# As this is a regular Python script, you may use any Python code to compute
# the settings provided here.
###############################################################################

# 'workspaces_dir' is where the DeDop Shell stores your workspaces.
# Use the tilde '~' (also on Windows) to point to your home directory.
#
# workspaces_dir = '~/.dedop/workspaces'


# 'launch_notebook_command' is the OS-specific shell command string used to launch a new Jupyter notebook server.
# The following template parameters may be used in the string and are replaced by DeDop:
#   - {title} - the title of a new terminal/command prompt.
#   - {command} - the actual command that launches the notebook server.
#   - {command_file} - an executable file that launches the notebook server.
#   - {prefix} - the path to the current Python environment in use.
# 'launch_notebook_in_new_terminal' should be set to True if your command
# creates a new terminal window.
#
# E.g. to launch a new, maximized command prompt on Windows use:
#
# launch_notebook_command = 'start "{title}" /Max {command}'
# launch_notebook_in_new_terminal = True
#
# E.g. to not launch a new terminal window at all:
#
# launch_notebook_command = '{command}'
# launch_notebook_in_new_terminal = False


# 'launch_editor_command' is the OS-specific shell command string used to edit your processor configuration files.
# The following template parameters may be used in the string and are replaced by DeDop:
#   - {file} - the file to be opened for editing.
#
# launch_editor_command = 'notepad "{file}"'


#------------------------------------------------------------------------------
# Developer section
#------------------------------------------------------------------------------
#
# 'processor_factory' is a Python callable which creates a new DDP instance used by the DeDop Shell
# (command-line interface).
#
#import dedop.model.processor
#processor_factory = dedop.model.processor.DummyProcessor

