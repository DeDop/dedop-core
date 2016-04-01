from ..base_algorithm import BaseAlgorithm

import numpy as np
from math import sqrt

class RangeCompressionAlgorithm(BaseAlgorithm):
    def __call__(self, working_surface_location):
        padded_size = self.zp_fact_range * self.chd.n_samples_sar

        self.beams_range_corr = np.zeros(
            (working_surface_location.data_stack_size, padded_size)
        )

        for beam_index in range(working_surface_location.data_stack_size):
            beam_zp = np.zeros(
                (padded_size, self.chd.n_looks_stack), dtype=complex
            )

            copy_len = len(working_surface_location.beams_geo_corr[beam_index, :])
            beam_zp[:copy_len] = working_surface_location.beams_geo_corr[beam_index, :]

            beam_fft = np.fft.fft(beam_zp)

            beam_shift = np.zeros(
                (padded_size, self.chd.n_looks_stack), dtype=complex
            )
            half_len = (self.chd.n_samples_sar * self.zp_fact_range) / 2
            beam_shift[:half_len] = beam_fft[half_len:]
            beam_shift[half_len:] = beam_fft[:half_len]

            self.beams_range_corr[beam_index, :] = np.abs(beam_shift) / sqrt(self.chd.n_samples_sar)

        return self.beams_range_corr