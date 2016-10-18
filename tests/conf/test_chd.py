import unittest
import os
import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile
from tests.testing import TestDataLoader


class TestCHD(unittest.TestCase):
    _root = os.path.join(os.path.dirname(__file__), '..', '..')
    _folder = os.path.join(_root, "test_data", "conf", "test_chd")

    _expected_file = os.path.join(
        _folder, "expected.txt"
    )
    _input_file = os.path.join(
        _folder, "chd.json"
    )
    _constants = os.path.join(
        _root, "test_data", "common", "CST.json"
    )

    def setUp(self):
        self.expected = TestDataLoader(self._expected_file)

        cst = ConstantsFile(self._constants)
        self.actual = CharacterisationFile(cst, self._input_file)

    def test_N_samples_sar(self):
        expected = self.expected["N_samples_sar_chd"]
        actual = self.actual.n_samples_sar

        self.assertAlmostEqual(expected, actual)

    def test_power_tx_ant_ku(self):
        expected = self.expected["power_tx_ant_ku_chd"]
        actual = self.actual.power_tx_ant_ku

        self.assertAlmostEqual(expected, actual)

    def test_alt_freq_multiplier(self):
        expected = self.expected["alt_freq_multiplier_chd"]
        actual = self.actual.alt_freq_multiplier

        self.assertAlmostEqual(expected, actual)

    def test_freq_ku(self):
        expected = self.expected["freq_ku_chd"]
        actual = self.actual.freq_ku

        self.assertAlmostEqual(expected, actual)

    def test_mean_sat_alt(self):
        expected = self.expected["mean_sat_alt_chd"]
        actual = self.actual.mean_sat_alt

        self.assertAlmostEqual(expected, actual)

    def test_pulse_length(self):
        expected = self.expected["pulse_length_chd"]
        actual = self.actual.pulse_length

        self.assertAlmostEqual(expected, actual)

    def test_bw_ku(self):
        expected = self.expected["bw_ku_chd"]
        actual = self.actual.bw_ku

        self.assertAlmostEqual(expected, actual)

    def test_N_ku_pulses_burst(self):
        expected = self.expected["N_ku_pulses_burst_chd"]
        actual = self.actual.n_ku_pulses_burst

        self.assertAlmostEqual(expected, actual)

    def test_antenna_gain_ku(self):
        expected = self.expected["antenna_gain_ku_chd"]
        actual = self.actual.antenna_gain_ku

        self.assertAlmostEqual(expected, actual)

    def test_antenna_weights(self):
        expected = self.expected["antenna_weights_chd"]
        actual = self.actual.antenna_weights

        self.assertTrue(np.allclose(expected, actual))

    def test_antenna_angles(self):
        expected = self.expected["antenna_angles_chd"]
        actual = self.actual.antenna_angles

        self.assertTrue(np.allclose(expected, actual))

    def test_antenna_angles_spacing(self):
        expected = self.expected["antenna_angles_spacing_chd"]
        actual = self.actual.antenna_angles_spacing

        self.assertAlmostEqual(expected, actual)

    def test_brf(self):
        expected = self.expected["brf_chd"]
        actual = self.actual.brf_sar

        self.assertAlmostEqual(expected, actual)

    def test_prf(self):
        expected = self.expected["prf_chd"]
        actual = self.actual.prf_sar

        self.assertAlmostEqual(expected, actual)

