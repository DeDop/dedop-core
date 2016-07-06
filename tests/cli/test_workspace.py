import os.path
from unittest import TestCase

from dedop.cli.workspace import WorkspaceManager, WorkspaceError

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
        self.manager.create_workspace('test')
        self.assertIsWorkspaceDir('test')

    def test_get_workspace_names(self):
        self.assertEqual(self.manager.get_workspace_names(), [])
        self.manager.create_workspace('ernie')
        self.manager.create_workspace('bert')
        self.manager.create_workspace('oscar')
        self.manager.create_workspace('bibo')
        self.assertEqual(self.manager.get_workspace_names(), ['bert', 'bibo', 'ernie', 'oscar'])

    def test_workspace_exists(self):
        self.manager.create_workspace('ernie')
        self.assertTrue(self.manager.workspace_exists('ernie'))
        self.assertFalse(self.manager.workspace_exists('bibo'))

    def test_delete_workspace(self):
        self.manager.create_workspace('ernie')
        self.assertIsWorkspaceDir('ernie', expected=True)
        self.manager.delete_workspace('ernie')
        self.assertIsWorkspaceDir('ernie', expected=False)

    def test_delete_non_existent_workspace(self):
        self.assertIsWorkspaceDir('ernie', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'workspace "ernie" does not exist',
                                   self.manager.delete_workspace,
                                   'ernie')

    def test_copy_workspace(self):
        self.manager.create_workspace('ernie')
        self.assertIsWorkspaceDir('ernie', expected=True)
        WorkspaceTestBase.createWorkspaceSubDir('ernie', 'sub_dir1')
        WorkspaceTestBase.createWorkspaceSubDir('ernie', 'sub_dir2')
        self.manager.copy_workspace('ernie', 'bert')
        self.assertIsWorkspaceDir('ernie', expected=True)
        self.assertIsWorkspaceDir('bert', expected=True)
        self.assertIsWorkspaceDir('bert', 'sub_dir1', expected=True)
        self.assertIsWorkspaceDir('bert', 'sub_dir2', expected=True)

    def test_copy_non_existent_workspace(self):
        self.assertIsWorkspaceDir('ernie', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'workspace "ernie" does not exist',
                                   self.manager.copy_workspace,
                                   'ernie', 'bert')

    def test_rename_workspace(self):
        self.manager.create_workspace('ernie')
        self.assertIsWorkspaceDir('ernie', expected=True)
        WorkspaceTestBase.createWorkspaceSubDir('ernie', 'sub_dir1')
        WorkspaceTestBase.createWorkspaceSubDir('ernie', 'sub_dir2')
        self.manager.rename_workspace('ernie', 'bert')
        self.assertIsWorkspaceDir('ernie', expected=False)
        self.assertIsWorkspaceDir('bert', expected=True)
        self.assertIsWorkspaceDir('bert', 'sub_dir1', expected=True)
        self.assertIsWorkspaceDir('bert', 'sub_dir2', expected=True)

    def test_rename_non_existent_workspace(self):
        self.assertIsWorkspaceDir('ernie', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'workspace "ernie" does not exist',
                                   self.manager.rename_workspace,
                                   'ernie', 'ernie2')

    def test_create_config(self):
        self.manager.create_workspace('ernie')
        self.assertIsWorkspaceDir('ernie', expected=True)
        self.manager.create_config('ernie', 'laugh')
        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=True)

    def test_delete_config(self):
        self.manager.create_workspace('ernie')
        self.manager.create_config('ernie', 'laugh')
        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=True)
        self.manager.delete_config('ernie', 'laugh')
        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=False)

    def test_delete_non_existent_config(self):
        self.manager.create_workspace('ernie')
        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=False)
        self.assertRaisedException(WorkspaceError,
                                   'configuration "laugh" inside workspace "ernie" does not exist',
                                   self.manager.delete_config,
                                   'ernie', 'laugh')

    def test_copy_config(self):
        self.manager.create_workspace('ernie')
        self.manager.create_config('ernie', 'laugh')
        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CST.json', expected=True)

        self.manager.copy_config('ernie', 'laugh', 'play')

        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=True)
        self.assertIsWorkspaceDir('ernie', 'configs', 'play', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'play', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'play', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'play', 'CST.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CST.json', expected=True)

    def test_copy_non_existent_config(self):
        self.manager.create_workspace('ernie')
        self.assertRaisedException(WorkspaceError,
                                   'configuration "laugh" inside workspace "ernie" does not exist',
                                   self.manager.copy_config,
                                   'ernie', 'laugh', 'play')

    def test_rename_config(self):
        self.manager.create_workspace('ernie')
        self.manager.create_config('ernie', 'laugh')
        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CST.json', expected=True)

        self.manager.rename_config('ernie', 'laugh', 'play')

        self.assertIsWorkspaceDir('ernie', 'configs', 'laugh', expected=False)
        self.assertIsWorkspaceDir('ernie', 'configs', 'play', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'play', 'CHD.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'play', 'CNF.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'play', 'CST.json', expected=True)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CHD.json', expected=False)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CNF.json', expected=False)
        self.assertIsWorkspaceFile('ernie', 'configs', 'laugh', 'CST.json', expected=False)

    def test_rename_non_existent_config(self):
        self.manager.create_workspace('ernie')
        self.assertRaisedException(WorkspaceError,
                                   'configuration "laugh" inside workspace "ernie" does not exist',
                                   self.manager.rename_config,
                                   'ernie', 'laugh', 'play')
