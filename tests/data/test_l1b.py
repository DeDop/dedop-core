import unittest
from tests.testing import TestDataLoader
import netCDF4 as nc
from math import degrees
import numpy as np

from dedop.data.output import L1BWriter
from dedop.model.surface_data import SurfaceData, SurfaceType
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.conf import *
from dedop.conf.enums import OutputFormat


class L1BTests(unittest.TestCase):
    _input_data = "test_data/data/test_l1b/inputs/input.txt"
    _output_fname = "test_data/data/test_l1b/temp/output.nc"
    _expected_data = "test_data/data/test_l1b/expected/expected.txt"

    _chd_file = "test_data/common/CHD.json"
    _cst_file = "test_data/common/CST.json"
    _cnf_file = "test_data/common/CNF.json"

    def setUp(self):
        self.cst = ConstantsFile(self._cst_file)
        self.cnf = ConfigurationFile(
            self._cnf_file, flag_output_format_cnf=OutputFormat.s3
        )
        self.chd = CharacterisationFile(
            self.cst, self._chd_file
        )

    def test_output(self):
        # load input and expected data
        data = TestDataLoader(
            self._input_data, delim=' '
        )

        # create L1BWriter
        writer = L1BWriter(
            chd=self.chd, cnf=self.cnf, cst=self.cst,
            filename=self._output_fname
        )
        writer.open()

        # write outputs

        for i in range(data["count"]):
            burst = L1AProcessingData(
                cst=self.cst,
                chd=self.chd,
                seq_num=i,
                isp_coarse_time=data["isp_coarse_time"][i],
                isp_fine_time=data["isp_fine_time"][i],
                sral_fine_time=data["sral_fine_time"][i],
                flag_time_status=data["flag_time_status"][i],
                nav_bul_status=data["nav_bul_status"][i],
                nav_bul_source=data["nav_bul_source"][i],
                source_seq_count=data["source_seq_count"][i],
                oper_instr=data["oper_instr"][i],
                SAR_mode=data["SAR_mode"][i],
                cl_gain=data["cl_gain"][i],
                acq_stat=data["acq_stat"][i],
                dem_eeprom=data["dem_eeprom"][i],
                loss_track=data["loss_track"][i],
                h0_nav_dem=data["h0_nav_dem"][i],
                h0_applied=data["h0_applied"][i],
                cor2_nav_dem=data["cor2_nav_dem"][i],
                cor2_applied=data["cor2_applied"][i],
                dh0=data["dh0"][i],
                agccode_ku=data["agccode_ku"][i],
                int_path_cor_ku=data["int_path_cor_ku"][i],
                agc_ku=data["agc_ku"][i],
                sig0_cal_ku=data["sig0_cal_ku"][i],
                surf_type=data["surface_type"][i],
                uso_cor=data["uso_cor"][i]
            )

            surf = SurfaceData(
                chd=self.chd,
                cst=self.cst,
                time_surf=data["time_surf"][i],
                prev_tai=0,
                prev_utc_secs=0,
                prev_utc_days=0,
                curr_day_length=60*60*24,
                gps_time_surf=data["gps_time_surf"][i],
                lat_surf=data["lat_surf"][i],
                lon_surf=data["lon_surf"][i],
                alt_sat=data["alt_sat"][i],
                alt_rate_sat=data["alt_rate_sat"][i],
                x_sat=data["x_sat"][i],
                y_sat=data["y_sat"][i],
                z_sat=data["z_sat"][i],
                x_vel_sat=data["x_vel_sat"][i],
                y_vel_sat=data["y_vel_sat"][i],
                z_vel_sat=data["z_vel_sat"][i],
                sigma0_scaling_factor=data["sigma0_scaling_factor"][i],
                data_stack_size=data["data_stack_size"][i],
                stack_std=data["stack_std"][i],
                stack_skewness=data["stack_skewness"][i],
                stack_kurtosis=data["stack_kurtosis"][i],
                look_angles_surf=data["beam_angles_surf"],
                waveform_multilooked=data["waveform_multilooked"][i] * np.ones((256)),
                stack_max=data["stack_max"][i],
                closest_burst_index=0,
                stack_bursts=[burst],
                win_delay_surf=data["win_delay_surf"][i]
            )
            writer.write_record(surf)

        # close writer
        writer.close()

        # open output file
        output = nc.Dataset(self._output_fname)

        # compare to expected values
        expected = TestDataLoader(
            self._expected_data, delim=' '
        )

        for i in range(expected["count"]):

            self.assertAlmostEqual(
                output.variables["time_l1b_echo_sar_ku"][i],
                expected["time_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["UTC_day_l1b_echo_sar_ku"][i],
                expected["UTC_day_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["UTC_sec_l1b_echo_sar_ku"][i],
                expected["UTC_sec_l1b_echo_sar_ku"][i]
            )
            # 630719981 is the time-delta between GPS & UTC
            self.assertAlmostEqual(
                output.variables["GPS_time_l1b_echo_sar_ku"][i],
                expected["GPS_time_l1b_echo_sar_ku"][i] + 630719981
            )
            # these are limited to 6 places because of errors caused
            # by all the conversions from rads to deg & back again
            self.assertAlmostEqual(
                output.variables["lat_l1b_echo_sar_ku"][i],
                degrees(expected["lat_l1b_echo_sar_ku"][i]),
                places=6
            )
            self.assertAlmostEqual(
                output.variables["lon_l1b_echo_sar_ku"][i],
                degrees(expected["lon_l1b_echo_sar_ku"][i]),
                places=6
            )
            self.assertAlmostEqual(
                output.variables["orb_alt_rate_l1b_echo_sar_ku"][i],
                expected["orb_alt_rate_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["x_pos_l1b_echo_sar_ku"][i],
                expected["x_pos_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["y_pos_l1b_echo_sar_ku"][i],
                expected["y_pos_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["z_pos_l1b_echo_sar_ku"][i],
                expected["z_pos_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["x_vel_l1b_echo_sar_ku"][i],
                expected["x_vel_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["y_vel_l1b_echo_sar_ku"][i],
                expected["y_vel_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["z_vel_l1b_echo_sar_ku"][i],
                expected["z_vel_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["surf_type_l1b_echo_sar_ku"][i],
                expected["surf_type_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["scale_factor_ku_l1b_echo_sar_ku"][i],
                expected["scale_factor_ku_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["nb_stack_l1b_echo_sar_ku"][i],
                expected["nb_stack_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["stdev_stack_l1b_echo_sar_ku"][i],
                expected["stdev_stack_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["skew_stack_l1b_echo_sar_ku"][i],
                expected["skew_stack_l1b_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["kurt_stack_l1b_echo_sar_ku"][i],
                expected["kurt_stack_l1b_echo_sar_ku"][i]
            )
            # TODO: multi-dimension arrays
            # self.assertAlmostEqual(
            #     output.variables["beam_ang_l1b_echo_sar_ku"][i],
            #     expected["beam_ang_l1b_echo_sar_ku"][i]
            # )
            for j in range(256):
                self.assertAlmostEqual(
                    output.variables["i2q2_meas_ku_l1b_echo_sar_ku"][i, j],
                    expected["i2q2_meas_ku_l1b_echo_sar_ku"][i], places=3
                )
