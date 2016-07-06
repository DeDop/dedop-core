import numpy as np

from dedop.model import L1AProcessingData

from .cal_algorithm import CALAlgorithm


class CAL2Algorithm(CALAlgorithm):
    """
    the CAL2 correction algorithm
    """

    def __call__(self, record: L1AProcessingData) -> np.ndarray:
        """
        apply the CAL2 algorithm
        """
        cal2_correction =\
            record.gprw_meas_ku[:self.chd.n_samples_sar]

        self.wfm_cal2_corrected = np.empty(
            (record.waveform_cor_sar.shape), dtype=np.float64
        )
        self.wfm_cal2_corrected[:, :] =\
            record.waveform_cor_sar[:, :] * cal2_correction

        return self.wfm_cal2_corrected
