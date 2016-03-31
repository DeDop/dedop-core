import json

class PropertyData(dict):
    def __getattr__(self, item):
        return self[item]


class ConstantsFileReader:
    def __init__(self, filename):
        with open(filename) as input_file:
            self._data = json.load(input_file)

    def __getitem__(self, name):
        return PropertyData(self._data[name])