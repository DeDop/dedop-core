from unittest import TestCase

from dedop.ui.inspect import inspect_l1b_product


class L1bProductInspectorTest(TestCase):
    def test_it(self):
        # Ok, not really a test yet, but at least we import L1bInspector
        with self.assertRaises(ValueError) as e:
            inspect_l1b_product(None, False)
        self.assertEquals(str(e.exception), 'file_path must be given')
