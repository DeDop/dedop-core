from math import sqrt, log10
import numpy as np

from dedop.model import SurfaceData
from dedop.conf.enums import AzimuthWindowingMethod
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

        # TODO: come back to this and replace it with something less messy
        max_stack = min(working_surface_location.data_stack_size, self.cnf.n_looks_stack)

        self.sigma0_scaling_factor_beam = np.zeros(
            (max_stack,), dtype=np.float64
        )

        sigma0_offset = 10 * log10(64) - \
            10 * log10(self.chd.power_tx_ant_ku) - 2 * self.chd.antenna_gain_ku +\
            30 * log10(self.cst.pi)

        for beam_index in range(max_stack):
            range_sat_surf = working_surface_location.range_sat_surf[beam_index]

            vel_sat_sar_norm =\
                working_surface_location.stack_bursts[beam_index].vel_sat_sar_norm

            pri_sar_pre_dat =\
                working_surface_location.stack_bursts[beam_index].pri_sar_pre_dat

            with np.errstate(divide='ignore'):
                azimuth_distance =\
                    (1 + range_sat_surf / self.cst.earth_radius) *\
                    wavelength_ku * range_sat_surf / pri_sar_pre_dat /\
                    (2 * vel_sat_sar_norm * self.chd.n_ku_pulses_burst)
            range_distance = 2 * sqrt(
                self.cst.c * range_sat_surf /
                (self.chd.pulse_length * chirp_slope_ku) *
                self.cst.earth_radius / (self.cst.earth_radius + range_sat_surf)
            )

            # TODO: apply factor based on window width?
            widening_factor = {
                AzimuthWindowingMethod.hamming: 1.486 * .92,
                AzimuthWindowingMethod.hanning: 1.0,  # fixme: add correct value
                AzimuthWindowingMethod.boxcar: 1.0,  # fixme: add correct value
                AzimuthWindowingMethod.disabled: 1.0
            }[self.cnf.flag_azimuth_windowing_method]
            surface_area = widening_factor * azimuth_distance * range_distance * .886

            self.sigma0_scaling_factor_beam[beam_index] = sigma0_offset +\
                40 * log10(range_sat_surf) - 20 * log10(wavelength_ku) - 10 * log10(surface_area)

        self.sigma0_scaling_factor = np.mean(self.sigma0_scaling_factor_beam)
        return self.sigma0_scaling_factor, self.sigma0_scaling_factor_beam
