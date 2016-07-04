import unittest
import os

from dedop.conf import CharacterisationFile, ConstantsFile
from tests.testing import TestDataLoader

class TestCHD(unittest.TestCase):
    _folder = os.path.join("test_data", "conf", "test_chd")

    _expected_file = os.path.join(
        _folder, "expected.txt"
    )
    _input_file = os.path.join(
        _folder, "chd.json"
    )
    _constants = os.path.join(
        _folder, "cst.json"
    )

    def setUp(self):
        self.expected = TestDataLoader(self._expected_file)

        cst = ConstantsFile(self._constants)
        self.actual = CharacterisationFile(cst, self._input_file)

    def test_pitch_bias(self):
        expected = self.expected["pitch_bias_chd"]
        actual = self.actual.pitch_bias

        self.assertAlmostEqual(expected, actual)

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

    def test_onboard_proc_sar_raw(self):
        expected = self.expected["onboard_proc_sar_raw_chd"]
        actual = self.actual.onboard_proc_sar_raw

        self.assertAlmostEqual(expected, actual)

    def test_yaw_bias(self):
        expected = self.expected["yaw_bias_chd"]
        actual = self.actual.yaw_bias

        self.assertAlmostEqual(expected, actual)

    def test_freq_ku(self):
        expected = self.expected["freq_ku_chd"]
        actual = self.actual.freq_ku

        self.assertAlmostEqual(expected, actual)

    def test_rfu_rx_gain_ground(self):
        expected = self.expected["rfu_rx_gain_ground_chd"]
        actual = self.actual.rfu_rx_gain_ground

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

    def test_cai_cor2_unit_conv(self):
        expected = self.expected["cai_cor2_unit_conv_chd"]
        actual = self.actual.cai_cor2_unit_conv

        self.assertAlmostEqual(expected, actual)

    def test_h0_cor2_unit_conv(self):
        expected = self.expected["h0_cor2_unit_conv_chd"]
        actual = self.actual.h0_cor2_unit_conv

        self.assertAlmostEqual(expected, actual)

    def test_i_sample_start(self):
        expected = self.expected["i_sample_start_chd"]
        actual = self.actual.i_sample_start

        self.assertAlmostEqual(expected, actual)

    def test_fai_shift_number(self):
        expected = self.expected["fai_shift_number_chd"]
        actual = self.actual.fai_shift_number

        self.assertAlmostEqual(expected, actual)

    def test_T0_h0_unit_conv(self):
        expected = self.expected["T0_h0_unit_conv_chd"]
        actual = self.actual.t0_h0_unit_conv

        self.assertAlmostEqual(expected, actual)

    def test_antenna_gain_ku(self):
        expected = self.expected["antenna_gain_ku_chd"]
        actual = self.actual.antenna_gain_ku

        self.assertAlmostEqual(expected, actual)

    def test_roll_bias(self):
        expected = self.expected["roll_bias_chd"]
        actual = self.actual.roll_bias

        self.assertAlmostEqual(expected, actual)

    def test_pri_T0_unit_conv(self):
        expected = self.expected["pri_T0_unit_conv_chd"]
        actual = self.actual.pri_T0_unit_conv

        self.assertAlmostEqual(expected, actual)
