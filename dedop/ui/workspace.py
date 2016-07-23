import fnmatch
import os.path
import pkgutil
import shutil
import subprocess
import sys
from typing import List

from dedop.ui.workspace_info import WorkspaceInfo

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

    @property
    def workspaces_dir(self):
        return self._workspaces_dir

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

    def get_workspace_info(self, workspace_name: str):
        """
        :param workspace_name: workspace name to be queried
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        dir_path = self._get_workspace_path(workspace_name)
        config_name = self.get_current_config_name(workspace_name)
        return WorkspaceInfo(dir_path, workspace_name, self.get_workspace_names(), config_name,
                             self.get_config_names(workspace_name))

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
        package = 'dedop.ui.defaults'
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

    def rename_config(self, workspace_name: str, config_name: str, new_config_name: str):
        """
        :param workspace_name: the workspace name where the config is to be renamed
        :param config_name: the name of the configuration to be renamed
        :param new_config_name: the name of the new configuration
        :raise: WorkspaceError
        """
        self._assert_workspace_exists(workspace_name)
        self._assert_config_exists(workspace_name, config_name)
        dir_path = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name)
        dir_path_new = self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, new_config_name)
        if os.path.exists(dir_path):
            try:
                os.rename(dir_path, dir_path_new)
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
        """
        :param workspace_name: workspace name to add the input
        :param input_paths: path to the input files to be added
        :param monitor: to monitor the progress
        """
        inputs_dir = self._ensure_dir_exists(self._get_workspace_path(workspace_name, 'inputs'))
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
        input_paths = [self._get_workspace_path(workspace_name, 'inputs', input_name) for input_name in input_names]
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
        inputs_dir = self._get_workspace_path(workspace_name, 'inputs')
        if os.path.exists(inputs_dir):
            return self.get_nc_filename_list(inputs_dir, pattern)
        return []

    def get_input_paths(self, workspace_name: str):
        return [self._get_workspace_path(workspace_name, 'inputs', name) for name in
                self.get_input_names(workspace_name)]

    # TODO forman make it public
    def _get_workspace_path(self, workspace_name, *paths):
        return os.path.join(self._workspaces_dir, workspace_name, *paths)

    # TODO forman make it public
    def _get_config_path(self, workspace_name, config_name, *paths):
        return self._get_workspace_path(workspace_name, _CONFIGS_DIR_NAME, config_name, *paths)

    def remove_outputs(self, workspace_name, config_name):
        """
        :param workspace_name: the workspace name in which the output files are located
        :param config_name: the config name with which the output files were created
        """
        output_dir = self.get_output_dir(workspace_name, config_name)
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
        outputs_dir = self.get_output_dir(workspace_name, config_name)
        if os.path.exists(outputs_dir):
            return self.get_nc_filename_list(outputs_dir, pattern)
        return []

    def inspect_l1b_product(self, workspace_name: str, l1b_path: str):

        package = 'dedop.ui.defaults'
        template_data = pkgutil.get_data(package, 'inspect-template.ipynb')
        notebook_json = template_data.decode("utf-8") \
            .replace('__L1B_FILE_PATH__', repr(l1b_path).replace('\\', '\\\\'))

        return self._launch_notebook_from_template(workspace_name, 'inspect', notebook_json, 'inspect - [%s]' %
                                                   self.name_to_title(l1b_path, 80))

    def compare_l1b_products(self, workspace_name, l1b_path_1: str, l1b_path_2: str):

        package = 'dedop.ui.defaults'
        template_data = pkgutil.get_data(package, 'compare-template.ipynb')
        notebook_json = template_data.decode("utf-8") \
            .replace('__L1B_FILE_PATH_1__', repr(l1b_path_1).replace('\\', '\\\\')) \
            .replace('__L1B_FILE_PATH_2__', repr(l1b_path_2).replace('\\', '\\\\'))

        return self._launch_notebook_from_template(workspace_name, 'compare', notebook_json, 'compare - [%s] [%s]' % (
            self.name_to_title(l1b_path_1, 40),
            self.name_to_title(l1b_path_2, 40),))

    @classmethod
    def name_to_title(cls, name, max_len):
        assert name
        assert max_len > 3
        return name if len(name) <= max_len else '...' + name[3 - max_len:]

    def _launch_notebook_from_template(self,
                                       workspace_name: str,
                                       notebook_basename: str,
                                       notebook_json: str,
                                       title: str):
        notebook_dir = self._get_workspace_path(workspace_name, 'notebooks')
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

    def launch_notebook(self, title: str, notebook_dir: str, notebook_path: str = None):
        # TODO (forman, 20160722): this command is for Windows, make it work for Mac OS and Linux
        # we must start a new terminal window so that users can close the Notebook session easily
        terminal_title = 'DeDop - %s' % title

        if sys.platform.startswith('win'):
            terminal_command = 'start "%s" /Min jupyter notebook --notebook-dir "%s"' % (terminal_title, notebook_dir)
            if notebook_path:
                terminal_command += ' "%s"' % notebook_path
        else:
            raise NotImplementedError('terminal_command')

        try:
            # print('calling:', command)
            subprocess.check_call(terminal_command, shell=True)
            print('A new terminal window named "%s" has been opened.' % terminal_title)
            print('Close the window or press CTRL+C within it to terminate the Notebook session.')
        except (subprocess.CalledProcessError, IOError, OSError) as error:
            raise WorkspaceError('failed to launch Jupyter Notebook: %s' % str(error))

    @staticmethod
    def get_nc_filename_list(outputs_dir, pattern):
        fn_list = [fn for fn in os.listdir(outputs_dir) if
                   fn.endswith('.nc') and os.path.isfile(os.path.join(outputs_dir, fn))]
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

    def _assert_workspace_exists(self, workspace_name):
        if not os.path.exists(self._get_workspace_path(workspace_name)):
            raise WorkspaceError('workspace "%s" does not exist' % workspace_name)

    def _assert_config_exists(self, workspace_name, config_name):
        if not os.path.exists(self._get_workspace_path(workspace_name, 'configs', config_name)):
            raise WorkspaceError(
                'configuration "%s" inside workspace "%s" does not exist' % (config_name, workspace_name))

    def get_output_dir(self, workspace_name, config_name):
        return self._get_workspace_path(workspace_name, 'configs', config_name, 'outputs')

    def get_output_path(self, workspace_name, config_name, *paths):
        return os.path.join(self.get_output_dir(workspace_name, config_name), *paths)
