import unittest
import os

from dedop.conf import ConfigurationFile
from dedop.conf.enums import AzimuthWindowingMethod
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

    def test_flag_doppler_range_correction(self):
        expected = self.expected["flag_doppler_range_correction_cnf"]
        actual = self.actual.flag_doppler_range_correction

        self.assertAlmostEqual(expected, actual)

    def test_flag_azimuth_windowing_method(self):
        expected = AzimuthWindowingMethod(
            self.expected["flag_azimuth_windowing_method_cnf"]
        )
        actual = self.actual.flag_azimuth_windowing_method

        self.assertEqual(expected, actual)

    def test_azimuth_window_width(self):
        expected = self.expected["azimuth_window_width_cnf"]
        actual = self.actual.azimuth_window_width

        self.assertAlmostEqual(expected, actual)

    def test_flag_window_delay_alignment_method(self):
        expected = self.expected["flag_window_delay_alignment_method_cnf"]
        actual = self.actual.flag_window_delay_alignment_method

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

    def test_flag_postphase_azimuth_processing(self):
        expected = self.expected["flag_postphase_azimuth_processing_cnf"]
        actual = self.actual.flag_postphase_azimuth_processing

        self.assertAlmostEqual(expected, actual)

    def test_flag_surface_weighting(self):
        expected = self.expected["flag_surface_weighting_cnf"]
        actual = self.actual.flag_surface_weighting

        self.assertAlmostEqual(expected, actual)

    def test_N_looks_stack(self):
        expected = self.expected["N_looks_stack_cnf"]
        actual = self.actual.n_looks_stack

        self.assertAlmostEqual(expected, actual)

    def test_flag_slant_range_correction(self):
        expected = self.expected["flag_slant_range_correction_cnf"]
        actual = self.actual.flag_slant_range_correction

        self.assertAlmostEqual(expected, actual)

    def test_flag_uso_correction(self):
        expected = self.expected["flag_uso_correction_cnf"]
        actual = self.actual.flag_uso_correction

        self.assertAlmostEqual(expected, actual)

    def test_flag_cal1_corrections(self):
        expected = self.expected["flag_cal1_corrections_cnf"]
        actual = self.actual.flag_cal1_corrections

        self.assertAlmostEqual(expected, actual)
