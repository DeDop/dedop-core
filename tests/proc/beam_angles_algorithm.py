import unittest
import numpy as np

from ..testing import TestDataLoader, MockObject

from dedop.proc.sar.algorithms.beam_angles import BeamAnglesAlgorithm
from dedop.proc.sar.surface_location_data import SurfaceLocationData
from dedop.io.input.packet import InstrumentSourcePacket
from dedop.conf import CharacterisationFile, ConstantsFile

class BeamAnglesAlgorithmTests(unittest.TestCase):
    cst_file = "common/cst.json"
    chd_file = "common/chd.json"

    input_01 = "proc/beam_angles_algorithm/beam_angles_algorithm_01/" \
               "input/inputs.txt"
    expected_01 = "proc/beam_angles_algorithm/beam_angles_algorithm_01/" \
                  "expected/expected.txt"

    input_02 = "proc/beam_angles_algorithm/beam_angles_algorithm_02/" \
               "input/inputs.txt"
    expected_02 = "proc/beam_angles_algorithm/beam_angles_algorithm_02/" \
                  "expected/expected.txt"


    def setUp(self):
        self.cst = ConstantsFile(self.cst_file)
        self.chd = CharacterisationFile(self.chd_file)
        self.beam_angles_algorithm = BeamAnglesAlgorithm(self.chd, self.cst)

    def test_beam_angles_algorithm_01(self):
        """
        beam angles algorithm test #01
        ------------------------------
        """

        # load the expected data object
        expected = TestDataLoader(self.expected_01, delim=' ')

        # load the input data
        input_data = TestDataLoader(self.input_01, delim=' ')

        # create surface location objects
        surfs = []

        for i, surf_num in enumerate(input_data["surface_counter"]):
            surf = SurfaceLocationData(
                self.cst, self.chd, surf_num,
                time_surf=input_data["time_surf"][i],
                x_surf=input_data["x_surf"][i],
                y_surf=input_data["y_surf"][i],
                z_surf=input_data["z_surf"][i],
            )
            surfs.append(surf)

        # create isp object
        isp = InstrumentSourcePacket(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_sar_sat=input_data["x_sar_sat"],
            y_sar_sat=input_data["y_sar_sat"],
            z_sar_sat=input_data["z_sar_sat"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"]
        )
        work_loc = input_data["working_surface_location_counter"]

        # execute beam angles algorithm
        self.beam_angles_algorithm(surfs, isp, work_loc)

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

        # create surface location objects
        surfs = []

        for i, surf_num in enumerate(input_data["surface_counter"]):
            surf = SurfaceLocationData(
                self.cst, self.chd, surf_num,
                time_surf=input_data["time_surf"][i],
                x_surf=input_data["x_surf"][i],
                y_surf=input_data["y_surf"][i],
                z_surf=input_data["z_surf"][i],
            )
            surfs.append(surf)

        # create isp object
        isp = InstrumentSourcePacket(
            self.cst, self.chd,
            time_sar_ku=input_data["time_sar_ku"],
            x_sar_sat=input_data["x_sar_sat"],
            y_sar_sat=input_data["y_sar_sat"],
            z_sar_sat=input_data["z_sar_sat"],
            x_vel_sat_sar=input_data["x_vel_sat_sar"],
            y_vel_sat_sar=input_data["y_vel_sat_sar"],
            z_vel_sat_sar=input_data["z_vel_sat_sar"],
            pri_sar_pre_dat=input_data["pri_sar_pre_dat"]
        )
        work_loc = input_data["working_surface_location_counter"]

        # execute beam angles algorithm
        self.beam_angles_algorithm(surfs, isp, work_loc)

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
