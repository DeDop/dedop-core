"""
Processor configuration management.
"""

__author__ = 'DeDop Development Team'

__all__ = [
    'CHD', 'CST', 'CNF'
]

from .chd import CharacterisationFile as CHD
from .cnf import ConfigurationFile as CNF
from .cst import ConstantsFile as CSTs

# chd = CharacterisationFile()
# cnf = ConfigurationFile()
# cst = ConstantsFile()