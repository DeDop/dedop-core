import unittest

from dedop.proc.sar.algorithms import SurfaceLocationAlgorithm
from dedop.proc.sar.surface_location_data import SurfaceLocationData
from dedop.conf import ConstantsFile, CharacterisationFile
from dedop.io.input.packet import InstrumentSourcePacket
from ..testing import TestDataLoader, MockObject

class SurfaceLocationAlgorithmTests(unittest.TestCase):
    constants_file = "common/cst.json"
    characterisation_file = "common/chd.json"

    expected_01 = "proc/surface_location_algorithm/surface_location_algorithm_01/expected/"\
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_01.Expected_01.txt"
    input_01 = "proc/surface_location_algorithm/surface_location_algorithm_01/input/"\
               "input_isps.txt"

    expected_02 = "proc/surface_location_algorithm/surface_location_algorithm_02/expected/" \
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_02.Expected_01.txt"
    input_02_isps = "proc/surface_location_algorithm/surface_location_algorithm_02/input/" \
                    "input_isps.txt"
    input_02_surfs = "proc/surface_location_algorithm/surface_location_algorithm_02/input/" \
                    "input_surfs.txt"

    expected_03 = "proc/surface_location_algorithm/surface_location_algorithm_03/expected/" \
                  "Hr_Algorithms.Surface_Location_Algorithm_Processing_03.Expected_01.txt"
    input_03_isps = "proc/surface_location_algorithm/surface_location_algorithm_03/input/" \
                    "input_isps.txt"
    input_03_surfs = "proc/surface_location_algorithm/surface_location_algorithm_03/input/" \
                     "input_surfs.txt"

    def setUp(self):
        self.cst = ConstantsFile(self.constants_file)
        self.chd = CharacterisationFile(self.characterisation_file)
        self.surface_location_algorithm = SurfaceLocationAlgorithm(self.chd, self.cst)

    def test_surface_location_algorithm_01(self):
        expected_data = TestDataLoader(self.expected_01, delim=' ')
        isps = list(MockObject.load_file(self.input_01, delim=' '))

        new_surf = self.surface_location_algorithm([], isps)

        self.assertTrue(new_surf, msg="failed to create new surface")

        surf = self.surface_location_algorithm.get_surface()

        self.assertAlmostEqual(surf["time_surf"], expected_data["time_surf"])

        self.assertAlmostEqual(surf["x_surf"], expected_data["x_surf"])
        self.assertAlmostEqual(surf["y_surf"], expected_data["y_surf"])
        self.assertAlmostEqual(surf["z_surf"], expected_data["z_surf"])

        self.assertAlmostEqual(surf["lat_surf"], expected_data["lat_surf"])
        self.assertAlmostEqual(surf["lon_surf"], expected_data["lon_surf"])
        self.assertAlmostEqual(surf["alt_surf"], expected_data["alt_surf"])

    def test_surface_location_algorithm_02(self):
        isps = list(MockObject.load_file(self.input_02_isps, delim=' '))
        isps = [InstrumentSourcePacket(i, self.cst, **isp) for i, isp in enumerate(isps)]

        surf = next(MockObject.load_file(self.input_02_surfs, delim=' '))
        surf.update(isps[0].__dict__)
        surfs = [SurfaceLocationData(surf, self.cst, self.chd)]

        new_surf = self.surface_location_algorithm(surfs, isps)

        self.assertFalse(new_surf, msg="erroneously created new surface")

    def test_surface_location_algorithm_03(self):
        expected_data = TestDataLoader(self.expected_03, delim=' ')

        isps = list(MockObject.load_file(self.input_03_isps, delim=' '))
        isps = [InstrumentSourcePacket(i, self.cst, **isp) for i, isp in enumerate(isps)]

        surfs = list(MockObject.load_file(self.input_03_surfs, delim=' '))
        for surf in surfs:
            surf.update(isps[0].__dict__)
        surfs = [SurfaceLocationData(surf, self.cst, self.chd) for surf in surfs]

        new_surf = self.surface_location_algorithm(surfs, isps)

        self.assertTrue(new_surf, msg="failed to create new surface")

        surf = self.surface_location_algorithm.get_surface()

        self.assertAlmostEqual(surf["time_surf"][0, 0], expected_data["time_surf"])

        self.assertAlmostEqual(surf["x_surf"][0, 0], expected_data["x_surf"], delta=1e-5)
        self.assertAlmostEqual(surf["y_surf"][0, 0], expected_data["y_surf"], delta=1e-5)
        self.assertAlmostEqual(surf["z_surf"][0, 0], expected_data["z_surf"], delta=1e-5)

        self.assertAlmostEqual(surf["lat_surf"], expected_data["lat_surf"], delta=1e-12)
        self.assertAlmostEqual(surf["lon_surf"], expected_data["lon_surf"], delta=1e-12)
        self.assertAlmostEqual(surf["alt_surf"], expected_data["alt_surf"], delta=1e-4)