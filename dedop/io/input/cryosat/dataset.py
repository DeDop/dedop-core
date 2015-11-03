from ..input_dataset import InputDataset
from .datafile import CryosatDatafile


class CryosatDataset(InputDataset):
    def __init__(self, filename):
        dset = CryosatDatafile(filename)
        InputDataset.__init__(self, dset)

        self.l1_mode_id_ku = CryosatArray(dset, 'time_orbit', 'mode_id_cr')
        self.time_day_ku = CryosatArray(dset, 'time_orbit', 'days')
        self.time_seconds_ku = CryosatArray(dset, 'time_orbit', 'seconds')


class CryosatArray:
    def __init__(self, dataset, group, variable):
        self.dset = dataset
        self.grp = group
        self.var = variable

    def __getitem__(self, index):
        if not isinstance(index, slice):
            return self.get_variable(index)
        start, stop, step = index.indices(self.dset.num_items * 20)
        return [
            self.get_variable(i) for i in range(start, stop, step)
        ]

    def get_variable(self, index):
        var_index = index % 20
        rec_index = index // 20

        grp = getattr(self.dset[rec_index], self.grp)
        return getattr(grp[var_index], self.var)
