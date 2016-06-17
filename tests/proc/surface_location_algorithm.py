import unittest

from dedop.conf import ConstantsFile, CharacterisationFile
from dedop.data.input.packet import InstrumentSourcePacket
from dedop.model import SurfaceData
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

    def initialise_algorithm(self, input_data):
        self.cst = ConstantsFile(
            c_cst=input_data['c_cst'],
            pi_cst=input_data['pi_cst'],
            semi_major_axis_cst=input_data['semi_major_axis_cst'],
            flat_coeff_cst=input_data['flat_coeff_cst'],
            semi_minor_axis_cst=input_data['semi_minor_axis_cst']
        )
        self.chd = CharacterisationFile(
            self.cst,
            freq_ku_chd=input_data['freq_ku_chd'],
            N_ku_pulses_burst_chd=input_data['n_ku_pulses_burst_chd'],
            pri_sar_pre_dat=input_data['pri_sar_pre_dat']
        )
        self.surface_location_algorithm = SurfaceLocationAlgorithm(self.chd, self.cst)

    def test_surface_location_algorithm_01(self):
        """
        surface location algorithm test 01
        ----------------------------------

        loads an input ISP and passes it as an initial
        item to the surface location algorithm.

        expected result is for the algorithm to create
        an initial surface location. Values of this
        location are validated.
        """
        # load expected data
        expected_data = TestDataLoader(self.expected_01, delim=' ')
        # load input data
        isp = TestDataLoader(self.input_01, delim=' ')

        self.initialise_algorithm(isp)

        # create ISP object
        isps = [
            InstrumentSourcePacket(
                self.cst, self.chd,
                time_sar_ku=isp["time_sar_ku"],
                lat_sar_sat=isp["lat_sar_sat"],
                lon_sar_sat=isp["lon_sar_sat"],
                alt_sar_sat=isp["alt_sar_sat"],
                win_delay_sar_ku=isp["win_delay_sar_ku"],
                x_sar_sat=0,
                y_sar_sat=0,
                z_sar_sat=0,
                alt_rate_sat_sar=0,
                roll_sar=0,
                pitch_sar=0,
                yaw_sar=0,
                x_vel_sat_sar=0,
                y_vel_sat_sar=0,
                z_vel_sat_sar=0
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

        # generate input ISP objects
        isps = [
            InstrumentSourcePacket(self.cst, self.chd, i,
                                   time_sar_ku=time,
                                   lat_sar_sat=inputs["lat_sar_sat"][i],
                                   lon_sar_sat=inputs["lon_sar_sat"][i],
                                   alt_sar_sat=inputs["alt_sar_sat"][i],
                                   win_delay_sar_ku=inputs["win_delay_sar_ku"][i])\
                for i, time in enumerate(inputs["time_sar_ku"])
        ]
        for isp in isps:
            isp.compute_location_sar_surf()

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

        # create all input ISP objects
        isps = [
            InstrumentSourcePacket(self.cst, self.chd, i,
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
                                   z_vel_sat_sar=0) \
            for i, time in enumerate(inputs["time_sar_ku"])
            ]
        # calculate surface position for each ISP
        for isp in isps:
            isp.compute_location_sar_surf()

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