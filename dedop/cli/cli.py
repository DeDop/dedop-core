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

from dedop.util.monitor import ConsoleMonitor, Monitor
from dedop.version import __version__

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

Type "%s license" for details.
""" % (CLI_NAME, CLI_NAME)

_LICENSE_INFO_PATH = os.path.dirname(__file__) + '/../../LICENSE'

_DOCS_URL = 'http://dedop.readthedocs.io/en/latest/'


class Command(metaclass=ABCMeta):
    """
    Represents (sub-)command for DeDop's command-line interface.
    If a plugin wishes to extend DeDop's CLI, it may append a new call derived from ``Command`` to the list
    ``REGISTRY``.
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
    def configure_parser(cls, parser):
        parser.add_argument('--name', '-n', metavar='NAME', nargs=1,
                            help='Give the processor run a name.')
        parser.add_argument('--config', '-c', metavar='CONFIG', nargs=1, default='default',
                            help='Use the given configuration.')
        parser.add_argument('--monitor', '-m', action='store_true',
                            help='Display progress information while processing.')
        parser.add_argument('l1a_sources', metavar='L1A_SOURCE', nargs='+',
                            help="L1A input files or directories")

    def execute(self, command_args):
        config = command_args.config
        name = command_args.name
        monitor = command_args.monitor
        l1a_sources = command_args.l1a_sources

        if monitor:
            monitor = ConsoleMonitor()
        else:
            monitor = Monitor.NULL

        # todo (nf, 20160616) - implement me
        return self.STATUS_OK


class ConfigCommand(Command):
    @classmethod
    def name(cls):
        return 'conf'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Configuration sub-commands.'
        return dict(help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser):
        # todo (nf, 20160616) - implement me
        pass

    def execute(self, command_args):
        # todo (nf, 20160616) - implement me
        return self.STATUS_OK


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
        # todo (nf, 20160616) - implement me
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
        # todo (nf, 20160616) - implement me
        pass

    def execute(self, command_args):
        # todo (nf, 20160616) - implement me
        return self.STATUS_OK


class WorkspaceCommand(Command):
    @classmethod
    def name(cls):
        return 'ws'

    @classmethod
    def parser_kwargs(cls):
        help_line = 'Manage workspaces.'
        return dict(help=help_line, description=help_line)

    @classmethod
    def configure_parser(cls, parser):
        pass

    def execute(self, command_args):
        pass


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


class DocsCommands(Command):
    @classmethod
    def name(cls):
        return 'docs'

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
    RunCommand,
    WorkspaceCommand,
    ConfigCommand,
    PlotCommand,
    CompareCommand,
    CopyrightCommand,
    LicenseCommand,
    DocsCommands,
]


# todo (nf, 20160616) - cli.main() should never exit the interpreter, configure argparse parser accordingly

def main(args=None):
    """
    The CLI's entry point function.

    :param args: list of command-line arguments of type ``str``.
    :return: A tuple (*status*, *message*)
    """

    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog=CLI_NAME,
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

    if message:
        if status:
            sys.stderr.write("%s: %s\n" % (CLI_NAME, message))
        else:
            sys.stdout.write("%s\n" % message)

    return status


if __name__ == '__main__':
    sys.exit(main())
