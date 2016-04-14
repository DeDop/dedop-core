import csv
import numpy as np
from ast import literal_eval

class TestDataLoader:
    def __init__(self, filepath):
        self._values = {}

        with open(filepath, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            for row in reader:
                name, *values = filter(bool, row)

                self._values[name] = np.asarray(
                    list(map(literal_eval, values))
                )

    def __getitem__(self, index):
        return self._values[index]

class MockObject(TestDataLoader):
    def __getattr__(self, item):
        return self._values.get(item, None)