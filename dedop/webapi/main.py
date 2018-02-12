import sys, os
from datetime import date

from cate.util.web import JsonRpcWebSocketHandler
from cate.util.web.webapi import run_main, url_pattern, WebAPIRequestHandler, WebAPIExitHandler
from tornado.web import Application

from dedop.conf.defaults import WEBAPI_PROGRESS_DEFER_PERIOD, WEBAPI_LOG_FILE_PREFIX, DEFAULT_VERSION_DATA_PATH, \
    ENV_LOCATION_FILE
from dedop.ui.workspace_manager import WorkspaceManager
from dedop.version import __version__
from dedop.webapi.websocket import WebSocketService

CLI_NAME = 'dedop-webapi'
CLI_DESCRIPTION = 'Delay Doppler Altimeter Data (DeDop) Web API'


# noinspection PyAbstractClass
class WebAPIVersionHandler(WebAPIRequestHandler):
    def get(self):
        self.write_status_ok(content={'name': CLI_NAME,
                                      'version': __version__,
                                      'timestamp': date.today().isoformat()})


def service_factory(application):
    return WebSocketService(application.workspace_manager)


# All JSON REST responses should have same structure, namely a dictionary as follows:
#
# {
#    "status": "ok" | "error",
#    "error": optional error-details,
#    "content": optional content, if status "ok"
# }

def create_application():
    application = Application([
        (url_pattern('/'), WebAPIVersionHandler),
        (url_pattern('/exit'), WebAPIExitHandler),
        (url_pattern('/app'), JsonRpcWebSocketHandler, dict(service_factory=service_factory,
                                                            report_defer_period=WEBAPI_PROGRESS_DEFER_PERIOD)),
    ])
    application.workspace_manager = WorkspaceManager()
    return application


def main(args=None) -> int:
    if not os.path.exists(DEFAULT_VERSION_DATA_PATH):
        os.makedirs(DEFAULT_VERSION_DATA_PATH, exist_ok=True)
    if not os.path.exists(ENV_LOCATION_FILE):
        with open(ENV_LOCATION_FILE, "w+") as f:
            f.write(sys.prefix)
    return run_main(CLI_NAME, CLI_DESCRIPTION, __version__,
                    application_factory=create_application,
                    log_file_prefix=WEBAPI_LOG_FILE_PREFIX,
                    args=args)


if __name__ == "__main__":
    sys.exit(main())
