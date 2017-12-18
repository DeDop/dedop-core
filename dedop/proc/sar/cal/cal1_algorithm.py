from ..base_algorithm import BaseAlgorithm
from dedop.model.l1a_processing_data import L1AProcessingData

import numpy as np
import math as m


class CAL1Algorithm(BaseAlgorithm):
    def __call__(self, burst: L1AProcessingData) -> None:
        if self.cnf.flag_cal1_corrections:
            fixed_gain = burst.agc_ku - burst.sig0_cal_ku

            samples = np.ones((1, self.chd.n_samples_sar))
            correction = np.sqrt(burst.cal1_power) * np.exp(1j*burst.cal1_phase) / m.sqrt(10 ** (fixed_gain / 10))
            # correction = (np.power(10, burst.cal1_power / 20)[:, np.newaxis] * samples) *\
            #               np.exp(1j * (burst.cal1_phase[:, np.newaxis] * samples)) / np.sqrt(10 ** (fixed_gain / 10))

            burst.waveform_cor_sar *= correction[:, np.newaxis] * samples
