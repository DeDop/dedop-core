import unittest

import numpy as np
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.proc.sar.cal import CAL2Algorithm
from tests.testing import TestDataLoader


class CAL2AlgorithmTests(unittest.TestCase):
    expected_01 = "test_data/proc/cal2_algorithm/cal2_algorithm_01/" \
                  "expected/expected.txt"
    inputs_01 = "test_data/proc/cal2_algorithm/cal2_algorithm_01/" \
                "input/inputs.txt"

    def initialise_algorithm(self, input_data: TestDataLoader) -> None:
        self.cnf = ConfigurationFile(
            flag_cal2_correction_cnf=True
        )
        self.cst = ConstantsFile()
        self.chd = CharacterisationFile(
            self.cst,
            N_ku_pulses_burst_chd=input_data['N_ku_pulses_burst_chd'],
            N_samples_sar_chd=input_data['N_samples_sar_chd']
        )
        self.cal2_algorithm = CAL2Algorithm(self.chd, self.cst, self.cnf)

    def test_cal2_algorithm_01(self) -> None:
        """
        CAL1 algorithm test #01
        -----------------------
        """
        expected = TestDataLoader(self.expected_01, delim=' ')
        input_data = TestDataLoader(self.inputs_01, delim=' ')

        self.initialise_algorithm(input_data)
        waveform_shape = (self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
        wfm_i = np.reshape(input_data["wfm_gain_cal1_corrected_i"], waveform_shape)
        wfm_q = np.reshape(input_data["wfm_gain_cal1_corrected_q"], waveform_shape)
        waveform_input = wfm_i + 1j*wfm_q

        burst = L1AProcessingData(
            self.cst, self.chd,
            cal2_array=input_data['gprw_meas_ku_l1a_echo_sar_ku'],
            waveform_cor_sar=waveform_input
        )

        self.cal2_algorithm(burst)

        waveform_shape = (self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
        wfm_i = np.reshape(expected["wfm_gain_cal1_cal2_corrected_i"], waveform_shape)
        wfm_q = np.reshape(expected["wfm_gain_cal1_cal2_corrected_q"], waveform_shape)
        waveform_expected = wfm_i + 1j*wfm_q

        self.assertTrue(
            np.allclose(np.real(burst.waveform_cor_sar), np.real(waveform_expected))
        )
        self.assertTrue(
            np.allclose(np.imag(burst.waveform_cor_sar), np.imag(waveform_expected))
        )
