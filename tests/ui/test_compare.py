from unittest import TestCase

from dedop.ui.compare import compare_l1b_products


class L1bComparatorTest(TestCase):
    # Ok, not really a test yet, but at least we import L1bInspector

    def test_without_files(self):
        with self.assertRaises(ValueError) as e:
            compare_l1b_products(None, None)
        self.assertEquals(str(e.exception), 'file_path_1 must be given')

    def test_with_files(self):
        compare_l1b_products("test_data/data/test_l1b/temp/output.nc",
                             "test_data/data/test_l1b/temp/output.nc")

