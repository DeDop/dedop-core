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
        self.sigma0_scaling_factor_beam = np.zeros(
            (working_surface_location.data_stack_size,),
            dtype=np.float64
        )
        max_stack = min(working_surface_location.data_stack_size, self.cnf.n_looks_stack)

        sigma0_offset =\
            10 * log10(64) +\
            30 * log10(self.cst.pi) -\
            10 * log10(self.chd.power_tx_ant_ku) -\
            2 * self.chd.antenna_gain_ku -\
            20 * log10(wavelength_ku) +\
            self.chd.ratio_trc_ku +\
            10 * log10(self.chd.n_ku_pulses_burst) # Np_PTR_SAR_Ku

            
        for beam_index in range(max_stack):
            range_sat_surf = working_surface_location.range_sat_surf[beam_index]
            burst = working_surface_location.stack_bursts[beam_index]

            vel_sat_sar_norm =\
                burst.vel_sat_sar_norm

            pri_sar_pre_dat =\
                burst.pri_sar_pre_dat

            with np.errstate(divide='ignore'):
                azimuth_distance =\
                    (1 + range_sat_surf / self.cst.earth_radius) *\
                    wavelength_ku * range_sat_surf / pri_sar_pre_dat /\
                    (2 * vel_sat_sar_norm * self.chd.n_ku_pulses_burst)
            range_distance = 2 * sqrt(
                self.cst.c * range_sat_surf * self.chd.ptr_width *
                self.cst.earth_radius / (self.cst.earth_radius + range_sat_surf)
            )
            surface_area = azimuth_distance * range_distance * 0.886

            self.sigma0_scaling_factor_beam[beam_index] = -1. * (sigma0_offset +
                40 * log10(range_sat_surf) - 10 * log10(surface_area) - #burst.agc_ku)
                working_surface_location.closest_burst.agc_ku)

        self.sigma0_scaling_factor = np.mean(self.sigma0_scaling_factor_beam)
        return self.sigma0_scaling_factor
