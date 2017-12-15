from ..base_algorithm import BaseAlgorithm
from dedop.model.l1a_processing_data import L1AProcessingData

import numpy as np
from numpy.fft import fftshift, fft, ifftshift, ifft


class CAL2Algorithm(BaseAlgorithm):
    def __call__(self, burst: L1AProcessingData) -> None:
        if self.cnf.flag_cal2_correction:
            pulses = np.ones((self.chd.n_ku_pulses_burst, 1))
            correction = burst.cal2_array[np.newaxis, :] * pulses

            wfm_fft = fftshift(fft(burst.waveform_cor_sar, self.chd.n_samples_sar, 1), 1)
            burst.waveform_cor_sar = ifft(ifftshift(wfm_fft / np.sqrt(correction), 1), self.chd.n_samples_sar, 1)
