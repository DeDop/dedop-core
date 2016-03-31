from .conf import *
from .cli import *
from .gui import *
from .io import *
from .proc import *
from .util import *

import unittest
import os

def run_tests():
    os.chdir('test_data/')
    unittest.main()