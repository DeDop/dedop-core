from unittest import TestCase

from dedop.cli.workspace import MemoryWorkspaceManager, Workspace


class WorkspaceTest(TestCase):
    def test_create_workspace(self):
        manager = MemoryWorkspaceManager()
        workspace = Workspace.create_workspace('test', manager=manager)
        self.assertIsNotNone(workspace)
        self.assertEqual(workspace.name, 'test')
        self.assertEqual(workspace.config_names, [])
        workspace.create_config('sido')
        workspace.create_config('udo')
        workspace.create_config('adi')
        workspace.create_config('bibo')
        self.assertEqual(workspace.config_names, ['adi', 'bibo', 'sido', 'udo'])

    def test_current_workspace(self):
        manager = MemoryWorkspaceManager()
        Workspace.create_workspace('test', manager=manager)
        workspace = Workspace.get_current_workspace(manager=manager)
        self.assertIsNone(workspace)

        manager.set_current_workspace_name('test')
        workspace = Workspace.get_current_workspace(manager=manager)
        self.assertIsNotNone(workspace)
        self.assertEqual(workspace.name, 'test')

    def test_current_config(self):
        manager = MemoryWorkspaceManager()
        Workspace.create_workspace('test', manager=manager)
        manager.set_current_workspace_name('test')
        workspace = Workspace.get_current_workspace(manager=manager)
        manager.set_current_config_name('test', 'bibo')

        config = workspace.current_config
        self.assertIsNotNone(config)
        self.assertEqual(config.name, 'bibo')


class ConfigTest(TestCase):
    def test_config_files(self):
        manager = MemoryWorkspaceManager()
        workspace = Workspace.create_workspace('testws', manager=manager)
        config = workspace.create_config('testconf')
        self.assertIsNotNone(config)
        self.assertEqual(config.name, 'testconf')
        self.assertEqual(config.chd_file, 'CHD.json')
        self.assertEqual(config.cnf_file, 'CNF.json')
        self.assertEqual(config.cst_file, 'CST.json')


