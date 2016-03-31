import unittest
import os

from dedop.conf import ConstantsFile
from ..testing import TestDataLoader

class TestCST(unittest.TestCase):
    _folder = os.path.join("conf", "test_cst")

    _expected_file = os.path.join(
            _folder, "expected.txt"
    )
    _input_file = os.path.join(
            _folder, "cst.json"
    )

    def setUp(self):
        self.expected = TestDataLoader(self._expected_file)
        self.actual = ConstantsFile(self._input_file)

    def test_c(self):
        expected = self.expected["c_cst"]
        actual = self.actual.c.value

        self.assertAlmostEqual(expected, actual)

    def test_semi_major_axis(self):
        expected = self.expected["semi_major_axis_cst"]
        actual = self.actual.semi_major_axis.value

        self.assertAlmostEqual(expected, actual)

    def test_earth_radius(self):
        expected = self.expected["earth_radius_cst"]
        actual = self.actual.earth_radius.value

        self.assertAlmostEqual(expected, actual)

    def test_sec_in_day(self):
        expected = self.expected["sec_in_day_cst"]
        actual = self.actual.sec_in_day.value

        self.assertAlmostEqual(expected, actual)

    def test_pi(self):
        expected = self.expected["pi_cst"]
        actual = self.actual.pi.value

        self.assertAlmostEqual(expected, actual)

    def test_flat_coeff(self):
        expected = self.expected["flat_coeff_cst"]
        actual = self.actual.flat_coeff.value

        self.assertAlmostEqual(expected, actual)

    def test_semi_minor_axis(self):
        expected = self.expected["semi_minor_axis_cst"]
        actual = self.actual.semi_minor_axis.value

        self.assertAlmostEqual(expected, actual)
