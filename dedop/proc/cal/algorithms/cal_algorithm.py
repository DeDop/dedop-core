from abc import ABCMeta, abstractmethod
import numpy as np

from dedop.conf import ConfigurationFile, ConstantsFile, CharacterisationFile
from dedop.model import L1AProcessingData


class CALAlgorithm(metaclass=ABCMeta):
    """
    base class for CAL1 and CAL2 algorithms
    """
    def __init__(self, cst: ConstantsFile, chd: CharacterisationFile, cnf: ConfigurationFile):
        """
        initialise algorithm. Store references to config files.
        """
        self.cst = cst
        self.cnf = cnf
        self.chd = chd

    @abstractmethod
    def __call__(self, record: L1AProcessingData) -> np.ndarray:
        """
        apply the algorithm
        """
