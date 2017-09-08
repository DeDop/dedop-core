import unittest

import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model import SurfaceData
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.proc.sar.algorithms.beam_angles import BeamAnglesAlgorithm
from tests.testing import TestDataLoader


class BeamAnglesAlgorithmTests(unittest.TestCase):
    input_01 = "test_data/proc/beam_angles_algorithm/beam_angles_algorithm_01/" \
               "input/inputs.txt"
    expected_01 = "test_data/proc/beam_angles_algorithm/beam_angles_algorithm_01/" \
                  "expected/expected.txt"

    input_02 = "test_data/proc/beam_angles_algorithm/beam_angles_algorithm_02/" \
               "input/inputs.txt"
    expected_02 = "test_data/proc/beam_angles_algorithm/beam_angles_algorithm_02/" \
                  "expected/expected.txt"

    def initialise_algorithm(self, input_data):
        self.cnf = ConfigurationFile()
        self.cst = ConstantsFile(
            c_cst=input_data['c_cst'],
            pi_cst=input_data['pi_cst']
        )
        self.chd = CharacterisationFile(
            self.cst,
            freq_ku_chd=input_data['freq_ku_chd'],
            N_ku_pulses_burst_chd=input_data['n_ku_pulses_burst_chd'],
            prf_sar_chd=1./input_data['pri_sar_pre_dat']
        )
        self.beam_angles_algorithm = BeamAnglesAlgorithm(self.chd, self.cst, self.cnf)

    def test_beam_angles_algorithm_01(self):
        """
        beam angles algorithm test #01
        ------------------------------
        """

        # load the expected data object
        expected = TestDataLoader(self.expected_01, delim=' ')

        # load the input data
        input_data = TestDataLoader(self.input_01, delim=' ')

        self.initialise_algorithm(input_data)

        # create surface location objects
        surfs = []

        for i, surf_num in enumerate(input_data["surface_counter"]):
            surf = SurfaceData(
                self.cst, self.chd, surf_num,
                # time_surf=input_data["time_surf"][i],
                x_surf=input_data["x_surf"][i],
                y_surf=input_data["y_surf"][i],
                z_surf=input_data["z_surf"][i],
            )
            surfs.append(surf)

        # create packet object
        packet = L1AProcessingData(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_sar_sat=input_data["x_sar_sat"],
            y_sar_sat=input_data["y_sar_sat"],
            z_sar_sat=input_data["z_sar_sat"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"],
            doppler_angle_sar_sat=input_data["doppler_angle_sar_sat"]
        )
        work_loc = input_data["working_surface_location_counter"]

        # execute beam angles algorithm
        self.beam_angles_algorithm(surfs, packet, surfs[work_loc])

        # confirm correct number of surfaces seen
        self.assertEqual(
            len(self.beam_angles_algorithm.surfaces_seen),
            expected["surfaces_seen"]
        )

        # confirm the working surface location is seen
        self.assertTrue(
            self.beam_angles_algorithm.work_location_seen,
            msg="working location seen"
        )

        # check beam angles are correct
        self.assertTrue(
            np.allclose(self.beam_angles_algorithm.beam_angles,
                        expected["beam_ang"]),
            msg="Beam Angles values are not correct"
        )

        # check surface indicies are correct
        self.assertTrue(
            np.array_equal(self.beam_angles_algorithm.surfaces_seen,
                           expected["surf_loc_index"]),
            msg="Surface Indicies are not correct"
        )

    def test_beam_angles_algorithm_02(self):
        """
        beam angles algorithm test #02
         -----------------------------
        """
        # load the expected data object
        expected = TestDataLoader(self.expected_02, delim=' ')

        # load the input data
        input_data = TestDataLoader(self.input_02, delim=' ')

        self.initialise_algorithm(input_data)
        # create surface location objects
        surfs = []

        for i, surf_num in enumerate(input_data["surface_counter"]):
            surf = SurfaceData(
                self.cst, self.chd, surf_num,
                # time_surf=input_data["time_surf"][i],
                x_surf=input_data["x_surf"][i],
                y_surf=input_data["y_surf"][i],
                z_surf=input_data["z_surf"][i],
            )
            surfs.append(surf)

        # create packet object
        packet = L1AProcessingData(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_sar_sat=input_data["x_sar_sat"],
            y_sar_sat=input_data["y_sar_sat"],
            z_sar_sat=input_data["z_sar_sat"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"],
            doppler_angle_sar_sat=input_data["doppler_angle_sar_sat"]
        )
        work_loc = input_data["working_surface_location_counter"]

        # execute beam angles algorithm
        self.beam_angles_algorithm(surfs, packet, work_loc)

        # confirm correct number of surfaces seen
        self.assertEqual(
            len(self.beam_angles_algorithm.surfaces_seen),
            expected["surfaces_seen"]
        )

        # confirm the working surface location is not seen
        self.assertFalse(
            self.beam_angles_algorithm.work_location_seen,
            msg="working location erroneously seen"
        )

        # check beam angles are correct
        self.assertTrue(
            np.allclose(self.beam_angles_algorithm.beam_angles,
                        expected["beam_ang"]),
            msg="Beam Angles values are not correct"
        )

        # check surface indicies are correct
        self.assertTrue(
            np.array_equal(self.beam_angles_algorithm.surfaces_seen,
                           expected["surf_loc_index"]),
            msg="Surface Indicies are not correct"
        )
