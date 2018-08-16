import unittest

import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model import SurfaceData
from dedop.proc.sar.algorithms import MultilookingAlgorithm
from tests.testing import TestDataLoader

class FakeBurst:
    def __init__(self, index: int):
        self.source_seq_count = index


class MultilookingAlgorithmTests(unittest.TestCase):
    inputs_01 = "test_data/proc/multilooking_algorithm/" \
                  "multilooking_algorithm_01/input/input.txt"
    expected_01 = "test_data/proc/multilooking_algorithm/" \
                  "multilooking_algorithm_01/expected/expected.txt"

    inputs_02 = "test_data/proc/multilooking_algorithm/" \
               "multilooking_algorithm_02/input/input.txt"
    expected_02 = "test_data/proc/multilooking_algorithm/" \
                  "multilooking_algorithm_02/expected/expected.txt"

    def initialise_algorithm(self, input_data):
        self.cnf = ConfigurationFile(
            zp_fact_range_cnf=input_data['zp_fact_range_cnf'],
            flag_avoid_zeros_in_multilooking=input_data['flag_avoid_zeros_in_multilooking'],
            N_looks_stack_cnf=input_data['n_looks_stack_cnf'],
            flag_antenna_weighting_cnf=False  # TODO: add tests for this ( will need to add field to input file )
        )
        self.cst = ConstantsFile(
            pi_cst=input_data['pi_cst']
        )
        self.chd = CharacterisationFile(
            self.cst,
            N_samples_sar_chd=input_data['n_samples_sar_chd']
        )
        self.multilooking_algorithm =\
            MultilookingAlgorithm(self.chd, self.cst, self.cnf)

    def zero_float_assertion(self, expected, actual, tol=1e-4):
        if expected == 0:
            self.assertEqual(expected, actual)
        else:
            rel_err = abs(expected - actual) / expected
            self.assertLess(rel_err, tol)

    def test_multilooking_algorithm_01(self):
        """

        :return:
        """
        expected = TestDataLoader(self.expected_01, delim=' ')
        input_data = TestDataLoader(self.inputs_01, delim=' ')

        self.multilooking_tests(input_data, expected)

    def test_multilooking_algorithm_02(self):
        """

        :return:
        """
        expected = TestDataLoader(self.expected_02, delim=' ')
        input_data = TestDataLoader(self.inputs_02, delim=' ')

        self.multilooking_tests(input_data, expected)

    def multilooking_tests(self, input_data, expected):
        """

        :param input_data:
        :param expected:
        :return:
        """
        self.initialise_algorithm(input_data)

        zp_fact_range = input_data['zp_fact_range_cnf']
        data_stack_size = input_data['data_stack_size']

        input_stack_mask_vector = input_data['stack_mask_vector']
        n_samples_max = self.chd.n_samples_sar * zp_fact_range

        stack_mask = np.reshape(
            input_data['stack_mask'],
            (data_stack_size, n_samples_max)
        )
        beams_masked = np.reshape(
            input_data['beams_masked'],
            (data_stack_size, n_samples_max)
        )

        stack_bursts = [FakeBurst(i) for i in range(data_stack_size)]

        working_location = SurfaceData(
            self.cst, self.chd,
            data_stack_size=data_stack_size,
            beam_angles_surf=input_data['beam_angles_surf'],
            look_angles_surf=input_data['look_angles_surf'],
            pointing_angles_surf=input_data['pointing_angles_surf'],
            doppler_angles_surf=input_data['doppler_angles_surf'],
            stack_mask_vector=input_stack_mask_vector,
            stack_mask=stack_mask,
            beams_masked=beams_masked,
            stack_bursts=stack_bursts
        )
        self.multilooking_algorithm.zp_fact_range =\
            input_data['zp_fact_range_cnf']
        self.multilooking_algorithm.flag_avoid_zeros_in_multilooking =\
            input_data['flag_avoid_zeros_in_multilooking']
        self.multilooking_algorithm.n_looks_stack =\
            input_data['n_looks_stack_cnf']
        self.multilooking_algorithm(working_location)

        expected_waveform = expected['wfm_ml_sar']
        for sample_index in range(n_samples_max):
            self.assertEqual(
                expected_waveform[sample_index],
                self.multilooking_algorithm.waveform_multilooked[sample_index]
            )
        self.zero_float_assertion(
            expected['stack_skewness'],
            self.multilooking_algorithm.stack_skewness
        )
        self.zero_float_assertion(
            expected['stack_kurtosis'],
            self.multilooking_algorithm.stack_kurtosis
        )
        self.zero_float_assertion(
            expected['stack_std'],
            self.multilooking_algorithm.stack_std
        )
        self.zero_float_assertion(
            expected['stack_look_angle_centre'],
            self.multilooking_algorithm.look_angle_centre
        )
        self.zero_float_assertion(
            expected['stack_pointing_angle_centre'],
            self.multilooking_algorithm.pointing_angle_centre
        )
        # look angle
        self.assertEqual(
            expected['start_look_angle'],
            self.multilooking_algorithm.start_look_angle
        )
        self.assertEqual(
            expected['stop_look_angle'],
            self.multilooking_algorithm.stop_look_angle
        )
        # doppler angle
        self.assertEqual(
            expected['start_doppler_angle'],
            self.multilooking_algorithm.start_doppler_angle
        )
        self.assertEqual(
            expected['stop_doppler_angle'],
            self.multilooking_algorithm.stop_doppler_angle
        )
        # pointing angle
        self.assertEqual(
            expected['start_pointing_angle'],
            self.multilooking_algorithm.start_pointing_angle
        )
        self.assertEqual(
            expected['stop_pointing_angle'],
            self.multilooking_algorithm.stop_pointing_angle
        )
        # beams contributing
        self.assertEqual(
            expected['n_beams_multilooking'],
            self.multilooking_algorithm.n_beams_multilooking
        )
        self.assertEqual(
            expected['n_beams_start_stop'],
            self.multilooking_algorithm.n_beams_start_stop
        )
        for expect, actual in zip(expected['stack_mask_vector_start_stop'],
                                  self.multilooking_algorithm.stack_mask_vector_start_stop):
            self.assertEqual(expect, actual)
        self.assertEqual(
            len(expected['stack_mask_vector_start_stop']),
            len(self.multilooking_algorithm.stack_mask_vector_start_stop)
        )