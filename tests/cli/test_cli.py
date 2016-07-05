import os.path
from unittest import TestCase

from dedop import cli
from dedop.util.fetchstd import fetch_std_streams
from tests.cli.test_workspace import WorkspaceTestBase

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')
WORKSPACES_DIR = os.path.join(TEST_DATA_DIR, 'test_cli')


class CliTest(WorkspaceTestBase, TestCase):
    def _test_main(self, args, expected_exit_code=0, expected_stdout=None, expected_stderr=None):
        with fetch_std_streams() as (stdout, stderr):
            exit_code = cli.main(args=args, workspace_manager=self.manager)
            self.assertEqual(exit_code, expected_exit_code)
        self._test_iobuf('stdout', stdout, expected_stdout)
        self._test_iobuf('stderr', stderr, expected_stderr)

    def _test_iobuf(self, name, iobuf, expected_text):
        message = 'actual %s was:\n%s\n%s\n%s\n' % (name, 120 * '-', iobuf.getvalue(), 120 * '-')
        if expected_text == '':
            self.assertEqual(iobuf.getvalue(), '', msg=message)
        elif isinstance(expected_text, str):
            self.assertIn(expected_text, iobuf.getvalue(), msg=message)
        elif expected_text:
            for expected_stdout_part in expected_text:
                self.assertIn(expected_stdout_part, iobuf.getvalue(), msg=message)

    def test_option_help(self):
        self._test_main(['--help'], expected_stdout='usage: dedop [-h]')
        self._test_main(['-h'], expected_stdout='usage: dedop [-h]')

    def test_option_version(self):
        self._test_main(['--version'], expected_stdout='dedop 0.1.0')

    def test_command_none(self):
        self._test_main([], expected_stdout='usage: dedop [-h]')

    def test_command_invalid(self):
        self._test_main(['pipo'], expected_exit_code=2, expected_stderr="invalid choice: 'pipo'")

    def test_command_license_command(self):
        self._test_main(['lic'], expected_stdout='GNU GENERAL PUBLIC LICENSE')

    def test_command_copyright(self):
        self._test_main(['cr'], expected_stdout='European Space Agency')

    def test_command_run_option_help(self):
        self._test_main(['run', '-h'], expected_stdout='usage:')

    def test_command_run(self):
        input_files = os.path.join(os.path.dirname(__file__), '*.nc')
        self._test_main(['mw', 'add', 'tests'],
                        expected_stdout=['created workspace "tests"',
                                         'current workspace is "tests"'])
        self._test_main(['mc', 'add', 'test-a'],
                        expected_stdout=['created configuration "test-a"',
                                         'current configuration is "test-a"'])
        self._test_main(['mi', 'add', input_files],
                        expected_stdout='added 2 inputs')
        self._test_main(['run'],
                        expected_stdout='Running DDP')

    def test_command_mw(self):
        self._test_main(['mw', 'add', 'tests'],
                        expected_stdout=['created workspace "tests"',
                                         'current workspace is "tests"'])
        self._test_main(['mw', 'cp', 'tests'],
                        expected_stdout=['workspace "tests" has been copied as "tests_copy"'])

        self._test_main(['mw', 'cp', 'tests', 'tests2'],
                        expected_stdout=['workspace "tests" has been copied as "tests2"'])

    def test_command_run_no_inputs(self):
        self._test_main(['run'],
                        expected_exit_code=30,
                        expected_stdout=['created workspace "default"',
                                         'created configuration "default" in workspace "default"'],
                        expected_stderr=['workspace "default" doesn\'t have any inputs yet'])

    def test_command_run_current(self):
        input_files = os.path.join(os.path.dirname(__file__), '*.nc')
        self._test_main(['mi', 'add', input_files],
                        expected_stdout=['created workspace "default"',
                                         'current workspace is "default"',
                                         'added 2 inputs'])
        self._test_main(['run'],
                        expected_stdout=['created configuration "default"',
                                         'current configuration is "default"',
                                         'Running DDP'])
