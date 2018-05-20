import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
from typing import List
import warnings

from dedop.model import SurfaceData
from ..base_algorithm import BaseAlgorithm
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.util.parameter import Parameter


def gauss(x, a, b, c):
    """
    describes a gaussian curve at positions in 'x',
    according to the parameters a, b, c.
    """
    return a * np.exp(-(x - b) ** 2 / (c ** 2))


def gauss_fit(x: np.ndarray, y: np.ndarray) -> List[float]:
    """attempt to fit a gaussian curve to the data described
    by x & y. Returns the fitting parameters"""

    # skip infinite values
    valid = np.isfinite(x) * np.isfinite(y)
    x = x[valid]
    y = y[valid]

    with warnings.catch_warnings():
        warnings.simplefilter("error", OptimizeWarning)

        try:
            fit_params, _ = curve_fit(
                gauss, x, y
            )
        except (RuntimeError, OptimizeWarning, TypeError):
            return [1, 1, 1]

    return fit_params


@Parameter("flag_avoid_zeros_in_multilooking", default_value=False)
class MultilookingAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile, cnf: ConfigurationFile):
        super().__init__(chd, cst, cnf)

        self.start_look_angle = 0
        self.stop_look_angle = 0
        self.start_doppler_angle = 0
        self.stop_doppler_angle = 0
        self.start_pointing_angle = 0
        self.stop_pointing_angle = 0
        self.look_angle_centre = 0
        self.pointing_angle_centre = 0
        self.start_beam_angle = 0
        self.stop_beam_angle = 0
        self.start_burst_index = 0
        self.stop_burst_index = 0

        self.stack_std = None
        self.stack_max = None
        self.stack_skewness = None
        self.stack_kurtosis = None

        self.n_beams_start_stop = 0
        self.n_beams_multilooking = 0

    def __call__(self, working_surface_location: SurfaceData) -> None:
        """
        compute multilooking for the current surface

        :param working_surface_location: current surface
        """
        # TODO: FLAG SURFACE WEIGHTING

        self.compute_stack_characterization_params(working_surface_location)

        beams_masked_aw = self.apply_antenna_weighting(working_surface_location, self.cnf.flag_antenna_weighting)

        self.compute_multilooking(working_surface_location, beams_masked_aw)

    def compute_stack_characterization_params(self, working_surface_location: SurfaceData) -> None:
        """
        compute stack characterization parameters for the current surface

        :param working_surface_location: current surface
        """
        beam_power = np.zeros((working_surface_location.data_stack_size,), dtype=np.float64)

        max_beam_power = 0

        beam_angles_complementary = np.abs(
            self.cst.pi / 2. - working_surface_location.beam_angles_surf
        )

        # find index and value of minimum complementary angle
        min_beam_angle_complementary_index =\
            np.argmin(beam_angles_complementary)

        beam_length = (self.chd.n_samples_sar // 2) * self.zp_fact_range

        max_stack = min(self.n_looks_stack, working_surface_location.data_stack_size)
        for beam_index in range(max_stack):
            beam_power[beam_index] =\
                np.sum(
                    working_surface_location.beams_masked[beam_index, :beam_length]
                )
            if beam_power[beam_index] > max_beam_power:
                max_beam_power = beam_power[beam_index]

        # only the central 249 beams will be used in the gaussian fitting:
        # the doppler-central beam, 124 to the left and 124 to the right.
        last_right_beam = min(min_beam_angle_complementary_index + 124,
                              max_stack - 1)
        first_left_beam = max(min_beam_angle_complementary_index - 124,
                              0)
        # the parameters and arrays for the gaussian fitting
        n_samples_fitting = last_right_beam - first_left_beam + 1

        beam_power_center = np.empty((n_samples_fitting,), dtype=np.float64)
        look_angles_surf_center = np.empty((n_samples_fitting,), dtype=np.float64)
        pointing_angles_surf_center = np.empty((n_samples_fitting,), dtype=np.float64)

        for beam_index in range(first_left_beam, last_right_beam+1):
            rel_beam_index = beam_index - first_left_beam

            beam_power_center[rel_beam_index] =\
                beam_power[beam_index] / max_beam_power
            look_angles_surf_center[rel_beam_index] =\
                working_surface_location.look_angles_surf[beam_index]
            pointing_angles_surf_center[rel_beam_index] =\
                working_surface_location.pointing_angles_surf[beam_index]

        x = np.arange(n_samples_fitting)

        fit_params_l = gauss_fit(look_angles_surf_center, beam_power_center)
        self.stack_max = fit_params_l[0]
        self.look_angle_centre = fit_params_l[1]
        self.stack_std = fit_params_l[2] / 2

        fit_params_p = gauss_fit(pointing_angles_surf_center, beam_power_center)
        self.pointing_angle_centre = fit_params_p[1]

        fit_params = gauss_fit(x, beam_power_center)

        power_fitted = gauss(x, *fit_params)

        power_fitted_mean = np.mean(
            power_fitted
        )
        power_fitted_std = np.std(
            power_fitted
        )

        self.stack_skewness = 0
        self.stack_kurtosis = 0

        for sample_index in range(n_samples_fitting):
            self.stack_skewness +=\
                ((power_fitted[sample_index] - power_fitted_mean) / power_fitted_std) ** 3
            self.stack_kurtosis += \
                ((power_fitted[sample_index] - power_fitted_mean) / power_fitted_std) ** 4

        self.stack_skewness /= n_samples_fitting
        self.stack_kurtosis = self.stack_kurtosis / n_samples_fitting - 3

    def apply_antenna_weighting(self, surface: SurfaceData, apply_weighting: bool = True) -> np.ndarray:
        """
        apply the antenna weighting ( if apply_weighting is True )

        :param surface: the current surface
        :param apply_weighting: weighting toggle
        """

        if apply_weighting:
            # create array for weighted beams
            beams_masked_aw = np.empty(surface.beams_masked.shape, dtype=np.float64)
            for beam_index in range(min(surface.data_stack_size, self.cnf.n_looks_stack)):
                # get the angle at the current index
                pointing_angle = surface.pointing_angles_surf[beam_index]
                # get the weighting for the current angle
                antenna_weight = self._select_weight_from_angle(pointing_angle)
                # apply the weighting to the current beam
                beams_masked_aw[beam_index, :] = surface.beams_masked[beam_index, :] * antenna_weight
        else:
            # just return the un-weighted beams
            beams_masked_aw = surface.beams_masked

        return beams_masked_aw

    def _select_weight_from_angle(self, angle: float) -> float:
        """
        returns the weighting for the provided pointing angle

        :param angle: pointing angle
        """
        if angle <= self.chd.antenna_angles[0]:
            # angle is at or below min. angle
            selected_weight = self.chd.antenna_weights[0]
        elif angle >= self.chd.antenna_angles[-1]:
            # angle is at or above max. angle
            selected_weight = self.chd.antenna_weights[-1]
        else:
            # angle is within range - interpolate value
            weight_index = (angle - self.chd.antenna_angles[0]) / self.chd.antenna_angles_spacing

            index_left = int(weight_index)
            index_right = index_left + 1

            weight_left = self.chd.antenna_weights[index_left]
            weight_right = self.chd.antenna_weights[index_right]

            # get proportion between the left & right weights
            alpha = (angle - weight_left) / self.chd.antenna_angles_spacing
            # interpolate value
            selected_weight = weight_left + alpha * (weight_right - weight_left)

        return selected_weight

    def compute_multilooking(self, surface: SurfaceData, weighted_beams: np.ndarray) -> None:
        """
        apply the multi-looking

        :param surface: the current surface
        :param weighted_beams: the input beams with weighting applied
        """
        start_beam_index = None
        stop_beam_index = None

        self.n_beams_multilooking = 0

        n_samples_max = self.chd.n_samples_sar * self.zp_fact_range

        self.waveform_multilooked = np.zeros(
            (n_samples_max,), dtype=np.float64
        )
        self.sample_counter = np.zeros(
            (n_samples_max,), dtype=np.float64
        )
        self.stack_mask_vector_start_stop = np.zeros(
            (self.n_looks_stack,),
            dtype=surface.stack_mask_vector.dtype
        )
        self.beam_angles_start_stop = np.zeros(
            (self.n_looks_stack,),
            dtype=surface.beam_angles_surf.dtype
        )
        self.look_angles_start_stop = np.zeros(
            (self.n_looks_stack,),
            dtype=surface.look_angles_surf.dtype
        )

        max_stack = min(self.n_looks_stack, surface.data_stack_size)
        for beam_index in range(max_stack):

            if surface.stack_mask_vector[beam_index] != 0:

                self.n_beams_multilooking += 1

                if start_beam_index is None:
                    start_beam_index = beam_index
                stop_beam_index = beam_index

            else:
                continue

            if self.flag_avoid_zeros_in_multilooking:
               mask = surface.stack_mask[beam_index, :]
            else:
               mask = 1
            self.waveform_multilooked[:] += weighted_beams[beam_index, :] * mask
            self.sample_counter[:] += mask

        self.waveform_multilooked /= self.sample_counter

        if stop_beam_index is None or start_beam_index is None:
            self.n_beams_start_stop = 0
            self.start_look_angle = 0
            self.stop_look_angle = 0
            self.start_doppler_angle = 0
            self.stop_doppler_angle = 0
            self.start_pointing_angle = 0
            self.stop_pointing_angle = 0
            self.start_beam_angle = 0
            self.stop_beam_angle = 0
            self.start_burst_index = 0
            self.stop_burst_index = 0
            return

        self.n_beams_start_stop = stop_beam_index - start_beam_index + 1

        self.start_look_angle =\
            surface.look_angles_surf[start_beam_index]
        self.stop_look_angle =\
            surface.look_angles_surf[stop_beam_index]

        self.start_doppler_angle = \
            surface.doppler_angles_surf[start_beam_index]
        self.stop_doppler_angle = \
            surface.doppler_angles_surf[stop_beam_index]

        self.start_pointing_angle = \
            surface.pointing_angles_surf[start_beam_index]
        self.stop_pointing_angle = \
            surface.pointing_angles_surf[stop_beam_index]

        self.start_beam_angle = \
            surface.beam_angles_surf[start_beam_index]
        self.stop_beam_angle = \
            surface.beam_angles_surf[stop_beam_index]

        self.start_burst_index = \
            surface.stack_bursts[0].source_seq_count
        self.stop_burst_index = \
            surface.stack_bursts[max_stack-1].source_seq_count

        self.stack_mask_vector_start_stop[:self.n_beams_start_stop] =\
            surface.stack_mask_vector[start_beam_index:stop_beam_index+1]
        self.beam_angles_start_stop[:self.n_beams_start_stop] = \
            surface.beam_angles_surf[start_beam_index:stop_beam_index+1]
        self.look_angles_start_stop[:self.n_beams_start_stop] = \
            surface.look_angles_surf[start_beam_index:stop_beam_index+1]
