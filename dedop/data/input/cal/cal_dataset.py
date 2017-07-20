import netCDF4 as nc


class CALDataset:
    @property
    def cal1_power_array_correction(self):
        return self.dset.variables["cal1_p2p_amplitude_sar"][:]

    @property
    def cal1_phase_array_correction(self):
        return self.dset.variables["cal1_p2p_phase_sar"][:]

    @property
    def cal2_array_correction(self):
        return self.dset.variables["cal2_lpf_sar"][:]

    def __init__(self, filename):
        self.dset = nc.Dataset(filename)

        if "cal1_p2p_amplitude_sar" not in self.dset.variables:
            raise MissingCALVariableError(filename, "cal1_p2p_amplitude_sar")

        if "cal1_p2p_phase_sar" not in self.dset.variables:
            raise MissingCALVariableError(filename, "cal1_p2p_phase_sar")

        if "cal2_lpf_sar" not in self.dset.variables:
            raise MissingCALVariableError(filename, "cal2_lpf_sar")

    def close(self):
        self.dset.close()


class MissingCALVariableError(Exception):
    def __init__(self, filename, varname):
        msg = "CAL file \"{}\" does not contain the field: {}".format(filename, varname)
        super().__init__(msg)
