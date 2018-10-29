import os.path
from unittest import TestCase

from dedop.cli import main
from dedop.model.processor import BaseProcessor, DummyProcessor
from dedop.util.fetchstd import fetch_std_streams
from tests.cli.test_workspace import WorkspaceTestBase

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')
WORKSPACES_DIR = os.path.join(TEST_DATA_DIR, 'test_cli')


def processor_factory(name=None,
                      chd_file=None,
                      cnf_file=None,
                      cst_file=None,
                      skip_l1bs=False,
                      output_dir=None) -> BaseProcessor:
    """
    Create a new dummy processor instance.

    :param name: the processor "run" name
    :param cnf_file: configuration definition file
    :param cst_file: constants definition file
    :param chd_file: characterisation definition file
    :param skip_l1bs: whether to skip L1B-S output
    :param output_dir: the output directory for L1B, L1B-S, and log-files, etc.
    :return: an object of type :py_class:`BaseProcessor`
    """
    return DummyProcessor(name, cnf_file, cst_file, chd_file, output_dir, skip_l1bs)


class CliTest(WorkspaceTestBase, TestCase):
    def _test_main(self, args, expected_exit_code=0, expected_stdout=None, expected_stderr=None):
        with fetch_std_streams() as (stdout, stderr):
            exit_code = main.main(args=args, workspace_manager=self.manager, processor_factory=processor_factory)
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
        self._test_main(['--version'], expected_stdout='1.5.1.dev1')

    # TODO(hans-permana, 20170217): try to investigate why no output is shown in the case of error
    # def test_command_none(self):
    #     self._test_main([], expected_exit_code=2, expected_stdout='usage: dedop [-h]')

    def test_command_invalid(self):
        self._test_main(['pipo'], expected_exit_code=2, expected_stderr="invalid choice: 'pipo'")

    def test_command_license_command(self):
        self._test_main(['license'], expected_stdout='GNU GENERAL PUBLIC LICENSE')

    def test_command_copyright(self):
        self._test_main(['copyright'], expected_stdout='European Space Agency')

    def test_command_workspace(self):
        self._test_main(['w', 'add', 'tests'],
                        expected_stdout=['created workspace "tests"',
                                         'current workspace is "tests"'])
        self._test_main(['w', 'cp', 'tests'],
                        expected_stdout=['copied workspace "tests" to "tests_1"'])

        self._test_main(['w', 'cp', 'tests', 'tests2'],
                        expected_stdout=['copied workspace "tests" to "tests2"'])

        self._test_main(['w', 'cp', 'tests', 'tests2'],
                        expected_stdout=['workspace "tests2" already exists',
                                         'copied workspace "tests" to "tests2_2"'])

        self._test_main(['w', 'rn', 'tests9'],
                        expected_stdout=['renamed workspace "tests" to "tests9"',
                                         'current workspace is "tests9"'])

        self._test_main(['w', 'rn', 'tests9'],
                        expected_stdout=['workspace "tests9" already exists',
                                         'renamed workspace "tests9" to "tests9_2"',
                                         'current workspace is "tests9_2"'])

        self._test_main(['w', 'rn', 'tests2', 'tests3'],
                        expected_stdout=['renamed workspace "tests2" to "tests3"'])

        self._test_main(['w', 'cur'],
                        expected_stdout=['current workspace is "tests9_2"'])

        self._test_main(['w', 'list'],
                        expected_stdout=['4 workspaces:',
                                         '1: tests2_2',
                                         '2: tests3',
                                         '3: tests9_2',
                                         '4: tests_1'])

        self._test_main(['w', 'rn'],
                        expected_exit_code=2,
                        expected_stderr='error: the following arguments are required: NEW_NAME')

        self._test_main(['w', 'rm', '-y', 'dummy_ws'],
                        expected_exit_code=1,
                        expected_stderr='workspace "dummy_ws" does not exist')

        self._test_main(['w', 'rm', '-y'],
                        expected_stdout=['removed workspace "tests9_2"',
                                         'current workspace is "tests2_2"'])

        self._test_main(['w', 'rm', '-y', 'tests3'],
                        expected_stdout=['removed workspace "tests3"'])

        self._test_main(['w', 'rm', '-y', 'tests_1'],
                        expected_stdout=['removed workspace "tests_1"'])

        self._test_main(['w', 'rm', '-y'],
                        expected_stdout=['removed workspace "tests2_2"'])

        self._test_main(['w', 'list'],
                        expected_stdout=['no workspaces'])

    def test_command_conf(self):
        self._test_main(['w', 'add', 'tests'],
                        expected_stdout=['created workspace "tests"',
                                         'current workspace is "tests"'])

        self._test_main(['c', 'add', 'config1'],
                        expected_stdout=['created DDP configuration "config1" in workspace "tests"',
                                         'current DDP configuration is "config1"'])

        self._test_main(['c', 'cp'],
                        expected_stdout=['copied DDP configuration "config1" to "config1_copy"'])

        self._test_main(['c', 'cp', 'config1', 'config9'],
                        expected_stdout=['copied DDP configuration "config1" to "config9"'])

        self._test_main(['c', 'cp', 'config1', 'config9'],
                        expected_stdout=['DDP configuration "config9" already exists',
                                         'copied DDP configuration "config1" to "config9_2"'])

        self._test_main(['c', 'rn', 'config2'],
                        expected_stdout=['renamed DDP configuration "config1" to "config2"',
                                         'current DDP configuration is "config2'])

        self._test_main(['c', 'rn', 'config9', 'config10'],
                        expected_stdout=['renamed DDP configuration "config9" to "config10"'])

        self._test_main(['c', 'rn', 'config10', 'config2'],
                        expected_stdout=['DDP configuration "config2" already exists',
                                         'renamed DDP configuration "config10" to "config2_2"'])

        self._test_main(['c', 'rn'],
                        expected_exit_code=2,
                        expected_stderr='error: the following arguments are required: NEW_NAME')

        self._test_main(['c', 'cur'],
                        expected_stdout=['current DDP configuration is "config2"'])

        self._test_main(['c', 'i'],
                        expected_stdout=['current workspace:               tests',
                                         'current DDP configuration:       config2',
                                         'current DDP configuration path:'])

        self._test_main(['c', 'list'],
                        expected_stdout=['4 DDP configurations in workspace "tests":',
                                         '1: config1_copy',
                                         '2: config2',
                                         '3: config2_2',
                                         '4: config9_2'])

        self._test_main(['c', 'rm', '-y', 'dummy_config'],
                        expected_exit_code=1,
                        expected_stderr=['DDP configuration "dummy_config" of workspace "tests" does not exist'])

        self._test_main(['c', 'rm', '-y', 'config2'],
                        expected_stdout=['removed DDP configuration "config2"',
                                         'current DDP configuration is "config1_copy"'])

        self._test_main(['c', 'rm', '-y', 'config2_2'],
                        expected_stdout=['removed DDP configuration "config2_2"'])

        self._test_main(['c', 'rm', '-y', 'config9_2'],
                        expected_stdout=['removed DDP configuration "config9_2"'])

        self._test_main(['c', 'rm', '-y', 'config1_copy'],
                        expected_stdout=['removed DDP configuration "config1_copy"'])

        self._test_main(['c', 'list'],
                        expected_stdout=['no DDP configurations in workspace "tests"'])

    def test_command_output(self):
        input_files = os.path.join(os.path.dirname(__file__), '*.nc')
        self._test_main(['w', 'add', 'tests'],
                        expected_stdout=['created workspace "tests"',
                                         'current workspace is "tests"'])

        self._test_main(['c', 'add', 'config1'],
                        expected_stdout=['created DDP configuration "config1"',
                                         'current DDP configuration is "config1"'])

        self._test_main(['i', 'add', input_files],
                        expected_stdout='added 2 inputs')

        self._test_main(['r'],
                        expected_stdout=['processing "config1": writing L1B'])

        self._test_main(['o', 'list'],
                        expected_stdout=['4 outputs created with config "config1" in workspace "tests":',
                                         '1: L1BS__01_config1.nc',
                                         '2: L1BS__02_config1.nc',
                                         '3: L1B__01_config1.nc',
                                         '4: L1B__02_config1.nc'])

        self._test_main(['o', 'cl', '-q'],
                        expected_stdout=['removed 4 outputs'])

        self._test_main(['o', 'list'],
                        expected_stdout=['no outputs created with config "config1" in workspace "tests"'])

    def test_command_input(self):
        input_files = os.path.join(os.path.dirname(__file__), '*.nc')
        self._test_main(['w', 'add', 'tests'],
                        expected_stdout=['created workspace "tests"',
                                         'current workspace is "tests"'])

        self._test_main(['c', 'add', 'config1'],
                        expected_stdout=['created DDP configuration "config1"',
                                         'current DDP configuration is "config1"'])

        self._test_main(['i', 'add', ''],
                        expected_exit_code=1,
                        expected_stderr='no matching inputs found')

        self._test_main(['i', 'add', input_files],
                        expected_stdout='added 2 inputs')

        self._test_main(['i', 'list'],
                        expected_stdout=['2 inputs in workspace "tests":',
                                         '1: L1A_01.nc',
                                         '2: L1A_02.nc'])

        self._test_main(['i', 'rm', '-q', 'non-existent-file'],
                        expected_exit_code=1,
                        expected_stderr='no matching inputs found')

        self._test_main(['i', 'rm', '-q'],
                        expected_stdout=['removed 2 inputs'])

        self._test_main(['i', 'list'],
                        expected_stdout=['no inputs in workspace "tests"'])

        self._test_main(['i', 'add', input_files])

        self._test_main(['i', 'list'],
                        expected_stdout=['2 inputs in workspace "tests":',
                                         '1: L1A_01.nc',
                                         '2: L1A_02.nc'])

        self._test_main(['i', 'rm', '-q', 'tests', 'L1A_01.nc'],
                        expected_stdout=['one input removed'])

        self._test_main(['i', 'list'],
                        expected_stdout=['1 input in workspace "tests":',
                                         '1: L1A_02.nc'])

    def test_command_run_option_help(self):
        self._test_main(['r', '-h'], expected_stdout='usage:')

    def test_command_run(self):
        input_files = os.path.join(os.path.dirname(__file__), '*.nc')
        self._test_main(['w', 'add', 'tests'],
                        expected_stdout=['created workspace "tests"',
                                         'current workspace is "tests"'])
        self._test_main(['c', 'add', 'test-a'],
                        expected_stdout=['created DDP configuration "test-a"',
                                         'current DDP configuration is "test-a"'])
        self._test_main(['i', 'add', input_files],
                        expected_stdout='added 2 inputs')
        self._test_main(['r'],
                        expected_stdout='processing "test-a"')

    def test_command_run_no_inputs(self):
        self._test_main(['r'],
                        expected_exit_code=1,
                        expected_stdout=['created workspace "default"',
                                         'created DDP configuration "default" in workspace "default"'],
                        expected_stderr=['workspace "default" doesn\'t have any inputs yet'])

    def test_command_run_current(self):
        input_files = os.path.join(os.path.dirname(__file__), '*.nc')
        self._test_main(['i', 'add', input_files],
                        expected_stdout=['created workspace "default"',
                                         'current workspace is "default"',
                                         'added 2 inputs'])
        self._test_main(['r'],
                        expected_stdout=['created DDP configuration "default"',
                                         'current DDP configuration is "default"',
                                         'processing "default"'])

    def test_command_status_short(self):
        self._test_main(['s'],
                        expected_stdout=['configuration location:',
                                         'workspaces location:',
                                         'workspaces total size:',
                                         'workspace names:',
                                         'current workspace:',
                                         'current DDP configuration:'])

