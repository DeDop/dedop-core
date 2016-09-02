import unittest
from tests.testing import TestDataLoader
from math import radians

from dedop.data.input.l1a import L1ADataset
from dedop.conf import *

class L1ATests(unittest.TestCase):
    _input_file = "test_data/data/test_l1a/inputs/l1a_test.nc"
    _expected_file = "test_data/data/test_l1a/expected/expected.txt"

    _chd_file = "test_data/common/CHD.json"
    _cst_file = "test_data/common/CST.json"
    _cnf_file = "test_data/common/CNF.json"

    def setUp(self):
        self.cst = ConstantsFile(self._cst_file)
        self.cnf = ConfigurationFile(self._cnf_file)
        self.chd = CharacterisationFile(
            self.cst, self._chd_file
        )

    def test_input(self):
        dset = L1ADataset(
            self._input_file,
            cst=self.cst,
            chd=self.chd,
            cnf=self.cnf)

        expected = TestDataLoader(
            self._expected_file, delim=' '
        )

        for i, isp in enumerate(dset):
            self.assertAlmostEqual(
                isp.time_sar_ku,
                expected["time_sar_ku"][i]
            )
            self.assertAlmostEqual(
                isp.time_sar_ku,
                expected["time_sar_ku"][i]
            )
            self.assertAlmostEqual(
                isp.isp_coarse_time,
                expected["isp_coarse_time"][i]
            )
            self.assertAlmostEqual(
                isp.isp_fine_time,
                expected["isp_fine_time"][i]
            )
            self.assertAlmostEqual(
                isp.sral_fine_time,
                expected["sral_fine_time"][i]
            )
            self.assertAlmostEqual(
                isp.days,
                expected["days"][i]
            )
            self.assertAlmostEqual(
                isp.seconds,
                expected["seconds"][i]
            )
            self.assertAlmostEqual(
                isp.burst_sar_ku,
                expected["burst_sar_ku"][i]
            )
            self.assertAlmostEqual(
                isp.lat_sar_sat,
                radians(expected["lat_sar_sat"][i])
            )
            self.assertAlmostEqual(
                isp.lon_sar_sat,
                radians(expected["lon_sar_sat"][i])
            )
            self.assertAlmostEqual(
                isp.alt_sar_sat,
                expected["alt_sar_sat"][i]
            )
            self.assertAlmostEqual(
                isp.alt_rate_sat_sar,
                expected["alt_rate_sat_sar"][i]
            )
            self.assertAlmostEqual(
                isp.x_vel_sat_sar,
                expected["x_vel_sat_sar"][i]
            )
            self.assertAlmostEqual(
                isp.y_vel_sat_sar,
                expected["y_vel_sat_sar"][i]
            )
            self.assertAlmostEqual(
                isp.z_vel_sat_sar,
                expected["z_vel_sat_sar"][i]
            )
            self.assertAlmostEqual(
                isp.roll_sar,
                radians(expected["roll_sar"][i])
            )
            self.assertAlmostEqual(
                isp.pitch_sar,
                radians(expected["pitch_sar"][i])
            )
            self.assertAlmostEqual(
                isp.yaw_sar,
                radians(expected["yaw_sar"][i])
            )
            self.assertAlmostEqual(
                isp.h0_sar,
                expected["h0_sar"][i]
            )
            self.assertAlmostEqual(
                isp.cor2_sar,
                expected["cor2_sar"][i]
            )
            self.assertAlmostEqual(
                isp.win_delay_sar_ku,
                expected["win_delay_sar_ku"][i]
            )
            self.assertAlmostEqual(
                isp.flag_time_status,
                expected["flag_time_status"][i]
            )
            self.assertAlmostEqual(
                isp.nav_bul_status,
                expected["nav_bul_status"][i]
            )
            self.assertAlmostEqual(
                isp.nav_bul_source,
                expected["nav_bul_source"][i]
            )
            self.assertAlmostEqual(
                isp.source_seq_count,
                expected["source_seq_count"][i]
            )
            self.assertAlmostEqual(
                isp.oper_instr,
                expected["oper_instr"][i]
            )
            self.assertAlmostEqual(
                isp.SAR_mode,
                expected["SAR_mode"][i]
            )
            self.assertAlmostEqual(
                isp.cl_gain,
                expected["cl_gain"][i]
            )
            self.assertAlmostEqual(
                isp.acq_stat,
                expected["acq_stat"][i]
            )
            self.assertAlmostEqual(
                isp.dem_eeprom,
                expected["dem_eeprom"][i]
            )
            self.assertAlmostEqual(
                isp.loss_track,
                expected["loss_track"][i]
            )
            self.assertAlmostEqual(
                isp.h0_nav_dem,
                expected["h0_nav_dem"][i]
            )
            self.assertAlmostEqual(
                isp.h0_applied,
                expected["h0_applied"][i]
            )
            self.assertAlmostEqual(
                isp.cor2_nav_dem,
                expected["cor2_nav_dem"][i]
            )
            self.assertAlmostEqual(
                isp.cor2_applied,
                expected["cor2_applied"][i]
            )
            self.assertAlmostEqual(
                isp.dh0,
                expected["dh0"][i]
            )
            self.assertAlmostEqual(
                isp.agccode_ku,
                expected["agccode_ku"][i]
            )
            self.assertAlmostEqual(
                isp.range_ku,
                expected["range_ku"][i]
            )
            self.assertAlmostEqual(
                isp.int_path_cor_ku,
                expected["int_path_cor_ku"][i]
            )
            self.assertAlmostEqual(
                isp.agc_ku,
                expected["agc_ku"][i]
            )
            self.assertAlmostEqual(
                isp.sig0_cal_ku,
                expected["sig0_cal_ku"][i]
            )