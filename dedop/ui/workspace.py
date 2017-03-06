import os
import sys
from collections import OrderedDict

from dedop.conf.defaults import DEFAULT_DATA_PATH, DEFAULT_WORKSPACE_PATH


class Workspace:
    def __init__(self, workspace_dir, name, is_current=False):
        if workspace_dir:
            self._workspace_dir = workspace_dir
        elif not workspace_dir and not name:
            self._workspace_dir = DEFAULT_WORKSPACE_PATH
        else:
            self._workspace_dir = os.path.join(DEFAULT_DATA_PATH, 'workspaces', name)
        self._name = name
        self._is_current = is_current

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_current(self) -> bool:
        return self._is_current

    @property
    def workspace_dir(self) -> str:
        return self._workspace_dir

    @classmethod
    def get_workspace_dir(cls, base_dir, name) -> str:
        return os.path.join(base_dir, name)

    @classmethod
    def create(cls, base_dir: str, name: str = None) -> 'Workspace':
        return Workspace(base_dir, name)

    @classmethod
    def open(cls, base_dir: str, name: str) -> 'Workspace':
        if not os.path.isdir(cls.get_workspace_dir(base_dir, name)):
            raise WorkspaceError('not a valid workspace: %s' % base_dir)
        return Workspace(base_dir, name)

    def save(self):
        base_dir = self.base_dir
        try:
            if not os.path.isdir(base_dir):
                os.mkdir(base_dir)
            workspace_dir = self.workspace_dir
            if not os.path.isdir(workspace_dir):
                os.mkdir(workspace_dir)
            self._is_modified = False
        except (IOError, OSError) as e:
            raise WorkspaceError(e)

    @classmethod
    def from_json_dict(cls, json_dict):
        base_dir = json_dict.get('base_dir', None)
        workspace_name = json_dict.get('workspace_name', None)
        is_current = json_dict.get('is_current', False)
        return Workspace(base_dir, workspace_name, is_current=is_current)

    def to_json_dict(self):
        return OrderedDict([('workspace_dir', self.workspace_dir),
                            ('name', self.name),
                            ('is_current', self.is_current),
                            ])


class WorkspaceError(Exception):
    def __init__(self, cause, *args, **kwargs):
        if isinstance(cause, Exception):
            super(WorkspaceError, self).__init__(str(cause), *args, **kwargs)
            _, _, traceback = sys.exc_info()
            self.with_traceback(traceback)
        elif isinstance(cause, str):
            super(WorkspaceError, self).__init__(cause, *args, **kwargs)
        else:
            super(WorkspaceError, self).__init__(*args, **kwargs)
        self._cause = cause

    @property
    def cause(self):
        return self._cause
