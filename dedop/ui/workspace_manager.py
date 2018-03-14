import collections
import fnmatch
import json
import ntpath
import os.path
import pkgutil
import shutil
import subprocess
import sys

from typing import List

from dedop.ui.workspace import Workspace
from dedop.ui.exception import WorkspaceError
from dedop.util.config import get_config_value

_DEFAULT_CONFIG_PACKAGE_NAME = 'dedop.ui.data.config'
_CRYOSAT_CONFIG_PACKAGE_NAME = 'dedop.ui.data.cryosat_config'
_WORKSPACES_DIR_NAME = 'workspaces'
_CONFIGS_DIR_NAME = 'configs'
_NOTEBOOKS_DIR_NAME = 'notebooks'
_INPUTS_DIR_NAME = 'inputs'
_OUTPUTS_DIR_NAME = 'outputs'
_CURRENT_FILE_NAME = '.current'

DEFAULT_WORKSPACES_DIR = os.path.expanduser(os.path.join('~', '.dedop', _WORKSPACES_DIR_NAME))
DEFAULT_TEMP_DIR = os.path.expanduser(os.path.join('~', '.dedop', 'temp'))


def _readline(file_path: str) -> str or None:
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as fp:
                return fp.readline()
        except (IOError, OSError) as e:
            raise WorkspaceError(str(e))
    return None


def _writeline(file_path: str, text: str):
    try:
        with open(file_path, 'w') as fp:
            fp.write(text)
    except (IOError, OSError) as e:
        raise WorkspaceError(str(e))


