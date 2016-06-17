import json
from typing import Any

class ConstantsFileReader:
    def __init__(self, filename: str=None, **kwargs: Any):
        if filename is not None:
            with open(filename) as input_file:
                self._data = {
                    k: v['value'] for k, v in json.load(input_file).items()
                }
        else:
            self._data = {}

        self._data.update(kwargs)

    def __getitem__(self, name: str) -> Any:
        return self._data[name]
