import numpy as np
from pyfftw.builders import fft
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile

from dedop.model import SurfaceData
from ..base_algorithm import BaseAlgorithm

class RangeCompressionAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile, cnf: ConfigurationFile):
        super().__init__(chd, cst, cnf)

    def __call__(self, working_surface_location: SurfaceData) -> None:
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

        # calc. FFT with zero-padding & orthogonal scaling
        fft_obj = fft(
            working_surface_location.beams_geo_corr, axis=1,
            n=padded_size, threads=4
        )
        beam_fft = fft_obj(working_surface_location.beams_geo_corr,
                           ortho=True, normalise_idft=False)

        # apply shift
        beam_shift = np.fft.fftshift(beam_fft, axes=1)[:stack_size]
        # TODO: REMOVE THIS !!
        # disable extra shift to fix alignment problem
        # beam_shift = beam_fft

        # store complex result
        self.beam_range_compr_iq[:stack_size, :] = beam_shift

        # compute square modulus
        self.beam_range_compr[:stack_size, :] =\
            np.abs(beam_shift) ** 2
