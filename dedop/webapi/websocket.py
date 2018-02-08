import json
import os

from cate.util.monitor import Monitor
from netCDF4 import Dataset
from typing import List

from dedop.proc.sar import L1BProcessor
from dedop.ui.workspace_manager import WorkspaceManager


class WebSocketService:
    """
    Object which implements dedop's server-side methods.

    All methods receive inputs deserialized from JSON-RCP requests and must
    return JSON-serializable outputs.

    :param: workspace_manager The current workspace manager.
    """

    def __init__(self, workspace_manager: WorkspaceManager):
        self.workspace_manager = workspace_manager

    def new_workspace(self, workspace_name) -> dict:
        workspace = self.workspace_manager.create_workspace(workspace_name)
        return workspace.to_json_dict()

    def delete_workspace(self, workspace_name) -> None:
        self.workspace_manager.delete_workspace(workspace_name)
        all_workspaces = self.workspace_manager.get_workspace_names()
        if 'default' in all_workspaces:
            self.set_current_workspace('default')
        elif len(all_workspaces) > 0:
            self.set_current_workspace(all_workspaces[0])
        else:
            self.set_current_workspace('')

    def copy_workspace(self, workspace_name, new_workspace_name) -> dict:
        workspace = self.workspace_manager.copy_workspace(workspace_name, new_workspace_name)
        return workspace.to_json_dict()

    def rename_workspace(self, workspace_name, new_workspace_name) -> dict:
        workspace = self.workspace_manager.rename_workspace(workspace_name, new_workspace_name)
        return workspace.to_json_dict()

    def get_current_workspace(self) -> dict:
        workspace = self.workspace_manager.get_current_workspace()
        return workspace.to_json_dict()

    def set_current_workspace(self, workspace_name) -> dict:
        workspace = self.workspace_manager.set_current_workspace_name(workspace_name)
        return workspace.to_json_dict()

    def get_all_workspaces(self) -> dict:
        workspaces = self.workspace_manager.get_workspaces()
        return {
            "workspaces": workspaces
        }

    def add_input_files(self, workspace_name: str, input_file_paths: List[str]):
        self.workspace_manager.add_inputs(workspace_name, input_file_paths, Monitor.NONE)

    def remove_input_files(self, workspace_name: str, input_names: List[str]):
        self.workspace_manager.remove_inputs(workspace_name, input_names, Monitor.NONE)

    def get_config_names(self, workspace_name: str) -> List[str]:
        return self.workspace_manager.get_config_names(workspace_name)

    def add_new_config(self, workspace_name: str, config_name: str, cryosat: bool):
        self.workspace_manager.create_config(workspace_name, config_name, cryosat=cryosat)

    def delete_config(self, workspace_name: str, config_name: str):
        self.workspace_manager.delete_config(workspace_name, config_name)
        all_configs = self.workspace_manager.get_config_names(workspace_name)
        if 'default' in all_configs:
            self.set_current_config(workspace_name, 'default')
        elif len(all_configs) > 0:
            self.set_current_config(workspace_name, all_configs[0])
        else:
            self.set_current_config(workspace_name, '')

    def copy_config(self, workspace_name: str, config_name: str, new_config_name: str):
        self.workspace_manager.copy_config(workspace_name, config_name, new_config_name)

    def rename_config(self, workspace_name: str, config_name: str, new_config_name: str):
        self.workspace_manager.rename_config(workspace_name, config_name, new_config_name)

    def get_current_config(self, workspace_name: str) -> dict:
        return {
            "name": self.workspace_manager.get_current_config_name(workspace_name)
        }

    def set_current_config(self, workspace_name: str, config_name: str):
        self.workspace_manager.set_current_config_name(workspace_name, config_name)

    def get_configs(self, workspace_name: str, config_name: str) -> dict:
        chd_config_json, chd_order = self.workspace_manager.get_config_json(workspace_name, config_name, "CHD")
        cnf_config_json, cnf_order = self.workspace_manager.get_config_json(workspace_name, config_name, "CNF")
        cst_config_json, cst_order = self.workspace_manager.get_config_json(workspace_name, config_name, "CST")
        return {
            "name": config_name,
            "chd": chd_config_json,
            "chd_order": chd_order,
            "cnf": cnf_config_json,
            "cnf_order": cnf_order,
            "cst": cst_config_json,
            "cst_order": cst_order
        }

    def get_default_config_versions(self) -> dict:
        chd_version, cnf_version, cst_version = self.workspace_manager.get_all_default_config_version()
        return {
            "chd_version": chd_version,
            "cnf_version": cnf_version,
            "cst_version": cst_version
        }

    def save_configs(self, workspace_name: str, config_name: str, configurations: dict):
        chd = json.dumps(configurations.get("chd"), indent=4, separators=(',', ': '), sort_keys=True)
        self.workspace_manager.write_config_file(workspace_name, config_name, "CHD", chd)
        cnf = json.dumps(configurations.get("cnf"), indent=4, separators=(',', ': '), sort_keys=True)
        self.workspace_manager.write_config_file(workspace_name, config_name, "CNF", cnf)
        cst = json.dumps(configurations.get("cst"), indent=4, separators=(',', ': '), sort_keys=True)
        self.workspace_manager.write_config_file(workspace_name, config_name, "CST", cst)

    def process(self, process_name: str, workspace_name: str, config_name: str, output_path, l1a_file: str,
                monitor: Monitor):
        chd_file = self.workspace_manager.get_config_file(workspace_name, config_name, "CHD")
        cnf_file = self.workspace_manager.get_config_file(workspace_name, config_name, "CNF")
        cst_file = self.workspace_manager.get_config_file(workspace_name, config_name, "CST")
        processor = L1BProcessor(process_name, cnf_file, cst_file, chd_file, output_path, skip_l1bs=False)
        processor.process(l1a_file, monitor=monitor)

    def upgrade_configs(self, workspace_name: str, config_name: str):
        self.workspace_manager.upgrade_all_config(workspace_name, config_name)
        return self.get_configs(workspace_name, config_name)

    def get_output_names(self, workspace_name: str, config_name: str) -> List[str]:
        return self.workspace_manager.get_output_names(workspace_name, config_name)

    def remove_output_files(self, workspace_name: str, config_name: str):
        self.workspace_manager.remove_outputs(workspace_name, config_name)

    def inspect_output(self, workspace_name: str, output_file_path: str):
        self.workspace_manager.inspect_l1b_product(workspace_name, output_file_path)

    def compare_outputs(self, workspace_name: str, output1_file_path: str, output2_file_path: str):
        self.workspace_manager.compare_l1b_products(workspace_name, output1_file_path, output2_file_path)

    def get_notebook_file_names(self, workspace_name: str):
        return self.workspace_manager.get_notebook_names(workspace_name)

    def launch_notebook(self, workspace_name: str, notebook_name: str):
        notebook_dir = os.path.join(self.workspace_manager.get_workspace_path(workspace_name), 'notebooks')
        notebook_path = os.path.join(notebook_dir, notebook_name)
        return self.workspace_manager.launch_notebook('DeDop - %s' % notebook_name, notebook_dir, notebook_path)

    @staticmethod
    def get_lat_lon(input_file_path) -> dict:
        ds = Dataset(input_file_path)
        latitude = ds['lat_l1a_echo_sar_ku'][:].tolist() if 'lat_l1a_echo_sar_ku' in ds.variables.keys() else []
        longitude = ds['lon_l1a_echo_sar_ku'][:].tolist() if 'lon_l1a_echo_sar_ku' in ds.variables.keys() else []
        ds.close()
        return {
            "lat": latitude,
            "lon": longitude
        }

    @staticmethod
    def get_max_min_coordinates(input_file_path) -> dict:
        ds = Dataset(input_file_path)
        latitude = ds['lat_l1a_echo_sar_ku'][:].tolist() if 'lat_l1a_echo_sar_ku' in ds.variables.keys() else []
        longitude = ds['lon_l1a_echo_sar_ku'][:].tolist() if 'lon_l1a_echo_sar_ku' in ds.variables.keys() else []
        ds.close()
        return {
            "lat": [latitude[0], latitude[-1]],
            "lon": [longitude[0], longitude[-1]]
        }

    @staticmethod
    def get_global_attributes(input_file_path) -> dict:
        ds = Dataset(input_file_path)
        global_attributes = ds.__dict__
        ds.close()
        return global_attributes
