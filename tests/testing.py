import csv
import numpy as np
from ast import literal_eval

class TestDataLoader:
    _default_delim = '\t'

    def __init__(self, filepath, delim=None):
        if delim is None:
            delim = self._default_delim

        self._values = {}

        with open(filepath, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=delim)
            for row in reader:
                name, *values = filter(bool, row)

                vals = list(map(literal_eval, values))

                if len(vals) > 1:
                    vals = np.asarray(vals)
                elif vals:
                    vals = vals[0]
                else:
                    vals = None

                self._values[name] = vals

    def __getitem__(self, index):
        return self._values[index]

class MockObject(TestDataLoader):
    def __init__(self, filepath):
        super().__init__(filepath, ' ')

    def __getattr__(self, item):
        return self._values.get(item, None)