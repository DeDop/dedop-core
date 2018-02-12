import os.path
from ..version import __version__

DEFAULT_DATA_DIR_NAME = '.dedop'
DEFAULT_DATA_PATH = os.path.join(os.path.expanduser('~'), DEFAULT_DATA_DIR_NAME)
DEFAULT_WORKSPACE_NAME = 'default'
DEFAULT_WORKSPACE_PATH = os.path.join(DEFAULT_DATA_PATH, 'workspaces', DEFAULT_WORKSPACE_NAME)
DEFAULT_VERSION_DATA_PATH = os.path.join(DEFAULT_DATA_PATH, __version__)

ENV_LOCATION_FILE = os.path.join(DEFAULT_VERSION_DATA_PATH, 'dedop.location')

#: allow a 100 ms period between two progress messages sent to the client
WEBAPI_PROGRESS_DEFER_PERIOD = 0.5

#: where a running WebAPI service logs to
WEBAPI_LOG_FILE_PREFIX = os.path.join(DEFAULT_VERSION_DATA_PATH, 'webapi.log')

#: By default, WebAPI service will auto-exit after 2 hours of inactivity, if WebAPI auto-exit enabled
WEBAPI_ON_INACTIVITY_AUTO_STOP_AFTER = 120 * 60.0
