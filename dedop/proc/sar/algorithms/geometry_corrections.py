import numpy as np
from numpy.linalg import norm

from ..base_algorithm import BaseAlgorithm


class GeometryCorrectionsAlgorithm(BaseAlgorithm):

    def __call__(self, working_surface_location, wv_length_ku):
        self.beams_geo_corr = np.zeros(
            (self.n_looks_stack, self.chd.n_samples_sar),
            dtype=complex
        )
        self.slant_range_corrections = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.range_sat_surf = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.doppler_corrections = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.win_delay_corrections = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )

        win_delay_ref = working_surface_location.win_delay_surf

        for beam_index in range(0, working_surface_location.data_stack_size):

            stack_burst = working_surface_location.stack_bursts[beam_index]

            self.compute_doppler_correction(
                working_surface_location, stack_burst, beam_index, wv_length_ku
            )
            self.compute_slant_range_correction(
                working_surface_location, stack_burst, beam_index
            )
            self.compute_win_delay_misalignments_correction(
                working_surface_location, stack_burst, beam_index, win_delay_ref
            )
            self.apply_corrections(
                working_surface_location, stack_burst, beam_index
            )

    def compute_doppler_correction(self, working_surface_location, stack_burst, beam_index, wv_length_ku):
        doppler_range = \
            -self.cst.c / wv_length_ku *\
            norm(stack_burst.vel_sat_sar) *\
            np.cos(working_surface_location.beam_angles_surf[beam_index]) *\
            self.chd.pulse_length / self.chd.bw_ku

        self.doppler_corrections[beam_index] =\
            2 / self.cst.c * doppler_range / working_surface_location.t0_surf[beam_index]

    def compute_slant_range_correction(self, working_surface_location, stack_burst, beam_index):
        isp_orbit_surf_ground_vector = np.matrix([
            [stack_burst.x_sar_sat - working_surface_location.x_surf],
            [stack_burst.y_sar_sat - working_surface_location.y_surf],
            [stack_burst.z_sar_sat - working_surface_location.z_surf]
        ])

        self.range_sat_surf[beam_index] = norm(
            isp_orbit_surf_ground_vector
        )

        slant_range_correction_time =\
            working_surface_location.win_delay_surf -\
            self.range_sat_surf[beam_index] * 2. / self.cst.c

        self.slant_range_corrections[beam_index] =\
            slant_range_correction_time / working_surface_location.t0_surf[beam_index]

    def compute_win_delay_misalignments_correction(self, working_surface_location, stack_burst, beam_index,
                                                   win_delay_ref):
        self.win_delay_corrections[beam_index] =\
            -(win_delay_ref - stack_burst.win_delay_sar_ku) /\
            working_surface_location.t0_surf[beam_index]

    def apply_corrections(self, working_surface_location, stack_burst, beam_index):
        shift = self.doppler_corrections[beam_index] +\
                self.slant_range_corrections[beam_index] +\
                self.win_delay_corrections[beam_index]

        sampleCorrectionPhaseConstant =\
            2j * self.cst.pi / self.chd.n_samples_sar * shift


        def transform(sample_index, beam_sample):
            sample_correction = np.exp(
                sampleCorrectionPhaseConstant * float(sample_index)
            )

            return beam_sample * sample_correction

        self.beams_geo_corr[beam_index, :] = np.asarray([
            transform(i, sample) for i, sample in
                enumerate(working_surface_location.beams_surf[beam_index, :])
        ])
