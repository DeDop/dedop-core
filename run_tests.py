from tests import *

import unittest
import os

if __name__ == "__main__":
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'test_data')

    os.chdir(path)
    unittest.main()
