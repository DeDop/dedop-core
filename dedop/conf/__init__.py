"""
Processor configuration management.
"""

__author__ = 'DeDop Development Team'

__all__ = [
    'chd', 'cnf', 'cst'
]

from .chd import CharacterisationFile
from .cnf import ConfigurationFile
from .cst import ConstantsFile

chd = CharacterisationFile()
cnf = ConfigurationFile()
cst = ConstantsFile()