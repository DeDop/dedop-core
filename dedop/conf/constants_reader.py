import json

class ConstantsFileReader:
    def __init__(self, filename=None, **kwargs):
        if filename is not None:
            with open(filename) as input_file:
                self._data = {
                    k: v['value'] for k, v in json.load(input_file).items()
                }
        else:
            self._data = {}

        self._data.update(kwargs)

    def __getitem__(self, name):
        return self._data[name]
