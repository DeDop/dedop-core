import os
import unittest

from dedop.ui.workspace_manager import WorkspaceManager
from dedop.webapi.websocket import WebSocketService


class WebSocketServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = WebSocketService(WorkspaceManager())
        self.clean_up_test_workspaces()

    @unittest.skipIf(os.environ.get('DEDOP_DISABLE_WEB_TESTS', None) == '1', 'DEDOP_DISABLE_WEB_TESTS = 1')
    def test_workspace_management(self):
        all_workspaces = self.service.get_all_workspaces()['workspaces']
        initial_workspace_count = len(all_workspaces)

        new_workspace = self.service.new_workspace('test_workspace')
        all_workspaces = self.service.get_all_workspaces()['workspaces']
        self.assertIn('test_workspace', [workspace['name'] for workspace in all_workspaces])
        self.assertIsInstance(new_workspace, dict)
        self.assertGreater(len(new_workspace), 1)
        self.assertTrue('workspace_dir' in new_workspace)
        self.assertTrue('name' in new_workspace)
        self.assertEqual(new_workspace['name'], 'test_workspace')
        self.assertTrue('is_current' in new_workspace)
        self.assertFalse(new_workspace['is_current'])
        workspace_count = initial_workspace_count + 1
        self.assertEqual(len(all_workspaces), workspace_count)

        self.service.set_current_workspace('test_workspace')
        self.assertEqual(self.service.get_current_workspace()['name'], 'test_workspace')

        copied_workspace = self.service.copy_workspace('test_workspace', 'test_workspace_copied')
        workspace_count += 1
        all_workspaces = self.service.get_all_workspaces()['workspaces']
        self.assertEqual(len(all_workspaces), workspace_count)
        self.assertIn('test_workspace_copied', [workspace['name'] for workspace in all_workspaces])
        self.assertEqual(copied_workspace['name'], 'test_workspace_copied')
        self.assertEqual(copied_workspace['is_current'], False)

        renamed_workspace = self.service.rename_workspace('test_workspace_copied', 'test_workspace_renamed')
        all_workspaces = self.service.get_all_workspaces()['workspaces']
        self.assertEqual(len(all_workspaces), workspace_count)
        self.assertIn('test_workspace_renamed', [workspace['name'] for workspace in all_workspaces])
        self.assertEqual(renamed_workspace['name'], 'test_workspace_renamed')
        self.assertEqual(renamed_workspace['is_current'], False)

        self.assertNotEqual(self.service.get_current_workspace()['name'], 'test_workspace_renamed')
        self.service.set_current_workspace('test_workspace_renamed')
        self.assertEqual(self.service.get_current_workspace()['name'], 'test_workspace_renamed')

        self.clean_up_test_workspaces()

    def test_config_management(self):
        ws_name = 'test_ws_config'
        self.service.new_workspace(ws_name)
        self.service.set_current_workspace('test_ws_config')

        versions = self.service.get_default_config_versions()
        self.assertIn('cnf_version', versions)
        self.assertEqual(versions['cnf_version'], 3)
        self.assertIn('chd_version', versions)
        self.assertEqual(versions['chd_version'], 1)
        self.assertIn('cst_version', versions)
        self.assertEqual(versions['cst_version'], 0)

        config_names = self.service.get_config_names(ws_name)
        initial_config_count = len(config_names) if config_names else 0

        self.service.add_new_config(ws_name, 'test_config_sentinel', False)
        config_count = initial_config_count + 1
        config_names = self.service.get_config_names(ws_name)
        self.assertIn('test_config_sentinel', config_names)
        self.assertEqual(len(config_names), config_count)

        self.service.set_current_config(ws_name, 'test_config_sentinel')
        self.assertEqual(self.service.get_current_config(ws_name)['name'], 'test_config_sentinel')

        sentinel_configs = self.service.get_configs(ws_name, 'test_config_sentinel')
        self.assertIn('name', sentinel_configs)
        self.assertEqual(sentinel_configs['name'], 'test_config_sentinel')
        self.assertIn('chd', sentinel_configs)
        self.assertIsInstance(sentinel_configs['chd'], dict)
        self.assertEqual(len(sentinel_configs['chd']), 16)
        self.assertEqual(sentinel_configs['chd']['mean_sat_alt_chd']['value'], 814500.0)
        self.assertEqual(sentinel_configs['chd']['brf_sar_chd']['value'], 78.53069)
        self.assertIn('cnf', sentinel_configs)
        self.assertIsInstance(sentinel_configs['cnf'], dict)
        self.assertEqual(len(sentinel_configs['cnf']), 24)
        self.assertEqual(sentinel_configs['cnf']['flag_cal2_correction_cnf']['value'], True)
        self.assertEqual(sentinel_configs['cnf']['N_looks_stack_cnf']['value'], 240)
        self.assertIn('cst', sentinel_configs)
        self.assertIsInstance(sentinel_configs['cst'], dict)
        self.assertEqual(len(sentinel_configs['cst']), 8)
        self.assertEqual(sentinel_configs['cst']['semi_major_axis_cst']['value'], 6378137.0)
        self.assertEqual(sentinel_configs['cst']['flat_coeff_cst']['value'], 0.00335281067183084)
        self.assertIn('chd_order', sentinel_configs)
        self.assertIn('cnf_order', sentinel_configs)
        self.assertIn('cst_order', sentinel_configs)

        self.service.add_new_config(ws_name, 'test_config_cryosat', True)
        config_count += 1
        config_names = self.service.get_config_names(ws_name)
        self.assertIn('test_config_cryosat', config_names)
        self.assertEqual(len(config_names), config_count)

        cryosat_configs = self.service.get_configs(ws_name, 'test_config_cryosat')
        self.assertIn('name', cryosat_configs)
        self.assertEqual(cryosat_configs['name'], 'test_config_cryosat')
        self.assertIn('chd', cryosat_configs)
        self.assertIsInstance(cryosat_configs['chd'], dict)
        self.assertEqual(len(cryosat_configs['chd']), 16)
        self.assertEqual(cryosat_configs['chd']['mean_sat_alt_chd']['value'], 717000)
        self.assertEqual(cryosat_configs['chd']['brf_sar_chd']['value'], 85.51521850207267)
        self.assertIn('cnf', cryosat_configs)
        self.assertIsInstance(cryosat_configs['cnf'], dict)
        self.assertEqual(len(cryosat_configs['cnf']), 24)
        self.assertEqual(cryosat_configs['cnf']['flag_cal2_correction_cnf']['value'], True)
        self.assertEqual(cryosat_configs['cnf']['N_looks_stack_cnf']['value'], 240)
        self.assertIn('cst', cryosat_configs)
        self.assertIsInstance(cryosat_configs['cst'], dict)
        self.assertEqual(len(cryosat_configs['cst']), 8)
        self.assertEqual(cryosat_configs['cst']['semi_major_axis_cst']['value'], 6378137.0)
        self.assertEqual(cryosat_configs['cst']['flat_coeff_cst']['value'], 0.00335281067183084)
        self.assertIn('chd_order', cryosat_configs)
        self.assertIn('cnf_order', cryosat_configs)
        self.assertIn('cst_order', cryosat_configs)

        self.service.copy_config(ws_name, 'test_config_sentinel', 'test_config_sentinel_copied')
        config_count += 1
        config_names = self.service.get_config_names(ws_name)
        self.assertIn('test_config_sentinel_copied', config_names)
        self.assertEqual(len(config_names), config_count)

        self.service.rename_config(ws_name, 'test_config_sentinel', 'test_config_sentinel_renamed')
        config_names = self.service.get_config_names(ws_name)
        self.assertIn('test_config_sentinel_renamed', config_names)
        self.assertEqual(len(config_names), config_count)

        self.assertNotEqual(self.service.get_current_config(ws_name)['name'], 'test_config_sentinel_renamed')
        self.service.set_current_config(ws_name, 'test_config_sentinel_renamed')
        self.assertEqual(self.service.get_current_config(ws_name)['name'], 'test_config_sentinel_renamed')

        self.service.delete_config(ws_name, 'test_config_sentinel_renamed')
        self.assertNotEqual(self.service.get_current_config(ws_name)['name'], 'test_config_sentinel_renamed')

    def test_input_data_management(self):
        input_file_name = "l1a_test.nc"
        test_input_file_path = "test_data/data/test_l1a/inputs/%s" % input_file_name
        ws_name = 'test_ws_input'
        self.service.new_workspace(ws_name)
        self.service.set_current_workspace('test_ws_input')

        self.service.add_input_files('test_ws_input', [test_input_file_path])
        global_attributes = self.service.get_global_attributes(test_input_file_path)
        self.assertEqual(global_attributes['title'], 'IPF SRAL Level 1A Measurement')
        self.assertEqual(global_attributes['altimeter_sensor_name'], 'SRAL')

        max_min_coordinates = self.service.get_max_min_coordinates(test_input_file_path)
        self.assertIn('lat', max_min_coordinates)
        self.assertEqual(max_min_coordinates['lat'], [-1e-06, 9e-06])
        self.assertIn('lon', max_min_coordinates)
        self.assertEqual(max_min_coordinates['lon'], [-1e-06, 9e-06])

        lat_lon = self.service.get_lat_lon(test_input_file_path)
        self.assertIn('lat', lat_lon)
        self.assertEqual(lat_lon['lat'],
                         [-1e-06, 1e-06, 2e-06, 3e-06, 4e-06, 4.9999999999999996e-06, 6e-06, 7e-06, 8e-06, 9e-06])
        self.assertIn('lon', lat_lon)
        self.assertEqual(lat_lon['lon'],
                         [-1e-06, 1e-06, 2e-06, 3e-06, 4e-06, 4.9999999999999996e-06, 6e-06, 7e-06, 8e-06, 9e-06])

        self.service.remove_input_files(ws_name, [input_file_name])

    def clean_up_test_workspaces(self):
        all_workspaces = self.service.get_all_workspaces()
        if all_workspaces['workspaces']:
            for workspace in all_workspaces['workspaces']:
                if workspace['name'] == 'test_workspace' \
                        or workspace['name'] == 'test_workspace_copied' \
                        or workspace['name'] == 'test_workspace_renamed' \
                        or workspace['name'] == 'test_ws_config' \
                        or workspace['name'] == 'test_ws_input':
                    self.service.delete_workspace(workspace['name'])
                else:
                    self.service.set_current_workspace(workspace['name'])
        self.assertNotEqual(self.service.get_current_workspace()['name'], 'test_workspace_copied')
        self.assertNotEqual(self.service.get_current_workspace()['name'], 'test_workspace_renamed')
        self.assertNotEqual(self.service.get_current_workspace()['name'], 'test_ws_config')
        self.assertNotEqual(self.service.get_current_workspace()['name'], 'test_ws_input')
