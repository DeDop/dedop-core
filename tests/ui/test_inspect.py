from unittest import TestCase

from dedop.ui.inspect import inspect_l1b_product


class L1bProductInspectorTest(TestCase):
    # Ok, not really a test yet, but at least we import L1bInspector

    def test_without_file(self):
        with self.assertRaises(ValueError) as e:
            inspect_l1b_product(None)
        self.assertEquals(str(e.exception), 'product_file_path must be given')

    def test_with_file(self):
        inspect_l1b_product("test_data/data/test_l1b/temp/output.nc")
