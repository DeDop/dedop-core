import unittest
import os

from dedop.conf import ConfigurationFile
from tests.testing import TestDataLoader


class TestCNF(unittest.TestCase):
    _root = os.path.join(os.path.dirname(__file__), '..', '..')
    _folder = os.path.join(_root, "test_data", "conf", "test_cnf")

    _expected_file = os.path.join(
            _folder, "expected.txt"
    )
    _input_file = os.path.join(
            _folder, "cnf.json"
    )

    def setUp(self):
        self.expected = TestDataLoader(self._expected_file)
        self.actual = ConfigurationFile(self._input_file)

    def test_pu_seed(self):
        expected = self.expected["pu_seed_cnf"]
        actual = self.actual.pu_seed

        self.assertAlmostEqual(expected, actual)

    def test_flag_doppler_range_correction(self):
        expected = self.expected["flag_doppler_range_correction_cnf"]
        actual = self.actual.flag_doppler_range_correction

        self.assertAlmostEqual(expected, actual)

    def test_n_samples_fitting_raw(self):
        expected = self.expected["n_samples_fitting_raw_cnf"]
        actual = self.actual.n_samples_fitting_raw

        self.assertAlmostEqual(expected, actual)

    def test_zero_freq_sample_number_sar(self):
        expected = self.expected["zero_freq_sample_number_sar_cnf"]
        actual = self.actual.zero_freq_sample_number_sar

        self.assertAlmostEqual(expected, actual)

    def test_num_lobes_int_cal1(self):
        expected = self.expected["num_lobes_int_cal1_cnf"]
        actual = self.actual.num_lobes_int_cal1

        self.assertAlmostEqual(expected, actual)

    def test_sigma_alt_surf_th(self):
        expected = self.expected["sigma_alt_surf_th_cnf"]
        actual = self.actual.sigma_alt_surf_th

        self.assertAlmostEqual(expected, actual)

    def test_n_samples_fitting_rmc(self):
        expected = self.expected["n_samples_fitting_rmc_cnf"]
        actual = self.actual.n_samples_fitting_rmc

        self.assertAlmostEqual(expected, actual)

    def test_k_fact_int_cal1(self):
        expected = self.expected["k_fact_int_cal1_cnf"]
        actual = self.actual.k_fact_int_cal1

        self.assertAlmostEqual(expected, actual)

    def test_N_beams_sub_stack(self):
        expected = self.expected["N_beams_sub_stack_cnf"]
        actual = self.actual.N_beams_sub_stack

        self.assertAlmostEqual(expected, actual)

    def test_thermal_noise_flag(self):
        expected = self.expected["thermal_noise_flag_cnf"]
        actual = self.actual.thermal_noise_flag

        self.assertAlmostEqual(expected, actual)

    def test_left_avoided_samples_cal2(self):
        expected = self.expected["left_avoided_samples_cal2_cnf"]
        actual = self.actual.left_avoided_samples_cal2

        self.assertAlmostEqual(expected, actual)

    def test_num_samp_out_wfm(self):
        expected = self.expected["num_samp_out_wfm_cnf"]
        actual = self.actual.num_samp_out_wfm

        self.assertAlmostEqual(expected, actual)

    def test_flag_cal1_power(self):
        expected = self.expected["flag_cal1_power_cnf"]
        actual = self.actual.flag_cal1_power

        self.assertAlmostEqual(expected, actual)

    def test_thermal_noise_first_range_bin(self):
        expected = self.expected["thermal_noise_first_range_bin_cnf"]
        actual = self.actual.thermal_noise_first_range_bin

        self.assertAlmostEqual(expected, actual)

    def test_flag_azimuth_processing_method(self):
        expected = self.expected["flag_azimuth_processing_method_cnf"]
        actual = self.actual.flag_azimuth_processing_method

        self.assertAlmostEqual(expected, actual)

    def test_flag_window_delay_alignment_method(self):
        expected = self.expected["flag_window_delay_alignment_method_cnf"]
        actual = self.actual.flag_window_delay_alignment_method

        self.assertAlmostEqual(expected, actual)

    def test_parameter_fitting_flag(self):
        expected = self.expected["parameter_fitting_flag_cnf"]
        actual = self.actual.parameter_fitting_flag

        self.assertAlmostEqual(expected, actual)

    def test_flag_cal2_correction(self):
        expected = self.expected["flag_cal2_correction_cnf"]
        actual = self.actual.flag_cal2_correction

        self.assertAlmostEqual(expected, actual)

    def test_flag_avoid_zeros_in_multilooking(self):
        expected = self.expected["flag_avoid_zeros_in_multilooking_cnf"]
        actual = self.actual.flag_avoid_zeros_in_multilooking

        self.assertAlmostEqual(expected, actual)

    def test_zp_fact_range(self):
        expected = self.expected["zp_fact_range_cnf"]
        actual = self.actual.zp_fact_range

        self.assertAlmostEqual(expected, actual)

    def test_flag_antenna_weighting(self):
        expected = self.expected["flag_antenna_weighting_cnf"]
        actual = self.actual.flag_antenna_weighting

        self.assertAlmostEqual(expected, actual)

    def test_sigma_z_seed(self):
        expected = self.expected["sigma_z_seed_cnf"]
        actual = self.actual.sigma_z_seed

        self.assertAlmostEqual(expected, actual)

    def test_min_num_contributing_looks(self):
        expected = self.expected["min_num_contributing_looks_cnf"]
        actual = self.actual.min_num_contributing_looks

        self.assertAlmostEqual(expected, actual)

    def test_roughness_seed(self):
        expected = self.expected["roughness_seed_cnf"]
        actual = self.actual.roughness_seed

        self.assertAlmostEqual(expected, actual)

    def test_zero_freq_sample_number_lrm(self):
        expected = self.expected["zero_freq_sample_number_lrm_cnf"]
        actual = self.actual.zero_freq_sample_number_lrm

        self.assertAlmostEqual(expected, actual)

    def test_flag_remove_doppler_ambiguities(self):
        expected = self.expected["flag_remove_doppler_ambiguities_cnf"]
        actual = self.actual.flag_remove_doppler_ambiguities

        self.assertAlmostEqual(expected, actual)

    def test_step_avg_cal1_pulse(self):
        expected = self.expected["step_avg_cal1_pulse_cnf"]
        actual = self.actual.step_avg_cal1_pulse

        self.assertAlmostEqual(expected, actual)

    def test_flag_postphase_azimuth_processing(self):
        expected = self.expected["flag_postphase_azimuth_processing_cnf"]
        actual = self.actual.flag_postphase_azimuth_processing

        self.assertAlmostEqual(expected, actual)

    def test_flag_surface_weighting(self):
        expected = self.expected["flag_surface_weighting_cnf"]
        actual = self.actual.flag_surface_weighting

        self.assertAlmostEqual(expected, actual)

    def test_right_avoided_samples_cal2(self):
        expected = self.expected["right_avoided_samples_cal2_cnf"]
        actual = self.actual.right_avoided_samples_cal2

        self.assertAlmostEqual(expected, actual)

    def test_N_looks_stack(self):
        expected = self.expected["N_looks_stack_cnf"]
        actual = self.actual.N_looks_stack

        self.assertAlmostEqual(expected, actual)

    def test_flag_cal1_source(self):
        expected = self.expected["flag_cal1_source_cnf"]
        actual = self.actual.flag_cal1_source

        self.assertAlmostEqual(expected, actual)

    def test_decimation_fact_range_l1bs(self):
        expected = self.expected["decimation_fact_range_l1bs_cnf"]
        actual = self.actual.decimation_fact_range_l1bs

        self.assertAlmostEqual(expected, actual)

    def test_width_avg_cal1_pulse(self):
        expected = self.expected["width_avg_cal1_pulse_cnf"]
        actual = self.actual.width_avg_cal1_pulse

        self.assertAlmostEqual(expected, actual)

    def test_flag_slant_range_correction(self):
        expected = self.expected["flag_slant_range_correction_cnf"]
        actual = self.actual.flag_slant_range_correction

        self.assertAlmostEqual(expected, actual)

    def test_flag_uso_correction(self):
        expected = self.expected["flag_uso_correction_cnf"]
        actual = self.actual.flag_uso_correction

        self.assertAlmostEqual(expected, actual)

    def test_max_fitting_iterations(self):
        expected = self.expected["max_fitting_iterations_cnf"]
        actual = self.actual.max_fitting_iterations

        self.assertAlmostEqual(expected, actual)

    def test_flag_l1bs_file(self):
        expected = self.expected["flag_l1bs_file_cnf"]
        actual = self.actual.flag_l1bs_file

        self.assertAlmostEqual(expected, actual)

    def test_zero_pad_fact_cal1(self):
        expected = self.expected["zero_pad_fact_cal1_cnf"]
        actual = self.actual.zero_pad_fact_cal1

        self.assertAlmostEqual(expected, actual)

    def test_flag_cal1_corrections(self):
        expected = self.expected["flag_cal1_corrections_cnf"]
        actual = self.actual.flag_cal1_corrections

        self.assertAlmostEqual(expected, actual)

    def test_thermal_noise_width(self):
        expected = self.expected["thermal_noise_width_cnf"]
        actual = self.actual.thermal_noise_width

        self.assertAlmostEqual(expected, actual)

    def test_flag_azimuth_weighting(self):
        expected = self.expected["flag_azimuth_weighting_cnf"]
        actual = self.actual.flag_azimuth_weighting

        self.assertAlmostEqual(expected, actual)

    def test_epoch_seed(self):
        expected = self.expected["epoch_seed_cnf"]
        actual = self.actual.epoch_seed

        self.assertAlmostEqual(expected, actual)
