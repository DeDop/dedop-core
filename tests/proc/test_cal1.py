import unittest

import numpy as np
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.proc.sar.cal import CAL1Algorithm
from tests.testing import TestDataLoader


class CAL1AlgorithmTests(unittest.TestCase):
    expected_01 = "test_data/proc/cal1_algorithm/cal1_algorithm_01/" \
                  "expected/expected.txt"
    inputs_01 = "test_data/proc/cal1_algorithm/cal1_algorithm_01/" \
                "input/inputs.txt"

    def initialise_algorithm(self, input_data: TestDataLoader) -> None:
        self.cnf = ConfigurationFile(
            flag_cal1_corrections_cnf=True
        )
        self.cst = ConstantsFile()
        self.chd = CharacterisationFile(
            self.cst,
            N_ku_pulses_burst_chd=input_data['N_ku_pulses_burst_chd'],
            N_samples_sar_chd=input_data['N_samples_sar_chd']
        )
        self.cal1_algorithm = CAL1Algorithm(self.chd, self.cst, self.cnf)

    def test_cal1_algorithm_01(self) -> None:
        """
        CAL1 algorithm test #01
        -----------------------
        """
        expected = TestDataLoader(self.expected_01, delim=' ')
        input_data = TestDataLoader(self.inputs_01, delim=' ')

        self.initialise_algorithm(input_data)
        waveform_shape = (self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
        wfm_i = np.reshape(input_data["wfm_cal_gain_uncorrected_i"], waveform_shape)
        wfm_q = np.reshape(input_data["wfm_cal_gain_uncorrected_q"], waveform_shape)
        waveform_input = wfm_i + 1j*wfm_q

        burst = L1AProcessingData(
            self.cst, self.chd,
            cal1_power=input_data['burst_power_cor_ku_l1a_echo_sar_ku'],
            cal1_phase=input_data['burst_phase_cor_ku_l1a_echo_sar_ku'],
            sig0_cal_ku=input_data['sig0_cal_ku_l1a_echo_sar_ku'],
            agc_ku=input_data['agc_ku_l1a_echo_sar_ku'],
            waveform_cor_sar=waveform_input
        )

        self.cal1_algorithm(burst)

        wfm_i = np.reshape(expected["wfm_gain_cal1_corrected_i"], waveform_shape)
        wfm_q = np.reshape(expected["wfm_gain_cal1_corrected_q"], waveform_shape)
        waveform_expected = wfm_i + 1j*wfm_q

        self.assertTrue(
            np.allclose(np.real(burst.waveform_cor_sar), np.real(waveform_expected))
        )
        self.assertTrue(
            np.allclose(np.imag(burst.waveform_cor_sar), np.imag(waveform_expected))
        )
