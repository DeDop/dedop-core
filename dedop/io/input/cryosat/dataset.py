from ..input_dataset import InputDataset
from .datafile import CryosatDatafile


class CryosatDataset(InputDataset):
    def __init__(self, filename):
        dset = CryosatDatafile(filename)
        InputDataset.__init__(self, dset)
