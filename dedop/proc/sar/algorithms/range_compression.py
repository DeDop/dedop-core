import numpy as np
from numpy.fft import fft, fftshift

from dedop.model import SurfaceData
from ..base_algorithm import BaseAlgorithm

class RangeCompressionAlgorithm(BaseAlgorithm):
    def __call__(self, working_surface_location: SurfaceData) -> None:
        # calc. size after zero padding factor applied
        padded_size = self.zp_fact_range * self.chd.n_samples_sar
        stack_size = working_surface_location.data_stack_size

        # create empty output arrays
        self.beam_range_compr = np.empty(
            (stack_size, padded_size),
            dtype=np.float64
        )
        self.beam_range_compr_iq = np.empty(
            (stack_size, padded_size),
            dtype=np.complex128
        )

        for beam_index in range(stack_size):

            # calc. FFT with zero-padding & orthogonal scaling
            beam_fft = fft(
                working_surface_location.beams_geo_corr[beam_index, :],
                n=padded_size, norm="ortho"
            )
            # apply shift
            beam_shift = fftshift(beam_fft)

            # store complex result
            self.beam_range_compr_iq[beam_index, :] = beam_shift

            # compute square modulus
            self.beam_range_compr[beam_index, :] =\
                np.abs(beam_shift) ** 2