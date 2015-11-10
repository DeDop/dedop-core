class InputDataset:
    def __init__(self, dataset):
        self._dset = dataset

    def close(self):
        self._dset.close()

    def __iter__(self):
        for packet in self._dset:
            yield packet
