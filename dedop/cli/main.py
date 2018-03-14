"""
This module provides DeDop's command-line interface (CLI) API and the CLI executable.

To use the CLI executable, invoke the module file as a script, type ``python3 dedop/ui/cli.py [ARGS] [OPTIONS]``. Type
`python3 dedop/ui/cli.py --help`` for usage help.

The CLI operates on sub-commands. New sub-commands can be added by inheriting from the :py:class:`Command` class
and extending the ``Command.REGISTRY`` list of known command classes.
"""

import argparse
import os.path
import subprocess
import sys

from cate.util.cli import run_main, Command, SubCommandCommand, CommandError

from dedop.ui.exception import WorkspaceError
from dedop.util.config import DEFAULT_CONFIG_FILE, get_config_path, get_config_value
from dedop.util.monitor import Monitor
from dedop.version import __version__

_DEFAULT_SUFFIX = '_1'

_DEFAULT_CONFIG_NAME = 'default'
_DEFAULT_WORKSPACE_NAME = 'default'

_STATUS_NO_WORKSPACE = 10, 'no current workspace, use option -w to name a WORKSPACE'
_STATUS_NO_CONFIG = 20, 'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"'
_STATUS_NO_INPUTS = 30, 'workspace "%s" doesn\'t have any inputs yet, use "dedop input add *.nc" to add some'
_STATUS_NO_MATCHING_INPUTS = 40, 'no matching inputs found'
_STATUS_NO_MATCHING_OUTPUTS = 40, 'no matching outputs found'

#: Name of the DeDop CLI executable.
CLI_NAME = 'dedop'
CLI_DESCRIPTION = 'Delay Doppler Altimeter Data (DeDop) command-line interface'

_LICENSE_INFO_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'LICENSE')
_DOCS_URL = 'http://dedop-core.readthedocs.io/en/latest/'
_LICENSE = """
{dedop} - ESA DeDop Shell, copyright (C) 2016 by the DeDop team and contributors

{dedop} has been developed under contract to the European Space Agency (ESA).

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Type "{dedop} license" for details.
""".format(dedop=CLI_NAME)

_WORKSPACE_MANAGER = None
_PROCESSOR_FACTORY = None


def _input(prompt, default=None):
    answer = input(prompt).strip()
    return answer if answer else default


def _get_workspace_name(command_args):
    workspace_name = command_args.workspace_name
    if workspace_name:
        return workspace_name
    workspace = _WORKSPACE_MANAGER.get_current_workspace()
    return workspace.name


def _get_workspace_and_config_name(command_args):
    workspace_name = command_args.workspace_name
    if not workspace_name:
        workspace = _WORKSPACE_MANAGER.get_current_workspace()
        workspace_name = workspace.name
    config_name = command_args.config_name
    if workspace_name and not config_name:
        config_name = _WORKSPACE_MANAGER.get_current_config_name(workspace_name)
    return workspace_name, config_name


def _expand_wildcard_paths(inputs_files):
    expanded_inputs = []
    import glob
    for input_files in inputs_files:
        if sys.version_info >= (3, 5):
            glob_input = glob.glob(input_files, recursive=True)
        else:
            glob_input = glob.glob(input_files)
        expanded_inputs.extend(glob_input)
    return expanded_inputs


