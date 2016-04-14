import unittest
import os

from dedop.conf import CharacterisationFile
from ..testing import TestDataLoader

class TestCHD(unittest.TestCase):
    _folder = os.path.join("conf", "test_chd")

    _expected_file = os.path.join(
            _folder, "expected.txt"
    )
    _input_file = os.path.join(
            _folder, "chd.json"
    )

    def setUp(self):
        self.expected = TestDataLoader(self._expected_file)
        self.actual = CharacterisationFile(self._input_file)

    def test_pitch_bias(self):
        expected = self.expected["pitch_bias_chd"]
        actual = self.actual.pitch_bias

        self.assertAlmostEqual(expected, actual)

    def test_max_power_ref_ground_cal1_sar_c(self):
        expected = self.expected["max_power_ref_ground_cal1_sar_c_chd"]
        actual = self.actual.max_power_ref_ground_cal1_sar_c

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_sar_c_cal1(self):
        expected = self.expected["onboard_proc_sar_c_cal1_chd"]
        actual = self.actual.onboard_proc_sar_c_cal1

        self.assertAlmostEqual(expected, actual)

    def test_max_power_ref_ground_cal1_sar_ku(self):
        expected = self.expected["max_power_ref_ground_cal1_sar_ku_chd"]
        actual = self.actual.max_power_ref_ground_cal1_sar_ku

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_lrm_ku_cal1(self):
        expected = self.expected["onboard_proc_lrm_ku_cal1_chd"]
        actual = self.actual.onboard_proc_lrm_ku_cal1

        self.assertAlmostEqual(expected, actual)

    def test_int_delay_ground_cal1_sar_c(self):
        expected = self.expected["int_delay_ground_cal1_sar_c_chd"]
        actual = self.actual.int_delay_ground_cal1_sar_c

        self.assertAlmostEqual(expected, actual)

    def test_N_samples_sar(self):
        expected = self.expected["N_samples_sar_chd"]
        actual = self.actual.n_samples_sar

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_sar_ku_cal1(self):
        expected = self.expected["onboard_proc_sar_ku_cal1_chd"]
        actual = self.actual.onboard_proc_sar_ku_cal1

        self.assertAlmostEqual(expected, actual)

    def test_power_tx_ant_ku(self):
        expected = self.expected["power_tx_ant_ku_chd"]
        actual = self.actual.power_tx_ant_ku

        self.assertAlmostEqual(expected, actual)

    def test_int_delay_ground_cal1_lrm_ku(self):
        expected = self.expected["int_delay_ground_cal1_lrm_ku_chd"]
        actual = self.actual.int_delay_ground_cal1_lrm_ku

        self.assertAlmostEqual(expected, actual)

    def test_N_samples_lrm(self):
        expected = self.expected["N_samples_lrm_chd"]
        actual = self.actual.n_samples_lrm

        self.assertAlmostEqual(expected, actual)

    def test_tx1_lrm(self):
        expected = self.expected["tx1_lrm_chd"]
        actual = self.actual.tx1_lrm

        self.assertAlmostEqual(expected, actual)

    def test_alt_freq_multiplier(self):
        expected = self.expected["alt_freq_multiplier_chd"]
        actual = self.actual.alt_freq_multiplier

        self.assertAlmostEqual(expected, actual)

    def test_N_cal_pulses_burst(self):
        expected = self.expected["N_cal_pulses_burst_chd"]
        actual = self.actual.n_cal_pulses_burst

        self.assertAlmostEqual(expected, actual)

    def test_N_c_pulses_burst(self):
        expected = self.expected["N_c_pulses_burst_chd"]
        actual = self.actual.n_c_pulses_burst

        self.assertAlmostEqual(expected, actual)

    def test_antenna_beamwidth_c(self):
        expected = self.expected["antenna_beamwidth_c_chd"]
        actual = self.actual.antenna_beamwidth_c

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_sar_raw(self):
        expected = self.expected["onboard_proc_sar_raw_chd"]
        actual = self.actual.onboard_proc_sar_raw

        self.assertAlmostEqual(expected, actual)

    def test_z_cog(self):
        expected = self.expected["z_cog_chd"]
        actual = self.actual.z_cog

        self.assertAlmostEqual(expected, actual)

    def test_yaw_bias(self):
        expected = self.expected["yaw_bias_chd"]
        actual = self.actual.yaw_bias

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_lrm_c(self):
        expected = self.expected["onboard_proc_lrm_c_chd"]
        actual = self.actual.onboard_proc_lrm_c

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_lrm_c_cal1(self):
        expected = self.expected["onboard_proc_lrm_c_cal1_chd"]
        actual = self.actual.onboard_proc_lrm_c_cal1

        self.assertAlmostEqual(expected, actual)

    def test_freq_c(self):
        expected = self.expected["freq_c_chd"]
        actual = self.actual.freq_c

        self.assertAlmostEqual(expected, actual)

    def test_freq_ku(self):
        expected = self.expected["freq_ku_chd"]
        actual = self.actual.freq_ku

        self.assertAlmostEqual(expected, actual)

    def test_ext_delay_ground_ku(self):
        expected = self.expected["ext_delay_ground_ku_chd"]
        actual = self.actual.ext_delay_ground_ku

        self.assertAlmostEqual(expected, actual)

    def test_tx1_sar(self):
        expected = self.expected["tx1_sar_chd"]
        actual = self.actual.tx1_sar

        self.assertAlmostEqual(expected, actual)

    def test_total_power_ref_ground_cal1_lrm_ku(self):
        expected = self.expected["total_power_ref_ground_cal1_lrm_ku_chd"]
        actual = self.actual.total_power_ref_ground_cal1_lrm_ku

        self.assertAlmostEqual(expected, actual)

    def test_total_power_ref_ground_cal1_sar_c(self):
        expected = self.expected["total_power_ref_ground_cal1_sar_c_chd"]
        actual = self.actual.total_power_ref_ground_cal1_sar_c

        self.assertAlmostEqual(expected, actual)

    def test_var_dig_gain_lrm_c_cal1_ref(self):
        expected = self.expected["var_dig_gain_lrm_c_cal1_ref_chd"]
        actual = self.actual.var_dig_gain_lrm_c_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_ext_delay_ground_c(self):
        expected = self.expected["ext_delay_ground_c_chd"]
        actual = self.actual.ext_delay_ground_c

        self.assertAlmostEqual(expected, actual)

    def test_x_cog(self):
        expected = self.expected["x_cog_chd"]
        actual = self.actual.x_cog

        self.assertAlmostEqual(expected, actual)

    def test_int_delay_ground_cal1_sar_ku(self):
        expected = self.expected["int_delay_ground_cal1_sar_ku_chd"]
        actual = self.actual.int_delay_ground_cal1_sar_ku

        self.assertAlmostEqual(expected, actual)

    def test_N_bursts_cycle(self):
        expected = self.expected["N_bursts_cycle_chd"]
        actual = self.actual.n_bursts_cycle

        self.assertAlmostEqual(expected, actual)

    def test_attcode_ground_cal1_lrm_ku(self):
        expected = self.expected["attcode_ground_cal1_lrm_ku_chd"]
        actual = self.actual.attcode_ground_cal1_lrm_ku

        self.assertAlmostEqual(expected, actual)

    def test_N_ku_pulses_rc(self):
        expected = self.expected["N_ku_pulses_rc_chd"]
        actual = self.actual.n_ku_pulses_rc

        self.assertAlmostEqual(expected, actual)

    def test_var_dig_gain_pulse_cal1_ref(self):
        expected = self.expected["var_dig_gain_pulse_cal1_ref_chd"]
        actual = self.actual.var_dig_gain_pulse_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_rfu_rx_gain_ground(self):
        expected = self.expected["rfu_rx_gain_ground_chd"]
        actual = self.actual.rfu_rx_gain_ground

        self.assertAlmostEqual(expected, actual)

    def test_z_ant(self):
        expected = self.expected["z_ant_chd"]
        actual = self.actual.z_ant

        self.assertAlmostEqual(expected, actual)

    def test_attcode_ground_cal1_lrm_c(self):
        expected = self.expected["attcode_ground_cal1_lrm_c_chd"]
        actual = self.actual.attcode_ground_cal1_lrm_c

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_pulse_cal1(self):
        expected = self.expected["onboard_proc_pulse_cal1_chd"]
        actual = self.actual.onboard_proc_pulse_cal1

        self.assertAlmostEqual(expected, actual)

    def test_mean_sat_alt(self):
        expected = self.expected["mean_sat_alt_chd"]
        actual = self.actual.mean_sat_alt

        self.assertAlmostEqual(expected, actual)

    def test_pulse_length(self):
        expected = self.expected["pulse_length_chd"]
        actual = self.actual.pulse_length

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_sar_rmc(self):
        expected = self.expected["onboard_proc_sar_rmc_chd"]
        actual = self.actual.onboard_proc_sar_rmc

        self.assertAlmostEqual(expected, actual)

    def test_max_power_ref_ground_cal1_lrm_ku(self):
        expected = self.expected["max_power_ref_ground_cal1_lrm_ku_chd"]
        actual = self.actual.max_power_ref_ground_cal1_lrm_ku

        self.assertAlmostEqual(expected, actual)

    def test_total_power_ref_ground_cal1_sar_ku(self):
        expected = self.expected["total_power_ref_ground_cal1_sar_ku_chd"]
        actual = self.actual.total_power_ref_ground_cal1_sar_ku

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_pulse_cal1_ref(self):
        expected = self.expected["onboard_proc_pulse_cal1_ref_chd"]
        actual = self.actual.onboard_proc_pulse_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_var_dig_gain_lrm_ku_cal1_ref(self):
        expected = self.expected["var_dig_gain_lrm_ku_cal1_ref_chd"]
        actual = self.actual.var_dig_gain_lrm_ku_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_bw_ku(self):
        expected = self.expected["bw_ku_chd"]
        actual = self.actual.bw_ku

        self.assertAlmostEqual(expected, actual)

    def test_var_dig_gain_sar_ku_cal1_ref(self):
        expected = self.expected["var_dig_gain_sar_ku_cal1_ref_chd"]
        actual = self.actual.var_dig_gain_sar_ku_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_y_ant(self):
        expected = self.expected["y_ant_chd"]
        actual = self.actual.y_ant

        self.assertAlmostEqual(expected, actual)

    def test_y_cog(self):
        expected = self.expected["y_cog_chd"]
        actual = self.actual.y_cog

        self.assertAlmostEqual(expected, actual)

    def test_N_ku_pulses_burst(self):
        expected = self.expected["N_ku_pulses_burst_chd"]
        actual = self.actual.n_ku_pulses_burst

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_lrm_ku_cal1_ref(self):
        expected = self.expected["onboard_proc_lrm_ku_cal1_ref_chd"]
        actual = self.actual.onboard_proc_lrm_ku_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_antenna_gain_c(self):
        expected = self.expected["antenna_gain_c_chd"]
        actual = self.actual.antenna_gain_c

        self.assertAlmostEqual(expected, actual)

    def test_cai_cor2_unit_conv(self):
        expected = self.expected["cai_cor2_unit_conv_chd"]
        actual = self.actual.cai_cor2_unit_conv

        self.assertAlmostEqual(expected, actual)

    def test_max_power_ref_ground_cal1_lrm_c(self):
        expected = self.expected["max_power_ref_ground_cal1_lrm_c_chd"]
        actual = self.actual.max_power_ref_ground_cal1_lrm_c

        self.assertAlmostEqual(expected, actual)

    def test_h0_cor2_unit_conv(self):
        expected = self.expected["h0_cor2_unit_conv_chd"]
        actual = self.actual.h0_cor2_unit_conv

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_lrm_ku(self):
        expected = self.expected["onboard_proc_lrm_ku_chd"]
        actual = self.actual.onboard_proc_lrm_ku

        self.assertAlmostEqual(expected, actual)

    def test_i_sample_start(self):
        expected = self.expected["i_sample_start_chd"]
        actual = self.actual.i_sample_start

        self.assertAlmostEqual(expected, actual)

    def test_fine_shift_number(self):
        expected = self.expected["fine_shift_number_chd"]
        actual = self.actual.fine_shift_number

        self.assertAlmostEqual(expected, actual)

    def test_fai_shift_number(self):
        expected = self.expected["fai_shift_number_chd"]
        actual = self.actual.fai_shift_number

        self.assertAlmostEqual(expected, actual)

    def test_T0_h0_unit_conv(self):
        expected = self.expected["T0_h0_unit_conv_chd"]
        actual = self.actual.t0_h0_unit_conv

        self.assertAlmostEqual(expected, actual)

    def test_power_tx_ant_c(self):
        expected = self.expected["power_tx_ant_c_chd"]
        actual = self.actual.power_tx_ant_c

        self.assertAlmostEqual(expected, actual)

    def test_antenna_gain_ku(self):
        expected = self.expected["antenna_gain_ku_chd"]
        actual = self.actual.antenna_gain_ku

        self.assertAlmostEqual(expected, actual)

    def test_antenna_beamwidth_ku(self):
        expected = self.expected["antenna_beamwidth_ku_chd"]
        actual = self.actual.antenna_beamwidth_ku

        self.assertAlmostEqual(expected, actual)

    def test_attcode_ground_cal1_sar_ku(self):
        expected = self.expected["attcode_ground_cal1_sar_ku_chd"]
        actual = self.actual.attcode_ground_cal1_sar_ku

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_sar_ku_cal1_ref(self):
        expected = self.expected["onboard_proc_sar_ku_cal1_ref_chd"]
        actual = self.actual.onboard_proc_sar_ku_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_uso_nominal_freq(self):
        expected = self.expected["uso_nominal_freq_chd"]
        actual = self.actual.uso_nominal_freq

        self.assertAlmostEqual(expected, actual)

    def test_x_ant(self):
        expected = self.expected["x_ant_chd"]
        actual = self.actual.x_ant

        self.assertAlmostEqual(expected, actual)

    def test_attcode_ground_cal1_sar_c(self):
        expected = self.expected["attcode_ground_cal1_sar_c_chd"]
        actual = self.actual.attcode_ground_cal1_sar_c

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_lrm_c_cal1_ref(self):
        expected = self.expected["onboard_proc_lrm_c_cal1_ref_chd"]
        actual = self.actual.onboard_proc_lrm_c_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_roll_bias(self):
        expected = self.expected["roll_bias_chd"]
        actual = self.actual.roll_bias

        self.assertAlmostEqual(expected, actual)

    def test_int_delay_ground_cal1_lrm_c(self):
        expected = self.expected["int_delay_ground_cal1_lrm_c_chd"]
        actual = self.actual.int_delay_ground_cal1_lrm_c

        self.assertAlmostEqual(expected, actual)

    def test_ins_losses_ground(self):
        expected = self.expected["ins_losses_ground_chd"]
        actual = self.actual.ins_losses_ground

        self.assertAlmostEqual(expected, actual)

    def test_N_c_pulses_rc(self):
        expected = self.expected["N_c_pulses_rc_chd"]
        actual = self.actual.n_c_pulses_rc

        self.assertAlmostEqual(expected, actual)

    def test_var_dig_gain_sar_c_cal1_ref(self):
        expected = self.expected["var_dig_gain_sar_c_cal1_ref_chd"]
        actual = self.actual.var_dig_gain_sar_c_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_bw_c(self):
        expected = self.expected["bw_c_chd"]
        actual = self.actual.bw_c

        self.assertAlmostEqual(expected, actual)

    def test_pri_T0_unit_conv(self):
        expected = self.expected["pri_T0_unit_conv_chd"]
        actual = self.actual.pri_T0_unit_conv

        self.assertAlmostEqual(expected, actual)

    def test_onboard_proc_sar_c_cal1_ref(self):
        expected = self.expected["onboard_proc_sar_c_cal1_ref_chd"]
        actual = self.actual.onboard_proc_sar_c_cal1_ref

        self.assertAlmostEqual(expected, actual)

    def test_total_power_ref_ground_cal1_lrm_c(self):
        expected = self.expected["total_power_ref_ground_cal1_lrm_c_chd"]
        actual = self.actual.total_power_ref_ground_cal1_lrm_c

        self.assertAlmostEqual(expected, actual)
