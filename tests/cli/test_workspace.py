import os.path
from unittest import TestCase

from dedop.cli.workspace import WorkspaceManager

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')
WORKSPACES_DIR = os.path.join(TEST_DATA_DIR, 'workspaces')


class WorkspaceTest(TestCase):
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

    def test_that_true_is_true(self):
        self.assertTrue(True)


class WorkspaceManagerTest(WorkspaceTest):
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
