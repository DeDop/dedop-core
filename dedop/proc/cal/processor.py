import numpy as np

from dedop.model import L1AProcessingData
from dedop.conf import ConstantsFile, CharacterisationFile, ConfigurationFile

from .algorithms import CAL1Algorithm, CAL2Algorithm


class CALProcessor:
    """
    the CAL processor
    """

    def __init__(self, cst: ConstantsFile, cnf: ConfigurationFile, chd: CharacterisationFile):
        """
        setup the CAL processor
        """
        self.cst = cst
        self.chd = chd
        self.cnf = cnf

        self.cal1 = CAL1Algorithm(
            cst=self.cst, chd=self.chd, cnf=self.cnf
        )
        self.cal2 = CAL2Algorithm(
            cst=self.cst, chd=self.chd, cnf=self.cnf
        )

    def process(self, record: L1AProcessingData) -> None:
        """
        apply CAL1 and CAL2 to the input record
        """
        if self.cnf.flag_cal1_corrections:
            cal1_corrected = self.cal1(record)
            record.waveform_cor_sar = cal1_corrected
        if self.cnf.flag_cal2_correction:
            cal2_corrected = self.cal2(record)
            record.waveform_cor_sar = cal2_corrected
