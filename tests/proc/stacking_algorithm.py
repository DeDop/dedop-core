import unittest
import numpy as np

from tests.testing import TestDataLoader

from dedop.proc.sar.algorithms import StackingAlgorithm
from dedop.io.input.packet import InstrumentSourcePacket, IspPid
from dedop.conf import CharacterisationFile, ConstantsFile
from dedop.proc.sar.surface_location_data import SurfaceLocationData


class StackingAlgorithmTests(unittest.TestCase):
    chd_file = "test_data/common/chd.json"
    cst_file = "test_data/common/cst.json"

    inputs_01 = "test_data/proc/stacking_algorithm/stacking_algorithm_01/" \
                "input/input.txt"
    expected_01 = "test_data/proc/stacking_algorithm/stacking_algorithm_01/" \
                  "expected/expected.txt"

    def setUp(self):
        self.chd = CharacterisationFile(self.chd_file)
        self.cst = ConstantsFile(self.cst_file)
        self.stacking_algorithm = StackingAlgorithm(self.chd, self.cst)

    def test_stacking_algorithm_01(self):
        """
        stacking algorithm test 01
        --------------------------
        """

        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        self.stacking_algorithm.n_looks_stack =\
            input_data["n_looks_stack_cnf"]

        all_stack_size = input_data["all_stack_size"]

        input_beam_angles_list = np.reshape(
            input_data["beam_angles_list"],
            (all_stack_size, self.chd.n_ku_pulses_burst)
        )
        isps = []

        for stack_index in range(all_stack_size):
            beams_focused = np.zeros(
                (self.chd.n_ku_pulses_burst, self.chd.n_samples_sar)
            )
            pid = IspPid.isp_echo_sar if input_data['isp_pid'][stack_index] == 7 else IspPid.isp_echo_rmc
            isp = InstrumentSourcePacket(
                self.cst, self.chd, stack_index,
                t0_sar=input_data["T0_sar"][stack_index],
                doppler_angle_sar_sat=input_data["doppler_angle_sar_sat"][stack_index],
                pitch_sar=input_data["pitch_sar"][stack_index],
                beam_angles_list=input_beam_angles_list[stack_index, :],
                beams_focused=beams_focused,
                isp_pid=pid
            )
            isps.append(isp)

        working_loc = SurfaceLocationData(
            self.cst, self.chd,
            stack_all_bursts=isps
        )
        for beam_index in input_data["stack_all_beam_indexes"]:
            working_loc.add_stack_beam_index(beam_index, 0, 0)

        self.stacking_algorithm(working_loc)

        self.assertEqual(
            self.stacking_algorithm.data_stack_size,
            expected["data_stack_size"]
        )
        # TODO: Activate this test when surface types are implemented
        # self.assertEqual(
        #     self.stacking_algorithm.surface_type,
        #     SurfaceType(expected["surface_type"])
        # )

        # beam_angles_surf
        self.assertTrue(
            np.allclose(
                self.stacking_algorithm.beam_angles_surf,
                expected["beam_angles_surf"]
            ),
            msg="beam_angles_surf do not match expected values"
        )
        # t0_surf
        self.assertTrue(
            np.allclose(
                self.stacking_algorithm.t0_surf,
                expected["t0_surf"]
            ),
            msg="t0_surf do not match expected values"
        )
        # doppler_angles_surf
        self.assertTrue(
            np.allclose(
                self.stacking_algorithm.doppler_angles_surf,
                expected["doppler_angles_surf"]
            ),
            msg="doppler_angles_surf do not match expected values"
        )
        # look_angles_surf
        self.assertTrue(
            np.allclose(
                self.stacking_algorithm.look_angles_surf,
                expected["look_angles_surf"]
            ),
            msg="look_angles_surf do not match expected values"
        )
        # pointing_angles_surf
        self.assertTrue(
            np.allclose(
                self.stacking_algorithm.pointing_angles_surf,
                expected["pointing_angles_surf"]
            ),
            msg="pointing_angles_surf do not match expected values"
        )

