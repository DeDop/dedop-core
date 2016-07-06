import numpy as np

from dedop.model import L1AProcessingData

from .cal_algorithm import CALAlgorithm


class CAL1Algorithm(CALAlgorithm):
    """
    algorithm for applying the CAL1 correction
    """
    def __call__(self, record: L1AProcessingData) -> np.ndarray:
        """
        apply the CAL1 correction
        """
        fft_length = self.chd.n_samples_sar * self.cnf.zero_pad_fact_cal1

        waveform_fft = np.fft.fft(
            record.waveform_cor_sar,
            n=fft_length, axis=1
        )
        waveform_fft = np.fft.fftshift(
            waveform_fft, axes=1
        )
        waveform_fft = self.apply_phase_correction(record, waveform_fft)
        waveform_fft = self.apply_power_correction(record, waveform_fft)

        # do ifft
        # unshift
        # return waveform

    def apply_phase_correction(self, record: L1AProcessingData, waveform_fft: np.ndarray) -> np.ndarray:
        """
        apply the phase correction
        """

    def apply_power_correction(self, record: L1AProcessingData, waveform_fft: np.ndarray) -> np.ndarray:
        """
        apply the power correction
        """