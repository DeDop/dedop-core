import os.path
from unittest import TestCase

from dedop.ui.workspace_manager import WorkspaceManager, WorkspaceError
from dedop.util.monitor import ConsoleMonitor

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')
WORKSPACES_DIR = os.path.join(TEST_DATA_DIR, 'workspaces')


# noinspection PyPep8Naming,PyUnresolvedReferences,PyAttributeOutsideInit
class WorkspaceTestBase:
    def setUp(self):
        self.manager = WorkspaceManager(workspaces_dir=WORKSPACES_DIR)
        self.manager.delete_all_workspaces()

    def tearDown(self):
        self.manager.delete_all_workspaces()

    def assertIsWorkspaceDir(self, *path, expected=True):
        self.assertEqual(os.path.isdir(os.path.join(WORKSPACES_DIR, *path)), expected)

    def assertIsWorkspaceFile(self, *path, expected=True):
        self.assertEqual(os.path.isfile(os.path.join(WORKSPACES_DIR, *path)), expected)

    def assertWorkspaceFileExists(self, *path, expected=True):
        self.assertEqual(os.path.exists(os.path.join(WORKSPACES_DIR, *path)), expected)

    def assertRaisedException(self, expected_exception, expected_message, func, *args):
        try:
            func(*args)
        except expected_exception as e:
            self.assertEqual(e.message, expected_message)
            return
        self.fail("Exception expected but none thrown.")

    @staticmethod
    def createWorkspaceSubDir(*path):
        os.mkdir(os.path.join(WORKSPACES_DIR, *path))

    @staticmethod
    def createWorkspaceFile(*path):
        open(os.path.join(WORKSPACES_DIR, *path), 'a')


