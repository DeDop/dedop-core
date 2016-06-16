from ..base_algorithm import BaseAlgorithm
from ....util.parameter import Parameter

import numpy as np
from numpy.linalg import norm
from math import sqrt, log10

from ..surface_location_data import SurfaceLocationData


class Sigma0ScalingFactorAlgorithm(BaseAlgorithm):
    def __call__(self, working_surface_location: SurfaceLocationData, wavelength_ku: float,
                 chirp_slope_ku: float) -> float:
        """
        calculates the sigma0 scaling factor

        :param working_surface_location:
        :return:
        """
        sigma0_scaling_factor_beam = np.zeros(
            (working_surface_location.data_stack_size),
            dtype=np.float64
        )
        for beam_index in range(working_surface_location.data_stack_size):
            range_sat_surf = working_surface_location.range_sat_surf[beam_index]

            vel_sat_sar_norm = norm(
                working_surface_location.stack_bursts[beam_index].vel_sat_sar
            )
            pri_sar_pre_dat =\
                working_surface_location.stack_bursts[beam_index].pri_sar_pre_dat

            azimuth_distance =\
                (1 + range_sat_surf) / self.cst.earth_radius *\
                wavelength_ku * range_sat_surf / pri_sar_pre_dat /\
                (2 * vel_sat_sar_norm * self.chd.n_ku_pulses_burst)
            range_distance = 2 * sqrt(
                self.cst.c * range_sat_surf /
                (self.chd.pulse_length * chirp_slope_ku) *
                self.cst.earth_radius / (self.cst.earth_radius + range_sat_surf)
            )
            surface_area = azimuth_distance * range_distance

            sigma0_scaling_factor_beam[beam_index] = 10 * log10(64) +\
                30 * log10(self.cst.pi) + 40 * log10(range_sat_surf) -\
                10 * log10(self.chd.power_tx_ant_ku) - 2 * self.chd.antenna_gain_ku -\
                20 * log10(wavelength_ku) - 10 * log10(surface_area) +\
                10 * log10(self.chd.n_samples_sar * self.zp_fact_range) -\
                10 * log10(self.chd.pulse_length * self.chd.pulse_length * chirp_slope_ku)

        self.sigma0_scaling_factor = np.mean(sigma0_scaling_factor_beam)
        return self.sigma0_scaling_factor