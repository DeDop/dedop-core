import os.path
import pkgutil
import shutil

from typing import List

_WORKSPACES_DIR_NAME = 'workspaces'
_CONFIGS_DIR_NAME = 'configs'
_CURRENT_FILE_NAME = '.current'

DEFAULT_WORKSPACES_DIR = os.path.expanduser(os.path.join('~', '.dedop', _WORKSPACES_DIR_NAME))


class WorkspaceError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# TODO (forman, 20180702): catch all IOError, OSError, etc and raise WorkspaceError instead

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
    3. Configurations: when creating a new configuration, the CNF, CST, CHD files are created from software defaults.
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

    def delete_all_workspaces(self) -> str:
        shutil.rmtree(self._workspaces_dir, ignore_errors=True)

    def get_current_workspace_name(self) -> str:
        file_path = os.path.join(self._workspaces_dir, _CURRENT_FILE_NAME)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as fp:
                return fp.readline()
        return None

    def set_current_workspace_name(self, workspace_name: str):
        self._assert_workspace_exists(workspace_name)
        file_path = os.path.join(self._workspaces_dir, _CURRENT_FILE_NAME)
        with open(file_path, 'w') as fp:
            fp.write(workspace_name)

    def workspace_exists(self, workspace_name) -> bool:
        return os.path.exists(self._get_workspace_path(workspace_name))

    def create_workspace(self, workspace_name: str) -> str:
        return self._ensure_dir_exists(self._get_workspace_path(workspace_name))

    def delete_workspace(self, workspace_name: str):
        self._assert_workspace_exists(workspace_name)
        dir_path = self._get_workspace_path(workspace_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)

    def get_workspace_names(self) -> List[str]:
        workspaces_dir = self._workspaces_dir
        if os.path.exists(workspaces_dir):
            return sorted([name for name in os.listdir(workspaces_dir)
                           if os.path.isdir(os.path.join(workspaces_dir, name))])
        return []

    def config_exists(self, workspace_name: str, config_name: str) -> bool:
        return os.path.exists(self._get_config_path(workspace_name, config_name))

    def create_config(self, workspace_name: str, config_name: str):
        self._assert_workspace_exists(workspace_name)
        dir_path = self._ensure_dir_exists(self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name))
        package = 'dedop.cli.defaults'
        self._copy_resource(package, 'CHD.json', dir_path)
        self._copy_resource(package, 'CNF.json', dir_path)
        self._copy_resource(package, 'CST.json', dir_path)

    def delete_config(self, workspace_name: str, config_name: str):
        self._assert_workspace_exists(workspace_name)
        dir_path = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)
        return None

    def get_config_file(self, workspace_name: str, config_name: str, config_file_key: str) -> str:
        return self._get_config_path(workspace_name, config_name, config_file_key + '.json')

    def get_config_names(self, workspace_name: str) -> List[str]:
        self._assert_workspace_exists(workspace_name)
        configs_dir = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME)
        if os.path.exists(configs_dir):
            return sorted([name for name in os.listdir(configs_dir) if os.path.isdir(os.path.join(configs_dir, name))])
        return None

    def get_current_config_name(self, workspace_name: str) -> str:
        self._assert_workspace_exists(workspace_name)
        file_path = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, _CURRENT_FILE_NAME)
        if os.path.exists(file_path):
            with open(file_path, 'r') as fp:
                return fp.readline()
        return None

    def set_current_config_name(self, workspace_name: str, config_name: str):
        self._assert_workspace_exists(workspace_name)
        file_path = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, _CURRENT_FILE_NAME)
        with open(file_path, 'w') as fp:
            fp.write(config_name)

    def add_inputs(self, workspace_name: str, inputs, monitor):
        inputs_dir = self._ensure_dir_exists(self._get_workspace_path(workspace_name, 'inputs'))
        with monitor.starting('Adding inputs', len(inputs)):
            for input in inputs:
                shutil.copy(input, os.path.join(inputs_dir, os.path.basename(input)))
                monitor.progress(1)

    def get_input_names(self, workspace_name: str):
        inputs_dir = self._get_workspace_path(workspace_name, 'inputs')
        if os.path.exists(inputs_dir):
            return sorted([name for name in os.listdir(inputs_dir) if
                           name.endswith('.nc') and os.path.isfile(os.path.join(inputs_dir, name))])
        return []

    def get_input_paths(self, workspace_name: str):
        return [self._get_workspace_path(workspace_name, 'inputs', name) for name in
                self.get_input_names(workspace_name)]

    def _get_workspace_path(self, workspace_name, *paths):
        return os.path.join(self._workspaces_dir, workspace_name, *paths)

    def _get_config_path(self, workspace_name, config_name, *paths):
        return self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name, *paths)

    @classmethod
    def _copy_resource(cls, package, file_name, dir_path):
        with open(os.path.join(dir_path, file_name), 'wb') as fp:
            fp.write(pkgutil.get_data(package, file_name))

    @classmethod
    def _ensure_dir_exists(cls, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def _assert_workspace_exists(self, workspace_name):
        if not os.path.exists(self._get_workspace_path(workspace_name)):
            raise WorkspaceError('workspace "%s" does not exist' % workspace_name)

    def get_output_dir(self, workspace_name, config_name):
        return self._get_workspace_path(workspace_name, 'output', config_name)
