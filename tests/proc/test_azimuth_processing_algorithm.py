import unittest

import numpy as np
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.conf.enums import AzimuthWindowingMethod, AzimuthProcessingMethod
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.proc.sar.algorithms import AzimuthProcessingAlgorithm
from tests.testing import TestDataLoader


class AzimuthProcessingAlgorithmTests(unittest.TestCase):
    expected_01 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_01/" \
                  "expected/expected.txt"
    inputs_01 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_01/" \
                "input/inputs.txt"

    expected_02 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_02/" \
                  "expected/expected.txt"
    inputs_02 = "test_data/proc/azimuth_processing_algorithm/azimuth_processing_algorithm_02/" \
                "input/inputs.txt"

    def initialise_algorithm(self, input_data):
        """
        :param input_data: the input data

        create cst and chd objects from input_data, then initialise
        an instance of the azimuth processing algorithm
        """
        proc_method = AzimuthProcessingMethod(input_data["flag_azimuth_processing_method_cnf"])

        self.cnf = ConfigurationFile(
            flag_azimuth_windowing_method_cnf=AzimuthWindowingMethod.disabled,
            flag_azimuth_processing_method_cnf=proc_method,
            azimuth_window_width_cnf=64
        )
        self.cst = ConstantsFile(
            pi_cst=input_data['pi_cst']
        )
        self.chd = CharacterisationFile(
            self.cst,
            N_ku_pulses_burst_chd=input_data['n_ku_pulses_burst_chd'],
            N_samples_sar_chd=input_data['n_samples_sar_chd']
        )
        self.azimuth_processing_algorithm = AzimuthProcessingAlgorithm(self.chd, self.cst, self.cnf)

    def test_azimuth_processing_algorithm_01(self):
        """
        azimuth processing algorithm test 01
        ------------------------------------

        tests the azimuth processing algorithm approximate method
        """
        expected = TestDataLoader(self.expected_01, delim=' ')
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        self.initialise_algorithm(input_data)

        # construct complex waveform
        waveform_shape = (self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
        wfm_i = np.reshape(input_data["wfm_cor_sar_i"], waveform_shape)
        wfm_q = np.reshape(input_data["wfm_cor_sar_q"], waveform_shape)
        wv_len = input_data["wv_length_ku"]

        # create input packet
        packet = L1AProcessingData(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"],
            beam_angles_list=input_data["beam_angles_list"],
            waveform_cor_sar=wfm_i+1j*wfm_q
        )
        # compute beam angles trend for packet
        packet.calculate_beam_angles_trend(
            input_data["beam_angles_list_size_previous_burst"],
            input_data["beam_angles_trend_previous_burst"]
        )

        # execute azimuth processing algorithm
        self.azimuth_processing_algorithm(packet, wv_len)

        beams_focused = self.azimuth_processing_algorithm.beams_focused

        # construct focused beams waveform
        wfm_i = np.reshape(expected["beams_focused_i"], waveform_shape)
        wfm_q = np.reshape(expected["beams_focused_q"], waveform_shape)

        for pulse_index in range(self.chd.n_ku_pulses_burst):
            for sample_index in range(self.chd.n_samples_sar):

                pos = "\nstack: {}/{}, sample: {}/{}".format(
                    pulse_index, self.chd.n_ku_pulses_burst,
                    sample_index, self.chd.n_samples_sar
                )

                expected_val = wfm_i[pulse_index, sample_index]
                actual_val = beams_focused[pulse_index, sample_index].real

                if expected_val == 0:
                    self.assertEqual(
                        expected_val,
                        actual_val,
                        msg=pos
                    )
                else:
                    rel_err = abs((expected_val - actual_val) / expected_val)
                    self.assertLess(rel_err, 2e-10, msg=pos)

                expected_val = wfm_q[pulse_index, sample_index]
                actual_val = beams_focused[pulse_index, sample_index].imag

                if expected_val == 0:
                    self.assertEqual(
                        expected_val,
                        actual_val,
                        msg=pos
                    )
                else:
                    rel_err = abs((expected_val - actual_val) / expected_val)
                    self.assertLess(rel_err, 2e-10, msg=pos)

    def test_azimuth_processing_algorithm_02(self):
        """
        azimuth processing algorithm test 02
        ------------------------------------

        tests the azimuth processing algorithm exact method
        """
        expected = TestDataLoader(self.expected_02, delim=' ')
        input_data = TestDataLoader(self.inputs_02, delim=' ')
        self.initialise_algorithm(input_data)

        # construct complex waveform
        waveform_shape = (self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
        wfm_i = np.reshape(input_data["wfm_cor_sar_i"], waveform_shape)
        wfm_q = np.reshape(input_data["wfm_cor_sar_q"], waveform_shape)
        wv_len = input_data["wv_length_ku"]

        # create input packet
        packet = L1AProcessingData(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"],
            beam_angles_list=input_data["beam_angles_list"],
            waveform_cor_sar=wfm_i + 1j * wfm_q
        )
        # compute beam angles trend for packet
        packet.calculate_beam_angles_trend(
            input_data["beam_angles_list_size_previous_burst"],
            input_data["beam_angles_trend_previous_burst"]
        )

        # execute azimuth processing algorithm
        self.azimuth_processing_algorithm(packet, wv_len)

        beams_focused = self.azimuth_processing_algorithm.beams_focused

        # construct focused beams waveform
        wfm_i = np.reshape(expected["beams_focused_i"], waveform_shape)
        wfm_q = np.reshape(expected["beams_focused_q"], waveform_shape)

        for pulse_index in range(self.chd.n_ku_pulses_burst):
            for sample_index in range(self.chd.n_samples_sar):

                pos = "\nstack: {}/{}, sample: {}/{}".format(
                    pulse_index, self.chd.n_ku_pulses_burst,
                    sample_index, self.chd.n_samples_sar
                )

                expected_val = wfm_i[pulse_index, sample_index]
                actual_val = beams_focused[pulse_index, sample_index].real

                if expected_val == 0:
                    self.assertEqual(
                        expected_val,
                        actual_val,
                        msg=pos
                    )
                else:
                    rel_err = abs((expected_val - actual_val) / expected_val)
                    self.assertLess(rel_err, 1e-10, msg=pos)

                expected_val = wfm_q[pulse_index, sample_index]
                actual_val = beams_focused[pulse_index, sample_index].imag

                if expected_val == 0:
                    self.assertEqual(
                        expected_val,
                        actual_val,
                        msg=pos
                    )
                else:
                    rel_err = abs((expected_val - actual_val) / expected_val)
                    self.assertLess(rel_err, 1e-10, msg=pos)