from .conf import *
from .cli import *
from .gui import *
from .io import *
from .proc import *
from .util import *

import unittest
import os

if __name__ == "__main__":
    os.chdir('test_data/')
    unittest.main()