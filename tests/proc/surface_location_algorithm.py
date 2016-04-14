import unittest

from dedop.proc.sar.algorithms import SurfaceLocationAlgorithm
from dedop.conf import ConstantsFile, CharacterisationFile
from ..testing import TestDataLoader, MockObject

class SurfaceLocationAlgorithmTests(unittest.TestCase):
    constants_file = "common/cst.json"
    characterisation_file = "common/chd.json"

    expected_01 = "proc/surface_location_algorithm/surface_location_algorithm_01/expected/"\
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_01.Expected_01.txt"
    input_01 = "proc/surface_location_algorithm/surface_location_algorithm_01/input/"\
               "Hr_Algorithms.Surface_Location_Algorithm_Processing_01.Input_01.txt"

    expected_02 = "proc/surface_location_algorithm/surface_location_algorithm_02/expected/" \
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_02.Expected_01.txt"
    input_02 = "surface_location_algorithm/surface_location_algorithm_02/input/" \
               "Hr_Algorithms.Surface_Location_Algorithm_Processing_02.Input_01.txt"

    expected_03 = "proc/surface_location_algorithm/surface_location_algorithm_03/expected/" \
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_03.Expected_01.txt"
    input_03 = "proc/surface_location_algorithm/surface_location_algorithm_03/input/" \
               "Hr_Algorithms.Surface_Location_Algorithm_Processing_03.Input_01.txt"

    def setUp(self):
        cst = ConstantsFile(self.constants_file)
        chd = CharacterisationFile(self.characterisation_file)
        self.surface_location_algorithm = SurfaceLocationAlgorithm(chd, cst)

    def test_surface_location_algorithm_01(self):
        expected_data = TestDataLoader(self.expected_01)
        isp = MockObject(self.input_01)

        surf = self.surface_location_algorithm([], [isp])

        self.assertIsNotNone(surf)

        self.assertAlmostEqual(surf.time_surf, expected_data["time_surf"])

        self.assertAlmostEqual(surf.x_surf, expected_data["x_surf"])
        self.assertAlmostEqual(surf.y_surf, expected_data["y_surf"])
        self.assertAlmostEqual(surf.z_surf, expected_data["z_surf"])

        self.assertAlmostEqual(surf.lat_surf, expected_data["lat_surf"])
        self.assertAlmostEqual(surf.lon_surf, expected_data["lon_surf"])
        self.assertAlmostEqual(surf.alt_surf, expected_data["alt_surf"])

    def test_surface_location_algorithm_02(self):
        isp = MockObject(self.input_02)

        surf = self.surface_location_algorithm(isp)

        self.assertIsNone(surf)

    def test_surface_location_algorithm_03(self):
        expected_data = TestDataLoader(self.expected_03)
        isp = MockObject(self.input_03)

        surf = self.surface_location_algorithm(isp)

        self.assertIsNotNone(surf)

        self.assertAlmostEqual(surf.time_surf, expected_data["time_surf"])

        self.assertAlmostEqual(surf.x_surf, expected_data["x_surf"])
        self.assertAlmostEqual(surf.y_surf, expected_data["y_surf"])
        self.assertAlmostEqual(surf.z_surf, expected_data["z_surf"])

        self.assertAlmostEqual(surf.lat_surf, expected_data["lat_surf"])
        self.assertAlmostEqual(surf.lon_surf, expected_data["lon_surf"])
        self.assertAlmostEqual(surf.alt_surf, expected_data["alt_surf"])