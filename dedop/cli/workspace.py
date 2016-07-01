_WS_DIR_NAME = 'workspaces'
_WS_CONFIGS_DIR_NAME = 'configs'
_WS_INPUT_L1A_DIR_NAME = 'input_l1a'
_WS_INPUT_L1B_DIR_NAME = 'output_l1b'
_WS_INPUT_L1BS_DIR_NAME = 'output_l1bs'
_WS_ANALYSES_DIR_NAME = 'analyses'

_CURRENT_WS_FILE_NAME = 'current_workspace.txt'
_CURRENT_CONFIG_FILE_NAME = 'current_config.txt'


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

    """

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def current(cls) -> 'Workspace':
        raise NotImplementedError()

    def rename(self, new_name: str):
        raise NotImplementedError()

    def copy(self, new_name: str):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def get_config(self, name: str):
        raise NotImplementedError()

    def get_current_config(self) -> str:
        raise NotImplementedError()

    def get_config_file(self, name: str) -> str:
        raise NotImplementedError()

    def rename_config(self, new_name: str):
        raise NotImplementedError()

    def copy_config(self, new_name: str):
        raise NotImplementedError()

    def add_config(self, new_name: str):
        raise NotImplementedError()

    def remove_config(self, new_name: str):
        raise NotImplementedError()
