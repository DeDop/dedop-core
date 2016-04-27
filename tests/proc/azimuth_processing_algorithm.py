import unittest
import numpy as np

from tests.testing import TestDataLoader

from dedop.proc.sar.algorithms import AzimuthProcessingAlgorithm
from dedop.proc.sar.algorithms.azimuth_processing import AzimuthProcessingMethods
from dedop.io.input.packet import InstrumentSourcePacket
from dedop.conf import CharacterisationFile, ConstantsFile


class AzimuthProcessingAlgorithmTests(unittest.TestCase):
    chd_file = "test_data/common/chd.json"
    cst_file = "test_data/common/cst.json"

    expected_01 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_01/" \
                  "expected/expected.txt"
    inputs_01 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_01/" \
                "input/inputs.txt"

    expected_02 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_02/" \
                  "expected/expected.txt"
    inputs_02 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_02/" \
                "input/inputs.txt"

    def setUp(self):
        self.chd = CharacterisationFile(self.chd_file)
        self.cst = ConstantsFile(self.cst_file)
        self.azimuth_processing_algorithm = AzimuthProcessingAlgorithm(self.chd, self.cst)

    def test_azimuth_processing_algorithm_01(self):
        """
        azimuth processing algorithm test 01
        ------------------------------------

        tests the azimuth processing algorithm approximate method
        """
        expected = TestDataLoader(self.expected_01, delim=' ')
        input_data = TestDataLoader(self.inputs_01, delim=' ')

        # construct complex waveform
        waveform_shape = (self.chd.n_samples_sar, self.chd.n_ku_pulses_burst)
            #(self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
        wfm_i = np.reshape(input_data["wfm_cor_sar_i"], waveform_shape)
        wfm_q = np.reshape(input_data["wfm_cor_sar_q"], waveform_shape)
        wv_len = input_data["wv_length_ku"]

        # create input ISP
        isp = InstrumentSourcePacket(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"],
            beam_angles_list=input_data["beam_angles_list"],
            waveform_cor_sar=wfm_i+1j*wfm_q
        )
        # compute beam angles trend for ISP
        isp.calculate_beam_angles_trend(
            input_data["beam_angles_list_size_previous_burst"],
            input_data["beam_angles_trend_previous_burst"]
        )

        # select processing method
        proc_method = AzimuthProcessingMethods(
            input_data["flag_azimuth_processing_method_cnf"]
        )
        # execute azimuth processing algorithm
        self.azimuth_processing_algorithm(isp, wv_len, method=proc_method)

        # construct focused beams waveform
        wfm_i = np.reshape(expected["beams_focused_i"], waveform_shape)
        wfm_q = np.reshape(expected["beams_focused_q"], waveform_shape)
        expected_waveform = wfm_i + 1j * wfm_q

        self.assertTrue(
            np.allclose(self.azimuth_processing_algorithm.beams_focused,
                        expected_waveform),
            msg="beams_focused does not match expected waveform"
        )

    def test_azimuth_processing_algorithm_02(self):
        """
        azimuth processing algorithm test 02
        ------------------------------------

        tests the azimuth processing algorithm exact method
        """
        expected = TestDataLoader(self.expected_02, delim=' ')
        input_data = TestDataLoader(self.inputs_02, delim=' ')

        # construct complex waveform
        waveform_shape = (self.chd.n_samples_sar, self.chd.n_ku_pulses_burst)
        # (self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
        wfm_i = np.reshape(input_data["wfm_cor_sar_i"], waveform_shape)
        wfm_q = np.reshape(input_data["wfm_cor_sar_q"], waveform_shape)
        wv_len = input_data["wv_length_ku"]

        # create input ISP
        isp = InstrumentSourcePacket(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"],
            beam_angles_list=input_data["beam_angles_list"],
            waveform_cor_sar=wfm_i + 1j * wfm_q
        )
        # compute beam angles trend for ISP
        isp.calculate_beam_angles_trend(
            input_data["beam_angles_list_size_previous_burst"],
            input_data["beam_angles_trend_previous_burst"]
        )

        # select processing method
        proc_method = AzimuthProcessingMethods(
            input_data["flag_azimuth_processing_method_cnf"]
        )
        # execute azimuth processing algorithm
        self.azimuth_processing_algorithm(isp, wv_len, method=proc_method)

        # construct focused beams waveform
        wfm_i = np.reshape(expected["beams_focused_i"], waveform_shape)
        wfm_q = np.reshape(expected["beams_focused_q"], waveform_shape)
        expected_waveform = wfm_i + 1j * wfm_q

        self.assertTrue(
            np.allclose(self.azimuth_processing_algorithm.beams_focused,
                        expected_waveform),
            msg="beams_focused does not match expected waveform"
        )