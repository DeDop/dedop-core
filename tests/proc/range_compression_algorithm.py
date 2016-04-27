import unittest
import numpy as np

from ..testing import TestDataLoader

from dedop.proc.sar.algorithms import RangeCompressionAlgorithm
from dedop.proc.sar.surface_location_data import SurfaceLocationData
from dedop.conf import CharacterisationFile, ConstantsFile


class RangeCompressionAlgorithmTests(unittest.TestCase):
    """
    Range compression algorithm tests
    """
    chd_file = "common/chd.json"
    cst_file = "common/cst.json"

    inputs_01 = "proc/range_compression_algorithm/range_compression_algorithm_01/" \
                "input/inputs.txt"
    expected_01 = "proc/range_compression_algorithm/range_compression_algorithm_01/" \
                  "expected/expected.txt"

    def setUp(self):
        self.chd = CharacterisationFile(self.chd_file)
        self.cst = ConstantsFile(self.cst_file)
        self.range_compression_algorithm = RangeCompressionAlgorithm(self.chd, self.cst)

    def test_range_compression_algorithm_01(self):
        """
        range compression algorithm test 01
        -----------------------------------
        """
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        input_beams_geo_corr = input_data["beams_geo_corr"]
        complex_beams_geo_corr = input_beams_geo_corr +\
            1j * np.flipud(input_beams_geo_corr)

        stack_size = input_data["data_stack_size"]
        beams_geo_corr = np.reshape(
            complex_beams_geo_corr,
            (stack_size, self.chd.n_samples_sar)
        )
        working_loc = SurfaceLocationData(
            self.cst, self.chd,
            data_stack_size=stack_size,
            beams_geo_corr=beams_geo_corr
        )
        self.range_compression_algorithm.zp_fact_range =\
            input_data["zp_fact_range_cnf"]
        self.range_compression_algorithm.n_looks_stack =\
            input_data["n_looks_stack_cnf"]

        self.range_compression_algorithm(working_loc)

        beam_range_compr = self.range_compression_algorithm.beam_range_compr
        beam_range_compr_i = np.real(
            self.range_compression_algorithm.beam_range_compr_iq
        )
        beam_range_compr_q = np.imag(
            self.range_compression_algorithm.beam_range_compr_iq
        )

        for stack_index in range(stack_size):
            for sample_index in range(self.chd.n_samples_sar):
                expected_index = stack_index * self.chd.n_samples_sar * \
                                 input_data["zp_fact_range_cnf"] + sample_index
                pos = "\nstack: {}/{}, sample: {}/{}".format(
                    stack_index, stack_size,
                    sample_index, self.chd.n_samples_sar
                )

                expected_val = expected["beams_range_compr"][expected_index]
                actual_val = beam_range_compr[stack_index, sample_index]

                if expected_val == 0:
                    self.assertEqual(
                        expected_val,
                        actual_val,
                        msg=pos
                    )
                else:
                    rel_err = abs((expected_val - actual_val) / expected_val)
                    self.assertLess(rel_err, 1e-11, msg=pos)

                expected_val = expected["beams_range_compr_i"][expected_index]
                actual_val = beam_range_compr_i[stack_index, sample_index]

                if expected_val == 0:
                    self.assertEqual(
                        expected_val,
                        actual_val,
                        msg=pos
                    )
                else:
                    rel_err = abs((expected_val - actual_val) / expected_val)
                    self.assertLess(rel_err, 1e-10, msg=pos)

                expected_val = expected["beams_range_compr_q"][expected_index]
                actual_val = beam_range_compr_q[stack_index, sample_index]

                if expected_val == 0:
                    self.assertEqual(
                        expected_val,
                        actual_val,
                        msg=pos
                    )
                else:
                    rel_err = abs((expected_val - actual_val) / expected_val)
                    self.assertLess(rel_err, 1e-10, msg=pos)
