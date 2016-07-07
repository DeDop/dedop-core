"""
This module provides DeDop's command-line interface (CLI) API and the CLI executable.

To use the CLI executable, invoke the module file as a script, type ``python3 cli.py [ARGS] [OPTIONS]``. Type
`python3 cli.py --help`` for usage help.

The CLI operates on sub-commands. New sub-commands can be added by inheriting from the :py:class:`Command` class
and extending the ``Command.REGISTRY`` list of known command classes.
"""

import argparse
import os.path
import sys
from abc import ABCMeta, abstractmethod

from typing import Tuple, Optional

from dedop.cli.dummy_processor import Processor
from dedop.cli.workspace import WorkspaceManager, WorkspaceError
from dedop.util.monitor import ConsoleMonitor, Monitor
from dedop.version import __version__

_DEFAULT_CONFIG_NAME = 'default'
_DEFAULT_WORKSPACE_NAME = 'default'

_STATUS_NO_WORKSPACE = 10, 'no current workspace, use option -w to name a WORKSPACE'
_STATUS_NO_CONFIG = 20, 'no current configuration, use "dedop config cur CONFIG"'
_STATUS_NO_INPUTS = 30, 'workspace "%s" doesn\'t have any inputs yet, use "dedop input add *.nc" to add some'
_STATUS_NO_MATCHING_INPUTS = 40, 'no matching inputs found'
_STATUS_NO_MATCHING_OUTPUTS = 40, 'no matching outputs found'

#: Name of the DeDop CLI executable.
CLI_NAME = 'dedop'

_LICENSE_INFO_PATH = os.path.dirname(__file__) + '/../../LICENSE'
_USER_MANUAL_URL = 'http://dedop.readthedocs.io/en/latest/'
_COPYRIGHT_INFO = """
%s - The ESA DeDop CLI Tool, Copyright (C) 2016 by European Space Agency (ESA)

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Type "%s lic" for details.
""" % (CLI_NAME, CLI_NAME)

_WORKSPACE_MANAGER = None


def _input(prompt, default=None):
    answer = input(prompt).strip()
    return answer if answer else default


def _get_workspace_name(command_args):
    workspace_name = command_args.workspace_name
    if workspace_name:
        return workspace_name
    return _WORKSPACE_MANAGER.get_current_workspace_name()


def _get_workspace_and_config_name(command_args):
    workspace_name = command_args.workspace_name
    if not workspace_name:
        workspace_name = _WORKSPACE_MANAGER.get_current_workspace_name()
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


def _open_file(chd_file):
    try:
        os.startfile(chd_file)
    except AttributeError:
        import subprocess
        subprocess.call(['open', chd_file], shell=True)


class Command(metaclass=ABCMeta):
    """
    Represents (sub-)command for DeDop's command-line interface.
    If a plugin wishes to extend DeDop's CLI, it may append a new call derived from ``Command`` to the list
    ``COMMAND_REGISTRY``.
    """

    #: Success value to be returned by :py:meth:`execute`. Its value is ``(0, None)``.
    STATUS_OK = (0, None)

    @classmethod
    @abstractmethod
    def name(cls):
        """
        Return the command's unique name.
        :return: the command's unique name.
        """

    @classmethod
    @abstractmethod
    def parser_kwargs(cls):
        """
        Return the keyword arguments passed to a ``argparse.ArgumentParser(**parser_kwargs)`` call.

        For the possible keywords refer to
        https://docs.python.org/3.5/library/argparse.html#argparse.ArgumentParser.

        :return: Parser keyword arguments.
        """

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        """
        Configure *parser*, i.e. make any required ``parser.add_argument(*args, **kwargs)`` calls.
        See https://docs.python.org/3.5/library/argparse.html#argparse.ArgumentParser.add_argument

        :param parser: The command parser to configure.
        """
        pass

    @abstractmethod
    def execute(self, command_args: argparse.Namespace) -> Optional[Tuple[int, str]]:
        """
        Execute this command and return a tuple (*status*, *message*) where *status* is the CLI executable's
        exit code and *message* a text to be printed before the executable
        terminates. If *status* is zero, the message will be printed to ``sys.stdout``, otherwise to ``sys.stderr``.
        Implementors may can return ``STATUS_OK`` on success.

        The command's arguments in *command_args* are attributes namespace returned by
        ``argparse.ArgumentParser.parse_args()``.
        Also refer to to https://docs.python.org/3.5/library/argparse.html#argparse.ArgumentParser.parse_args


        :param command_args: The command's arguments.
        :return: `None`` (= status ok) or a tuple (*status*, *message*) of type (``int``, ``str``)
                 where *message* may be ``None``.
        """

    @classmethod
    def new_monitor(cls):
        return ConsoleMonitor(stay_in_line=True, progress_bar_size=32)


