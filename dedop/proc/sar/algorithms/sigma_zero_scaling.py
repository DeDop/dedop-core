from math import sqrt, log10
import numpy as np

from dedop.model import SurfaceData
from ..base_algorithm import BaseAlgorithm


class Sigma0ScalingFactorAlgorithm(BaseAlgorithm):
    def __call__(self, working_surface_location: SurfaceData, wavelength_ku: float,
                 chirp_slope_ku: float) -> float:
        """
        calculates the sigma0 scaling factor

        :param working_surface_location: current surface
        :param wavelength_ku: ku band wavelength
        :param chirp_slope_ku: chirp slope
        """
        sigma0_scaling_factor_beam = np.zeros(
            (working_surface_location.data_stack_size,),
            dtype=np.float64
        )
        # TODO: come back to this and replace it with something less messy
        if self.n_looks_stack is not None:
            max_stack = min(working_surface_location.data_stack_size, self.n_looks_stack)
        else:
            max_stack = working_surface_location.data_stack_size  # TODO

        sigma0_offset = 10 * log10(64) - \
            10 * log10(self.chd.power_tx_ant_ku) - 2 * self.chd.antenna_gain_ku +\
            10 * log10(self.chd.n_samples_sar * self.zp_fact_range) -\
            10 * log10(self.chd.pulse_length * self.chd.pulse_length * chirp_slope_ku)
            
        for beam_index in range(max_stack):
            range_sat_surf = working_surface_location.range_sat_surf[beam_index]

            vel_sat_sar_norm =\
                working_surface_location.stack_bursts[beam_index].vel_sat_sar_norm

            pri_sar_pre_dat =\
                working_surface_location.stack_bursts[beam_index].pri_sar_pre_dat

            with np.errstate(divide='ignore'):
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

            sigma0_scaling_factor_beam[beam_index] = sigma0_offset +\
                30 * log10(self.cst.pi) + 40 * log10(range_sat_surf) -\
                20 * log10(wavelength_ku) - 10 * log10(surface_area)

        self.sigma0_scaling_factor = np.mean(sigma0_scaling_factor_beam)
        return self.sigma0_scaling_factor
