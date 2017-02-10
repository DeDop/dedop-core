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

    def test_action(self, param1: str) -> dict:
        return {
            "status": "ok",
            "content": "successful test",
            "arg": param1
        }

    def new_workspace(self, workspace_name) -> dict:
        workspace = self.workspace_manager.create_workspace(workspace_name)
        return workspace.to_json_dict()

    def delete_workspace(self, workspace_name) -> None:
        self.workspace_manager.delete_workspace(workspace_name)
