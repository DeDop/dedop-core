import unittest

from dedop.conf import ConstantsFile, CharacterisationFile, ConfigurationFile
from dedop.model import SurfaceData
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.proc.sar.algorithms import SurfaceLocationAlgorithm
from tests.testing import TestDataLoader

class SurfaceLocationAlgorithmTests(unittest.TestCase):
    expected_01 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_01/expected/"\
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_01.Expected_01.txt"
    input_01 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_01/input/"\
               "inputs.txt"

    expected_02 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_02/expected/" \
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_02.Expected_01.txt"
    input_02 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_02/input/" \
               "inputs.txt"

    expected_03 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_03/expected/" \
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_03.Expected_01.txt"
    input_03 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_03/input/" \
               "inputs.txt"

    expected_04 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_04/expected/" \
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_04.Expected_01.txt"
    input_04 = "test_data/proc/surface_location_algorithm/surface_location_algorithm_04/input/" \
               "inputs.txt"

    def initialise_algorithm(self, input_data: TestDataLoader):
        self.cnf = ConfigurationFile(
            flag_surface_focusing_cnf=input_data["flag_surface_focusing_cnf"],
            surface_focusing_lat_cnf=input_data.get("surface_focusing_lat_cnf"),
            surface_focusing_lon_cnf=input_data.get("surface_focusing_lon_cnf"),
            surface_focusing_alt_cnf=input_data.get("surface_focusing_alt_cnf")
        )
        self.cst = ConstantsFile(
            c_cst=input_data['c_cst'],
            pi_cst=input_data['pi_cst'],
            semi_major_axis_cst=input_data['semi_major_axis_cst'],
            flat_coeff_cst=input_data['flat_coeff_cst'],
            semi_minor_axis_cst=input_data['semi_minor_axis_cst'],
            sec_in_day_cst=60*60*24
        )
        self.chd = CharacterisationFile(
            self.cst,
            freq_ku_chd=input_data['freq_ku_chd'],
            N_ku_pulses_burst_chd=input_data['n_ku_pulses_burst_chd'],
            pri_sar_pre_dat=input_data['pri_sar_pre_dat']
        )
        self.surface_location_algorithm = SurfaceLocationAlgorithm(self.chd, self.cst, self.cnf)

    def test_surface_location_algorithm_01(self):
        """
        surface location algorithm test 01
        ----------------------------------

        loads an input packet and passes it as an initial
        item to the surface location algorithm.

        expected result is for the algorithm to create
        an initial surface location. Values of this
        location are validated.
        """
        # load expected data
        expected_data = TestDataLoader(self.expected_01, delim=' ')
        # load input data
        packet = TestDataLoader(self.input_01, delim=' ')

        self.initialise_algorithm(packet)

        # create packet object
        isps = [
            L1AProcessingData(
                self.cst, self.chd,
                time_sar_ku=packet["time_sar_ku"],
                lat_sar_sat=packet["lat_sar_sat"],
                lon_sar_sat=packet["lon_sar_sat"],
                alt_sar_sat=packet["alt_sar_sat"],
                win_delay_sar_ku=packet["win_delay_sar_ku"],
                x_sar_sat=0,
                y_sar_sat=0,
                z_sar_sat=0,
                alt_rate_sat_sar=0,
                roll_sar=0,
                pitch_sar=0,
                yaw_sar=0,
                x_vel_sat_sar=0,
                y_vel_sat_sar=0,
                z_vel_sat_sar=0,
                days=packet["time_sar_ku"] // self.cst.sec_in_day,
                seconds=packet["time_sar_ku"] % self.cst.sec_in_day
            )
        ]

        # execute surface location algorithm
        new_surf = self.surface_location_algorithm([], isps)

        # confirm new surface is created
        self.assertTrue(new_surf, msg="failed to create new surface")

        # retreive & validate surface properties
        surf = self.surface_location_algorithm.get_surface()

        self.assertAlmostEqual(surf["time_surf"], expected_data["time_surf"])

        self.assertAlmostEqual(surf["x_surf"], expected_data["x_surf"])
        self.assertAlmostEqual(surf["y_surf"], expected_data["y_surf"])
        self.assertAlmostEqual(surf["z_surf"], expected_data["z_surf"])

        self.assertAlmostEqual(surf["lat_surf"], expected_data["lat_surf"])
        self.assertAlmostEqual(surf["lon_surf"], expected_data["lon_surf"])
        self.assertAlmostEqual(surf["alt_surf"], expected_data["alt_surf"])

    def test_surface_location_algorithm_02(self):
        """
        surface location algorithm test 02
        ----------------------------------

        loads multiple input ISPs and one input surface location.
        expected result is for the surface location algorithm to
        determine that a new surface location should not yet be
        calculated
        """
        # load input data
        inputs = TestDataLoader(self.input_02, delim=' ')
        self.initialise_algorithm(inputs)

        # generate input packet objects
        isps = [
            L1AProcessingData(self.cst, self.chd, i,
                              time_sar_ku=time,
                              lat_sar_sat=inputs["lat_sar_sat"][i],
                              lon_sar_sat=inputs["lon_sar_sat"][i],
                              alt_sar_sat=inputs["alt_sar_sat"][i],
                              win_delay_sar_ku=inputs["win_delay_sar_ku"][i]) \
            for i, time in enumerate(inputs["time_sar_ku"])
            ]
        for packet in isps:
            packet.compute_location_sar_surf()

        # create prior surface location object
        surf = SurfaceData(self.cst, self.chd,
                           time_surf=inputs["time_surf"],
                           x_surf=inputs["x_surf"],
                           y_surf=inputs["y_surf"],
                           z_surf=inputs["z_surf"],
                           x_sat=inputs["x_sat"],
                           y_sat=inputs["y_sat"],
                           z_sat=inputs["z_sat"],
                           x_vel_sat=inputs["x_vel_sat"],
                           y_vel_sat=inputs["y_vel_sat"],
                           z_vel_sat=inputs["z_vel_sat"]
                           )
        surf.compute_surf_sat_vector()
        surf.compute_angular_azimuth_beam_resolution(
            inputs["pri_sar_pre_dat"]
        )

        # execute surface location algorithm
        new_surf = self.surface_location_algorithm([surf], isps)

        # confirm that no new surface is generated
        self.assertFalse(new_surf, msg="erroneously created new surface")

    def test_surface_location_algorithm_03(self):
        """
        surface location algorithm test 03
        ----------------------------------

        loads multiple input ISPs and one input surface location.
        expected result is for the surface location algorithm to
        generate a new surface location. The attributes of this
        new surface location are then validated against the expected
        values.
        """
        # load the expected data
        expected_data = TestDataLoader(self.expected_03, delim=' ')

        # load the input data
        inputs = TestDataLoader(self.input_03, delim=' ')

        self.initialise_algorithm(inputs)

        # create all input packet objects
        isps = [
            L1AProcessingData(self.cst, self.chd, i,
                              time_sar_ku=time,
                              lat_sar_sat=inputs["lat_sar_sat"][i],
                              lon_sar_sat=inputs["lon_sar_sat"][i],
                              alt_sar_sat=inputs["alt_sar_sat"][i],
                              win_delay_sar_ku=inputs["win_delay_sar_ku"][i],
                              x_sar_sat=0,
                              y_sar_sat=0,
                              z_sar_sat=0,
                              alt_rate_sat_sar=0,
                              roll_sar=0,
                              pitch_sar=0,
                              yaw_sar=0,
                              x_vel_sat_sar=0,
                              y_vel_sat_sar=0,
                              z_vel_sat_sar=0,
                              days=inputs["time_sar_ku"] // self.cst.sec_in_day,
                              seconds=inputs["time_sar_ku"] % self.cst.sec_in_day) \
            for i, time in enumerate(inputs["time_sar_ku"])
            ]
        # calculate surface position for each packet
        for packet in isps:
            packet.compute_location_sar_surf()

        # create the prior surface location object
        surf = SurfaceData(self.cst, self.chd,
                           time_surf=inputs["time_surf"],
                           x_surf=inputs["x_surf"],
                           y_surf=inputs["y_surf"],
                           z_surf=inputs["z_surf"],
                           x_sat=inputs["x_sat"],
                           y_sat=inputs["y_sat"],
                           z_sat=inputs["z_sat"],
                           x_vel_sat=inputs["x_vel_sat"],
                           y_vel_sat=inputs["y_vel_sat"],
                           z_vel_sat=inputs["z_vel_sat"]
                           )
        # compute properties of the surface location
        surf.compute_surf_sat_vector()
        surf.compute_angular_azimuth_beam_resolution(
            inputs["pri_sar_pre_dat"]
        )

        # execute the surface location algorithm
        new_surf = self.surface_location_algorithm([surf], isps)

        # confirm new surface has been created
        self.assertTrue(new_surf, msg="failed to create new surface")

        # retreive properties of the surface location
        surf = self.surface_location_algorithm.get_surface()

        # validate properties
        self.assertAlmostEqual(surf["time_surf"], expected_data["time_surf"])

        self.assertAlmostEqual(surf["x_surf"], expected_data["x_surf"], delta=1e-5)
        self.assertAlmostEqual(surf["y_surf"], expected_data["y_surf"], delta=1e-5)
        self.assertAlmostEqual(surf["z_surf"], expected_data["z_surf"], delta=1e-5)

        self.assertAlmostEqual(surf["lat_surf"], expected_data["lat_surf"], delta=1e-12)
        self.assertAlmostEqual(surf["lon_surf"], expected_data["lon_surf"], delta=1e-12)
        self.assertAlmostEqual(surf["alt_surf"], expected_data["alt_surf"], delta=1e-4)

    def test_surface_location_algorithm_04(self):
        """
        surface location algorithm test 04
        ----------------------------------

        loads multiple input ISPs and two input surface locations.
        expected result is for the surface location algorithm to
        generate a new surface location and focus the position of the previous
        one towards the target position. The attributes of these
        surface locations are then validated against the expected
        values.
        """
        # load the expected data
        expected_data = TestDataLoader(self.expected_04, delim=' ')

        # load the input data
        inputs = TestDataLoader(self.input_04, delim=' ')

        self.initialise_algorithm(inputs)

        # create all input packet objects
        isps = [
            L1AProcessingData(self.cst, self.chd, i,
                              time_sar_ku=time,
                              lat_sar_sat=inputs["lat_sar_sat"][i],
                              lon_sar_sat=inputs["lon_sar_sat"][i],
                              alt_sar_sat=inputs["alt_sar_sat"][i],
                              win_delay_sar_ku=inputs["win_delay_sar_ku"][i],
                              x_sar_sat=inputs["x_sar_sat"][i],
                              y_sar_sat=inputs["y_sar_sat"][i],
                              z_sar_sat=inputs["z_sar_sat"][i],
                              alt_rate_sat_sar=0,
                              roll_sar=inputs["roll_sar"][i],
                              pitch_sar=inputs["pitch_sar"][i],
                              yaw_sar=inputs["yaw_sar"][i],
                              x_vel_sat_sar=inputs["x_vel_sat_sar"][i],
                              y_vel_sat_sar=inputs["y_vel_sat_sar"][i],
                              z_vel_sat_sar=inputs["z_vel_sat_sar"][i],
                              days=inputs["time_sar_ku"] // self.cst.sec_in_day,
                              seconds=inputs["time_sar_ku"] % self.cst.sec_in_day) \
            for i, time in enumerate(inputs["time_sar_ku"])
            ]
        # calculate surface position for each packet
        for packet in isps:
            packet.compute_location_sar_surf()

        surfs = []
        # create the prior surface location object
        for i, time in enumerate(inputs["time_surf"]):
            surf = SurfaceData(
                self.cst, self.chd,
                time_surf=time,
                x_surf=inputs["x_surf"][i],
                y_surf=inputs["y_surf"][i],
                z_surf=inputs["z_surf"][i],
                lat_surf=inputs["lat_surf"][i],
                lon_surf=inputs["lon_surf"][i],
                alt_surf=inputs["alt_surf"][i],
                x_sat=inputs["x_sat"][i],
                y_sat=inputs["y_sat"][i],
                z_sat=inputs["z_sat"][i],
                lat_sat=inputs["lat_sat"][i],
                lon_sat=inputs["lon_sat"][i],
                alt_sat=inputs["alt_sat"][i],
                x_vel_sat=inputs["x_vel_sat"][i],
                y_vel_sat=inputs["y_vel_sat"][i],
                z_vel_sat=inputs["z_vel_sat"][i],
                focus_target_distance=inputs["focus_target_distance"][i],
                win_delay_surf=inputs["win_delay_surf"][i]
            )
            surf.compute_surf_sat_vector()
            surf.compute_angular_azimuth_beam_resolution(
                inputs["pri_sar_pre_dat"][i]
            )
            surfs.append(surf)

        # execute the surface location algorithm
        new_surf = self.surface_location_algorithm(surfs, isps)

        # confirm new surface has been created
        self.assertTrue(new_surf, msg="failed to create new surface")

        # retreive properties of the surface location
        surf = surfs[1]

        # validate properties
        self.assertAlmostEqual(surf.time_surf, expected_data["time_surf"])

        self.assertAlmostEqual(surf.x_surf, expected_data["x_surf"], delta=1e-5)
        self.assertAlmostEqual(surf.y_surf, expected_data["y_surf"], delta=1e-5)
        self.assertAlmostEqual(surf.z_surf, expected_data["z_surf"], delta=1e-5)

        self.assertAlmostEqual(surf.lat_surf, expected_data["lat_surf"], delta=1e-12)
        self.assertAlmostEqual(surf.lon_surf, expected_data["lon_surf"], delta=1e-12)
        self.assertAlmostEqual(surf.alt_surf, expected_data["alt_surf"], delta=1e-4)

        self.assertAlmostEqual(surf.win_delay_surf, expected_data["win_delay_surf"])