# def test_command_status_long_empty(self):
#     self._test_main(['s', '--long'],
#                     expected_stdout=['Workspaces:',
#                                      '(no workspaces yet)',
#                                      'Inputs:',
#                                      '(no inputs yet)',
#                                      'DDP configurations:',
#                                      '(no DDP configurations yet)',
#                                      'Outputs:',
#                                      '(no outputs yet)',
#                                      ])
#
# def test_command_status_long(self):
#     input_files = os.path.join(os.path.dirname(__file__), '*.nc')
#     self._test_main(['w', 'add', 'tests'],
#                     expected_stdout=['created workspace "tests"',
#                                      'current workspace is "tests"'])
#
#     self._test_main(['c', 'add', 'config1'],
#                     expected_stdout=['created DDP configuration "config1" in workspace "tests"',
#                                      'current DDP configuration is "config1"'])
#
#     self._test_main(['i', 'add', input_files],
#                     expected_stdout='added 2 inputs')
#
#     self._test_main(['r'],
#                     expected_stdout='processing "config1": writing L1B')
#
#     self._test_main(['s', '--long'],
#                     expected_stdout=['Workspaces:',
#                                      '*tests',
#                                      'Inputs:',
#                                      'L1A_01.nc		0 MiB',
#                                      'L1A_02.nc		0 MiB',
#                                      'DDP configurations:',
#                                      '*config1',
#                                      'Outputs:',
#                                      'L1BS__01_config1.nc		0 MiB',
#                                      'L1BS__02_config1.nc		0 MiB',
#                                      'L1B__01_config1.nc		0 MiB',
#                                      'L1B__02_config1.nc		0 MiB'])
#
