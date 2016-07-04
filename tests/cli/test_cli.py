import os.path
import sys
from contextlib import contextmanager
from io import StringIO

from dedop import cli
from tests.cli.test_workspace import WorkspaceTest

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')
WORKSPACES_DIR = os.path.join(TEST_DATA_DIR, 'test_cli')


@contextmanager
def fetch_std_streams():
    sys.stdout.flush()
    sys.stderr.flush()

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout.flush()
        sys.stderr.flush()

        sys.stdout = old_stdout
        sys.stderr = old_stderr


class CliTest(WorkspaceTest):

    def _test_main(self, args, expected_exit_code=0, expected_stdout='', expected_stderr=''):
        with fetch_std_streams() as (stdout, stderr):
            exit_code = cli.main(args=args, workspace_manager=self.manager)
            self.assertEqual(exit_code, expected_exit_code)

        if expected_stdout:
            self.assertIn(expected_stdout, stdout.getvalue(), msg='actual stdout was:\n[%s]\n' % stdout.getvalue())
        else:
            self.assertEqual(stdout.getvalue(), '')

        if expected_stderr:
            self.assertIn(expected_stderr, stderr.getvalue(), msg='actual stderr was:\n[%s]\n' % stdout.getvalue())
        else:
            self.assertEqual(stderr.getvalue(), '')

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

    def test_command_run_current(self):
        inputs = os.path.join(os.path.dirname(__file__), '*.nc')
        self._test_main(['mw', 'new', 'tests'], expected_stdout='created workspace "tests"')
        self._test_main(['mc', 'new', 'test-a'], expected_stdout='created configuration "test-a"')
        self._test_main(['mi', 'add', inputs], expected_stdout='added 2 inputs')
        self._test_main(['run'], expected_stdout='Running DDP')
