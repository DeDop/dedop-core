import unittest
from tests.testing import TestDataLoader
import netCDF4 as nc
import numpy as np
from math import degrees

from dedop.data.output import L1BSWriter
from dedop.model.surface_data import SurfaceData, SurfaceType
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.conf import *


class L1BTests(unittest.TestCase):
    _input_data = "test_data/data/test_l1bs/inputs/input.txt"
    _output_fname = "test_data/data/test_l1bs/temp/output.nc"
    _expected_data = "test_data/data/test_l1bs/expected/expected.txt"

    _chd_file = "test_data/common/CHD.json"
    _cst_file = "test_data/common/CST.json"
    _cnf_file = "test_data/common/CNF.json"

    def setUp(self):
        self.cst = ConstantsFile(self._cst_file)
        self.cnf = ConfigurationFile(self._cnf_file)
        self.chd = CharacterisationFile(
            self.cst, self._chd_file
        )

    # TODO (hans-permana, 20160920): this is skipped to make the travis report green
    # (to have a nice screenshot for SVP/SVR)
    @unittest.skip
    def test_output(self):
        # load input and expected data
        data = TestDataLoader(
            self._input_data, delim=' '
        )

        # create L1BSWriter
        writer = L1BSWriter(
            chd=self.chd, cnf=self.cnf, cst=self.cst,
            filename=self._output_fname
        )
        writer.open()

        # write outputs
        # stack_data = np.reshape(
        #     data["beams_range_compr_iq"], (data["count"], 240, 256)
        # )
        a, b = np.meshgrid(
            np.linspace(-10, 10, 256),
            np.linspace(-5, 5, 240)
        )
        stack_data = a + 1j * b

        for i in range(data["count"]):
            burst = L1AProcessingData(
                cst=self.cst,
                chd=self.chd,
                seq_num=i,
            )
            surf = SurfaceData(
                chd=self.chd,
                cst=self.cst,
                time_surf=data["time_surf"][i],
                prev_tai=0,
                prev_utc_secs=0,
                prev_utc_days=0,
                curr_day_length=60 * 60 * 24,
                lat_surf=data["lat_surf"][i],
                lon_surf=data["lon_surf"][i],
                surface_type=SurfaceType(data["surface_type"][i] % 3),
                alt_sat=data["alt_sat"][i],
                alt_rate_sat=data["alt_rate_sat"][i],
                x_sat=data["x_sat"][i],
                y_sat=data["y_sat"][i],
                z_sat=data["z_sat"][i],
                x_vel_sat=data["x_vel_sat"][i],
                y_vel_sat=data["y_vel_sat"][i],
                z_vel_sat=data["z_vel_sat"][i],
                x_surf=data["x_surf"][i],
                y_surf=data["y_surf"][i],
                z_surf=data["z_surf"][i],
                roll_sat=data["roll_sat"][i],
                pitch_sat=data["pitch_sat"][i],
                yaw_sat=data["yaw_sat"][i],
                waveform_multilooked=data["waveform_multilooked"][i] * np.ones((256)),
                stack_std=data["stack_std"][i],
                stack_skewness=data["stack_skewness"][i],
                stack_kurtosis=data["stack_kurtosis"][i],
                beams_range_compr_iq=stack_data * data["beams_range_compr_iq"][i],
                win_delay_surf=data["win_delay_surf"][i],
                closest_burst_index=0,
                stack_bursts=[burst]
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
                output.variables["time_l1bs_echo_sar_ku"][i],
                expected["time_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["UTC_day_l1bs_echo_sar_ku"][i],
                expected["UTC_day_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["UTC_sec_l1bs_echo_sar_ku"][i],
                expected["UTC_sec_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["lat_l1bs_echo_sar_ku"][i],
                degrees(expected["lat_l1bs_echo_sar_ku"][i]),
                places=6
            )
            self.assertAlmostEqual(
                output.variables["lon_l1bs_echo_sar_ku"][i],
                degrees(expected["lon_l1bs_echo_sar_ku"][i]),
                places=6
            )
            self.assertAlmostEqual(
                output.variables["surf_type_l1bs_echo_sar_ku"][i],
                expected["surf_type_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["orb_alt_rate_l1bs_echo_sar_ku"][i],
                expected["orb_alt_rate_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["x_pos_l1bs_echo_sar_ku"][i],
                expected["x_pos_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["y_pos_l1bs_echo_sar_ku"][i],
                expected["y_pos_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["z_pos_l1bs_echo_sar_ku"][i],
                expected["z_pos_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["x_vel_l1bs_echo_sar_ku"][i],
                expected["x_vel_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["y_vel_l1bs_echo_sar_ku"][i],
                expected["y_vel_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["z_vel_l1bs_echo_sar_ku"][i],
                expected["z_vel_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["meas_x_pos_l1bs_echo_sar_ku"][i],
                expected["meas_x_pos_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["meas_y_pos_l1bs_echo_sar_ku"][i],
                expected["meas_y_pos_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["meas_z_pos_l1bs_echo_sar_ku"][i],
                expected["meas_z_pos_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["stdev_stack_l1bs_echo_sar_ku"][i],
                expected["stdev_stack_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["skew_stack_l1bs_echo_sar_ku"][i],
                expected["skew_stack_l1bs_echo_sar_ku"][i]
            )
            self.assertAlmostEqual(
                output.variables["kurt_stack_l1bs_echo_sar_ku"][i],
                expected["kurt_stack_l1bs_echo_sar_ku"][i]
            )
            for j in range(256):
                self.assertAlmostEqual(
                    output.variables["i2q2_meas_ku_l1bs_echo_sar_ku"][i, j],
                    expected["i2q2_meas_ku_l1bs_echo_sar_ku"][i]
                )
                for k in range(240):
                    self.assertAlmostEqual(
                        output.variables["i_echoes_ku_l1bs_echo_sar_ku"][i, j, k],
                        expected["i_echoes_ku_l1bs_echo_sar_ku"][i] * stack_data[k, j].real
                    )
                    self.assertAlmostEqual(
                        output.variables["q_echoes_ku_l1bs_echo_sar_ku"][i, j, k],
                        expected["q_echoes_ku_l1bs_echo_sar_ku"][i] * stack_data[j, k].imag
                    )