class WorkspaceManager:
    """
    Manages DeDop workspaces.

    A workspace contains multiple DDP configurations, source files and analysis results.
    A workspace is physically represented by a directory in the file system organised as follows:

    * ``.dedop/workspaces/``
      * ``<workspace-name>/``
        * ``configs``
          * ``<config-name>/*.json``
        * ``inputs/*.nc``
        * ``outputs/<config-name>/*.*``


    Technical requirements
    ----------------------
    1. Save disk space: We should avoid copies of L1A input files in every workspace. We may have a
       ``.dedop/inputs/`` containing the actual files and in workspace ``test3``
       we have ``.dedop/workspaces/test3/inputs`` which only contains symbolic links.
       (While we can use symbolic links on Unixes we could use text files containing the actual paths
       in Windows.)
    2. Context information: we need a **current workspace**. This could be physically represented
       by a file ``.dedop/workspaces/.current`` which contains the name of the current workspace.
       The name of current configuration within the current workspace could be stored in
       ``.dedop/workspaces/<workspace-name>/configs/.current``.
    3. Configurations: when creating a new configuration, the CNF, CST, CHD files are created from software data.
       This allows a user to share their workspace with someone else without worrying about whether
       either has edited their default configurations.
    4. Ease of use: there should be always a valid current workspace and current config. If ``workspaces``  is empty,
       ``default`` is used (and created). If ``configs`` of current workspace is empty,
       ``default`` is used (and created). Users can use both 'dedop ws rn NEW_NAME' and 'dedop ws cp NEW_NAME' to rename
       and copy the ``default``. The same is possible for the configuration.
    5. May be good to include current workspace and config names in cursor prompt
    """

    def __init__(self, workspaces_dir=None):
        self._workspaces_dir = workspaces_dir if workspaces_dir else DEFAULT_WORKSPACES_DIR

    @property
    def workspaces_dir(self):
        return self._workspaces_dir

    def delete_all_workspaces(self) -> str:
        if os.path.isdir(self._workspaces_dir):
            try:
                shutil.rmtree(self._workspaces_dir)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def get_current_workspace(self) -> Workspace:
        current_workspace = _readline(os.path.join(self._workspaces_dir, _CURRENT_FILE_NAME))
        return Workspace(None, current_workspace)

    def set_current_workspace_name(self, workspace_name: str):
        self._assert_workspace_exists(workspace_name)
        _writeline(os.path.join(self._workspaces_dir, _CURRENT_FILE_NAME), workspace_name)
        workspace_dir = self.get_workspace_path(workspace_name)
        return Workspace(workspace_dir, workspace_name, is_current=True)

    def workspace_exists(self, workspace_name) -> bool:
        return os.path.exists(self.get_workspace_path(workspace_name))

    def create_workspace(self, workspace_name: str) -> Workspace:
        """
        :param workspace_name: new workspace name
        :raise: WorkspaceError: when workspace already exists
        """
        if not workspace_name:
            raise WorkspaceError('no workspace name is specified')
        workspace_dir = self.get_workspace_path(workspace_name)
        if os.path.isdir(workspace_dir) and os.listdir(workspace_dir):
            raise WorkspaceError('workspace "%s" already exists' % workspace_name)
        self._ensure_dir_exists(workspace_dir)
        return Workspace(workspace_dir, workspace_name)

    def delete_workspace(self, workspace_name: str):
        """
        :param workspace_name: workspace name to be deleted
        :raise: WorkspaceError: thrown when workspace not found or cannot delete the workspace
        """
        self._assert_workspace_exists(workspace_name)
        dir_path = self.get_workspace_path(workspace_name)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def copy_workspace(self, workspace_name: str, new_workspace_name: str):
        """
        :param workspace_name: workspace name to be copied
        :param new_workspace_name: new workspace name
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        dir_path = self.get_workspace_path('')
        if os.path.exists(dir_path):
            try:
                shutil.copytree(os.path.join(dir_path, workspace_name),
                                os.path.join(dir_path, new_workspace_name))
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))
        workspace_dir = self.get_workspace_path(new_workspace_name)
        return Workspace(workspace_dir, new_workspace_name)

    def rename_workspace(self, workspace_name: str, new_workspace_name: str):
        """
        :param workspace_name: workspace name to be renamed
        :param new_workspace_name: new workspace name
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        if not new_workspace_name:
            raise WorkspaceError("missing the new workspace name")
        dir_path = self.get_workspace_path('')
        if os.path.exists(dir_path):
            try:
                shutil.move(os.path.join(dir_path, workspace_name),
                            os.path.join(dir_path, new_workspace_name))
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))
        workspace_dir = self.get_workspace_path(new_workspace_name)
        return Workspace(workspace_dir, new_workspace_name)

    def get_workspace_names(self) -> List[str]:
        workspaces_dir = self._workspaces_dir
        if os.path.exists(workspaces_dir):
            return sorted([name for name in os.listdir(workspaces_dir)
                           if os.path.isdir(os.path.join(workspaces_dir, name))])
        return []

    def get_workspaces(self) -> List[str]:
        workspaces_dir = self._workspaces_dir
        if os.path.exists(workspaces_dir):
            workspaces = [
                Workspace(os.path.join(workspaces_dir, name), name).to_json_dict() if name != '.current' else None
                for name in os.listdir(workspaces_dir)]
            return list(filter(None, workspaces))

    def config_exists(self, workspace_name: str, config_name: str) -> bool:
        config_dir = self.get_config_path(workspace_name, config_name)
        return os.path.isdir(config_dir) and os.listdir(config_dir)

    def create_config(self, workspace_name: str, config_name: str, cryosat: bool = False):
        """
        :param cryosat: True to create a config based on cryosat template
        :param workspace_name: the workspace name where the config is to be created
        :param config_name: the name of the configuration to be added
        """
        self._assert_workspace_exists(workspace_name)
        if self.config_exists(workspace_name, config_name):
            raise WorkspaceError('workspace "%s" already contains a configuration "%s"' % (workspace_name, config_name))
        config_dir = self.get_config_path(workspace_name, config_name)
        dir_path = self._ensure_dir_exists(config_dir)
        package = _CRYOSAT_CONFIG_PACKAGE_NAME if cryosat else _DEFAULT_CONFIG_PACKAGE_NAME
        # TODO (forman, 20160727): copy text files so that '\n' is replaced by OS-specific line separator
        self._copy_resource(package, 'CHD.json', dir_path)
        self._copy_resource(package, 'CNF.json', dir_path)
        self._copy_resource(package, 'CST.json', dir_path)

    def delete_config(self, workspace_name: str, config_name: str):
        """
        :param workspace_name: the workspace name where the config is to be removed
        :param config_name: the name of the configuration to be removed
        :return:
        """
        self._assert_workspace_exists(workspace_name)
        self._assert_config_exists(workspace_name, config_name)
        dir_path = self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def copy_config(self, workspace_name: str, config_name: str, new_config_name: str):
        """
        :param workspace_name: the workspace name where the config is to be copied
        :param config_name: the name of the configuration to be copied
        :param new_config_name: the name of the new configuration
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        self._assert_config_exists(workspace_name, config_name)
        dir_path = self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name)
        dir_path_new = self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, new_config_name)
        if os.path.exists(dir_path):
            try:
                shutil.copytree(dir_path, dir_path_new)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def rename_config(self, workspace_name: str, config_name: str, new_config_name: str):
        """
        :param workspace_name: the workspace name where the config is to be renamed
        :param config_name: the name of the configuration to be renamed
        :param new_config_name: the name of the new configuration
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        self._assert_config_exists(workspace_name, config_name)
        dir_path = self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name)
        dir_path_new = self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, new_config_name)
        if os.path.exists(dir_path):
            try:
                os.rename(dir_path, dir_path_new)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def get_config_file(self, workspace_name: str, config_name: str, config_file_key: str) -> str:
        return self.get_config_path(workspace_name, config_name, config_file_key + '.json')

    def get_config_json(self, workspace_name: str, config_name: str, config_file_key: str):
        file_path = self.get_config_file(workspace_name, config_name, config_file_key)
        config_json = self._open_config_json(file_path)
        config_order = [name for name in config_json]
        return config_json, sorted(config_order, key=str.lower)

    def write_config_file(self, workspace_name: str, config_name: str, config_file_key: str, configuration: str):
        file_path = self.get_config_file(workspace_name, config_name, config_file_key)
        with open(file_path, 'r+') as f:
            f.seek(0)
            f.write(configuration)
            f.truncate()

    def get_config_names(self, workspace_name: str) -> List[str]:
        self._assert_workspace_exists(workspace_name)
        configs_dir = self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME)
        if os.path.exists(configs_dir):
            return sorted([name for name in os.listdir(configs_dir) if os.path.isdir(os.path.join(configs_dir, name))])
        return None

    def get_current_config_name(self, workspace_name: str) -> str:
        self._assert_workspace_exists(workspace_name)
        return _readline(self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, _CURRENT_FILE_NAME))

    def set_current_config_name(self, workspace_name: str, config_name: str):
        self._assert_workspace_exists(workspace_name)
        self._assert_config_exists(workspace_name, config_name)
        _writeline(self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, _CURRENT_FILE_NAME), config_name)

    def get_config_version(self, workspace_name: str, config_name: str, config_file_key: str) -> int:
        config, _ = self.get_config_json(workspace_name, config_name, config_file_key)
        return config['__metainf__']['version'] if '__metainf__' in config else -1

    def get_all_config_version(self, workspace_name: str, config_name: str) -> tuple:
        chd_config_version = self.get_config_version(workspace_name, config_name, "CHD")
        cnf_config_version = self.get_config_version(workspace_name, config_name, "CNF")
        cst_config_version = self.get_config_version(workspace_name, config_name, "CST")
        return chd_config_version, cnf_config_version, cst_config_version

    def get_default_config_version(self, config_file_key: str) -> int:
        default_config = self._get_default_config(config_file_key)
        return default_config['__metainf__']['version'] if '__metainf__' in default_config else -1

    def get_all_default_config_version(self) -> tuple:
        chd_config_version = self.get_default_config_version("CHD")
        cnf_config_version = self.get_default_config_version("CNF")
        cst_config_version = self.get_default_config_version("CST")
        return chd_config_version, cnf_config_version, cst_config_version

    def upgrade_all_config(self, workspace_name: str, config_name: str) -> tuple:
        chd_new_version = self.upgrade_config(workspace_name, config_name, "CHD")
        cnf_new_version = self.upgrade_config(workspace_name, config_name, "CNF")
        cst_new_version = self.upgrade_config(workspace_name, config_name, "CST")
        return chd_new_version, cnf_new_version, cst_new_version

    def upgrade_config(self, workspace_name: str, config_name: str, config_file_key: str):
        current_config, _ = self.get_config_json(workspace_name, config_name, config_file_key)
        default_config = self._get_default_config(config_file_key)
        config_json = self._do_upgrade_config(current_config, default_config)
        updated_version = config_json['__metainf__']['version'] if '__metainf__' in config_json else -1
        updated_config = self._json_to_str(config_json)
        self.write_config_file(workspace_name, config_name, config_file_key, updated_config)
        return updated_version

    @staticmethod
    def _do_upgrade_config(current_config: dict, default_config: dict) -> dict:
        try:
            current_version = current_config['__metainf__']['version']
        except KeyError:
            current_version = -1
        default_version = default_config['__metainf__']['version']
        if current_version >= default_version:
            return current_config
        added_or_modified_list = []
        removed_list = []
        for change in default_config['__metainf__']['changelog']:
            if change['version'] <= current_version:
                continue
            for parameter in change['parameters']:
                parameter_key = parameter[0]
                if parameter[1] == "*" or parameter[1] == "+":
                    removed_list.remove(parameter_key) if parameter_key in removed_list else None
                    added_or_modified_list.append(
                        parameter_key) if parameter_key not in added_or_modified_list else None
                elif parameter[1] == "-":
                    added_or_modified_list.remove(parameter_key) if parameter_key in added_or_modified_list else None
                    removed_list.append(parameter_key) if parameter_key not in removed_list else None
        for key in added_or_modified_list:
            current_config[key] = default_config[key]
        for parameter_key in removed_list:
            current_config.pop(parameter_key) if parameter_key in current_config else None
        current_config['__metainf__'] = default_config['__metainf__']
        return current_config

    @staticmethod
    def _json_to_str(json_dict):
        return json.dumps(json_dict, indent=4, separators=(',', ': '), sort_keys=True)

    @staticmethod
    def _get_default_config(config_file_key):
        default_config_data = pkgutil.get_data(_DEFAULT_CONFIG_PACKAGE_NAME, config_file_key + '.json')
        default_config = json.loads(default_config_data.decode("utf-8"), object_pairs_hook=collections.OrderedDict)
        return default_config

    @staticmethod
    def _open_config_json(file_path):
        with open(file_path) as data_file:
            config_json = json.load(data_file, object_pairs_hook=collections.OrderedDict)
        return config_json

    def add_inputs(self, workspace_name: str, input_paths, monitor):
        """
        :param workspace_name: workspace name to add the input
        :param input_paths: path to the input files to be added
        :param monitor: to monitor the progress
        """
        inputs_dir = self._ensure_dir_exists(self.get_inputs_path(workspace_name))
        with monitor.starting('adding inputs', len(input_paths)):
            for input_path in input_paths:
                try:
                    shutil.copy(input_path, os.path.join(inputs_dir, os.path.basename(input_path)))
                except (IOError, OSError) as e:
                    raise WorkspaceError(str(e))
                monitor.progress(1)

    def remove_inputs(self, workspace_name, input_names, monitor):
        """
        :param workspace_name: workspace name in which the inputs are to be removed
        :param input_names: name of input files to be removed
        :param monitor: to monitor the progress
        """
        input_paths = [self.get_inputs_path(workspace_name, input_name) for input_name in input_names]
        with monitor.starting('removing inputs', len(input_paths)):
            for input_path in input_paths:
                if os.path.exists(input_path):
                    try:
                        os.remove(input_path)
                    except (IOError, OSError) as e:
                        raise WorkspaceError(str(e))
                monitor.progress(1)

    # TODO forman rename to get_input_filenames
    def get_input_names(self, workspace_name: str, pattern=None):
        """
        :param workspace_name: workspace name in which the input files are to be queried
        :param pattern: a regex to identify the input files to be listed
        """
        inputs_dir = self.get_inputs_path(workspace_name)
        if os.path.exists(inputs_dir):
            return self.get_nc_filename_list(inputs_dir, pattern)
        return []

    def get_input_paths(self, workspace_name: str):
        return [self.get_inputs_path(workspace_name, name) for name in
                self.get_input_names(workspace_name)]

    def get_workspace_path(self, workspace_name, *paths) -> str:
        return os.path.join(self._workspaces_dir, workspace_name, *paths)

    def get_config_path(self, workspace_name, config_name, *paths):
        return self.get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name, *paths)

    def get_inputs_path(self, workspace_name, *paths):
        return self.get_workspace_path(workspace_name, _INPUTS_DIR_NAME, *paths)

    def get_outputs_path(self, workspace_name, config_name, *paths):
        return self.get_config_path(workspace_name, config_name, _OUTPUTS_DIR_NAME, *paths)

    def remove_outputs(self, workspace_name, config_name):
        """
        :param workspace_name: the workspace name in which the output files are located
        :param config_name: the config name with which the output files were created
        """
        output_dir = self.get_outputs_path(workspace_name, config_name)
        if not os.path.exists(output_dir):
            raise WorkspaceError('output directory does not exist')
        output_names = os.listdir(output_dir)
        output_paths = [os.path.join(output_dir, output_name) for output_name in output_names]
        for output_path in output_paths:
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except (IOError, OSError) as e:
                    raise WorkspaceError(str(e))

    # TODO forman rename to get_output_filenames
    def get_output_names(self, workspace_name: str, config_name: str, pattern=None):
        """
        :param workspace_name: workspace name in which the output files are to be listed
        :param config_name: config name with which the output files were created
        :param pattern: a regex to identify the output files to be listed
        """
        outputs_dir = self.get_outputs_path(workspace_name, config_name)
        if os.path.exists(outputs_dir):
            return self.get_nc_filename_list(outputs_dir, pattern)
        return []

    def get_notebook_names(self, workspace_name: str) -> List[str]:
        self._assert_workspace_exists(workspace_name)
        notebook_dir = self.get_workspace_path(workspace_name, _NOTEBOOKS_DIR_NAME)
        if os.path.exists(notebook_dir):
            return sorted(
                [name for name in os.listdir(notebook_dir) if name.endswith(".ipynb")
                 and os.path.isfile(os.path.join(notebook_dir, name))])
        return []

    def inspect_l1b_product(self, workspace_name: str, l1b_path: str):
        template_data = pkgutil.get_data('dedop.ui.data.notebooks', 'inspect-template.ipynb')
        notebook_json = template_data.decode("utf-8") \
            .replace('__L1B_FILE_PATH__', repr(l1b_path).replace('\\', '\\\\'))
        product_name = ntpath.basename(l1b_path)
        return self._launch_notebook_from_template(workspace_name,
                                                   'inspect-%s' % product_name,
                                                   notebook_json,
                                                   'inspect - [%s]' %
                                                   self._limit_title(l1b_path, 60))

    def compare_l1b_products(self, workspace_name, l1b_path_1: str, l1b_path_2: str):
        template_data = pkgutil.get_data('dedop.ui.data.notebooks', 'compare-template.ipynb')
        notebook_json = template_data.decode("utf-8") \
            .replace('__L1B_FILE_PATH_1__', repr(l1b_path_1).replace('\\', '\\\\')) \
            .replace('__L1B_FILE_PATH_2__', repr(l1b_path_2).replace('\\', '\\\\'))
        product1_name = ntpath.basename(l1b_path_1)
        product2_name = ntpath.basename(l1b_path_2)
        return self._launch_notebook_from_template(workspace_name,
                                                   'compare-%s-%s' % (product1_name, product2_name),
                                                   notebook_json,
                                                   'compare - [%s] [%s]' % (self._limit_title(l1b_path_1, 30),
                                                                            self._limit_title(l1b_path_2, 30),))

    def _launch_notebook_from_template(self,
                                       workspace_name: str,
                                       notebook_basename: str,
                                       notebook_json: str,
                                       title: str):
        notebook_dir = self.get_workspace_path(workspace_name, 'notebooks')
        if not os.path.exists(notebook_dir):
            try:
                os.mkdir(notebook_dir)
            except (IOError, OSError) as e:
                return 60, str(e)

        index = 0
        while True:
            index += 1
            notebook_filename = '%s-%d.ipynb' % (notebook_basename, index)
            notebook_path = os.path.join(notebook_dir, notebook_filename)
            if not os.path.exists(notebook_path):
                break

        # noinspection PyUnboundLocalVariable
        with open(notebook_path, 'w') as fp:
            fp.write(notebook_json)
            print('wrote notebook file "%s"' % notebook_path)

        self.launch_notebook(title, notebook_dir, notebook_path=notebook_path)

    @classmethod
    def launch_notebook(cls, title: str, notebook_dir: str, notebook_path: str = None):

        # we start a new terminal/command window here so that non-expert users can close the Notebook session easily
        # by closing the newly created window.

        terminal_title = 'DeDop - %s' % title

        notebook_command = 'jupyter notebook --notebook-dir "%s"' % notebook_dir
        notebook_command_with_prefix = '{prefix}/bin/{notebook_command}'.format(prefix=sys.prefix,
                                                                                notebook_command=notebook_command)
        if notebook_path:
            notebook_command += ' "%s"' % notebook_path
            notebook_command_with_prefix += ' "%s"' % notebook_path

        launch_notebook_command_template = get_config_value('launch_notebook_command', None)
        launch_notebook_in_new_terminal = True
        if launch_notebook_command_template:
            if isinstance(launch_notebook_command_template, str) and launch_notebook_command_template.strip():
                launch_notebook_command_template = launch_notebook_command_template.strip()
            else:
                launch_notebook_command_template = None
            if not launch_notebook_command_template:
                raise WorkspaceError('configuration parameter "launch_notebook_command" must be a non-empty string')
            launch_notebook_in_new_terminal = get_config_value('launch_notebook_in_new_terminal', False)
        else:
            if sys.platform.startswith('win'):
                # Windows
                # launch_notebook_command_template = 'start "{title}" /Min {command}'
                launch_notebook_command_template = 'start "{title}" /Min "{command_file}"'
            elif sys.platform == 'darwin':
                # Mac OS X
                launch_notebook_command_template = 'open -a Terminal "{command_file}"'
            elif shutil.which("konsole"):
                # KDE
                launch_notebook_command_template = 'konsole -p tabtitle="{title}" -e \'{command}\' & disown'
            elif shutil.which("gnome-terminal"):
                # GNOME / Ubuntu
                launch_notebook_command_template = 'gnome-terminal -e \'{command}\''
            elif shutil.which("xterm"):
                launch_notebook_command_template = 'xterm  -T "{title}" -e \'{command}\''
            else:
                launch_notebook_command_template = notebook_command_with_prefix
                launch_notebook_in_new_terminal = False

        command_file = ''
        if '{command_file}' in launch_notebook_command_template:
            try:
                if not os.path.exists(DEFAULT_TEMP_DIR):
                    os.makedirs(DEFAULT_TEMP_DIR)

                command_basename = 'dedop-notebook-server'
                if sys.platform.startswith('win'):
                    command_file = os.path.join(DEFAULT_TEMP_DIR, command_basename + '.bat')
                    with open(command_file, 'w') as fp:
                        fp.write('call "{prefix}/Scripts/activate.bat" "{prefix}"\n'
                                 'call {command}\n'.format(prefix=sys.prefix, command=notebook_command))
                else:
                    import stat
                    command_file = os.path.join(DEFAULT_TEMP_DIR, command_basename)
                    with open(command_file, 'w') as fp:
                        fp.write('#!/bin/bash\n'
                                 'source "{prefix}/bin/activate" "{prefix}"\n'
                                 '{command}\n'.format(prefix=sys.prefix, command=notebook_command))
                    os.chmod(command_file, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
            except (OSError, IOError) as error:
                raise WorkspaceError(str(error))

        launch_notebook_command = launch_notebook_command_template.format(title=terminal_title,
                                                                          command=notebook_command_with_prefix,
                                                                          command_file=command_file,
                                                                          prefix=sys.prefix)
        try:
            print('calling:', launch_notebook_command)
            subprocess.check_call(launch_notebook_command, shell=True)
            if launch_notebook_in_new_terminal:
                print('A terminal window titled "%s" has been opened.' % cls._limit_title(terminal_title, 30, mode='l'))
                print('Close that window or press CTRL+C within it to terminate the Notebook session.')
        except (subprocess.CalledProcessError, IOError, OSError) as error:
            raise WorkspaceError('failed to launch Jupyter Notebook: %s' % str(error))

    @classmethod
    def open_file(cls, path):
        launch_editor_command_template = get_config_value('launch_editor_command', None)
        if launch_editor_command_template:
            if isinstance(launch_editor_command_template, str) and launch_editor_command_template.strip():
                launch_editor_command_template = launch_editor_command_template.strip()
            else:
                launch_editor_command_template = None
            if not launch_editor_command_template:
                raise WorkspaceError('configuration parameter "launch_editor_command" must be a non-empty string')
        else:
            try:
                # Windows:
                # Start a file with its associated application.
                os.startfile(path)
                return
            except AttributeError:
                if shutil.which('xdg-open'):
                    # Unix Desktops
                    # xdg-open opens a file or URL in the user's preferred application.
                    launch_editor_command_template = 'xdg-open "{file}"'
                elif shutil.which('open'):
                    # Mac OS X
                    # Open a file or folder. The open command opens a file (or a folder or URL), just as
                    # if you had double-clicked the file's icon.
                    launch_editor_command_template = 'open "{file}"'
                else:
                    print('warning: don\'t know how to open %s' % path)
                    return

        launch_editor_command = launch_editor_command_template.format(file=path)
        try:
            # print('launch_editor_command:', launch_editor_command)
            subprocess.call(launch_editor_command, shell=True)
        except (IOError, OSError) as error:
            raise WorkspaceError(str(error))

    @staticmethod
    def get_nc_filename_list(directory, pattern):
        fn_list = [fn for fn in os.listdir(directory) if
                   fn.endswith('.nc') and os.path.isfile(os.path.join(directory, fn))]
        if isinstance(pattern, str):
            fn_list = [fn for fn in fn_list if fnmatch.fnmatch(fn, pattern)]
        elif pattern:
            new_fn_list = []
            for fn in fn_list:
                for p in pattern:
                    if fnmatch.fnmatch(fn, p):
                        new_fn_list.append(fn)
            fn_list = new_fn_list
        return sorted(fn_list)

    @classmethod
    def _copy_resource(cls, package, file_name, dir_path):
        try:
            with open(os.path.join(dir_path, file_name), 'wb') as fp:
                fp.write(pkgutil.get_data(package, file_name))
        except (IOError, OSError) as e:
            raise WorkspaceError(str(e))

    @classmethod
    def _ensure_dir_exists(cls, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))
        return dir_path

    @classmethod
    def _limit_title(cls, name, max_len, mode='r'):
        assert name
        assert max_len > 3
        assert mode == 'r' or mode == 'l'
        return name if len(name) <= max_len else (
            '...' + name[3 - max_len:] if mode == 'r' else name[:max_len - 3] + '...')

    def _assert_workspace_exists(self, workspace_name):
        if not os.path.exists(self.get_workspace_path(workspace_name)):
            raise WorkspaceError('workspace "%s" does not exist' % workspace_name)

    def _assert_config_exists(self, workspace_name, config_name):
        if not os.path.exists(self.get_config_path(workspace_name, config_name)):
            raise WorkspaceError(
                'DDP configuration "%s" of workspace "%s" does not exist' % (config_name, workspace_name))
