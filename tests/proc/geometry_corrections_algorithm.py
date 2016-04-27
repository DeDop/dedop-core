import unittest
import numpy as np

from ..testing import TestDataLoader

from dedop.proc.sar.algorithms import GeometryCorrectionsAlgorithm
from dedop.proc.sar.surface_location_data import SurfaceLocationData
from dedop.io.input.packet import InstrumentSourcePacket
from dedop.conf import CharacterisationFile, ConstantsFile


class GeometryCorrectionsAlgorithmTests(unittest.TestCase):
    """
    Set of tests for the Geometry Corrections Algorithm
    """
    # set paths for constants files
    cst_file = "common/cst.json"
    chd_file = "common/chd.json"

    # set paths for input / expected files
    inputs_01 = "proc/geometry_corrections_algorithm/" \
                "geometry_corrections_algorithm_01/" \
                "input/inputs.txt"
    expected_01 = "proc/geometry_corrections_algorithm/" \
                  "geometry_corrections_algorithm_01/" \
                  "expected/expected.txt"

    inputs_02 = "proc/geometry_corrections_algorithm/" \
                "geometry_corrections_algorithm_02/" \
                "input/inputs.txt"
    expected_02 = "proc/geometry_corrections_algorithm/" \
                  "geometry_corrections_algorithm_02/" \
                  "expected/expected.txt"

    inputs_03 = "proc/geometry_corrections_algorithm/" \
                "geometry_corrections_algorithm_03/" \
                "input/inputs.txt"
    expected_03 = "proc/geometry_corrections_algorithm/" \
                  "geometry_corrections_algorithm_03/" \
                  "expected/expected.txt"

    def setUp(self):
        self.chd = CharacterisationFile(self.chd_file)
        self.cst = ConstantsFile(self.cst_file)
        self.geometry_corrections_algorithm =\
            GeometryCorrectionsAlgorithm(self.chd, self.cst)

    def test_geometry_corrections_algorithm_01(self):
        """
        geometry corrections algorithm test 01
        --------------------------------------

        """
        # open data files
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        # create stack of ISPs
        isps = []

        stack_size = input_data["data_stack_size"]
        for stack_index in range(stack_size):
            isp = InstrumentSourcePacket(
                self.cst, self.chd,
                x_vel_sat_sar=input_data["x_vel_sat_sar"][stack_index],
                y_vel_sat_sar=input_data["y_vel_sat_sar"][stack_index],
                z_vel_sat_sar=input_data["z_vel_sat_sar"][stack_index],
                x_sar_sat=input_data["x_sar_sat"][stack_index],
                y_sar_sat=input_data["y_sar_sat"][stack_index],
                z_sar_sat=input_data["z_sar_sat"][stack_index],
                win_delay_sar_ku=input_data["win_delay_sar_ku"][stack_index]
            )
            isps.append(isp)

        # create working surface location
        beams_surf = np.reshape(
            input_data["beams_surf"],
            (stack_size, self.chd.n_samples_sar)
        )

        working_loc = SurfaceLocationData(
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

        self.geometry_corrections_algorithm.n_looks_stack =\
            input_data["n_looks_stack_cnf"]

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

        for index, (i, q) in enumerate(zip(np.real(flat_corr), np.imag(flat_corr))):
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