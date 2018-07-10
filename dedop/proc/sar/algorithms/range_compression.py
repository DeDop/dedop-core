import numpy as np
from numpy.fft import fft, fftshift

from dedop.model import SurfaceData
from ..base_algorithm import BaseAlgorithm

class RangeCompressionAlgorithm(BaseAlgorithm):
    def __call__(self, working_surface_location: SurfaceData) -> None:
        """
        compute range compression for teh current surface

        :param working_surface_location: current surface
        """
        # calc. size after zero padding factor applied
        padded_size = self.zp_fact_range * self.chd.n_samples_sar
        stack_size = min(working_surface_location.data_stack_size, self.n_looks_stack)

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
            # NB: in some early L1A data products, the waveforms had had one-too-many or one-too-few FFT shifts applied.
            #     this meant that the L1B/L1B-S files produced by DeDop would also have incorrectly swapped waveforms.
            #     to prevent this problem, we previously disabled the following FFT shift, (with the line `beam_shift =
            #     beam_fft`), however, current L1As do not have this problem, so we apply the shift as expected.
            beam_shift = fftshift(beam_fft) # / padded_size

            # store complex result
            self.beam_range_compr_iq[beam_index, :] = beam_shift

            # compute square modulus
            self.beam_range_compr[beam_index, :] =\
                np.abs(beam_shift) ** 2
