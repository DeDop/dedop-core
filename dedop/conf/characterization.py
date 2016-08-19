from .auxiliary_file_reader import *
from .constants import ConstantsFile

from typing import Any


class CharacterisationFile(AuxiliaryFileReader):
    """
    class for loading the Characterisation File
    """
    _id = "CHD"

    pitch_bias = AuxiliaryParameter(
        "pitch_bias_chd",
        """pitch bias measured in-flight""",
        param_type=float)
    n_samples_sar = AuxiliaryParameter(
        "N_samples_sar_chd",
        """number of samples per each SAR pulse""",
        param_type=int)
    power_tx_ant_ku = AuxiliaryParameter(
        "power_tx_ant_ku_chd",
        """antenna SSPA RF peak transmitted power in Ku band""",
        param_type=float)
    onboard_proc_sar_raw = AuxiliaryParameter(
        "onboard_proc_sar_raw_chd",
        """combination of on-board fixed digital gains for the SAR raw digital
            chain from ADC converter to TM (it includes ADC, FFTs, beta)""",
        param_type=float)
    yaw_bias = AuxiliaryParameter(
        "yaw_bias_chd",
        """yaw bias measured in-flight""",
        param_type=float)
    freq_ku = AuxiliaryParameter(
        "freq_ku_chd",
        """emitted frequency in Ku-band""",
        param_type=float)
    rfu_rx_gain_ground = AuxiliaryParameter(
        "rfu_rx_gain_ground_chd",
        """combination of RFU gains in the receiving chain""",
        param_type=float)
    pulse_length = AuxiliaryParameter(
        "pulse_length_chd",
        """pulse length""",
        param_type=float)
    bw_ku = AuxiliaryParameter(
        "bw_ku_chd",
        """Ku-band bandwidth""",
        param_type=float)
    n_ku_pulses_burst = AuxiliaryParameter(
        "N_ku_pulses_burst_chd",
        """number of ku-band pulses per burst""",
        param_type=int)
    cai_cor2_unit_conv = AuxiliaryParameter(
        "cai_cor2_unit_conv_chd",
        """factor that converts CAI to COR2 units""",
        param_type=float)
    h0_cor2_unit_conv = AuxiliaryParameter(
        "h0_cor2_unit_conv_chd",
        """factor that converts H0 to COR2 units""",
        param_type=int)
    i_sample_start = AuxiliaryParameter(
        "i_sample_start_chd",
        """the RMC ASIC truncates the time domain burst and keeps only
            the range gates with indexes going from (i_sample_start) to
            (i_sample_start_chd + N_samples_sar_chd // 2-1)""",
        param_type=int)
    fai_shift_number = AuxiliaryParameter(
        "fai_shift_number_chd",
        """number of fai shifts to complete one sample in LRM and SAR
            science waveforms""",
        param_type=int)
    t0_h0_unit_conv = AuxiliaryParameter(
        "T0_h0_unit_conv_chd",
        """factor that converts T0 to H0 units""",
        param_type=float)
    antenna_gain_ku = AuxiliaryParameter(
        "antenna_gain_ku_chd",
        """antenna gain for ku-band""")
    roll_bias = AuxiliaryParameter(
        "roll_bias_chd",
        """roll bias measured in-flight""",
        param_type=float)
    pri_T0_unit_conv = AuxiliaryParameter(
        "pri_T0_unit_conv_chd",
        """factor for converting from PRI to T0 units""",
        param_type=float)
    uso_freq_nom = AuxiliaryParameter(
        "uso_freq_nom_chd",
        """USO frequency nominal value""",
        param_type=float)
    alt_freq_multiplier = AuxiliaryParameter(
        "alt_freq_multiplier_chd",
        param_type=float)
    pri_sar = AuxiliaryParameter(
        "pri_sar_chd",
        """pulse repetition interval""",
        param_type=float)
    mean_sat_alt = AuxiliaryParameter(
        "mean_sat_alt_chd",
        """mean altitude of the satellite""",
        param_type=float)

    @property
    def chirp_slope_ku(self) -> float:
        """the chirp slope for the Ku-band (derived parameter)"""
        if self._chirp_slope_ku is None:
            self._chirp_slope_ku = self.bw_ku / self.pulse_length
        return self._chirp_slope_ku

    @property
    def wv_length_ku(self) -> float:
        """the Ku-band wavelength (derived parameter)"""
        if self._wv_length_ku is None:
            self._wv_length_ku = self.cst.c / self.freq_ku
        return self._wv_length_ku

    @property
    def t0_nom(self):
        return 1. / (self.uso_freq_nom * self.alt_freq_multiplier)

    def __init__(self, cst: ConstantsFile, filename: str=None, **kwargs: Any):
        """
        create a new CharacterisationFile object
        """
        self._wv_length_ku = kwargs.pop(
            'wv_length_ku_chd', None
        )
        self._chirp_slope_ku = kwargs.pop(
            'chirp_slope_ku_chd', None
        )

        self.cst = cst
        super().__init__(filename, **kwargs)
