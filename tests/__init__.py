from tests.conf import *
from tests.cli import *
from tests.gui import *
from tests.data import *
from tests.proc import *
from tests.util import *

import unittest
import os

def run_tests():
    os.chdir('test_data/')
    unittest.main()