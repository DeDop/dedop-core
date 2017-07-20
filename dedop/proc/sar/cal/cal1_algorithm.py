from ..base_algorithm import BaseAlgorithm
from dedop.data.input.cal import CALDataset
from dedop.conf import ConstantsFile, CharacterisationFile, ConfigurationFile
from dedop.model.l1a_processing_data import L1AProcessingData

import numpy as np


class CAL1Algorithm(BaseAlgorithm):
    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile, cnf: ConfigurationFile, cal_data: CALDataset):
        self.cal = cal_data
        super().__init__(chd, cst, cnf)

    def __call__(self, burst: L1AProcessingData) -> None:
        if self.cnf.flag_cal1_corrections:
            samples = np.ones((1, self.chd.n_samples_sar))
            correction = (np.power(10, self.cal.cal1_power_array_correction / 20)[:, np.newaxis] * samples) *\
                          np.exp(1j * (self.cal.cal1_phase_array_correction[:, np.newaxis] * samples))

            burst.waveform_cor_sar *= correction
