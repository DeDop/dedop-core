import json
import os
from os import path


class Preferences:
    def __init__(self, name, dir_path=None, ext='prefs'):
        self.name = name
        self.data = dict()
        if not dir_path:
            dir_path = path.join(path.expanduser("~"), '.dedop')
        self.file = path.join(dir_path, name + '.' + ext)

    def exists(self):
        return path.exists(self.file)

    def load(self):
        if self.exists():
            with open(self.file) as fp:
                self.data = json.load(fp)

    def store(self):
        data_dir = path.dirname(self.file)
        if not path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        with open(self.file, 'w') as fp:
            json.dump(self.data, fp, sort_keys=True, indent='    ')

    def get(self, qualified_name, default_value=None):
        names = qualified_name.split('.')
        parent = self.data
        max_name_index = len(names) - 1
        for i in range(max_name_index):
            name = names[i]
            if not _is_dict_key(parent, name):
                return default_value
            parent = parent[name]
        name = names[max_name_index]
        if name in parent:
            return parent[name]
        else:
            return default_value

    def set(self, qualified_name, value):
        names = qualified_name.split('.')
        parent = self.data
        max_name_index = len(names) - 1
        for i in range(max_name_index):
            name = names[i]
            if not _is_dict_key(parent, name):
                parent[name] = dict()
            parent = parent[name]
        name = names[max_name_index]
        parent[name] = value

def _is_dict_key(parent, name):
    return name in parent and hasattr(parent[name], '__getitem__')

