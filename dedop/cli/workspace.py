import os.path
import pkgutil
import shutil
from abc import ABCMeta, abstractmethod
from typing import List

_WS_DIR_NAME = 'workspaces'
_WS_CONFIGS_DIR_NAME = 'configs'
_WS_INPUT_L1A_DIR_NAME = 'input_l1a'
_WS_INPUT_L1B_DIR_NAME = 'output_l1b'
_WS_INPUT_L1BS_DIR_NAME = 'output_l1bs'
_WS_ANALYSES_DIR_NAME = 'analyses'

_CURRENT_WS_FILE_NAME = 'current_workspace.txt'
_CURRENT_CONFIG_FILE_NAME = 'current_config.txt'


class WorkspaceError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WorkspaceManager(metaclass=ABCMeta):
    @abstractmethod
    def get_current_workspace_name(self) -> str:
        pass

    @abstractmethod
    def set_current_workspace_name(self, workspace_name: str):
        pass

    @abstractmethod
    def create_workspace(self, workspace_name: str):
        pass

    @abstractmethod
    def delete_workspace(self, workspace_name: str):
        pass

    @abstractmethod
    def get_workspace_names(self) -> List[str]:
        pass

    @abstractmethod
    def create_config(self, workspace_name: str, config_name: str):
        pass

    @abstractmethod
    def delete_config(self, workspace_name: str, config_name: str):
        pass

    @abstractmethod
    def get_config_file(self, workspace_name: str, config_name: str, config_file_key: str) -> str:
        pass

    @abstractmethod
    def get_config_names(self, workspace_name: str) -> List[str]:
        pass

    @abstractmethod
    def get_current_config_name(self, workspace_name: str) -> str:
        pass

    @abstractmethod
    def set_current_config_name(self, workspace_name: str, config_name: str) -> str:
        pass


class MemoryWorkspaceManager(WorkspaceManager):
    def __init__(self):
        self._current_workspace_name = None
        self._workspaces = dict()

    def get_current_workspace_name(self) -> str:
        return self._current_workspace_name

    def set_current_workspace_name(self, workspace_name: str):
        self._assert_workspace_exists(workspace_name)
        self._current_workspace_name = workspace_name

    def create_workspace(self, workspace_name: str):
        if workspace_name in self._workspaces:
            raise WorkspaceError('workspace "%s" exists' % workspace_name)
        self._workspaces[workspace_name] = {}

    def delete_workspace(self, workspace_name: str):
        self._assert_workspace_exists(workspace_name)
        del self._workspaces[workspace_name]

    def get_workspace_names(self) -> List[str]:
        return sorted(self._workspaces.keys())

    def create_config(self, workspace_name: str, config_name: str):
        self._assert_workspace_exists(workspace_name)
        workspace_dict = self._workspaces[workspace_name]
        if _WS_CONFIGS_DIR_NAME not in workspace_dict:
            workspace_dict[_WS_CONFIGS_DIR_NAME] = {}
        configs_dict = workspace_dict[_WS_CONFIGS_DIR_NAME]
        if config_name in configs_dict:
            raise WorkspaceError('config "%s" exists in workspace "%s"' % (config_name, workspace_name))
        configs_dict[config_name] = dict(CHD='CHD.json', CNF='CNF.json', CST='CST.json')

    def delete_config(self, workspace_name: str, config_name: str):
        self._assert_workspace_exists(workspace_name)
        workspace_dict = self._workspaces[workspace_name]
        configs_dict = workspace_dict.get(_WS_CONFIGS_DIR_NAME, {})
        if config_name in configs_dict:
            del configs_dict[config_name]

    def get_config_file(self, workspace_name: str, config_name: str, config_file_key: str) -> str:
        self._assert_workspace_exists(workspace_name)
        workspace_dict = self._workspaces[workspace_name]
        configs_dict = workspace_dict.get(_WS_CONFIGS_DIR_NAME, {})
        config_dict = configs_dict.get(config_name, {})
        return config_dict.get(config_file_key, None)

    def get_config_names(self, workspace_name: str) -> List[str]:
        self._assert_workspace_exists(workspace_name)
        workspace_dict = self._workspaces[workspace_name]
        return sorted(workspace_dict.get(_WS_CONFIGS_DIR_NAME, {}).keys())

    def get_current_config_name(self, workspace_name: str) -> str:
        self._assert_workspace_exists(workspace_name)
        workspace_dict = self._workspaces[workspace_name]
        return workspace_dict.get(_CURRENT_CONFIG_FILE_NAME, None)

    def set_current_config_name(self, workspace_name: str, config_name: str) -> str:
        self._assert_workspace_exists(workspace_name)
        workspace_dict = self._workspaces[workspace_name]
        workspace_dict[_CURRENT_CONFIG_FILE_NAME] = config_name

    def _assert_workspace_exists(self, workspace_name):
        if workspace_name not in self._workspaces:
            raise WorkspaceError('unknown workspace: %s' % workspace_name)


