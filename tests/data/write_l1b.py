import os
import unittest
import netCDF4 as nc

from dedop.data.output import L1BWriter
from dedop.conf import CharacterisationFile, ConfigurationFile, ConstantsFile

from tests.testing import TestDataLoader

class L1BWriterTests(unittest.TestCase):
    _root = os.path.join(os.path.dirname(__file__), '..', '..')
    _folder = os.path.join(_root, "test_data", "common")
    _folder_data = os.path.join(_root, "test_data", "data")

    _output_name = os.path.join(_folder_data, "test_l1b", "temp", "l1b.nc")

    chd_file = os.path.join(_folder, "CHD.json")
    cnf_file = os.path.join(_folder, "CNF.json")
    cst_file = os.path.join(_folder, "CST.json")

    expected = os.path.join(_folder_data, "test_l1b", "expected", "expected.txt")

    def setUp(self):
        self.chd = CharacterisationFile(
            self.cst_file,
            self.chd_file
        )
        self.cnf = ConfigurationFile(
            self.cnf_file
        )
        self.cst = ConstantsFile(
            self.cst_file
        )

        self.writer = L1BWriter(self.chd, self.cnf, self.cst, self._output_name)
        self.writer.create_all_dimensions()
        self.writer.create_all_variables()


    def test_l1bs_output_01(self):
        expected = TestDataLoader(self.expected)

        self.writer.close()

        output = nc.Dataset(self._output_name)

        # removed legacy code, to be filled with proper test assertions
        # TODO: this test is broken

        output.close()


    def test_l1bs_output_02(self):
        pass
