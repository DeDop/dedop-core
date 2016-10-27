import unittest

import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model import SurfaceData, SurfaceType
from dedop.proc.sar.algorithms import StackMaskingAlgorithm
from tests.testing import TestDataLoader


class StackMaskingAlgorithmTests(unittest.TestCase):
    """
    test cases for the stack masking algorithm
    """

    inputs_01 = "test_data/proc/stack_masking_algorithm/" \
                "stack_masking_algorithm_01/input/inputs.txt"
    expected_01 = "test_data/proc/stack_masking_algorithm/" \
                  "stack_masking_algorithm_01/expected/expected.txt"

    inputs_02 = "test_data/proc/stack_masking_algorithm/" \
                "stack_masking_algorithm_02/input/inputs.txt"
    expected_02 = "test_data/proc/stack_masking_algorithm/" \
                  "stack_masking_algorithm_02/expected/expected.txt"

    def initilise_algorithm(self, input_data):
        self.cnf = ConfigurationFile(
            zp_fact_range_cnf=input_data["zp_fact_range_cnf"],
            N_looks_stack_cnf=input_data["n_looks_stack_cnf"],
            flag_remove_doppler_ambiguities_cnf=input_data["flag_remove_doppler_ambiguities_cnf"],
            flag_stack_masking_cnf=input_data["flag_stack_masking_cnf"]
        )
        self.cst = ConstantsFile()
        self.chd = CharacterisationFile(
            self.cst,
            N_samples_sar_chd=input_data['n_samples_sar_chd'],
            i_sample_start_chd=input_data['i_sample_start_chd']
        )
        self.stack_masking_algorithm = StackMaskingAlgorithm(self.chd, self.cst, self.cnf)

    def test_stack_masking_algorithm_01(self):
        """
        stack masking algorithm tests 01
        --------------------------------

        with raw surface
        """
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        self._stack_masking_algorithm_tests(input_data, expected)

    def test_stack_masking_algorithm_02(self):
        """
        stack masking algorithm tests 02
        --------------------------------

        with masking disabled
        """
        input_data = TestDataLoader(self.inputs_02, delim=' ')
        expected = TestDataLoader(self.expected_02, delim=' ')

        self._stack_masking_algorithm_tests(input_data, expected)

    def _stack_masking_algorithm_tests(self, input_data, expected):
        """
        runs the stack masking algorithm test with provided input data
        and expected values

        :param input_data: TestDataLoader object containing inputs
        :param expected: TestDataLoader object containing expected values
        :return: None
        """
        self.initilise_algorithm(input_data)

        stack_size = input_data["data_stack_size"]
        zp_fact_range = self.cnf.zp_fact_range

        beams_range_compr_samples =\
            np.tile(input_data["beams_range_compr"], 2)
        beams_range_compr = np.reshape(
            beams_range_compr_samples,
            (stack_size, self.chd.n_samples_sar * zp_fact_range)
        )

        working_loc = SurfaceData(
            cst=self.cst, chd=self.chd,
            data_stack_size=stack_size,
            surface_type=SurfaceType(input_data["surface_type"]),
            doppler_corrections=input_data["doppler_corrections"],
            slant_range_corrections=input_data["slant_range_corrections"],
            win_delay_corrections=input_data["win_delay_corrections"],
            beams_range_compr=beams_range_compr
        )

        # set stack masking cnf parameters

        self.stack_masking_algorithm(working_loc)
        stack_mask_vector_actual = self.stack_masking_algorithm.stack_mask_vector
        beams_masked_actual = self.stack_masking_algorithm.beams_masked

        stack_mask_vector_expected = expected["stack_mask_vector"]
        beams_masked_expected = np.reshape(
            expected["beams_masked"],
            (stack_size, self.chd.n_samples_sar * zp_fact_range)
        )


        for stack_index in range(stack_size):
            # compare beams masked values
            for sample_index in range(self.chd.n_samples_sar * zp_fact_range):
                self.assertEqual(
                    beams_masked_actual[stack_index, sample_index],
                    beams_masked_expected[stack_index, sample_index],
                    msg="stack_index: {}/{}, sample_index: {}/{}".format(
                        stack_index, stack_size,
                        sample_index, self.chd.n_samples_sar
                    )
                )
            # compare stack mask vector value
            self.assertEqual(
                stack_mask_vector_actual[stack_index],
                stack_mask_vector_expected[stack_index],
                msg="stack_index: {}/{}".format(
                    stack_index, stack_size
                )
            )
