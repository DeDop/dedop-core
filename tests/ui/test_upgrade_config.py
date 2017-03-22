import json
import os.path
import pkgutil
from unittest import TestCase

from dedop.ui.workspace_manager import WorkspaceManager

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test_data')
WORKSPACES_DIR = os.path.join(TEST_DATA_DIR, 'workspaces')


# noinspection PyPep8Naming,PyUnresolvedReferences,PyAttributeOutsideInit
class UpgradeConfigTestBase:
    def setUp(self):
        self.manager = WorkspaceManager(workspaces_dir=WORKSPACES_DIR)

    def assertKeyExist(self, key: str, config: dict, expected=True):
        self.assertEqual(key in config, expected)

    def assertConfigVersion(self, version: int, config: dict):
        self.assertEqual(config['__metainf__']['version'], version)

    def assertVersionUnavailable(self, config: dict):
        try:
            config['__metainf__']['version']
        except KeyError:
            return
        self.fail("Exception expected but none thrown.")

    @staticmethod
    def get_config_json(config_file_name: str, package_name='tests.ui'):
        current_config_data = pkgutil.get_data(package_name, config_file_name)
        current_config = json.loads(current_config_data.decode("utf-8"))
        return current_config


class UpgradeConfigTest(UpgradeConfigTestBase, TestCase):
    def test_upgrade_config(self):
        current_config = self.get_config_json('base-config.json')
        self.assertKeyExist("flag_cal1_corrections_cnf", current_config)
        self.assertKeyExist("flag_cal2_correction_cnf", current_config)
        self.assertKeyExist("flag_uso_correction_cnf", current_config)
        self.assertKeyExist("__metainf__", current_config, expected=False)
        self.assertVersionUnavailable(current_config)

        default_config = self.get_config_json("config-with-metainfv1.json")
        self.assertKeyExist("flag_cal1_corrections_cnf", default_config)
        self.assertKeyExist("flag_cal2_correction_cnf", default_config)
        self.assertKeyExist("flag_uso_correction_cnf", default_config)
        self.assertKeyExist("flag_azimuth_processing_method_cnf", default_config)
        self.assertKeyExist("__metainf__", default_config)
        self.assertConfigVersion(1, default_config)

        updated_config = self.manager._do_upgrade_config(current_config, default_config)
        self.assertEqual(len(updated_config), 5)
        self.assertKeyExist("flag_cal1_corrections_cnf", updated_config)
        self.assertKeyExist("flag_cal2_correction_cnf", updated_config)
        self.assertKeyExist("flag_uso_correction_cnf", updated_config)
        self.assertKeyExist("flag_azimuth_processing_method_cnf", updated_config)
        self.assertKeyExist("__metainf__", updated_config)
        self.assertConfigVersion(1, updated_config)
        self.assertEqual(updated_config["flag_azimuth_processing_method_cnf"]['value'], True)

    def test_upgrade_config_v2(self):
        current_config = self.get_config_json('base-config.json')
        self.assertKeyExist("flag_cal1_corrections_cnf", current_config)
        self.assertKeyExist("flag_cal2_correction_cnf", current_config)
        self.assertKeyExist("flag_uso_correction_cnf", current_config)
        self.assertKeyExist("__metainf__", current_config, expected=False)
        self.assertVersionUnavailable(current_config)

        default_config = self.get_config_json("config-with-metainfv2.json")
        self.assertKeyExist("flag_cal1_corrections_cnf", default_config)
        self.assertKeyExist("flag_cal2_correction_cnf", default_config)
        self.assertKeyExist("flag_uso_correction_cnf", default_config)
        self.assertKeyExist("flag_azimuth_processing_method_cnf", default_config)
        self.assertKeyExist("new_field", default_config)
        self.assertKeyExist("__metainf__", default_config)
        self.assertConfigVersion(2, default_config)

        updated_config = self.manager._do_upgrade_config(current_config, default_config)
        self.assertEqual(len(updated_config), 6)
        self.assertKeyExist("flag_cal1_corrections_cnf", updated_config)
        self.assertKeyExist("flag_cal2_correction_cnf", updated_config)
        self.assertKeyExist("flag_uso_correction_cnf", updated_config)
        self.assertKeyExist("flag_azimuth_processing_method_cnf", updated_config)
        self.assertKeyExist("new_field", updated_config)
        self.assertKeyExist("__metainf__", updated_config)
        self.assertConfigVersion(2, updated_config)
        self.assertEqual(updated_config["flag_azimuth_processing_method_cnf"]['value'], False)
        self.assertEqual(updated_config["new_field"], {'value': 123, 'description': 'A test field', 'units': None})

    def test_upgrade_config_v3(self):
        current_config = self.get_config_json('base-config.json')
        self.assertKeyExist("flag_cal1_corrections_cnf", current_config)
        self.assertKeyExist("flag_cal2_correction_cnf", current_config)
        self.assertKeyExist("flag_uso_correction_cnf", current_config)
        self.assertKeyExist("__metainf__", current_config, expected=False)
        self.assertVersionUnavailable(current_config)

        default_config = self.get_config_json("config-with-metainfv3.json")
        self.assertEqual(len(default_config), 2)
        self.assertKeyExist("new_field", default_config)
        self.assertKeyExist("__metainf__", default_config)
        self.assertConfigVersion(3, default_config)

        updated_config = self.manager._do_upgrade_config(current_config, default_config)
        self.assertEqual(len(updated_config), 2)
        self.assertKeyExist("new_field", updated_config)
        self.assertKeyExist("__metainf__", updated_config)
        self.assertConfigVersion(3, updated_config)
        self.assertEqual(updated_config["new_field"], {'value': 123, 'description': 'A test field', 'units': None})

    def test_upgrade_nothing(self):
        current_config = self.get_config_json('config-with-metainfv3.json')
        self.assertEqual(len(current_config), 2)
        self.assertKeyExist("new_field", current_config)
        self.assertKeyExist("__metainf__", current_config)
        self.assertConfigVersion(3, current_config)

        default_config = self.get_config_json("config-with-metainfv3.json")
        self.assertEqual(len(default_config), 2)
        self.assertKeyExist("new_field", default_config)
        self.assertKeyExist("__metainf__", default_config)
        self.assertConfigVersion(3, default_config)

        updated_config = self.manager._do_upgrade_config(current_config, default_config)
        self.assertEqual(updated_config, current_config)
