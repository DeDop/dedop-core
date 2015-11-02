class InputDataset:
    def __init__(self, dataset):
        self._dset = dataset

    def close(self):
        self._dset.close()

