import unittest

import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model import SurfaceData
from dedop.proc.sar.algorithms import RangeCompressionAlgorithm
from tests.testing import TestDataLoader


@unittest.skip("need to update expected values for Range Compression tests")
class RangeCompressionAlgorithmTests(unittest.TestCase):
    """
    Range compression algorithm tests
    """
    inputs_01 = "test_data/proc/range_compression_algorithm/range_compression_algorithm_01/" \
                "input/inputs.txt"
    expected_01 = "test_data/proc/range_compression_algorithm/range_compression_algorithm_01/" \
                  "expected/expected.txt"

    def initialise_algotithm(self, input_data):
        self.cnf = ConfigurationFile(
            zp_fact_range_cnf=input_data["zp_fact_range_cnf"],
            N_looks_stack_cnf=input_data["n_looks_stack_cnf"]
        )
        self.cst = ConstantsFile()
        self.chd = CharacterisationFile(
            self.cst, N_samples_sar_chd=input_data['n_samples_sar_chd']
        )
        self.range_compression_algorithm = RangeCompressionAlgorithm(self.chd, self.cst, self.cnf)

    def test_range_compression_algorithm_01(self):
        """
        range compression algorithm test 01
        -----------------------------------
        """
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        self.initialise_algotithm(input_data)

        input_beams_geo_corr = input_data["beams_geo_corr"]
        complex_beams_geo_corr = input_beams_geo_corr +\
            1j * np.flipud(input_beams_geo_corr)

        stack_size = input_data["data_stack_size"]
        beams_geo_corr = np.reshape(
            complex_beams_geo_corr,
            (stack_size, self.chd.n_samples_sar)
        )
        working_loc = SurfaceData(
            self.cst, self.chd,
            data_stack_size=stack_size,
            beams_geo_corr=beams_geo_corr
        )
        self.range_compression_algorithm(working_loc)

        beam_range_compr = self.range_compression_algorithm.beam_range_compr
        beam_range_compr_i = np.real(
            self.range_compression_algorithm.beam_range_compr_iq
        )
        beam_range_compr_q = np.imag(
            self.range_compression_algorithm.beam_range_compr_iq
        )
        expected_range_compr = np.reshape(
            expected["beams_range_compr"],
            beam_range_compr.shape, order='F'
        )
        expected_range_compr_i = np.reshape(
            expected["beams_range_compr_i"],
            beam_range_compr.shape, order='F'
        )
        expected_range_compr_q = np.reshape(
            expected["beams_range_compr_q"],
            beam_range_compr.shape, order='F'
        )
        self.assertTrue(
            np.allclose(beam_range_compr, expected_range_compr)
        )
        self.assertTrue(
            np.allclose(beam_range_compr_i, expected_range_compr_i)
        )
        self.assertTrue(
            np.allclose(beam_range_compr_q, expected_range_compr_q)
        )

        # for stack_index in range(stack_size):
        #     for sample_index in range(self.chd.n_samples_sar):
        #         expected_index = stack_index * self.chd.n_samples_sar * \
        #                          input_data["zp_fact_range_cnf"] + sample_index
        #         pos = "\nstack: {}/{}, sample: {}/{}".format(
        #             stack_index, stack_size,
        #             sample_index, self.chd.n_samples_sar
        #         )
        #
        #         expected_val = expected["beams_range_compr"][expected_index]
        #         actual_val = beam_range_compr[stack_index, sample_index]
        #
        #         if expected_val == 0:
        #             self.assertEqual(
        #                 expected_val,
        #                 actual_val,
        #                 msg=pos
        #             )
        #         else:
        #             rel_err = abs((expected_val - actual_val) / expected_val)
        #             self.assertLess(rel_err, 1e-11, msg=pos)
        #
        #         expected_val = expected["beams_range_compr_i"][expected_index]
        #         actual_val = beam_range_compr_i[stack_index, sample_index]
        #
        #         if expected_val == 0:
        #             self.assertEqual(
        #                 expected_val,
        #                 actual_val,
        #                 msg=pos
        #             )
        #         else:
        #             rel_err = abs((expected_val - actual_val) / expected_val)
        #             self.assertLess(rel_err, 1e-9, msg=pos)
        #
        #         expected_val = expected["beams_range_compr_q"][expected_index]
        #         actual_val = beam_range_compr_q[stack_index, sample_index]
        #
        #         if expected_val == 0:
        #             self.assertEqual(
        #                 expected_val,
        #                 actual_val,
        #                 msg=pos
        #             )
        #         else:
        #             rel_err = abs((expected_val - actual_val) / expected_val)
        #             self.assertLess(rel_err, 1e-9, msg=pos)
