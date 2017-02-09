class WebSocketService:
    """
    Object which implements Cate's server-side methods.

    All methods receive inputs deserialized from JSON-RCP requests and must
    return JSON-serializable outputs.

    :param: workspace_manager The current workspace manager.
    """

    def __init__(self):
        print("WebSocketService created")

    def test_action(self, param1: str) -> dict:
        return {
            "status": "ok",
            "content": "successful test",
            "arg": param1
        }
