import fnmatch
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


def _readline(file_path: str) -> str:
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
        if os.path.isdir(self._workspaces_dir):
            try:
                shutil.rmtree(self._workspaces_dir)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def get_current_workspace_name(self) -> str:
        return _readline(os.path.join(self._workspaces_dir, _CURRENT_FILE_NAME))

    def set_current_workspace_name(self, workspace_name: str):
        self._assert_workspace_exists(workspace_name)
        _writeline(os.path.join(self._workspaces_dir, _CURRENT_FILE_NAME), workspace_name)

    def workspace_exists(self, workspace_name) -> bool:
        return os.path.exists(self._get_workspace_path(workspace_name))

    def create_workspace(self, workspace_name: str) -> str:
        """
        :param workspace_name:
        :return: workspace path
        :raise: WorkspaceError
        """
        workspace_dir = self._get_workspace_path(workspace_name)
        if os.path.isdir(workspace_dir) and os.listdir(workspace_dir):
            raise WorkspaceError('workspace "%s" already exists' % workspace_name)
        return self._ensure_dir_exists(workspace_dir)

    def delete_workspace(self, workspace_name: str):
        """
        :param workspace_name: workspace name
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        dir_path = self._get_workspace_path(workspace_name)
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
        dir_path = self._get_workspace_path('')
        if os.path.exists(dir_path):
            try:
                shutil.copytree(os.path.join(dir_path, workspace_name),
                                os.path.join(dir_path, new_workspace_name))
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def rename_workspace(self, workspace_name: str, new_workspace_name: str):
        """
        :param workspace_name: workspace name to be renamed
        :param new_workspace_name: new workspace name
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        if not new_workspace_name:
            raise WorkspaceError("missing the new workspace name")
        dir_path = self._get_workspace_path('')
        if os.path.exists(dir_path):
            try:
                shutil.move(os.path.join(dir_path, workspace_name),
                            os.path.join(dir_path, new_workspace_name))
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

    def print_workspace_info(self, workspace_name: str):
        """
        :param workspace_name: workspace name to be queried
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        dir_path = self._get_workspace_path(workspace_name)
        print('Available workspace:')
        for ws in self.get_workspace_names():
            if ws == workspace_name:
                print('  ' + ws + '*')
            else:
                print('  ' + ws)
        print('')
        print('Available configurations:')
        if os.listdir(self._get_workspace_path(workspace_name)):
            for cf in self.get_config_names(workspace_name):
                if cf == self.get_current_config_name(workspace_name):
                    print('  ' + cf + '*')
                else:
                    print('  ' + cf)
            print('')
        print('Available input files:')
        if os.path.isdir(os.path.join(dir_path, 'inputs')):
            for file in os.listdir(os.path.join(dir_path, 'inputs')):
                file_path = os.path.join(dir_path, 'inputs', file)
                print('  %s\t%s MB' % (file, os.path.getsize(file_path) >> 20))
            print('')
        print('Available output files:')
        if os.path.isdir(os.path.join(dir_path, 'output')):
            for file in os.listdir(os.path.join(dir_path, 'output')):
                config_path = os.path.join(dir_path, 'output', file)
                print('with %s configuration' % file)
                print('===========================')
                for dataset_file in os.listdir(config_path):
                    dataset_path = os.path.join(config_path, dataset_file)
                    print('  %s\t\t%s MB' % (dataset_file, os.path.getsize(dataset_path) >> 20))
                print('')

    def get_workspace_names(self) -> List[str]:
        workspaces_dir = self._workspaces_dir
        if os.path.exists(workspaces_dir):
            return sorted([name for name in os.listdir(workspaces_dir)
                           if os.path.isdir(os.path.join(workspaces_dir, name))])
        return []

    def config_exists(self, workspace_name: str, config_name: str) -> bool:
        config_dir = self._get_config_path(workspace_name, config_name)
        return os.path.isdir(config_dir) and os.listdir(config_dir)

    def create_config(self, workspace_name: str, config_name: str):
        """
        :param workspace_name: the workspace name where the config is to be created
        :param config_name: the name of the configuration to be added
        """
        self._assert_workspace_exists(workspace_name)
        if self.config_exists(workspace_name, config_name):
            raise WorkspaceError('workspace "%s" already contains a configuration "%s"' % (workspace_name, config_name))
        config_dir = self._get_config_path(workspace_name, config_name)
        dir_path = self._ensure_dir_exists(config_dir)
        package = 'dedop.cli.defaults'
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
        dir_path = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name)
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
        dir_path = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name)
        dir_path_new = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, new_config_name)
        if os.path.exists(dir_path):
            try:
                shutil.copytree(dir_path, dir_path_new)
            except (IOError, OSError) as e:
                raise WorkspaceError(str(e))

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
        return _readline(self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, _CURRENT_FILE_NAME))

    def set_current_config_name(self, workspace_name: str, config_name: str):
        self._assert_workspace_exists(workspace_name)
        _writeline(self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, _CURRENT_FILE_NAME), config_name)

    def add_inputs(self, workspace_name: str, input_paths, monitor):
        inputs_dir = self._ensure_dir_exists(self._get_workspace_path(workspace_name, 'inputs'))
        with monitor.starting('adding inputs', len(input_paths)):
            for input_path in input_paths:
                try:
                    shutil.copy(input_path, os.path.join(inputs_dir, os.path.basename(input_path)))
                except (IOError, OSError) as e:
                    raise WorkspaceError(str(e))
                monitor.progress(1)

    def remove_inputs(self, workspace_name, input_names, monitor):
        input_paths = [self._get_workspace_path(workspace_name, 'inputs', input_name) for input_name in input_names]
        with monitor.starting('removing inputs', len(input_paths)):
            for input_path in input_paths:
                if os.path.exists(input_path):
                    try:
                        os.remove(input_path)
                    except (IOError, OSError) as e:
                        raise WorkspaceError(str(e))
                monitor.progress(1)

    def get_input_names(self, workspace_name: str, pattern=None):
        inputs_dir = self._get_workspace_path(workspace_name, 'inputs')
        if os.path.exists(inputs_dir):
            fn_list = [fn for fn in os.listdir(inputs_dir) if
                       fn.endswith('.nc') and os.path.isfile(os.path.join(inputs_dir, fn))]
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

    def _assert_workspace_exists(self, workspace_name):
        if not os.path.exists(self._get_workspace_path(workspace_name)):
            raise WorkspaceError('workspace "%s" does not exist' % workspace_name)

    def _assert_config_exists(self, workspace_name, config_name):
        if not os.path.exists(self._get_workspace_path(workspace_name, 'configs', config_name)):
            raise WorkspaceError(
                'configuration "%s" inside workspace "%s" does not exist' % (config_name, workspace_name))

    def get_output_dir(self, workspace_name, config_name):
        return self._get_workspace_path(workspace_name, 'output', config_name)