class DefaultWorkspaceManager(WorkspaceManager):
    def __init__(self):
        self._workspaces_dir = os.path.expanduser(os.path.join('~', '.dedop', _WS_DIR_NAME))

    def get_current_workspace_name(self) -> str:
        file_path = os.path.join(self._workspaces_dir, _CURRENT_WS_FILE_NAME)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as fp:
                return fp.read()
        return None

    def set_current_workspace_name(self, workspace_name: str):
        self._ensure_dir_exists(self._workspaces_dir)
        file_path = os.path.join(self._workspaces_dir, _CURRENT_WS_FILE_NAME)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'w') as fp:
                fp.write(workspace_name)

    def create_workspace(self, workspace_name: str):
        return self._ensure_dir_exists(self._get_workspace_path(workspace_name))

    def delete_workspace(self, workspace_name: str):
        dir_path = self._get_workspace_path(workspace_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)

    def get_workspace_names(self) -> List[str]:
        dir_path = self._workspaces_dir
        if os.path.exists(dir_path):
            return sorted([dir_path for dir_path in os.listdir(dir_path) if not os.path.isfile])
        return []

    def create_config(self, workspace_name: str, config_name):
        dir_path = self._ensure_dir_exists(self._get_workspace_path(workspace_name, _WS_CONFIGS_DIR_NAME, config_name))
        package = 'dedop.cli.defaults'
        self._copy_resource(package, 'CHD.json', dir_path)
        self._copy_resource(package, 'CNF.json', dir_path)
        self._copy_resource(package, 'CST.json', dir_path)

    def delete_config(self, workspace_name: str, config_name):
        dir_path = self._get_workspace_path(workspace_name, _WS_CONFIGS_DIR_NAME, config_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)
        return None

    def get_config_file(self, workspace_name: str, config_name: str, config_file_key: str) -> str:
        return self._get_workspace_path(workspace_name, _WS_CONFIGS_DIR_NAME, config_name, config_file_key + '.json')

    def get_config_names(self, workspace_name: str) -> List[str]:
        dir_path = self._get_workspace_path(workspace_name, _WS_CONFIGS_DIR_NAME)
        if os.path.exists(dir_path):
            return sorted([dir_path for dir_path in os.listdir(dir_path) if not os.path.isfile])
        return None

    def get_current_config_name(self, workspace_name: str) -> str:
        file_path = self._get_workspace_path(workspace_name, _CURRENT_CONFIG_FILE_NAME)
        if os.path.exists(file_path):
            with open(file_path, 'r') as fp:
                fp.read()
        return None

    def set_current_config_name(self, workspace_name: str, config_name: str) -> str:
        file_path = self._get_workspace_path(workspace_name, _CURRENT_CONFIG_FILE_NAME)
        with open(file_path, 'w') as fp:
            fp.write(config_name)

    def _get_workspace_path(self, workspace_name, *dir_names):
        return os.path.join(self._workspaces_dir, workspace_name, *dir_names)

    @classmethod
    def _copy_resource(cls, package, file_name, dir_path):
        with open(os.path.join(dir_path, file_name), 'wb') as fp:
            fp.write(pkgutil.get_data(package, file_name))

    @classmethod
    def _ensure_dir_exists(cls, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        return dir_path


WORKSPACE_MANAGER = DefaultWorkspaceManager()


class Config:
    """
    :param cnf_file: Configuration definition file
    :param chd_file: Characterisation definition file
    :param cst_file: Constants definition file
    """

    def __init__(self, workspace: 'Workspace', name):
        self._workspace = workspace
        self._name = name

    @property
    def workspace(self):
        return self._workspace

    @property
    def name(self):
        return self._name

    @property
    def chd_file(self) -> str:
        return self._get_file('CHD')

    @property
    def cnf_file(self) -> str:
        return self._get_file('CNF')

    @property
    def cst_file(self) -> str:
        return self._get_file('CST')

    def rename(self, new_name: str):
        # self.workspace.manager.rename_config(self.workspace.name, self.name, new_name)
        raise NotImplementedError()

    def copy(self, new_name: str):
        # self.workspace.manager.copy_config(self.workspace.name, self.name, new_name)
        raise NotImplementedError()

    def delete(self):
        self.workspace.manager.delete_config(self.workspace.name, self.name)

    def _get_file(self, file_name) -> str:
        return self.workspace.manager.get_config_file(self.workspace.name, self.name, file_name)


class Workspace:
    """
    A workspace contains multiple DDP configurations, source files and analysis results.
    Physically it is represented by a directory in the local file system organised as follows:

    * ``.dedop/workspaces/``
      * ``<workspace-name>``/``
        * ``configs/*.json``
        * ``input_l1a/*.nc``
        * ``output_l1b/<config-name>/*.nc``
        * ``output_l1bs/<config-name>/\*.nc``
        * ``analyses/<config-name>/``


    Technical requirements
    ----------------------
    1. Save disk space: We should avoid copies of L1A input files in every workspace. We may have a
       ``.dedop/input_l1a/`` containing the actual files and in workspace ``test3``
       we have ``.dedop/workspaces/test3/input_l1a`` which only contains symbolic links.
       (While we can use symbolic links on Unixes we could use text files containing the actual paths
       in Windows.)
    2. Context information: we need a **current workspace**. This could be physically represented
       by a file ``.dedop/current_workspace.txt`` which contains the name of the current workspace.
       The name of current configuration within the current workspace could be stored in
       ``.dedop/<workspace-name>/current_config.txt``.
    3. Configurations: when creating a new configuration, the CNF, CST, CHD files are created from software defaults.
       This allows a user to share their workspace with someone else without worrying about whether
       either has edited their default configurations.

    """

    def __init__(self, manager: WorkspaceManager, name: str):
        self._manager = manager
        self._name = name

    @property
    def manager(self):
        return self._manager

    @property
    def name(self):
        return self._name

    @classmethod
    def get_current_workspace(cls, manager: WorkspaceManager = None) -> 'Workspace':
        manager = manager if manager else WORKSPACE_MANAGER
        workspace_name = manager.get_current_workspace_name()
        if not workspace_name:
            return None
        return Workspace(manager, workspace_name)

    @classmethod
    def create_workspace(cls, workspace_name: str, manager: WorkspaceManager = None) -> 'Workspace':
        manager = manager if manager else WORKSPACE_MANAGER
        manager.create_workspace(workspace_name)
        return Workspace(manager, workspace_name)

    def rename(self, new_name: str):
        # self.manager.rename_workspace(self.name, new_name)
        raise NotImplementedError()

    def copy(self, new_name: str):
        # self.manager.copy_workspace(self.name, new_name)
        raise NotImplementedError()

    def delete(self):
        self.manager.delete_workspace(self.name)

    def create_config(self, config_name: str):
        self.manager.create_config(self.name, config_name)
        return Config(self, config_name)

    def get_config(self, config_name: str) -> Config:
        return Config(self, config_name)

    @property
    def config_names(self) -> List[str]:
        return self.manager.get_config_names(self.name)

    @property
    def current_config(self) -> Config:
        config_name = self.manager.get_current_config_name(self.name)
        return Config(self, config_name) if config_name else None
