from unittest import TestCase

from dedop.ui.compare import compare_l1b_products


class L1bComparatorTest(TestCase):
    def test_it(self):
        # Ok, not really a test yet, but at least we import L1bComparator
        with self.assertRaises(ValueError) as e:
            compare_l1b_products(None, 'y', False)
        self.assertEquals(str(e.exception), 'output_path must be given')
        with self.assertRaises(ValueError) as e:
            compare_l1b_products('x', '', False)
        self.assertEquals(str(e.exception), 'output_path must be given')
