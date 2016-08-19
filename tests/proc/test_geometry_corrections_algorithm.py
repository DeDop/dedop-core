import unittest

import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model import SurfaceData
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.proc.sar.algorithms import GeometryCorrectionsAlgorithm
from tests.testing import TestDataLoader


class GeometryCorrectionsAlgorithmTests(unittest.TestCase):
    """
    Set of tests for the Geometry Corrections Algorithm
    """

    # set paths for input / expected files
    inputs_01 = "test_data/proc/geometry_corrections_algorithm/" \
                "geometry_corrections_algorithm_01/" \
                "input/inputs.txt"
    expected_01 = "test_data/proc/geometry_corrections_algorithm/" \
                  "geometry_corrections_algorithm_01/" \
                  "expected/expected.txt"

    inputs_02 = "test_data/proc/geometry_corrections_algorithm/" \
                "geometry_corrections_algorithm_02/" \
                "input/inputs.txt"
    expected_02 = "test_data/proc/geometry_corrections_algorithm/" \
                  "geometry_corrections_algorithm_02/" \
                  "expected/expected.txt"

    inputs_03 = "test_data/proc/geometry_corrections_algorithm/" \
                "geometry_corrections_algorithm_03/" \
                "input/inputs.txt"
    expected_03 = "test_data/proc/geometry_corrections_algorithm/" \
                  "geometry_corrections_algorithm_03/" \
                  "expected/expected.txt"

    def initialize_algorithm(self, input_data):
        self.cnf = ConfigurationFile(
            N_looks_stack_cnf=input_data["n_looks_stack_cnf"],
            flag_doppler_range_correction_cnf=input_data["flag_doppler_range_correction_cnf"],
            flag_slant_range_correction_cnf=input_data["flag_slant_range_correction_cnf"]
        )
        self.cst = ConstantsFile(
            c_cst=input_data['c_cst'],
            pi_cst=input_data['pi_cst']
        )
        self.chd = CharacterisationFile(
            self.cst,
            N_samples_sar_chd=input_data['n_samples_sar_chd'],
            pulse_length_chd=input_data['pulse_length_chd'],
            bw_ku_chd=input_data['bw_ku_chd'],
            wv_length_ku_chd=input_data['wv_length_ku']
        )
        self.geometry_corrections_algorithm =\
            GeometryCorrectionsAlgorithm(self.chd, self.cst, self.cnf)

    def test_geometry_corrections_algorithm_01(self):
        """
        geometry corrections algorithm test 01
        --------------------------------------
        doppler corrections enabled
        slant range corrections enabled
        """
        # open data files
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        self._geometry_corrections_algorithm_tests(input_data, expected)

    def test_geometry_corrections_algorithm_02(self):
        """
        geometry corrections algorithm test 02
        --------------------------------------
        doppler corrections disabled
        slant range corrections enabled
        """
        # open data files
        input_data = TestDataLoader(self.inputs_02, delim=' ')
        expected = TestDataLoader(self.expected_02, delim=' ')

        self._geometry_corrections_algorithm_tests(input_data, expected)

    def test_geometry_corrections_algorithm_03(self):
        """
        geometry corrections algorithm test 03
        --------------------------------------
        doppler corrections enabled
        slant range corrections disabled
        """
        # open data files
        input_data = TestDataLoader(self.inputs_03, delim=' ')
        expected = TestDataLoader(self.expected_03, delim=' ')

        self._geometry_corrections_algorithm_tests(input_data, expected)

    def _geometry_corrections_algorithm_tests(self, input_data, expected):
        self.initialize_algorithm(input_data)
        # create stack of ISPs
        isps = []

        stack_size = input_data["data_stack_size"]
        for stack_index in range(stack_size):
            packet = L1AProcessingData(
                self.cst, self.chd,
                x_vel_sat_sar=input_data["x_vel_sat_sar"][stack_index],
                y_vel_sat_sar=input_data["y_vel_sat_sar"][stack_index],
                z_vel_sat_sar=input_data["z_vel_sat_sar"][stack_index],
                x_sar_sat=input_data["x_sar_sat"][stack_index],
                y_sar_sat=input_data["y_sar_sat"][stack_index],
                z_sar_sat=input_data["z_sar_sat"][stack_index],
                win_delay_sar_ku=input_data["win_delay_sar_ku"][stack_index]
            )
            isps.append(packet)

        # create working surface location
        beams_surf = np.reshape(
            input_data["beams_surf"],
            (stack_size, self.chd.n_samples_sar)
        )

        working_loc = SurfaceData(
            self.cst, self.chd,
            stack_bursts=isps,
            data_stack_size=stack_size,
            win_delay_surf=input_data["win_delay_surf"],
            x_surf=input_data["x_surf"],
            y_surf=input_data["y_surf"],
            z_surf=input_data["z_surf"],
            beam_angles_surf=input_data["beam_angles_surf"],
            t0_surf=input_data["T0_surf"],
            beams_surf=beams_surf
        )


        # TODO: add window delay alignment method selection
        self.geometry_corrections_algorithm(working_loc, input_data["wv_length_ku"])

        self.assertTrue(
            np.allclose(
                self.geometry_corrections_algorithm.doppler_corrections,
                expected["doppler_corrections"]
            ),
            msg="Doppler corrections do not match"
        )
        self.assertTrue(
            np.allclose(
                self.geometry_corrections_algorithm.range_sat_surf,
                expected["range_sat_surf"]
            ),
            msg="Range Sat Surf does not match"
        )
        self.assertTrue(
            np.allclose(
                self.geometry_corrections_algorithm.slant_range_corrections,
                expected["slant_range_corrections"], atol=1e-8
            ),
            msg="Slant Range Corrections do not match"
        )
        self.assertTrue(
            np.allclose(
                self.geometry_corrections_algorithm.win_delay_corrections,
                expected["win_delay_corrections"]
            ),
            msg="window delay corrections do not match"
        )
        flat_corr = np.ravel(self.geometry_corrections_algorithm.beams_geo_corr)
        components = zip(np.real(flat_corr), np.imag(flat_corr))

        for index, (i, q) in enumerate(components):
            expected_i = expected["beams_geo_corr_i"][index]
            expected_q = expected["beams_geo_corr_q"][index]

            if expected_i == 0:
                self.assertEqual(
                    expected_i, i
                )
            else:
                rel_err = abs((expected_i - i) / expected_i)
                self.assertLess(rel_err, 2e-4)

            if expected_q == 0:
                self.assertEqual(
                    expected_q, q
                )
            else:
                rel_err = abs((expected_q - q) / expected_q)
                self.assertLess(rel_err, 2e-4)