class WorkspaceManagerTest(WorkspaceTestBase, TestCase):
    def test_create_workspace(self):
        self.manager.create_workspace('test_ws')
        self.assertIsWorkspaceDir('test_ws')

    def test_get_workspace_names(self):
        self.assertEqual(self.manager.get_workspace_names(), [])
        self.manager.create_workspace('ernie_ws')
        self.manager.create_workspace('bert_ws')
        self.manager.create_workspace('oscar_ws')
        self.manager.create_workspace('bibo_ws')
        self.assertEqual(self.manager.get_workspace_names(), ['bert_ws', 'bibo_ws', 'ernie_ws', 'oscar_ws'])

    def test_workspace_exists(self):
        self.manager.create_workspace('ernie_ws')
        self.assertTrue(self.manager.workspace_exists('ernie_ws'))
        self.assertFalse(self.manager.workspace_exists('bibo'))

    def test_delete_workspace(self):
        self.manager.create_workspace('ernie_ws')
        self.assertIsWorkspaceDir('ernie_ws', expected=True)
        self.manager.delete_workspace('ernie_ws')
        self.assertIsWorkspaceDir('ernie_ws', expected=False)

    def test_delete_non_existent_workspace(self):
        self.assertIsWorkspaceDir('ernie_ws', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'workspace "ernie_ws" does not exist',
                                   self.manager.delete_workspace,
                                   'ernie_ws')

    def test_copy_workspace(self):
        self.manager.create_workspace('ernie_ws')
        self.assertIsWorkspaceDir('ernie_ws', expected=True)
        self.createWorkspaceSubDir('ernie_ws', 'sub_dir1')
        self.createWorkspaceSubDir('ernie_ws', 'sub_dir2')
        self.manager.copy_workspace('ernie_ws', 'bert_ws')
        self.assertIsWorkspaceDir('ernie_ws', expected=True)
        self.assertIsWorkspaceDir('bert_ws', expected=True)
        self.assertIsWorkspaceDir('bert_ws', 'sub_dir1', expected=True)
        self.assertIsWorkspaceDir('bert_ws', 'sub_dir2', expected=True)

    def test_copy_non_existent_workspace(self):
        self.assertIsWorkspaceDir('ernie_ws', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'workspace "ernie_ws" does not exist',
                                   self.manager.copy_workspace,
                                   'ernie_ws', 'bert_ws')

    def test_rename_workspace(self):
        self.manager.create_workspace('ernie_ws')
        self.assertIsWorkspaceDir('ernie_ws', expected=True)
        self.createWorkspaceSubDir('ernie_ws', 'sub_dir1')
        self.createWorkspaceSubDir('ernie_ws', 'sub_dir2')
        self.manager.rename_workspace('ernie_ws', 'bert_ws')
        self.assertIsWorkspaceDir('ernie_ws', expected=False)
        self.assertIsWorkspaceDir('bert_ws', expected=True)
        self.assertIsWorkspaceDir('bert_ws', 'sub_dir1', expected=True)
        self.assertIsWorkspaceDir('bert_ws', 'sub_dir2', expected=True)

    def test_rename_non_existent_workspace(self):
        self.assertIsWorkspaceDir('ernie_ws', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'workspace "ernie_ws" does not exist',
                                   self.manager.rename_workspace,
                                   'ernie_ws', 'ernie2')

    def test_create_config(self):
        self.manager.create_workspace('ernie_ws')
        self.assertIsWorkspaceDir('ernie_ws', expected=True)
        self.manager.create_config('ernie_ws', 'bibo_conf')
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=True)

    def test_delete_config(self):
        self.manager.create_workspace('ernie_ws')
        self.manager.create_config('ernie_ws', 'bibo_conf')
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=True)
        self.manager.delete_config('ernie_ws', 'bibo_conf')
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=False)

    def test_delete_non_existent_config(self):
        self.manager.create_workspace('ernie_ws')
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'DDP configuration "bibo_conf" of workspace "ernie_ws" does not exist',
                                   self.manager.delete_config,
                                   'ernie_ws', 'bibo_conf')

    def test_copy_config(self):
        self.manager.create_workspace('ernie_ws')
        self.manager.create_config('ernie_ws', 'bibo_conf')
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CST.json', expected=True)

        self.manager.copy_config('ernie_ws', 'bibo_conf', 'piggy_conf')

        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=True)
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'piggy_conf', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'piggy_conf', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'piggy_conf', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'piggy_conf', 'CST.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CST.json', expected=True)

    def test_copy_non_existent_config(self):
        self.manager.create_workspace('ernie_ws')
        self.assertRaisedException(WorkspaceError,
                                   'DDP configuration "bibo_conf" of workspace "ernie_ws" does not exist',
                                   self.manager.copy_config,
                                   'ernie_ws', 'bibo_conf', 'piggy_conf')

    def test_rename_config(self):
        self.manager.create_workspace('ernie_ws')
        self.manager.create_config('ernie_ws', 'bibo_conf')
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CST.json', expected=True)

        self.manager.rename_config('ernie_ws', 'bibo_conf', 'piggy_conf')

        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'bibo_conf', expected=False)
        self.assertIsWorkspaceDir('ernie_ws', 'configs', 'piggy_conf', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'piggy_conf', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'piggy_conf', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'piggy_conf', 'CST.json', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CHD.json', expected=False)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CNF.json', expected=False)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'CST.json', expected=False)

    def test_rename_non_existent_config(self):
        self.manager.create_workspace('ernie_ws')
        self.assertRaisedException(WorkspaceError,
                                   'DDP configuration "bibo_conf" of workspace "ernie_ws" does not exist',
                                   self.manager.rename_config,
                                   'ernie_ws', 'bibo_conf', 'piggy_conf')

    def test_list_output_files(self):
        self.manager.create_workspace('ernie_ws')
        self.manager.create_config('ernie_ws', 'bibo_conf')
        output_dir = self.manager.get_outputs_path('ernie_ws', 'bibo_conf')
        self.createWorkspaceSubDir(output_dir)
        self.createWorkspaceFile(output_dir, 'output1.nc')
        self.createWorkspaceFile(output_dir, 'output2.nc')
        self.createWorkspaceFile(output_dir, 'output3.nc')
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output1.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output2.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output3.nc', expected=True)

        output_files = self.manager.get_output_names('ernie_ws', 'bibo_conf')

        self.assertTrue('output1.nc' in output_files)
        self.assertTrue('output2.nc' in output_files)
        self.assertTrue('output3.nc' in output_files)

    def test_remove_output_files(self):
        self.manager.create_workspace('ernie_ws')
        self.manager.create_config('ernie_ws', 'bibo_conf')
        output_dir = self.manager.get_outputs_path('ernie_ws', 'bibo_conf')
        self.createWorkspaceSubDir(output_dir)
        self.createWorkspaceFile(output_dir, 'output1.nc')
        self.createWorkspaceFile(output_dir, 'output2.nc')
        self.createWorkspaceFile(output_dir, 'output3.nc')
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output1.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output2.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output3.nc', expected=True)

        self.manager.remove_outputs('ernie_ws', 'bibo_conf')

        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output1.nc', expected=False)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output2.nc', expected=False)
        self.assertIsWorkspaceFile('ernie_ws', 'configs', 'bibo_conf', 'outputs', 'output3.nc', expected=False)

    def test_remove_non_existent_outputs(self):
        # no error thrown when files do not exist inside outputs dir
        self.manager.create_workspace('ernie_ws')
        self.manager.create_config('ernie_ws', 'bibo_conf')

        self.assertRaisedException(WorkspaceError,
                                   'output directory does not exist',
                                   self.manager.remove_outputs,
                                   'ernie_ws', 'bibo_conf')

        self.createWorkspaceSubDir(WORKSPACES_DIR, 'ernie_ws', 'configs', 'bibo_conf', 'outputs')
        self.manager.remove_outputs('ernie_ws', 'bibo_conf')

    def test_add_inputs(self):
        self.manager.create_workspace('ernie_ws')
        input_path = os.path.join(WORKSPACES_DIR, 'ernie_ws', 'test-input.nc')
        self.createWorkspaceFile('ernie_ws', 'test-input.nc')

        self.manager.add_inputs('ernie_ws', [input_path], ConsoleMonitor(stay_in_line=True, progress_bar_size=32))

        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'test-input.nc', expected=True)

    def test_list_input_files(self):
        self.manager.create_workspace('ernie_ws')
        input_dir = os.path.join(WORKSPACES_DIR, 'ernie_ws', 'inputs')
        self.createWorkspaceSubDir(input_dir)
        self.createWorkspaceFile(input_dir, 'input1.nc')
        self.createWorkspaceFile(input_dir, 'input2.nc')
        self.createWorkspaceFile(input_dir, 'input3.nc')
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input1.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input2.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input3.nc', expected=True)

        input_files = self.manager.get_input_names('ernie_ws')

        self.assertTrue('input1.nc' in input_files)
        self.assertTrue('input2.nc' in input_files)
        self.assertTrue('input3.nc' in input_files)

    def test_remove_input_files(self):
        self.manager.create_workspace('ernie_ws')
        input_dir = os.path.join(WORKSPACES_DIR, 'ernie_ws', 'inputs')
        self.createWorkspaceSubDir(input_dir)
        self.createWorkspaceFile(input_dir, 'input1.nc')
        self.createWorkspaceFile(input_dir, 'input2.nc')
        self.createWorkspaceFile(input_dir, 'input3.nc')
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input1.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input2.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input3.nc', expected=True)

        self.manager.remove_inputs('ernie_ws', ['input1.nc'], ConsoleMonitor(stay_in_line=True, progress_bar_size=32))

        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input1.nc', expected=False)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input2.nc', expected=True)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input3.nc', expected=True)

        self.manager.remove_inputs('ernie_ws', ['input2.nc', 'input3.nc'],
                                   ConsoleMonitor(stay_in_line=True, progress_bar_size=32))

        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input1.nc', expected=False)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input2.nc', expected=False)
        self.assertIsWorkspaceFile('ernie_ws', 'inputs', 'input3.nc', expected=False)
