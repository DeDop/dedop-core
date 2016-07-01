import numpy as np
from scipy.optimize import curve_fit
from typing import List

from dedop.model import SurfaceData
from ..base_algorithm import BaseAlgorithm
from ....conf import CharacterisationFile, ConstantsFile
from ....util.parameter import Parameter


def gauss(x, a, b, c):
    """
    describes a gaussian curve at positions in 'x',
    according to the parameters a, b, c.
    """
    return a * np.exp(-(x - b) ** 2 / (c ** 2))


def gauss_fit(x: np.ndarray, y: np.ndarray) -> List[float]:
    """attempt to fit a gaussian curve to the data descibed
    by x & y. Returns the fitting parameters"""

    try:
        fit_params, _ = curve_fit(
            gauss, x, y
        )
    except RuntimeError:
        return [1, 1, 1]

    return fit_params


@Parameter("flag_avoid_zeros_in_multilooking", default_value=False)
class MultilookingAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile):
        super().__init__(chd, cst)

        self.start_look_angle = 0
        self.stop_look_angle = 0
        self.start_doppler_angle = 0
        self.stop_doppler_angle = 0
        self.start_pointing_angle = 0
        self.stop_pointing_angle = 0
        self.look_angle_centre = 0
        self.pointing_angle_centre = 0

        self.stack_std = 0
        self.stack_skewness = 0
        self.stack_kurtosis = 0

        self.n_beams_start_stop = 0
        self.n_beams_multilooking = 0

    def __call__(self, working_surface_location: SurfaceData) -> None:
        """

        :param working_surface_location:
        :return:
        """
        # TODO: FLAG SURFACE WEIGHTING

        # TODO: FLAG ANTENNA WEIGHTING (...or in azimuth processing?)

        # TODO: GAPS

        self.compute_stack_characterization_params(working_surface_location)

        self.compute_multilooking(working_surface_location)

    def compute_stack_characterization_params(self, working_surface_location: SurfaceData) -> None:
        """

        :param working_surface_location:
        :return:
        """
        beam_power = np.zeros((working_surface_location.data_stack_size), dtype=np.float64)

        max_beam_power = 0

        beam_angles_complementary = np.abs(
            self.cst.pi / 2. - working_surface_location.beam_angles_surf
        )

        # find index and value of minimum complementary angle
        min_beam_angle_complementary_index =\
            np.argmin(beam_angles_complementary)

        beam_length = (self.chd.n_samples_sar / 2) * self.zp_fact_range
        for beam_index in range(working_surface_location.data_stack_size):
            beam_power[beam_index] =\
                np.sum(
                    working_surface_location.beams_masked[beam_index, :beam_length]
                )
            if beam_power[beam_index] > max_beam_power:
                max_beam_power = beam_power[beam_index]

        # only the central 249 beams will be used in the gaussian fitting:
        # the doppler-central beam, 124 to the left and 124 to the right.
        last_right_beam = min(min_beam_angle_complementary_index + 124,
                              working_surface_location.data_stack_size - 1)
        first_left_beam = max(min_beam_angle_complementary_index - 124,
                              0)
        # the parameters and arrays for the gaussian fitting
        n_samples_fitting = last_right_beam - first_left_beam + 1

        beam_power_center = np.empty((n_samples_fitting), dtype=np.float64)
        look_angles_surf_center = np.empty((n_samples_fitting), dtype=np.float64)
        pointing_angles_surf_center = np.empty((n_samples_fitting), dtype=np.float64)

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

    def compute_multilooking(self, working_surface_location: SurfaceData) -> None:
        """

        :param working_surface_location:
        :return:
        """
        start_beam_index = None
        stop_beam_index = None

        self.n_beams_multilooking = 0

        n_samples_max = self.chd.n_samples_sar * self.zp_fact_range

        self.waveform_multilooked = np.zeros(
            (n_samples_max,), dtype=np.float64
        )
        self.sample_counter = np.zeros(
            (n_samples_max,), dtype=int
        )

        for beam_index in range(working_surface_location.data_stack_size):

            if working_surface_location.stack_mask_vector[beam_index] != 0:

                self.n_beams_multilooking += 1

                if start_beam_index is None:
                    start_beam_index = beam_index
                stop_beam_index = beam_index

            else:
                continue

            for sample_index in range(self.chd.n_samples_sar * self.zp_fact_range):
                if self.flag_avoid_zeros_in_multilooking:
                    if working_surface_location.stack_mask[beam_index, sample_index] == 0:
                        continue
                self.waveform_multilooked[sample_index] += working_surface_location.beams_masked[beam_index, sample_index]
                self.sample_counter[sample_index] += 1

        self.waveform_multilooked /= self.sample_counter# / self.waveform_multilooked

        self.n_beams_start_stop = stop_beam_index - start_beam_index + 1

        self.start_look_angle =\
            working_surface_location.look_angles_surf[start_beam_index]
        self.stop_look_angle =\
            working_surface_location.look_angles_surf[stop_beam_index]

        self.start_doppler_angle = \
            working_surface_location.doppler_angles_surf[start_beam_index]
        self.stop_doppler_angle = \
            working_surface_location.doppler_angles_surf[stop_beam_index]

        self.start_pointing_angle = \
            working_surface_location.pointing_angles_surf[start_beam_index]
        self.stop_pointing_angle = \
            working_surface_location.pointing_angles_surf[stop_beam_index]

        self.stack_mask_vector_start_stop = np.zeros(
            (self.n_looks_stack,),
            dtype=working_surface_location.stack_mask_vector.dtype
        )
        self.stack_mask_vector_start_stop[:self.n_beams_start_stop] =\
            working_surface_location.stack_mask_vector[start_beam_index:stop_beam_index+1]
