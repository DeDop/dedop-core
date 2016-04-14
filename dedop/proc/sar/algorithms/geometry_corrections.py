import numpy as np
from numpy.linalg import norm

from ....io.consts import chd, cnf, cst
from ..base_algorithm import BaseAlgorithm

class GeometryCorrectionsAlgorithm(BaseAlgorithm):

    def __init__(self, chd, cst):
        self.slant_range_corrections = []
        self.range_sat_surf = []
        self.doppler_corrections = []
        self.win_delay_corrections = []

        super().__init__(chd, cst)

    def __call__(self, working_surface_location):
        beam_geo_corr = np.zeros(
            (chd.N_samples_sar, self.n_looks_stack),
            dtype=complex
        )
        win_delay_ref = working_surface_location.win_delay_surf

        for beam_index in range(0, working_surface_location.data_stack_size):

            stack_burst = working_surface_location.stack_bursts[beam_index]

            self.computeDopplerCorrection(
                working_surface_location, stack_burst, beam_index
            )
            self.computeSlantRangeCorrection(
                working_surface_location, stack_burst, beam_index
            )
            self.computeWinDelayMisalignmentsCorrection(
                working_surface_location, stack_burst, beam_index, win_delay_ref
            )
            self.applyCorrections(
                working_surface_location, stack_burst, beam_index
            )

    def computeDopplerCorrection(self, working_surface_location, stack_burst, beam_index):
        doppler_range = \
            -cst.c / chd.wv_length_ku *\
            norm(stack_burst.vel_sat_sar) *\
            np.cos(working_surface_location.beam_angles_surf[beam_index]) *\
            chd.pulse_length / chd.bw_ku

        self.doppler_corrections[beam_index] =\
            2 / cst.c * doppler_range / working_surface_location.t0_surf[beam_index]

    def computeSlantRangeCorrection(self, working_surface_location, stack_burst,  beam_index):
        isp_orbit_surf_ground_vector =\
            stack_burst.pos_sar_sat - working_surface_location.pos_surf

        self.range_sat_surf[beam_index] = norm(
            isp_orbit_surf_ground_vector
        )

        slant_range_correction_time =\
            win_delay_ref - self.range_sat_surf[beam_index] * 2 / cst.c

        self.slant_range_corrections[beam_index] =\
            slant_range_correction_time / working_surface_location.t0_surf[beam_index]

    def computeWinDelayMisalignmentsCorrection(self, working_surface_location, stack_burst, beam_index, win_delay_ref):
        self.win_delay_corrections[beam_index] =\
            -(win_delay_ref - stack_burst.win_delay_sar_ku) /\
            working_surface_location.t0_surf[beam_index]

    def applyCorrections(self, working_surface_location, stack_burst, beam_index):
        shift = self.doppler_corrections[beam_index] +\
                self.slant_range_corrections[beam_index] +\
                self.win_delay_corrections[beam_index]

        sampleCorrectionPhaseConstant = 2j * cst.pi / chd.N_samples_sar * shift

        def transform(sample_index, beam_sample):
            sample_correction = np.exp(
                sampleCorrectionPhaseConstant * sample_index
            )

            return beam_sample * sample_correction

        working_surface_location.beams_surf = [
            transform(i, sample) for i, sample in\
                enumerate(working_surface_location.beams_surf)
        ]