def _dir_size(dir_path):
    total = 0
    for entry in os.scandir(dir_path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += _dir_size(entry.path)
    return total


def _print_config_versions(chd_version, cnf_version, cst_version):
    print("Config versions:")
    print('    CHD.json:', 'version ' + str(chd_version) if chd_version > -1 else 'no-version')
    print('    CNF.json:', 'version ' + str(cnf_version) if cnf_version > -1 else 'no-version')
    print('    CST.json:', 'version ' + str(cst_version) if cst_version > -1 else 'no-version')


def _require_upgrade(workspace_name: str, config_name: str) -> bool:
    current_chd_version, current_cnf_version, current_cst_version = _WORKSPACE_MANAGER.get_all_config_version(
        workspace_name, config_name)
    default_chd_version, default_cnf_version, default_cst_version = _WORKSPACE_MANAGER.get_all_default_config_version()
    if default_chd_version > current_chd_version \
            or default_cnf_version > current_cnf_version \
            or default_cst_version > current_cst_version:
        return True
    else:
        return False


class RunProcessorCommand(Command):
    CMD_NAME = 'run'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Run the Delay Doppler Processor (DDP).'
        return dict(aliases=['r'], help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument('-s', '--skip-l1bs', action='store_true',
                            help='Skip generation of L1B-S files.')
        parser.add_argument('-q', '--quiet', action='store_true',
                            help='Suppress output of progress information.')
        parser.add_argument('-w', '--workspace', dest='workspace_name', metavar='WORKSPACE',
                            help='Use WORKSPACE, defaults to current workspace.')
        parser.add_argument('-c', '--config', dest='config_name', metavar='CONFIG',
                            help='Use CONFIG in workspace, defaults to current DDP configuration.')
        parser.add_argument('-i', '--inputs', metavar='L1A_FILE', nargs='*',
                            help='L1A input files. Defaults to all L1A files in workspace.')
        parser.add_argument('-o', '--output', dest='output_dir', metavar='DIR',
                            help='Alternative output directory.')
        parser.add_argument('-a', '--all-configs', dest='all_configs', action='store_true',
                            help='Run all DDP configurations in workspace. Cannot be used with option -c')

    def execute(self, command_args):
        from dedop.model.exception import ProcessorException

        try:
            if command_args.all_configs and command_args.config_name:
                raise CommandError('option -a cannot be used with option -c"')

            workspace_name, config_name = _get_workspace_and_config_name(command_args)
            if not workspace_name:
                workspace_name = ManageWorkspacesCommand.create_default_workspace()

            if command_args.all_configs:
                config_names = _WORKSPACE_MANAGER.get_config_names(workspace_name)
                if not config_names:
                    raise CommandError(
                        'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
            else:
                if not config_name:
                    config_name = ManageConfigsCommand.create_default_config(workspace_name)
                config_names = [config_name]

            inputs = command_args.inputs if command_args.inputs else _WORKSPACE_MANAGER.get_input_paths(workspace_name)
            if not inputs:
                raise CommandError(
                    'workspace "%s" doesn\'t have any inputs yet, use "dedop input add *.nc" to add some'
                    % workspace_name)

            for config_name in config_names:
                chd_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CHD')
                cnf_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CNF')
                cst_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CST')
                output_dir = command_args.output_dir if command_args.output_dir else \
                    _WORKSPACE_MANAGER.get_outputs_path(workspace_name, config_name)
                skip_l1bs = command_args.skip_l1bs

                # noinspection PyCallingNonCallable
                processor = _PROCESSOR_FACTORY(config_name,
                                               chd_file=chd_file,
                                               cnf_file=cnf_file,
                                               cst_file=cst_file,
                                               output_dir=output_dir,
                                               skip_l1bs=skip_l1bs)
                for input_file in inputs:
                    monitor = Monitor.NULL if command_args.quiet else self.new_monitor()
                    processor.process(input_file, monitor=monitor)

        except (WorkspaceError, ProcessorException) as error:
            raise CommandError(error)


class ManageWorkspacesCommand(SubCommandCommand):
    @classmethod
    def name(cls):
        return 'workspace'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage DeDop workspaces.'
        return dict(aliases=['w'], help=help_line, description=help_line)

    @classmethod
    def configure_parser_and_subparsers(cls, parser, subparsers):
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")

        parser.set_defaults(ws_parser=parser)

        parser_add = subparsers.add_parser('add', help='Add new workspace')
        parser_add.add_argument(**workspace_name_attributes)
        parser_add.set_defaults(ws_command=cls.execute_add)

        parser_remove = subparsers.add_parser('remove', aliases=['rm'], help='Remove workspace')
        parser_remove.add_argument(nargs='?', **workspace_name_attributes)
        parser_remove.set_defaults(ws_command=cls.execute_remove)
        parser_remove.add_argument('-y', '--yes', action='store_true', help='Do not ask for confirmation.')

        parser_copy = subparsers.add_parser('copy', aliases=['cp'], help='Copy workspace')
        parser_copy.add_argument(nargs='?', **workspace_name_attributes)
        parser_copy.add_argument('new_name', metavar='NEW_NAME', nargs='?', help='Name of the new workspace')
        parser_copy.set_defaults(ws_command=cls.execute_copy)

        parser_rename = subparsers.add_parser('rename', aliases=['rn'], help='Rename workspace')
        parser_rename.add_argument(nargs='?', **workspace_name_attributes)
        parser_rename.add_argument('new_name', metavar='NEW_NAME', help='New name of the workspace')
        parser_rename.set_defaults(ws_command=cls.execute_rename)

        parser_current = subparsers.add_parser('current', aliases=['cur'], help='Current workspace')
        parser_current.add_argument(nargs='?', **workspace_name_attributes)
        parser_current.set_defaults(ws_command=cls.execute_current)

        parser_list = subparsers.add_parser('list', aliases=['ls'], help='List workspaces')
        parser_list.set_defaults(ws_command=cls.execute_list)

    def execute(self, command_args):
        if hasattr(command_args, 'ws_command') and command_args.ws_command:
            return command_args.ws_command(command_args)
        else:
            command_args.ws_parser.print_help()

    @classmethod
    def execute_add(cls, command_args):
        workspace_name = command_args.workspace_name
        try:
            cls.create_workspace(workspace_name, exists_ok=False)
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_remove(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace')
        if command_args.yes:
            answer = 'yes'
        else:
            answer = _input('remove workspace "%s"? [yes]' % workspace_name, 'yes')
        if answer.lower() == 'yes':
            try:
                _WORKSPACE_MANAGER.delete_workspace(workspace_name)
                print('removed workspace "%s"' % workspace_name)
                workspace = _WORKSPACE_MANAGER.get_current_workspace()
                if workspace_name == workspace.name:
                    workspace_names = _WORKSPACE_MANAGER.get_workspace_names()
                    if 'default' in workspace_names:
                        cls.set_current_workspace('default')
                    elif len(workspace_names) > 0:
                        cls.set_current_workspace(workspace_names[0])
                    else:
                        cls.set_current_workspace(None)
            except WorkspaceError as error:
                raise CommandError(error)

    @classmethod
    def execute_copy(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace')
        new_name = command_args.new_name
        if not new_name:
            new_name = workspace_name + _DEFAULT_SUFFIX
        new_name = cls.ensure_unique_name(new_name)
        try:
            _WORKSPACE_MANAGER.copy_workspace(workspace_name, new_name)
            print('copied workspace "%s" to "%s"' % (workspace_name, new_name))
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_rename(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace')
        new_name = cls.ensure_unique_name(command_args.new_name)
        try:
            _WORKSPACE_MANAGER.rename_workspace(workspace_name, new_name)
            print('renamed workspace "%s" to "%s"' % (workspace_name, new_name))
            workspace = _WORKSPACE_MANAGER.get_current_workspace()
            if workspace_name == workspace.name:
                cls.set_current_workspace(new_name)
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_current(cls, command_args):
        try:
            if command_args.workspace_name:
                cls.set_current_workspace(command_args.workspace_name)
            else:
                workspace = _WORKSPACE_MANAGER.get_current_workspace()
                workspace_name = workspace.name
                if workspace_name:
                    print('current workspace is "%s"' % workspace_name)
                else:
                    print('no current workspace')
        except WorkspaceError as error:
            raise CommandError(error)

    # noinspection PyUnusedLocal
    @classmethod
    def execute_list(cls, command_args):
        workspace_names = _WORKSPACE_MANAGER.get_workspace_names()
        num_workspaces = len(workspace_names)
        if num_workspaces == 0:
            print('no workspaces')
        elif num_workspaces == 1:
            print('1 workspace:')
        else:
            print('%d workspaces:' % num_workspaces)
        for i in range(num_workspaces):
            workspace_name = workspace_names[i]
            print('%3d: %s' % (i + 1, workspace_name))

    @classmethod
    def create_default_workspace(cls) -> str:
        return cls.create_workspace(_DEFAULT_WORKSPACE_NAME, exists_ok=True)

    @classmethod
    def create_workspace(cls, workspace_name, exists_ok=False) -> str:
        if exists_ok and _WORKSPACE_MANAGER.workspace_exists(_DEFAULT_WORKSPACE_NAME):
            return workspace_name
        _WORKSPACE_MANAGER.create_workspace(workspace_name)
        print('created workspace "%s"' % workspace_name)
        cls.set_current_workspace(workspace_name)
        return workspace_name

    @classmethod
    def set_current_workspace(cls, workspace_name):
        if workspace_name:
            _WORKSPACE_MANAGER.set_current_workspace_name(workspace_name)
            print('current workspace is "%s"' % workspace_name)
        else:
            _WORKSPACE_MANAGER.set_current_workspace_name('')

    @classmethod
    def ensure_unique_name(cls, new_name):
        index = 2
        valid_new_name = new_name
        workspace_names = _WORKSPACE_MANAGER.get_workspace_names()
        while valid_new_name in workspace_names:
            print('workspace "%s" already exists' % valid_new_name)
            valid_new_name = '%s_%d' % (new_name, index)
            index += 1
        return valid_new_name


class ManageConfigsCommand(SubCommandCommand):
    @classmethod
    def name(cls):
        return 'config'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage DeDop DDP configurations.'
        return dict(aliases=['c'], help=help_line, description=help_line)

    @classmethod
    def configure_parser_and_subparsers(cls, parser, subparsers):
        config_name_attributes = dict(dest='config_name', metavar='CONFIG', help="Name of the DDP configuration")

        parser.set_defaults(cf_parser=parser)

        parser_add = subparsers.add_parser('add', help='Add new DDP configuration')
        cls.setup_default_parser_argument(parser_add)
        parser_add.add_argument(**config_name_attributes)
        parser_add.add_argument('--cryosat-adapted', action='store_true',
                                help='Initialise configuration with parameters for '
                                     'processing reconditioned Cryosat-2 FBR data')
        parser_add.set_defaults(cf_command=cls.execute_add)

        parser_remove = subparsers.add_parser('remove', aliases=['rm'], help='Remove DDP configuration')
        parser_remove.add_argument('-y', '--yes', action='store_true',
                                   help='Do not ask for confirmation.')
        cls.setup_default_parser_argument(parser_remove)
        parser_remove.add_argument(nargs='?', **config_name_attributes)
        parser_remove.set_defaults(cf_command=cls.execute_remove)

        parser_edit = subparsers.add_parser('edit', aliases=['ed'], help='Edit DDP configuration')
        cls.setup_default_parser_argument(parser_edit)
        parser_edit.add_argument(nargs='?', **config_name_attributes)
        parser_edit.set_defaults(cf_command=cls.execute_edit)

        parser_copy = subparsers.add_parser('copy', aliases=['cp'], help='Copy DDP configuration')
        cls.setup_default_parser_argument(parser_copy)
        parser_copy.add_argument(nargs='?', **config_name_attributes)
        parser_copy.add_argument('new_name', metavar='NEW_NAME', nargs='?', help='Name of the new DDP configuration')
        parser_copy.set_defaults(cf_command=cls.execute_copy)

        parser_rename = subparsers.add_parser('rename', aliases=['rn'], help='Rename DDP configuration')
        cls.setup_default_parser_argument(parser_rename)
        parser_rename.add_argument(nargs='?', **config_name_attributes)
        parser_rename.add_argument('new_name', metavar='NEW_NAME', help='New name of the DDP configuration')
        parser_rename.set_defaults(cf_command=cls.execute_rename)

        parser_info = subparsers.add_parser('info', aliases=['i'], help='Show DDP configuration info')
        cls.setup_default_parser_argument(parser_info)
        parser_info.add_argument(nargs='?', **config_name_attributes)
        parser_info.set_defaults(cf_command=cls.execute_info)

        parser_current = subparsers.add_parser('current', aliases=['cur'], help='Current DDP configuration')
        cls.setup_default_parser_argument(parser_current)
        parser_current.add_argument(nargs='?', **config_name_attributes)
        parser_current.set_defaults(cf_command=cls.execute_current)

        parser_list = subparsers.add_parser('list', aliases=['ls'], help='List DDP configurations')
        cls.setup_default_parser_argument(parser_list)
        parser_list.set_defaults(cf_command=cls.execute_list)

        parser_upgrade = subparsers.add_parser('upgrade', aliases=['up'],
                                               help='Upgrade DDP configurations to the newest versions')
        cls.setup_default_parser_argument(parser_upgrade)
        parser_upgrade.add_argument(nargs='?', **config_name_attributes)
        parser_upgrade.set_defaults(cf_command=cls.execute_upgrade)

        parser_version = subparsers.add_parser('version', aliases=['v'], help='Show DDP configuration versions')
        cls.setup_default_parser_argument(parser_version)
        parser_version.add_argument(nargs='?', **config_name_attributes)
        parser_version.set_defaults(cf_command=cls.execute_version)

    @classmethod
    def setup_default_parser_argument(cls, parser):
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")
        parser.add_argument('-w', '--workspace', **workspace_name_attributes)

    def execute(self, command_args):
        if hasattr(command_args, 'cf_command') and command_args.cf_command:
            return command_args.cf_command(command_args)
        else:
            command_args.cf_parser.print_help()

    @classmethod
    def execute_add(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        try:
            cls.create_config(workspace_name, config_name, exist_ok=False, cryosat=command_args.cryosat_adapted)
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_remove(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if not config_name:
            raise CommandError(
                'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
        if command_args.yes:
            answer = 'yes'
        else:
            answer = _input('remove DDP configuration "%s"? [yes]' % config_name, 'yes')
        if answer.lower() == 'yes':
            try:
                _WORKSPACE_MANAGER.delete_config(workspace_name, config_name)
                print('removed DDP configuration "%s"' % config_name)
                if config_name == _WORKSPACE_MANAGER.get_current_config_name(workspace_name):
                    config_names = _WORKSPACE_MANAGER.get_config_names(workspace_name)
                    if 'default' in config_names:
                        cls.set_current_config(workspace_name, 'default')
                    elif len(config_names) > 0:
                        cls.set_current_config(workspace_name, config_names[0])
                    else:
                        cls.set_current_config(workspace_name, None)
            except WorkspaceError as error:
                raise CommandError(error)

    @classmethod
    def execute_copy(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if not config_name:
            raise CommandError(
                'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
        new_name = command_args.new_name
        if not new_name:
            new_name = config_name + '_copy'
        new_name = cls.ensure_unique_name(workspace_name, new_name)
        try:
            _WORKSPACE_MANAGER.copy_config(workspace_name, config_name, new_name)
            print('copied DDP configuration "%s" to "%s"' % (config_name, new_name))
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_rename(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if not config_name:
            raise CommandError(
                'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
        new_name = cls.ensure_unique_name(workspace_name, command_args.new_name)
        try:
            _WORKSPACE_MANAGER.rename_config(workspace_name, config_name, new_name)
            print('renamed DDP configuration "%s" to "%s"' % (config_name, new_name))
            if config_name == _WORKSPACE_MANAGER.get_current_config_name(workspace_name):
                cls.set_current_config(workspace_name, new_name)
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_edit(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        try:
            if not workspace_name:
                workspace_name = ManageWorkspacesCommand.create_default_workspace()
            if not config_name:
                config_name = cls.create_default_config(workspace_name)
            chd_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CHD')
            cnf_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CNF')
            cst_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CST')
            _WORKSPACE_MANAGER.open_file(chd_file)
            _WORKSPACE_MANAGER.open_file(cnf_file)
            _WORKSPACE_MANAGER.open_file(cst_file)
        except (WorkspaceError, IOError, OSError) as error:
            raise CommandError(error)

    @classmethod
    def execute_current(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            workspace_name = _DEFAULT_WORKSPACE_NAME
        try:
            if config_name:
                cls.set_current_config(workspace_name, config_name)
            else:
                config_name = _WORKSPACE_MANAGER.get_current_config_name(workspace_name)
                if config_name:
                    print('current DDP configuration is "%s"' % config_name)
                else:
                    print('no current DDP configuration')
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_info(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if not config_name:
            raise CommandError(
                'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
        config_path = _WORKSPACE_MANAGER.get_config_path(workspace_name, config_name)
        print('current workspace:              ', workspace_name)
        print('current DDP configuration:      ', config_name)
        print('current DDP configuration path: ', config_path)
        if sys.platform.startswith('win'):
            # /A-D = don't show directories
            subprocess.check_call('dir /A-D "%s"' % config_path, shell=True)
        else:
            subprocess.check_call('ls "%s"' % config_path, shell=True)

    @classmethod
    def execute_list(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        config_names = _WORKSPACE_MANAGER.get_config_names(workspace_name)
        num_configs = len(config_names) if config_names else 0
        if num_configs == 0:
            print('no DDP configurations in workspace "%s"' % workspace_name)
        elif num_configs == 1:
            print('1 DDP configuration in workspace "%s":' % workspace_name)
        else:
            print('%d DDP configurations in workspace "%s":' % (num_configs, workspace_name))
        for i in range(num_configs):
            config_name = config_names[i]
            print('%3d: %s' % (i + 1, config_name))

    @classmethod
    def execute_upgrade(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if _require_upgrade(workspace_name, config_name):
            chd_version, cnf_version, cst_version = _WORKSPACE_MANAGER.upgrade_all_config(workspace_name, config_name)
            print("Upgrade successful!")
            print()
            _print_config_versions(chd_version, cnf_version, cst_version)
        else:
            print("Current configurations are already up to date. No upgrade has been performed.")

    @classmethod
    def execute_version(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        chd_version, cnf_version, cst_version = _WORKSPACE_MANAGER.get_all_config_version(workspace_name, config_name)
        print("Workspace name :", workspace_name)
        print("Config name    :", config_name)
        print()
        _print_config_versions(chd_version, cnf_version, cst_version)

    @classmethod
    def create_default_config(cls, workspace_name) -> str:
        return cls.create_config(workspace_name, _DEFAULT_CONFIG_NAME, exist_ok=True)

    @classmethod
    def create_config(cls, workspace_name, config_name, exist_ok=True, cryosat=False) -> str:
        """
        Create a new configuration *config_name* in workspace *workspace_name*.

        :param cryosat: if true, create a new configuration based on Cryosat-2 FBR config template
        :param workspace_name: Workspace name
        :param config_name: Configuration name
        :param exist_ok: if True, *config_name* may already exist
        :return: *config_name*
        :raise: WorkspaceError
        """
        if not workspace_name:
            workspace_name = ManageWorkspacesCommand.create_default_workspace()
        if exist_ok and _WORKSPACE_MANAGER.config_exists(workspace_name, config_name):
            return config_name
        _WORKSPACE_MANAGER.create_config(workspace_name, config_name, cryosat=cryosat)
        print('created DDP configuration "%s" in workspace "%s"' % (config_name, workspace_name))
        cls.set_current_config(workspace_name, config_name)
        return config_name

    @classmethod
    def set_current_config(cls, workspace_name, config_name):
        """
        Make *config_name* the current configuration in workspace *workspace_name*.

        :param workspace_name: Workspace name
        :param config_name: Configuration name
        :raise: WorkspaceError
        """
        if config_name:
            _WORKSPACE_MANAGER.set_current_config_name(workspace_name, config_name)
            print('current DDP configuration is "%s"' % config_name)
        else:
            _WORKSPACE_MANAGER.set_current_config_name(workspace_name, '')

    @classmethod
    def ensure_unique_name(cls, workspace_name, new_name):
        index = 2
        valid_new_name = new_name
        config_names = _WORKSPACE_MANAGER.get_config_names(workspace_name)
        while valid_new_name in config_names:
            print('DDP configuration "%s" already exists' % valid_new_name)
            valid_new_name = '%s_%d' % (new_name, index)
            index += 1
        return valid_new_name


class ManageInputsCommand(SubCommandCommand):
    CMD_NAME = 'input'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage L1A inputs.'
        return dict(aliases=['i'], help=help_line, description=help_line)

    @classmethod
    def configure_parser_and_subparsers(cls, parser, subparsers):
        parser.set_defaults(mi_parser=parser)

        parser_add = subparsers.add_parser('add', help='Add new inputs')
        cls.setup_default_parser_argument(parser_add)
        parser_add.add_argument('-q', '--quiet', action='store_true',
                                help='Suppress output of progress information.')
        parser_add.add_argument('inputs', metavar='L1A_FILE', nargs='+',
                                help="L1A input file to add to workspace.")
        parser_add.set_defaults(mi_command=cls.execute_add)

        parser_remove = subparsers.add_parser('remove', aliases=['rm'], help='Remove inputs')
        cls.setup_default_parser_argument(parser_remove)
        parser_remove.add_argument('-q', '--quiet', action='store_true',
                                   help='Suppress output of progress information.')
        parser_remove.add_argument('inputs', metavar='L1A_FILE', nargs='*',
                                   help="L1A input file to add to workspace.")
        parser_remove.set_defaults(mi_command=cls.execute_remove)

        parser_list = subparsers.add_parser('list', aliases=['ls'], help='List inputs')
        cls.setup_default_parser_argument(parser_list)
        parser_list.add_argument('pattern', metavar='WC', nargs='?',
                                 help="Wildcard pattern.")
        parser_list.set_defaults(mi_command=cls.execute_list)

    @classmethod
    def setup_default_parser_argument(cls, parser):
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")
        parser.add_argument('-w', '--workspace', **workspace_name_attributes)

    def execute(self, command_args):
        if hasattr(command_args, 'mi_command') and command_args.mi_command:
            return command_args.mi_command(command_args)
        else:
            command_args.mi_parser.print_help()

    @classmethod
    def execute_add(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        inputs = command_args.inputs
        if not inputs:
            inputs = [os.path.join('.', '*.nc')]
        inputs = _expand_wildcard_paths(inputs)
        if not inputs:
            raise CommandError('no matching inputs found')
        monitor = Monitor.NULL if command_args.quiet else cls.new_monitor()
        try:
            if not workspace_name:
                workspace_name = ManageWorkspacesCommand.create_default_workspace()
            _WORKSPACE_MANAGER.add_inputs(workspace_name, inputs, monitor)
            input_count = len(inputs)
            if input_count == 0:
                print('no inputs added')
            elif input_count == 1:
                print('one input added')
            else:
                print('added %s inputs' % input_count)
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_remove(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        input_names = command_args.inputs
        if not input_names:
            input_names = '*.nc'
        input_names = _WORKSPACE_MANAGER.get_input_names(workspace_name, pattern=input_names)
        if not input_names:
            raise CommandError('no matching inputs found')
        monitor = Monitor.NULL if command_args.quiet else cls.new_monitor()
        answer = 'yes' if command_args.quiet else _input('delete inputs "%s"? [yes]' % input_names, 'yes').lower()
        if answer.lower() == 'yes':
            try:
                _WORKSPACE_MANAGER.remove_inputs(workspace_name, input_names, monitor)
                input_count = len(input_names)
                if input_count == 0:
                    print('no inputs removed')
                elif input_count == 1:
                    print('one input removed')
                else:
                    print('removed %s inputs' % input_count)
            except WorkspaceError as error:
                raise CommandError(error)

    @classmethod
    def execute_list(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        pattern = command_args.pattern
        input_names = _WORKSPACE_MANAGER.get_input_names(workspace_name, pattern=pattern)
        num_inputs = len(input_names)
        if num_inputs == 0:
            print('no inputs in workspace "%s"' % workspace_name)
        elif num_inputs == 1:
            print('1 input in workspace "%s":' % workspace_name)
        else:
            print('%d inputs in workspace "%s":' % (num_inputs, workspace_name))
        for i in range(num_inputs):
            input_name = input_names[i]
            print('%3d: %s' % (i + 1, input_name))


class ManageOutputsCommand(SubCommandCommand):
    CMD_NAME = 'output'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage and analyse L1B outputs.'
        return dict(aliases=['o'], help=help_line, description=help_line)

    @classmethod
    def configure_parser_and_subparsers(cls, parser, subparsers):
        parser.set_defaults(mo_parser=parser)  # so we cant print usage, if no sub-command given

        parser_clean = subparsers.add_parser('clean', aliases=['cl'],
                                             help='Clean outputs folder of current configuration or CONFIG')
        cls.set_workspace_config_parser_arguments(parser_clean)
        parser_clean.add_argument('-q', '--quiet', action='store_true',
                                  help='Suppress output of progress information.')
        parser_clean.set_defaults(mo_command=cls.execute_clean)

        parser_list = subparsers.add_parser('list', aliases=['ls'],
                                            help='List outputs folder of current configuration or CONFIG')
        cls.set_workspace_config_parser_arguments(parser_list)
        parser_list.add_argument('pattern', metavar='WC', nargs='?',
                                 help="Wildcard pattern.")
        parser_list.set_defaults(mo_command=cls.execute_list)

        parser_open = subparsers.add_parser('open', aliases=['op'],
                                            help='Open outputs folder of current configuration or CONFIG')
        cls.set_workspace_config_parser_arguments(parser_open)
        parser_open.set_defaults(mo_command=cls.execute_open)

        parser_inspect = subparsers.add_parser('inspect', aliases=['ins'], help='Inspect L1B product')
        cls.set_workspace_config_parser_arguments(parser_inspect)
        parser_inspect.add_argument('l1b_filename', metavar='L1B_FILENAME',
                                    help='The filename or path of the a L1B product. If only a filename is given, '
                                         'it must exist in outputs of the given workspace/configuration.')
        parser_inspect.set_defaults(mo_command=cls.execute_inspect)

        parser_compare = subparsers.add_parser('compare', aliases=['cmp'], help='Compare two L1B products')
        cls.set_workspace_config_parser_arguments(parser_compare)
        cls.set_workspace2_config2_parser_arguments(parser_compare)
        parser_compare.add_argument('l1b_filename_1', metavar='L1B_FILENAME_1',
                                    help='The filename or path of the first L1B product. If only a filename is given, '
                                         'it must exist in outputs of the given workspace/configuration.')
        parser_compare.add_argument('l1b_filename_2', metavar='L1B_FILENAME_2', nargs='?',
                                    help='The filename or path of the second L1B product. If only a filename is given, '
                                         'it must exist in outputs of the given second or first '
                                         'workspace/configuration. If omitted, the first filename or path is used.')
        parser_compare.set_defaults(mo_command=cls.execute_compare)

    @classmethod
    def set_workspace_config_parser_arguments(cls, parser):
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE',
                                         help="Name of the workspace.")
        parser.add_argument('-w', '--workspace', **workspace_name_attributes)
        config_name_attributes = dict(dest='config_name', metavar='CONFIG',
                                      help="Name of the DDP configuration.")
        parser.add_argument('-c', '--config', **config_name_attributes)

    @classmethod
    def set_workspace2_config2_parser_arguments(cls, parser):
        workspace_name_attributes = dict(dest='workspace_name_2', metavar='WORKSPACE_2',
                                         help="The workspace of the second L1B product.")
        parser.add_argument('-W', '--workspace-2', **workspace_name_attributes)
        config_name_attributes = dict(dest='config_name_2', metavar='CONFIG_2',
                                      help="The DDP configuration of the second L1B product")
        parser.add_argument('-C', '--config-2', **config_name_attributes)

    def execute(self, command_args):
        if hasattr(command_args, 'mo_command') and command_args.mo_command:
            return command_args.mo_command(command_args)
        else:
            command_args.mo_parser.print_help()

    @classmethod
    def execute_clean(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if not config_name:
            raise CommandError(
                'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
        output_names = _WORKSPACE_MANAGER.get_output_names(workspace_name, config_name)
        if not output_names:
            raise CommandError('no matching outputs found')
        answer = 'yes' if command_args.quiet else _input('clean outputs directory? [yes]', 'yes')
        if answer.lower() == 'yes':
            try:
                _WORKSPACE_MANAGER.remove_outputs(workspace_name, config_name)
                output_count = len(output_names)
                if output_count == 0:
                    print('no outputs removed')
                elif output_count == 1:
                    print('one output removed')
                else:
                    print('removed %s outputs' % output_count)
            except WorkspaceError as error:
                raise CommandError(error)

    @classmethod
    def execute_open(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if not config_name:
            raise CommandError(
                'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
        try:
            outputs_dir = _WORKSPACE_MANAGER.get_outputs_path(workspace_name, config_name)
            if os.path.exists(outputs_dir):
                _WORKSPACE_MANAGER.open_file(outputs_dir)
            else:
                print(
                    'no outputs created with DDP configuration "%s" in workspace "%s"' % (config_name, workspace_name))
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_inspect(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        try:
            if not workspace_name:
                workspace_name = ManageWorkspacesCommand.create_default_workspace()

            l1b_filename = command_args.l1b_filename
            if os.path.dirname(l1b_filename):
                l1b_path = os.path.abspath(l1b_filename)
            else:
                if not config_name:
                    raise CommandError(
                        'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
                l1b_path = _WORKSPACE_MANAGER.get_outputs_path(workspace_name, config_name, l1b_filename)
            if not os.path.exists(l1b_path):
                raise CommandError('L1B product not found: %s' % l1b_path)

            _WORKSPACE_MANAGER.inspect_l1b_product(workspace_name, l1b_path)
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_compare(cls, command_args):
        workspace_name_1, config_name_1 = _get_workspace_and_config_name(command_args)
        try:
            if not workspace_name_1:
                workspace_name_1 = ManageWorkspacesCommand.create_default_workspace()
            workspace_name_2 = command_args.workspace_name_2
            workspace_name_2 = workspace_name_2 if workspace_name_2 else workspace_name_1
            config_name_2 = command_args.config_name_2
            config_name_2 = config_name_2 if config_name_2 else config_name_1

            l1b_filename_1 = command_args.l1b_filename_1
            if os.path.dirname(l1b_filename_1):
                l1b_path_1 = os.path.abspath(l1b_filename_1)
            else:
                if not config_name_1:
                    raise CommandError(
                        'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
                l1b_path_1 = _WORKSPACE_MANAGER.get_outputs_path(workspace_name_1, config_name_1, l1b_filename_1)
            if not os.path.exists(l1b_path_1):
                raise CommandError('First L1B product not found: %s' % l1b_path_1)

            l1b_filename_2 = command_args.l1b_filename_2
            if os.path.dirname(l1b_filename_1):
                l1b_path_2 = os.path.abspath(l1b_filename_2)
            else:
                if not workspace_name_2:
                    raise CommandError('no current workspace, use option -w to name a WORKSPACE')
                if not config_name_2:
                    raise CommandError(
                        'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
                l1b_path_2 = _WORKSPACE_MANAGER.get_outputs_path(workspace_name_2, config_name_2, l1b_filename_2)
            if not os.path.exists(l1b_path_2):
                raise CommandError('Second L1B product not found: %s' % l1b_path_2)

            if os.path.samefile(l1b_path_1, l1b_path_2):
                print('warning: comparing "%s" with itself')

            _WORKSPACE_MANAGER.compare_l1b_products(workspace_name_1, l1b_path_1, l1b_path_2)
        except WorkspaceError as error:
            raise CommandError(error)

    @classmethod
    def execute_list(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            raise CommandError('no current workspace, use option -w to name a WORKSPACE')
        if not config_name:
            raise CommandError(
                'no current configuration, use "dedop config add CONFIG" or "dedop config cur CONFIG"')
        pattern = command_args.pattern
        output_names = _WORKSPACE_MANAGER.get_output_names(workspace_name, config_name, pattern=pattern)
        num_outputs = len(output_names)
        if num_outputs == 0:
            print('no outputs created with config "%s" in workspace "%s"' % (config_name, workspace_name))
        elif num_outputs == 1:
            print('1 output created with config "%s" in workspace "%s":' % (config_name, workspace_name))
        else:
            print('%d outputs created with config "%s" in workspace "%s":' % (num_outputs, config_name, workspace_name))
        for i in range(num_outputs):
            output_name = output_names[i]
            print('%3d: %s' % (i + 1, output_name))


class OpenNotebookCommand(Command):
    @classmethod
    def name(cls):
        return 'notebook'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Open a Jupyter Notebook for DeDop.'
        return dict(help=help_line, description=help_line)

    def execute(self, command_args):
        workspaces_dir = _WORKSPACE_MANAGER.workspaces_dir
        if not os.path.exists(workspaces_dir):
            try:
                os.makedirs(workspaces_dir)
            except (OSError, IOError) as error:
                raise CommandError(error)
        try:
            _WORKSPACE_MANAGER.launch_notebook('Notebook', workspaces_dir)
        except WorkspaceError as error:
            raise CommandError(error)


class ShowStatusCommand(Command):
    @classmethod
    def name(cls):
        return 'status'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Print DeDop status information.'
        return dict(aliases=['s'], help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument('-l', '--long', action='store_true',
                            help='show extended status information')

    def execute(self, command_args):
        # TODO (forman, 20160727): use command_args.long to print extended status info
        if command_args.long:
            print('warning: option "--long" not yet supported')
            # workspace_info = _WORKSPACE_MANAGER.get_workspace_info()
            # print(workspace_info.get_workspace_info_string())
        workspaces_dir = _WORKSPACE_MANAGER.workspaces_dir
        if os.path.exists(workspaces_dir):
            workspace_names = _WORKSPACE_MANAGER.get_workspace_names()
            if workspace_names:
                workspace_names = ', '.join(workspace_names)
            else:
                workspace_names = '(not set)'
            workspace = _WORKSPACE_MANAGER.get_current_workspace()
            cur_workspace_name = workspace.name
            if cur_workspace_name:
                cur_config_name = _WORKSPACE_MANAGER.get_current_config_name(cur_workspace_name)
                if not cur_config_name:
                    cur_config_name = '(not set)'
            else:
                cur_workspace_name = '(not set)'
                cur_config_name = '(not set)'
            try:
                workspaces_size = '%s MiB' % (_dir_size(workspaces_dir) >> 20)
            except (WorkspaceError, IOError, OSError) as error:
                workspaces_size = '(error: %s)' % str(error)
        else:
            workspaces_dir = '(not yet created)'
            workspaces_size = '(not yet created)'
            workspace_names = '(not yet created)'
            cur_workspace_name = '(not set)'
            cur_config_name = '(not set)'

        print('configuration location:     %s' % DEFAULT_CONFIG_FILE)
        print('workspaces location:        %s' % workspaces_dir)
        print('workspaces total size:      %s' % workspaces_size)
        print('workspace names:            %s' % workspace_names)
        print('current workspace:          %s' % cur_workspace_name)
        print('current DDP configuration:  %s' % cur_config_name)


class ShowCopyrightCommand(Command):
    @classmethod
    def name(cls):
        return 'copyright'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Print DeDop copyright information.'
        return dict(help=help_line, description=help_line)

    def execute(self, command_args):
        print(_LICENSE)


class ShowLicenseCommand(Command):
    @classmethod
    def name(cls):
        return 'license'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Print DeDop license information.'
        return dict(help=help_line, description=help_line)

    def execute(self, command_args):
        with open(_LICENSE_INFO_PATH) as fp:
            content = fp.read()
            print(content)


class ShowManualCommand(Command):
    @classmethod
    def name(cls):
        return 'man'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Open DeDop user manual in browser window.'
        return dict(help=help_line, description=help_line)

    def execute(self, command_args):
        import webbrowser
        webbrowser.open_new_tab(_DOCS_URL)


#: List of sub-commands supported by the CLI. Entries are classes derived from :py:class:`Command` class.
#: DeDop plugins may extend this list by their commands during plugin initialisation.


class ExitException(Exception):
    """Used in ``NoExitArgumentParser`` instead of exiting the current process."""

    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __str__(self):
        return '%s (%s)' % (self.message, self.status)


class NoExitArgumentParser(argparse.ArgumentParser):
    """
    Special ``argparse.ArgumentParser`` that never directly exits the current process.
    It raises an ``ExitException`` instead.
    """

    def __init__(self, *args, **kwargs):
        super(NoExitArgumentParser, self).__init__(*args, **kwargs)

    def exit(self, status=0, message=None):
        """Overrides the base class method in order to raise an ``ExitException``."""
        raise ExitException(status, message)


# def main(args=None, workspace_manager=None, processor_factory=None):
#     """
#     The entry point function of the DeDop command-line interface.
#
#     :param args: list of command-line arguments of type ``str``.
#     :param workspace_manager: optional :py:class:`WorkspaceManager` object.
#     :param processor_factory: optional function used to create the processor instance. Must have the
#         same signature as _py:func:`new_l1b_processor`.
#     :return: An integer exit code where zero means success
#     """
#
#     if args is None:
#         args = sys.argv[1:]
#
#     if not processor_factory:
#         processor_factory = get_config_value('processor_factory')
#
#     global _PROCESSOR_FACTORY
#     _PROCESSOR_FACTORY = processor_factory if processor_factory else new_l1b_processor
#
#     workspaces_dir = get_config_path('workspaces_dir')
#
#     global _WORKSPACE_MANAGER
#     _WORKSPACE_MANAGER = workspace_manager if workspace_manager else WorkspaceManager(workspaces_dir=workspaces_dir)
#
#     parser = NoExitArgumentParser(prog=CLI_NAME,
#                                   description='ESA DeDop Shell, version %s' % __version__)
#     parser.add_argument('--version', action='version', version=__version__)
#     parser.add_argument('-e', '--errors', dest='print_stack_trace', action='store_true',
#                         help='on error, print full Python stack trace')
#     parser.add_argument('--new-conf', dest='new_conf', action='store_true',
#                         help='write a new DeDop tools configuration file and exit')
#     subparsers = parser.add_subparsers(
#         dest='command_name',
#         metavar='COMMAND',
#         help='One of the following commands. Type "COMMAND -h" to get command-specific help.'
#     )
#
#     for command_class in COMMAND_REGISTRY:
#         command_name = command_class.name()
#         command_parser_kwargs = command_class.parser_kwargs()
#         command_parser = subparsers.add_parser(command_name, **command_parser_kwargs)
#         command_class.configure_parser(command_parser)
#         command_parser.set_defaults(command_class=command_class)
#
#     print_stack_trace = False
#     try:
#         args_obj = parser.parse_args(args)
#         print_stack_trace = args_obj.print_stack_trace
#
#         if args_obj.new_conf:
#             try:
#                 config_file = write_default_config_file()
#                 print('wrote new %s' % config_file)
#                 status, message = 0, None
#             except (IOError, OSError) as error:
#                 status, message = 1, str(error)
#         elif args_obj.command_name and args_obj.command_class:
#             assert args_obj.command_name and args_obj.command_class
#             status_and_message = args_obj.command_class().execute(args_obj)
#             if not status_and_message:
#                 status_and_message = Command.STATUS_OK
#             status, message = status_and_message
#         else:
#             parser.print_help()
#             status, message = 0, None
#     except ExitException as e:
#         status, message = e.status, e.message
#
#     if message:
#         if status:
#             sys.stderr.write("%s: %s\n" % (CLI_NAME, message))
#             if print_stack_trace:
#                 import traceback
#                 traceback.print_stack()
#         else:
#             sys.stdout.write("%s\n" % message)
#
#     return status

COMMAND_REGISTRY = [
    ManageWorkspacesCommand,
    ManageConfigsCommand,
    ManageInputsCommand,
    ManageOutputsCommand,
    RunProcessorCommand,
    ShowStatusCommand,
    OpenNotebookCommand,
    ShowManualCommand,
    ShowCopyrightCommand,
    ShowLicenseCommand,
]


# use by 'sphinxarg' to generate the documentation
def _make_dedop_parser():
    from cate.util.cli import _make_parser
    return _make_parser(CLI_NAME, CLI_DESCRIPTION, __version__, COMMAND_REGISTRY, license_text=_LICENSE,
                        docs_url=_DOCS_URL)


def main(args=None, workspace_manager=None, processor_factory=None) -> int:
    from dedop.model.processor import BaseProcessor
    from dedop.proc.sar import L1BProcessor
    from dedop.ui.workspace_manager import WorkspaceManager

    def new_l1b_processor(name: str,
                          cnf_file: str = None,
                          cst_file: str = None,
                          chd_file: str = None,
                          output_dir: str = '.',
                          skip_l1bs: bool = True) -> BaseProcessor:
        """
        Create a new L1B processor instance.

        :param name: the processor "run" name
        :param cnf_file: configuration definition file
        :param cst_file: constants definition file
        :param chd_file: characterisation definition file
        :param output_dir: the output directory for L1B, L1B-S, and log-files, etc.
        :param skip_l1bs: whether to skip L1B-S output
        :return: an object of type :py_class:`BaseProcessor`
        """
        return L1BProcessor(name, cnf_file, cst_file, chd_file, output_dir, skip_l1bs)

    if not processor_factory:
        processor_factory = get_config_value('processor_factory')

    global _PROCESSOR_FACTORY
    _PROCESSOR_FACTORY = processor_factory if processor_factory else new_l1b_processor

    workspaces_dir = get_config_path('workspaces_dir')

    global _WORKSPACE_MANAGER
    _WORKSPACE_MANAGER = workspace_manager if workspace_manager else WorkspaceManager(workspaces_dir=workspaces_dir)

    return run_main(CLI_NAME,
                    CLI_DESCRIPTION,
                    __version__,
                    COMMAND_REGISTRY,
                    license_text=_LICENSE,
                    docs_url=_DOCS_URL,
                    args=args)


if __name__ == '__main__':
    sys.exit(main())