class RunProcessorCommand(Command):
    CMD_NAME = 'run'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Run the DeDop processor (DDP).'
        return dict(help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument('-s', '--skip-l1bs', action='store_true',
                            help='Skip generation of L1B-S files.')
        parser.add_argument('-q', '--quiet', action='store_true',
                            help='Suppress output of progress information.')
        parser.add_argument('-w', '--workspace', dest='workspace_name', metavar='WORKSPACE',
                            help='Use WORKSPACE, defaults to current workspace.')
        parser.add_argument('-c', '--config', dest='config_name', metavar='CONFIG',
                            help='Use CONFIG in workspace, defaults to current configuration.')
        parser.add_argument('-i', '--inputs', metavar='L1A_FILE', nargs='*',
                            help="L1A input files. Defaults to all L1A files in workspace.")
        parser.add_argument('-o', '--output', dest='output_dir', metavar='DIR',
                            help="Alternative output directory.")

    def execute(self, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            workspace_name = ManageWorkspacesCommand.create_workspace(_DEFAULT_WORKSPACE_NAME, exists_ok=True)
        if not config_name:
            config_name = ManageConfigsCommand.create_config(workspace_name, _DEFAULT_CONFIG_NAME, exist_ok=True)
        inputs = command_args.inputs if command_args.inputs else _WORKSPACE_MANAGER.get_input_paths(workspace_name)
        if not inputs:
            code, msg = _STATUS_NO_INPUTS
            return code, msg % workspace_name
        monitor = Monitor.NULL if command_args.quiet else self.new_monitor()
        output_dir = command_args.output_dir if command_args.output_dir else _WORKSPACE_MANAGER.get_output_dir(
            workspace_name, config_name)
        chd_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CHD')
        cnf_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CNF')
        cst_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CST')
        skip_l1bs = command_args.skip_l1bs

        # TODO (forman, 20160616): use real DDP here
        # -------------------------------------------------------
        processor = Processor(config_name=config_name,
                              chd_file=chd_file,
                              cnf_file=cnf_file,
                              cst_file=cst_file,
                              skip_l1bs=skip_l1bs,
                              output_dir=output_dir)
        status = processor.process_sources(monitor, *inputs)
        # -------------------------------------------------------
        return status


class ManageWorkspacesCommand(Command):
    @classmethod
    def name(cls):
        return 'workspace'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage DeDop workspaces.'
        return dict(aliases=['mw'], help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(help='DeDop workspace sub-commands')

        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")

        parser_add = subparsers.add_parser('add', help='Add new workspace')
        parser_add.add_argument(**workspace_name_attributes)
        parser_add.set_defaults(ws_command=cls.execute_add)

        parser_remove = subparsers.add_parser('remove', aliases=['rm'], help='Remove workspace')
        parser_remove.add_argument(nargs='?', **workspace_name_attributes)
        parser_remove.set_defaults(ws_command=cls.execute_remove)

        parser_copy = subparsers.add_parser('copy', aliases=['cp'], help='Copy workspace')
        parser_copy.add_argument(nargs='?', **workspace_name_attributes)
        parser_copy.add_argument('new_name', metavar='NEW_NAME', nargs='?', help='Name of the new workspace')
        parser_copy.set_defaults(ws_command=cls.execute_copy)

        parser_rename = subparsers.add_parser('rename', aliases=['rn'], help='Rename workspace')
        parser_rename.add_argument(nargs='?', **workspace_name_attributes)
        parser_rename.add_argument('new_name', metavar='NEW_NAME', help='New name of the workspace')
        parser_rename.set_defaults(ws_command=cls.execute_rename)

        parser_info = subparsers.add_parser('info', aliases=['i'], help='Show workspace')
        parser_info.add_argument(nargs='?', **workspace_name_attributes)
        parser_info.set_defaults(ws_command=cls.execute_info)

        parser_current = subparsers.add_parser('current', aliases=['cur'], help='Current workspace')
        parser_current.add_argument(nargs='?', **workspace_name_attributes)
        parser_current.set_defaults(ws_command=cls.execute_current)

        parser_list = subparsers.add_parser('list', aliases=['ls'], help='List workspaces')
        parser_list.set_defaults(ws_command=cls.execute_list)

    def execute(self, command_args):
        return command_args.ws_command(command_args)

    @classmethod
    def execute_add(cls, command_args):
        workspace_name = command_args.workspace_name
        try:
            cls.create_workspace(workspace_name, exists_ok=False)
            return cls.STATUS_OK
        except WorkspaceError as error:
            return 1, str(error)

    @classmethod
    def execute_remove(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return 1, 'no current workspace'
        answer = _input('delete workspace "%s"? [yes]' % workspace_name, 'yes')
        if answer.lower() == 'yes':
            try:
                _WORKSPACE_MANAGER.delete_workspace(workspace_name)
                print('deleted workspace "%s"' % workspace_name)
            except WorkspaceError as error:
                return 1, str(error)
        return cls.STATUS_OK

    @classmethod
    def execute_copy(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return 1, 'no current workspace'
        new_name = command_args.new_name
        # TODO (hans-permana, 20160707): ensure the new ws name is unique
        if not new_name:
            new_name = workspace_name + '_copy'
        try:
            _WORKSPACE_MANAGER.copy_workspace(workspace_name, new_name)
            print('copied workspace "%s" to "%s"' % (workspace_name, new_name))
        except WorkspaceError as error:
            return 1, str(error)
        return cls.STATUS_OK

    @classmethod
    def execute_rename(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return 1, 'no current workspace'
        new_name = command_args.new_name
        # TODO (hans-permana, 20160707): ensure the new ws name is unique
        try:
            _WORKSPACE_MANAGER.rename_workspace(workspace_name, new_name)
            print('renamed workspace "%s" to "%s"' % (workspace_name, new_name))
            if workspace_name == _WORKSPACE_MANAGER.get_current_workspace_name():
                cls.set_current_workspace(new_name)
        except WorkspaceError as error:
            return 1, str(error)
        return cls.STATUS_OK

    @classmethod
    def execute_current(cls, command_args):
        try:
            if command_args.workspace_name:
                cls.set_current_workspace(command_args.workspace_name)
            else:
                workspace_name = _WORKSPACE_MANAGER.get_current_workspace_name()
                if workspace_name:
                    print('current workspace is "%s"' % workspace_name)
                else:
                    print('no current workspace')
        except WorkspaceError as e:
            return 1, str(e)
        return cls.STATUS_OK

    @classmethod
    def execute_info(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        _WORKSPACE_MANAGER.print_workspace_info(workspace_name)
        return cls.STATUS_OK

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
        return cls.STATUS_OK

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
        _WORKSPACE_MANAGER.set_current_workspace_name(workspace_name)
        print('current workspace is "%s"' % workspace_name)


class ManageConfigsCommand(Command):
    @classmethod
    def name(cls):
        return 'config'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage DeDop configurations.'
        return dict(aliases=['mc'], help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")
        parser.add_argument('-w', '--workspace', **workspace_name_attributes)

        config_name_attributes = dict(dest='config_name', metavar='CONFIG', help="Name of the configuration")

        subparsers = parser.add_subparsers(help='DeDop configuration sub-commands')

        parser_add = subparsers.add_parser('add', help='Add new configuration')
        parser_add.add_argument(**config_name_attributes)
        parser_add.set_defaults(cf_command=cls.execute_add)

        parser_remove = subparsers.add_parser('remove', aliases=['rm'], help='Remove configuration')
        parser_remove.add_argument(nargs='?', **config_name_attributes)
        parser_remove.set_defaults(cf_command=cls.execute_remove)

        parser_edit = subparsers.add_parser('edit', aliases=['ed'], help='Edit configuration')
        parser_edit.add_argument(nargs='?', **config_name_attributes)
        parser_edit.set_defaults(cf_command=cls.execute_edit)

        parser_copy = subparsers.add_parser('copy', aliases=['cp'], help='Copy configuration')
        parser_copy.add_argument(nargs='?', **config_name_attributes)
        parser_copy.add_argument('new_name', metavar='NEW_NAME', nargs='?', help='Name of the new configuration')
        parser_copy.set_defaults(cf_command=cls.execute_copy)

        parser_rename = subparsers.add_parser('rename', aliases=['rn'], help='Rename configuration')
        parser_rename.add_argument(nargs='?', **config_name_attributes)
        parser_rename.add_argument('new_name', metavar='NEW_NAME', help='New name of the configuration')
        parser_rename.set_defaults(cf_command=cls.execute_rename)

        parser_info = subparsers.add_parser('info', aliases=['i'], help='Show configuration')
        parser_info.add_argument(nargs='?', **config_name_attributes)
        parser_info.set_defaults(cf_command=cls.execute_info)

        parser_current = subparsers.add_parser('current', aliases=['cur'], help='Current configuration')
        parser_current.add_argument(nargs='?', **config_name_attributes)
        parser_current.set_defaults(cf_command=cls.execute_current)

        parser_list = subparsers.add_parser('list', aliases=['ls'], help='List configurations')
        parser_list.set_defaults(cf_command=cls.execute_list)

    def execute(self, command_args):
        return command_args.cf_command(command_args)

    @classmethod
    def execute_add(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        try:
            cls.create_config(workspace_name, config_name, exist_ok=False)
        except WorkspaceError as error:
            return 1, str(error)

    @classmethod
    def execute_remove(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        answer = _input('delete configuration "%s"? [yes]' % config_name, 'yes')
        if answer.lower() == 'yes':
            try:
                _WORKSPACE_MANAGER.delete_config(workspace_name, config_name)
                print('deleted configuration "%s"' % config_name)
            except WorkspaceError as error:
                return 1, str(error)
        return cls.STATUS_OK

    @classmethod
    def execute_copy(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        new_name = command_args.new_name
        # TODO (hans-permana, 20160707): ensure the new config name is unique
        if not new_name:
            new_name = config_name + '_copy'
        try:
            _WORKSPACE_MANAGER.copy_config(workspace_name, config_name, new_name)
            print('copied configuration "%s" to "%s"' % (config_name, new_name))
        except WorkspaceError as error:
            return 1, str(error)
        return cls.STATUS_OK

    @classmethod
    def execute_rename(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        new_name = command_args.new_name
        # TODO (hans-permana, 20160707): ensure the new config name is unique
        try:
            _WORKSPACE_MANAGER.rename_config(workspace_name, config_name, new_name)
            print('renamed configuration "%s" to "%s"' % (config_name, new_name))
            if config_name == _WORKSPACE_MANAGER.get_current_config_name(workspace_name):
                cls.set_current_config(workspace_name, new_name)
        except WorkspaceError as error:
            return 1, str(error)
        return cls.STATUS_OK

    @classmethod
    def execute_edit(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            workspace_name = ManageWorkspacesCommand.create_workspace(_DEFAULT_WORKSPACE_NAME, exists_ok=True)
        if not config_name:
            config_name = cls.create_config(workspace_name, _DEFAULT_CONFIG_NAME, exist_ok=True)
        try:
            chd_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CHD')
            cnf_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CNF')
            cst_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CST')
            _open_file(chd_file)
            _open_file(cnf_file)
            _open_file(cst_file)
        except WorkspaceError as error:
            return 1, str(error)
        return cls.STATUS_OK

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
                    print('current configuration is "%s"' % config_name)
                else:
                    print('no current configuration')
        except WorkspaceError as e:
            return 1, str(e)
        return cls.STATUS_OK

    @classmethod
    def execute_info(cls, command_args):
        workspace_name, config_name = _get_workspace_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        # TODO (forman, 20180702): implement 'mc info' command
        #
        # Implementation here...
        #
        print('TODO: show configuration %s' % config_name)
        return cls.STATUS_OK

    @classmethod
    def execute_list(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        config_names = _WORKSPACE_MANAGER.get_config_names(workspace_name)
        num_configs = len(config_names)
        if num_configs == 0:
            print('no configurations in workspace "%s"' % workspace_name)
        elif num_configs == 1:
            print('1 configuration in workspace "%s":' % workspace_name)
        else:
            print('%d configurations in workspace "%s":' % (num_configs, workspace_name))
        for i in range(num_configs):
            config_name = config_names[i]
            print('%3d: %s' % (i + 1, config_name))
        return cls.STATUS_OK

    @classmethod
    def create_config(cls, workspace_name, config_name, exist_ok=True) -> str:
        """
        Create a new configuration *config_name* in workspace *workspace_name*.

        :param workspace_name: Workspace name
        :param config_name: Configuration name
        :param exist_ok: if True, *config_name* may already exist
        :return: *config_name*
        :raise: WorkspaceError
        """
        if not workspace_name:
            workspace_name = ManageWorkspacesCommand.create_workspace(_DEFAULT_WORKSPACE_NAME, exists_ok=True)
        if exist_ok and _WORKSPACE_MANAGER.config_exists(workspace_name, config_name):
            return config_name
        _WORKSPACE_MANAGER.create_config(workspace_name, config_name)
        print('created configuration "%s" in workspace "%s"' % (config_name, workspace_name))
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
        _WORKSPACE_MANAGER.set_current_config_name(workspace_name, config_name)
        print('current configuration is "%s"' % config_name)


class ManageInputsCommand(Command):
    CMD_NAME = 'input'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage L1A inputs.'
        return dict(aliases=['mi'], help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")
        parser.add_argument('-w', '--workspace', **workspace_name_attributes)

        subparsers = parser.add_subparsers(help='L1A inputs sub-commands')

        parser_add = subparsers.add_parser('add', help='Add new inputs')
        parser_add.add_argument('-q', '--quiet', action='store_true',
                                help='Suppress output of progress information.')
        parser_add.add_argument('inputs', metavar='L1A_FILE', nargs='+',
                                help="L1A input file to add to workspace.")
        parser_add.set_defaults(mi_command=cls.execute_add)

        parser_remove = subparsers.add_parser('remove', aliases=['rm'], help='Remove inputs')
        parser_remove.add_argument('-q', '--quiet', action='store_true',
                                   help='Suppress output of progress information.')
        parser_remove.add_argument('inputs', metavar='L1A_FILE', nargs='*',
                                   help="L1A input file to add to workspace.")
        parser_remove.set_defaults(mi_command=cls.execute_remove)

        parser_list = subparsers.add_parser('list', aliases=['ls'], help='List inputs')
        parser_list.add_argument('pattern', metavar='WC', nargs='?',
                                 help="Wildcard pattern.")
        parser_list.set_defaults(mi_command=cls.execute_list)

    def execute(self, command_args):
        return command_args.mi_command(command_args)

    @classmethod
    def execute_add(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        inputs = command_args.inputs
        if not inputs:
            inputs = [os.path.join('.', '*.nc')]
        inputs = _expand_wildcard_paths(inputs)
        if not inputs:
            return _STATUS_NO_MATCHING_INPUTS
        monitor = Monitor.NULL if command_args.quiet else cls.new_monitor()
        try:
            if not workspace_name:
                workspace_name = ManageWorkspacesCommand.create_workspace(_DEFAULT_WORKSPACE_NAME, exists_ok=True)
            _WORKSPACE_MANAGER.add_inputs(workspace_name, inputs, monitor)
            input_count = len(inputs)
            if input_count == 0:
                print('no inputs added')
            elif input_count == 1:
                print('one input added')
            else:
                print('added %s inputs' % input_count)
        except WorkspaceError as e:
            return 30, str(e)
        return cls.STATUS_OK

    @classmethod
    def execute_remove(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        input_names = command_args.inputs
        if not input_names:
            input_names = '*.nc'
        input_names = _WORKSPACE_MANAGER.get_input_names(workspace_name, pattern=input_names)
        if not input_names:
            return _STATUS_NO_MATCHING_INPUTS
        monitor = Monitor.NULL if command_args.quiet else cls.new_monitor()
        # TODO (hans-permana, 20160707): ask the user to confirm the deletion
        try:
            _WORKSPACE_MANAGER.remove_inputs(workspace_name, input_names, monitor)
            input_count = len(input_names)
            if input_count == 0:
                print('no inputs removed')
            elif input_count == 1:
                print('one input removed')
            else:
                print('removed %s inputs' % input_count)
        except WorkspaceError as e:
            return 30, str(e)
        return cls.STATUS_OK

    @classmethod
    def execute_list(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
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
        return cls.STATUS_OK


class ManageOutputsCommand(Command):
    CMD_NAME = 'output'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage L1B outputs.'
        return dict(aliases=['mo'], help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        # TODO (hans-permana, 20160707): make the general arguments visible in sub-command
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE',
                                         help="Name of the workspace.")
        parser.add_argument('-w', '--workspace', **workspace_name_attributes)

        config_name_attributes = dict(dest='config_name', metavar='CONFIG',
                                      help="Name of the configuration.")
        parser.add_argument('-c', '--config', **config_name_attributes)

        parser.set_defaults(mo_parser=parser)

        subparsers = parser.add_subparsers(help='L1B outputs sub-commands')

        parser_clean = subparsers.add_parser('clean', aliases=['cl'], help='Clean output')
        parser_clean.add_argument(nargs='?', **workspace_name_attributes)
        parser_clean.add_argument(nargs='?', **config_name_attributes)
        parser_clean.add_argument('outputs', metavar='L1B_FILE', nargs='*',
                                  help="L1B output file to be removed from workspace.")
        parser_clean.add_argument('-q', '--quiet', action='store_true',
                                  help='Suppress output of progress information.')
        parser_clean.set_defaults(mo_command=cls.execute_clean)

        parser_compare = subparsers.add_parser('compare', aliases=['cm'], help='Compare outputs')
        parser_compare.add_argument('other_config_name', metavar='OTHER', help='Another configuration')
        parser_compare.set_defaults(mo_command=cls.execute_compare)

        parser_analyse = subparsers.add_parser('analyse', aliases=['an'], help='Analyse output')
        parser_analyse.set_defaults(mo_command=cls.execute_analyse)

        parser_list = subparsers.add_parser('list', aliases=['ls'], help='List outputs')
        parser_list.add_argument('pattern', metavar='WC', nargs='?',
                                 help="Wildcard pattern.")
        parser_list.set_defaults(mo_command=cls.execute_list)

    def execute(self, command_args):
        if hasattr(command_args, 'mo_command') and command_args.mo_command:
            return command_args.mo_command(command_args)
        else:
            command_args.mo_parser.print_help()

    @classmethod
    def execute_clean(cls, command_args):
        # TODO (hans-permana, 20160707): modify the behaviour to clean everything in the output dir
        # TODO (hans-permana, 20160707): ask the user to confirm the deletion
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        output_names = command_args.outputs
        if not output_names:
            output_names = '*.nc'
        output_names = _WORKSPACE_MANAGER.get_output_names(workspace_name, config_name, pattern=output_names)
        if not output_names:
            return _STATUS_NO_MATCHING_OUTPUTS
        monitor = Monitor.NULL if command_args.quiet else cls.new_monitor()
        try:
            _WORKSPACE_MANAGER.remove_outputs(workspace_name, config_name, output_names, monitor)
            output_count = len(output_names)
            if output_count == 0:
                print('no outputs removed')
            elif output_count == 1:
                print('one output removed')
            else:
                print('removed %s outputs' % output_count)
        except WorkspaceError as e:
            return 30, str(e)
        return cls.STATUS_OK

    @classmethod
    def execute_compare(cls, command_args):
        workspace_name, config_name_1 = _get_workspace_and_config_name(command_args)
        if not config_name_1:
            config_name_1 = _WORKSPACE_MANAGER.get_current_config_name(workspace_name)
            if not config_name_1:
                return _STATUS_NO_CONFIG
        config_name_2 = command_args.other_config_name
        if not _WORKSPACE_MANAGER.config_exists(workspace_name, config_name_1):
            return 50, 'workspace "%s" doesn\'t contain a configuration "%s"' % (workspace_name, config_name_1)
        if not _WORKSPACE_MANAGER.config_exists(workspace_name, config_name_2):
            return 50, 'workspace "%s" doesn\'t contain a configuration "%s"' % (workspace_name, config_name_2)
        # TODO (forman, 20160704): implement "mo compare" command
        #
        # Implementation here...
        #
        print('TODO: comparing output of "%s" and "%s"' % (config_name_1, config_name_2))
        return cls.STATUS_OK

    @classmethod
    def execute_analyse(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        # TODO (forman, 20160704): implement "mo analyse" command
        #
        # Implementation here...
        #
        print('TODO: analysing output of "%s"' % config_name)
        return cls.STATUS_OK

    @classmethod
    def execute_list(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
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
        return cls.STATUS_OK


class ShowCopyrightCommand(Command):
    @classmethod
    def name(cls):
        return 'cr'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Print copyright information.'
        return dict(help=help_line, description=help_line)

    def execute(self, command_args):
        print(_COPYRIGHT_INFO)
        return self.STATUS_OK


class ShowLicenseCommand(Command):
    @classmethod
    def name(cls):
        return 'lic'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Print license information.'
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
        webbrowser.open_new_tab(_USER_MANUAL_URL)
        return self.STATUS_OK


#: List of sub-commands supported by the CLI. Entries are classes derived from :py:class:`Command` class.
#: DeDop plugins may extend this list by their commands during plugin initialisation.
COMMAND_REGISTRY = [
    RunProcessorCommand,
    ManageWorkspacesCommand,
    ManageConfigsCommand,
    ManageInputsCommand,
    ManageOutputsCommand,
    ShowManualCommand,
    ShowCopyrightCommand,
    ShowLicenseCommand,
]


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


def main(args=None, workspace_manager=None):
    """
    The entry point function of the DeDop command-line interface.

    :param args: list of command-line arguments of type ``str``.
    :param workspace_manager: optional :py:class:`WorkspaceManager` object.
    :return: An integer exit code where zero means success
    """

    global _WORKSPACE_MANAGER
    _WORKSPACE_MANAGER = workspace_manager if workspace_manager else WorkspaceManager()

    if args is None:
        args = sys.argv[1:]

    parser = NoExitArgumentParser(prog=CLI_NAME,
                                  description='ESA DeDop command-line interface, version %s' % __version__)
    parser.add_argument('--version', action='version', version='%s %s' % (CLI_NAME, __version__))
    parser.add_argument('-e', '--errors', dest='print_stack_trace', action='store_true',
                        help='on error, print full Python stack trace')
    subparsers = parser.add_subparsers(
        dest='command_name',
        metavar='COMMAND',
        help='One of the following commands. Type "COMMAND -h" to get command-specific help.'
    )

    for command_class in COMMAND_REGISTRY:
        command_name = command_class.name()
        command_parser_kwargs = command_class.parser_kwargs()
        command_parser = subparsers.add_parser(command_name, **command_parser_kwargs)
        command_class.configure_parser(command_parser)
        command_parser.set_defaults(command_class=command_class)

    print_stack_trace = False
    try:
        args_obj = parser.parse_args(args)
        print_stack_trace = args_obj.print_stack_trace

        if args_obj.command_name and args_obj.command_class:
            assert args_obj.command_name and args_obj.command_class
            status_and_message = args_obj.command_class().execute(args_obj)
            if not status_and_message:
                status_and_message = Command.STATUS_OK
            status, message = status_and_message
        else:
            parser.print_help()
            status, message = 0, None
    except ExitException as e:
        status, message = e.status, e.message

    if message:
        if status:
            sys.stderr.write("%s: %s\n" % (CLI_NAME, message))
            if print_stack_trace:
                import traceback
                traceback.print_stack()
        else:
            sys.stdout.write("%s\n" % message)

    return status


if __name__ == '__main__':
    sys.exit(main())
