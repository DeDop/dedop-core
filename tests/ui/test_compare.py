import os
from unittest import TestCase

from dedop.ui.compare import compare_l1b_products


class L1bComparatorTest(TestCase):
    # Ok, not really a test yet, but at least we import L1bInspector

    def test_without_files(self):
        with self.assertRaises(ValueError) as e:
            compare_l1b_products(None, None)
        self.assertEqual(str(e.exception), 'file_path_1 must be given')

    def test_with_files(self):
        _root = os.path.join(os.path.dirname(__file__), '..', '..')
        _folder = os.path.join(_root, "test_data", "data", "test_l1bs", "temp")

        output_file = os.path.join(_folder, "output.nc")

        compare_l1b_products(output_file, output_file)

