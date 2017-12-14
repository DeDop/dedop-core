from ..base_algorithm import BaseAlgorithm
from dedop.model.l1a_processing_data import L1AProcessingData

import numpy as np
from numpy.fft import fftshift, fft, ifftshift, ifft


class CAL2Algorithm(BaseAlgorithm):
    def __call__(self, burst: L1AProcessingData) -> None:
        if self.cnf.flag_cal2_correction:
            pulses = np.ones((self.chd.n_ku_pulses_burst, 1))

            aux = fftshift(fft(burst.waveform_cor_sar, self.chd.n_samples_sar, 2), 2)
            burst.waveform_cor_sar = ifft(ifftshift(aux * (pulses * burst.cal2_array),
                                                    2), self.chd.n_samples_sar, 2)
