from ..input_dataset import InputDataset
from .datafile import CryosatDatafile


class CryosatDataset(InputDataset):
    def __init__(self, filename, cst):
        dset = CryosatDatafile(filename)
        super().__init__(dset, cst)
