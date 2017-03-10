from cate.util import Monitor
from netCDF4 import Dataset
from typing import List

from dedop.ui.workspace_manager import WorkspaceManager


class WebSocketService:
    """
    Object which implements Cate's server-side methods.

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
        workspace_names = self.workspace_manager.get_workspace_names()
        return {
            "workspaces": workspace_names
        }

    def add_input_files(self, workspace_name: str, input_file_paths: List[str]):
        self.workspace_manager.add_inputs(workspace_name, input_file_paths, Monitor.NONE)

    def remove_input_files(self, workspace_name: str, input_names: str):
        self.workspace_manager.remove_inputs(workspace_name, input_names, Monitor.NONE)

    def get_all_configs(self, workspace_name: str) -> List[str]:
        return self.workspace_manager.get_config_names(workspace_name)

    def add_new_config(self, workspace_name: str, config_name: str):
        self.workspace_manager.create_config(workspace_name, config_name)

    def delete_config(self, workspace_name: str, config_name: str):
        self.workspace_manager.delete_config(workspace_name, config_name)

    def copy_config(self, workspace_name: str, config_name: str, new_config_name: str):
        self.workspace_manager.copy_config(workspace_name, config_name, new_config_name)

    def rename_config(self, workspace_name: str, config_name: str, new_config_name: str):
        self.workspace_manager.rename_config(workspace_name, config_name, new_config_name)

    def get_current_config(self, workspace_name: str) -> str:
        return self.workspace_manager.get_current_config_name(workspace_name)

    def set_current_config(self, workspace_name: str, config_name: str):
        self.workspace_manager.set_current_config_name(workspace_name, config_name)

    @staticmethod
    def get_global_attributes(input_file_path):
        ds = Dataset(input_file_path)
        return ds.__dict__
