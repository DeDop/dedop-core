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

_STATUS_NO_WORKSPACE = 10, 'no current workspace, use option -w to name a WORKSPACE'
_STATUS_NO_CONFIG = 20, 'no current configuration, use "dedop config cur CONFIG"'
_STATUS_NO_INPUTS = 30, 'workspace "%s" doesn\'t have any inputs yet, use "dedop input add *.nc" to add some'

#: Name of the DeDop CLI executable.
CLI_NAME = 'dedop'

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

_LICENSE_INFO_PATH = os.path.dirname(__file__) + '/../../LICENSE'

_DOCS_URL = 'http://dedop.readthedocs.data/en/latest/'

_WORKSPACE_MANAGER = WorkspaceManager()


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
    if not config_name:
        config_name = _WORKSPACE_MANAGER.get_current_config_name(workspace_name)
    return workspace_name, config_name


def _expand_wildcard_paths(inputs):
    expanded_inputs = []
    import glob
    for input in inputs:
        # TODO (forman, 20160704): 'recursive' is Python 3.5, add support for Python 3.x
        expanded_inputs.extend(glob.glob(input, recursive=True))
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


# TODO (forman, 20180702): WorkspaceCommand: catch WorkspaceError from all WorkspaceManager calls


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
        subparsers = parser.add_subparsers(help='Workspace sub-commands')

        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")

        parser_new = subparsers.add_parser('new', help='Create new workspace')
        parser_new.add_argument(**workspace_name_attributes)
        parser_new.set_defaults(ws_command=cls.execute_new)

        parser_del = subparsers.add_parser('del', help='Delete workspace')
        parser_del.add_argument(nargs='?', **workspace_name_attributes)
        parser_del.set_defaults(ws_command=cls.execute_del)

        parser_cp = subparsers.add_parser('cp', help='Copy workspace')
        parser_cp.add_argument(nargs='?', **workspace_name_attributes)
        parser_cp.add_argument('new_name', metavar='NEW_NAME', nargs='?', help='Name of the new workspace')
        parser_cp.set_defaults(ws_command=cls.execute_cp)

        parser_rn = subparsers.add_parser('rn', help='Rename workspace')
        parser_rn.add_argument(nargs='?', **workspace_name_attributes)
        parser_rn.add_argument('new_name', metavar='NEW_NAME', help='New name of the workspace')
        parser_rn.set_defaults(ws_command=cls.execute_rn)

        parser_inf = subparsers.add_parser('inf', help='Show workspace')
        parser_inf.add_argument(nargs='?', **workspace_name_attributes)
        parser_inf.set_defaults(ws_command=cls.execute_inf)

        parser_cur = subparsers.add_parser('cur', help='Current workspace')
        parser_cur.add_argument(nargs='?', **workspace_name_attributes)
        parser_cur.set_defaults(ws_command=cls.execute_cur)

        parser_ls = subparsers.add_parser('ls', help='List workspaces')
        parser_ls.set_defaults(ws_command=cls.execute_ls)

    def execute(self, command_args):
        return command_args.ws_command(command_args)

    @classmethod
    def execute_new(cls, command_args):
        workspace_name = command_args.workspace_name
        try:
            _WORKSPACE_MANAGER.create_workspace(workspace_name)
            _WORKSPACE_MANAGER.set_current_workspace_name(workspace_name)
            print('created workspace "%s"' % workspace_name)
        except WorkspaceError as error:
            return 1, str(error)

    @classmethod
    def execute_del(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return 1, 'no current workspace'
        try:
            answer = _input('delete workspace "%s"? [yes]' % workspace_name, 'yes')
            if answer.lower() == 'yes':
                _WORKSPACE_MANAGER.delete_workspace(workspace_name)
                print('deleted workspace "%s"' % workspace_name)
        except WorkspaceError as error:
            return 1, str(error)

    @classmethod
    def execute_cp(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return 1, 'no current workspace'
        new_name = command_args.new_name
        if not new_name:
            new_name = workspace_name + '_copy'
        # while os.path.exists(..., new_name) ...
        # TODO (forman, 20180702): implement 'ws cp' command, use shutils
        print('TODO: copy workspace "%s" to "%s"' % (workspace_name, new_name))

    @classmethod
    def execute_rn(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            return 1, 'no current workspace'
        new_name = command_args.new_name
        # TODO (forman, 20180702): implement 'ws rn' command
        print('TODO: rename workspace "%s" to "%s"' % (workspace_name, new_name))

    @classmethod
    def execute_cur(cls, command_args):
        try:
            if command_args.workspace_name:
                _WORKSPACE_MANAGER.set_current_workspace_name(command_args.workspace_name)
            workspace_name = _WORKSPACE_MANAGER.get_current_workspace_name()
            if workspace_name:
                print('current workspace:', workspace_name)
            else:
                print('no current workspace')
        except WorkspaceError as e:
            return 1, str(e)

    @classmethod
    def execute_inf(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        # TODO (forman, 20180702): implement 'ws inf' command
        print('TODO: show workspace %s' % workspace_name)

    @classmethod
    def execute_ls(cls, command_args):
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
            print('%3d - %s' % (i + 1, workspace_name))


# TODO (forman, 20180702): ConfigCommand: catch WorkspaceError from all WorkspaceManager calls


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

        subparsers = parser.add_subparsers(help='Configuration sub-commands')

        parser_new = subparsers.add_parser('new', help='Create new configuration')
        parser_new.add_argument(**config_name_attributes)
        parser_new.set_defaults(cf_command=cls.execute_new)

        parser_del = subparsers.add_parser('del', help='Delete configuration')
        parser_del.add_argument(nargs='?', **config_name_attributes)
        parser_del.set_defaults(cf_command=cls.execute_del)

        parser_del = subparsers.add_parser('edt', help='Edit configuration')
        parser_del.add_argument(nargs='?', **config_name_attributes)
        parser_del.set_defaults(cf_command=cls.execute_edt)

        parser_cp = subparsers.add_parser('cp', help='Copy configuration')
        parser_cp.add_argument(nargs='?', **workspace_name_attributes)
        parser_cp.add_argument('new_name', metavar='NEW_NAME', nargs='?', help='Name of the new configuration')
        parser_cp.set_defaults(cf_command=cls.execute_cp)

        parser_rn = subparsers.add_parser('rn', help='Rename configuration')
        parser_rn.add_argument(nargs='?', **workspace_name_attributes)
        parser_rn.add_argument('new_name', metavar='NEW_NAME', help='New name of the configuration')
        parser_rn.set_defaults(cf_command=cls.execute_rn)

        parser_inf = subparsers.add_parser('inf', help='Show configuration')
        parser_inf.add_argument(nargs='?', **config_name_attributes)
        parser_inf.set_defaults(cf_command=cls.execute_inf)

        parser_cur = subparsers.add_parser('cur', help='Current configuration')
        parser_cur.add_argument(nargs='?', **config_name_attributes)
        parser_cur.set_defaults(cf_command=cls.execute_cur)

        parser_ls = subparsers.add_parser('ls', help='List configurations')
        parser_ls.set_defaults(cf_command=cls.execute_ls)

    def execute(self, command_args):
        return command_args.cf_command(command_args)

    @classmethod
    def execute_new(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            # TODO (forman, 20160704): create workspace 'default' and make it current
            return _STATUS_NO_WORKSPACE
        try:
            # if command_args.force and not _WORKSPACE_MANAGER.workspace_exists(workspace_name):
            #    _WORKSPACE_MANAGER.create_workspace(workspace_name)
            #    _WORKSPACE_MANAGER.set_current_workspace_name(workspace_name)
            #    print('created workspace "%s"' % workspace_name)
            _WORKSPACE_MANAGER.create_config(workspace_name, config_name)
            _WORKSPACE_MANAGER.set_current_config_name(workspace_name, config_name)
            print('created configuration "%s" in workspace "%s"' % (config_name, workspace_name))
        except WorkspaceError as error:
            return 1, str(error)

    @classmethod
    def execute_del(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        try:
            answer = _input('delete configuration "%s"? [yes]' % config_name, 'yes')
            if answer.lower() == 'yes':
                _WORKSPACE_MANAGER.delete_config(workspace_name, config_name)
                print('deleted configuration "%s"' % config_name)
        except WorkspaceError as error:
            return 1, str(error)

    @classmethod
    def execute_cp(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        new_name = command_args.new_name
        if not new_name:
            new_name = workspace_name + '_copy'
        # while os.path.exists(..., new_name) ...
        # TODO (forman, 20180702): implement 'cf cp' command
        print('TODO: copy configuration "%s" to "%s"' % (workspace_name, new_name))

    @classmethod
    def execute_rn(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        new_name = command_args.new_name
        # TODO (forman, 20180702): implement 'cf rn' command
        print('TODO: rename configuration "%s" to "%s"' % (workspace_name, new_name))

    @classmethod
    def execute_edt(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        try:
            chd_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CHD')
            cnf_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CNF')
            cst_file = _WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CST')
            _open_file(chd_file)
            _open_file(cnf_file)
            _open_file(cst_file)
        except WorkspaceError as error:
            return 1, str(error)

    @classmethod
    def execute_cur(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        try:
            if config_name:
                _WORKSPACE_MANAGER.set_current_config_name(workspace_name, config_name)
            config_name = _WORKSPACE_MANAGER.get_current_config_name(workspace_name)
            if config_name:
                print('current configuration in workspace "%s" is "%s"' % (workspace_name, config_name))
            else:
                print('no current configuration in workspace "%s"' % workspace_name)
        except WorkspaceError as e:
            return 1, str(e)

    @classmethod
    def execute_inf(cls, command_args):
        workspace_name, config_name = _get_workspace_and_config_name(command_args)
        if not workspace_name:
            return _STATUS_NO_WORKSPACE
        if not config_name:
            return _STATUS_NO_CONFIG
        # TODO (forman, 20180702): implement 'cf inf' command
        print('TODO: show configuration %s' % config_name)

    @classmethod
    def execute_ls(cls, command_args):
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
            print('%3d - %s' % (i + 1, config_name))


class ManageInputsCommand(Command):
    CMD_NAME = 'input'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage L1A input files.'
        return dict(aliases=['mi'], help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        workspace_name_attributes = dict(dest='workspace_name', metavar='WORKSPACE', help="Name of the workspace")
        parser.add_argument('-w', '--workspace', **workspace_name_attributes)

        subparsers = parser.add_subparsers(help='Input sub-commands')

        parser_add = subparsers.add_parser('add', help='Add new inputs')
        parser_add.add_argument('-q', '--quiet', action='store_true',
                                help='Suppress output of progress information.')
        parser_add.add_argument('inputs', metavar='L1A_FILE', nargs='*',
                                help="L1A input file to add to workspace.")
        parser_add.set_defaults(mi_command=cls.execute_add)

    def execute(self, command_args):
        return command_args.mi_command(command_args)

    @classmethod
    def execute_add(cls, command_args):
        workspace_name = _get_workspace_name(command_args)
        if not workspace_name:
            # TODO (forman, 20160704): create workspace 'default' and make it current
            return _STATUS_NO_WORKSPACE
        monitor = Monitor.NULL if command_args.quiet else ConsoleMonitor()
        inputs = _expand_wildcard_paths(command_args.inputs)
        print('inputs:', inputs)
        _WORKSPACE_MANAGER.add_inputs(workspace_name, inputs, monitor)
        input_count = len(inputs)
        if input_count == 0:
            print('no inputs added')
        elif input_count == 1:
            print('one input added')
        else:
            print('added %s inputs' % input_count)
        return cls.STATUS_OK


class RunCommand(Command):
    CMD_NAME = 'run'

    @classmethod
    def name(cls):
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Run the DeDop processor with given configuration.'
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
            # TODO (forman, 20160704): create workspace 'default' and make it current
            return _STATUS_NO_WORKSPACE
        if not config_name:
            # TODO (forman, 20160704): create configuration 'default' and make it current
            return _STATUS_NO_CONFIG
        inputs = command_args.inputs if command_args.inputs else _WORKSPACE_MANAGER.get_input_paths(workspace_name)
        if not inputs:
            code, msg = _STATUS_NO_INPUTS
            return code, msg % workspace_name
        output_dir = command_args.output_dir if command_args.output_dir else _WORKSPACE_MANAGER.get_output_dir(
            workspace_name, config_name)
        processor = Processor(config_name=config_name,
                              chd_file=_WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CHD'),
                              cnf_file=_WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CNF'),
                              cst_file=_WORKSPACE_MANAGER.get_config_file(workspace_name, config_name, 'CST'),
                              skip_l1bs=command_args.skip_l1bs,
                              output_dir=output_dir)
        status = processor.process_sources(Monitor.NULL if command_args.quiet else ConsoleMonitor(),
                                           *inputs)
        return status


class PlotCommand(Command):
    @classmethod
    def name(cls):
        return 'plot'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Provide plotting for processing result analysis.'
        return dict(help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser):
        pass

    def execute(self, command_args):
        # TODO (forman, 20160616) - PlotCommand: implement execute
        return self.STATUS_OK


class CompareCommand(Command):
    @classmethod
    def name(cls):
        return 'cmp'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Compare results of two processor runs.'
        return dict(help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser):
        # TODO (forman, 20160616) - CompareCommand: implement configure_parser
        pass

    def execute(self, command_args):
        # TODO (forman, 20160616) - CompareCommand: implement execute
        return self.STATUS_OK


class CopyrightCommand(Command):
    @classmethod
    def name(cls):
        return 'cr'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Print copyright information.'
        return dict(help=help_line, description=help_line)

    def execute(self, command_args):
        print(_COPYRIGHT_INFO)


class LicenseCommand(Command):
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


class DocCommand(Command):
    @classmethod
    def name(cls):
        return 'doc'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Display documentation in a browser window.'
        return dict(help=help_line, description=help_line)

    def execute(self, command_args):
        import webbrowser
        webbrowser.open_new_tab(_DOCS_URL)


#: List of sub-commands supported by the CLI. Entries are classes derived from :py:class:`Command` class.
#: DeDop plugins may extend this list by their commands during plugin initialisation.
COMMAND_REGISTRY = [
    ManageWorkspacesCommand,
    ManageConfigsCommand,
    ManageInputsCommand,
    RunCommand,
    PlotCommand,
    CompareCommand,
    CopyrightCommand,
    LicenseCommand,
    DocCommand,
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
    The CLI's entry point function.

    :param args: list of command-line arguments of type ``str``.
    :return: A tuple (*status*, *message*)
    """

    global _WORKSPACE_MANAGER
    _WORKSPACE_MANAGER = workspace_manager if workspace_manager else  WorkspaceManager()

    if args is None:
        args = sys.argv[1:]

    parser = NoExitArgumentParser(prog=CLI_NAME,
                                  description='ESA DeDop command-line interface, version %s' % __version__)
    parser.add_argument('--version', action='version', version='%s %s' % (CLI_NAME, __version__))
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

    try:
        args_obj = parser.parse_args(args)

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
        else:
            sys.stdout.write("%s\n" % message)

    return status


if __name__ == '__main__':
    sys.exit(main())
