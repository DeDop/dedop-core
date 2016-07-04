from .constants_reader import *
from .cst import ConstantsFile

from typing import Any

class CharacterisationFile(ConstantsFileReader):
    """
    class for loading the Characterisation File
    """
    
    @property
    def pitch_bias(self) -> float:
        """Pitch bias measured in-flight"""
        return self["pitch_bias_chd"]
    
    @property
    def n_samples_sar(self) -> int:
        """Number of samples per each SAR pulse"""
        return self["N_samples_sar_chd"]

    @property
    def power_tx_ant_ku(self) -> float:
        """Antenna SSPA RF Peak Transmitted Power in Ku band"""
        return self["power_tx_ant_ku_chd"]

    @property
    def onboard_proc_sar_raw(self) -> float:
        """Combination of on-board fixed digital gains for the SAR Raw digital
            chain from ADC converter to TM (it includes ADC, FFTs, beta)"""
        return self["onboard_proc_sar_raw_chd"]
    
    @property
    def yaw_bias(self) -> float:
        """Yaw bias measured in-flight"""
        return self["yaw_bias_chd"]

    @property
    def freq_ku(self) -> float:
        """Emitted frequency in Ku-band"""
        return self["freq_ku_chd"]

    @property
    def rfu_rx_gain_ground(self) -> float:
        """Combination of RFU gains in the receiving chain"""
        return self["rfu_rx_gain_ground_chd"]
    
    @property
    def pulse_length(self) -> float:
        """Pulse length"""
        return self["pulse_length_chd"]

    @property
    def bw_ku(self) -> float:
        """Ku-band bandwidth"""
        return self["bw_ku_chd"]
    
    @property
    def n_ku_pulses_burst(self) -> int:
        """Number of Ku-band pulses per burst"""
        return self["N_ku_pulses_burst_chd"]
    
    @property
    def cai_cor2_unit_conv(self) -> float:
        """Factor that converts CAI to COR2 units"""
        return self["cai_cor2_unit_conv_chd"]

    @property
    def h0_cor2_unit_conv(self) -> float:
        """Factor that converts HO to COR2 units"""
        return self["h0_cor2_unit_conv_chd"]
    
    @property
    def i_sample_start(self) -> int:
        """The RMC ASIC truncates the time domain burst and keeps only the range
            gates with indexes going from (i_sample_start_chd) to
            (i_sample_start_chd + N_samples_sar_chd/2-1)"""
        return self["i_sample_start_chd"]
    
    @property
    def fai_shift_number(self) -> float:
        """Number of fai shifts to complete one sample in LRM and SAR science
            waveforms"""
        return self["fai_shift_number_chd"]
    
    @property
    def t0_h0_unit_conv(self) -> float:
        """Factor that converts T0 to H0 units"""
        return self["T0_h0_unit_conv_chd"]
    
    @property
    def antenna_gain_ku(self) -> float:
        """Antenna gain for Ku-band"""
        return self["antenna_gain_ku_chd"]

    @property
    def roll_bias(self) -> float:
        """Roll bias measured in-flight"""
        return self["roll_bias_chd"]

    @property
    def pri_T0_unit_conv(self) -> float:
        """Factor that converts PRI to T0 units"""
        return self["pri_T0_unit_conv_chd"]

    @property
    def uso_freq_nom(self) -> float:
        """uso freq nom value"""
        return self["uso_freq_nom_chd"]

    @property
    def alt_freq_multiplier(self) -> float:
        """alt freq multiplier value"""
        return self["alt_freq_multiplier_chd"]

    @property
    def pri_sar(self) -> float:
        """pulse repetition interval"""
        return self["pri_sar_chd"]

    @property
    def t0_nom(self) -> float:
        """nominal value for T0"""
        return 1. / (self.uso_freq_nom * self.alt_freq_multiplier)

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
    def mean_sat_alt(self) -> float:
        """mean satellite altitude"""
        return self["mean_sat_alt_chd"]
    
    def __init__(self, cst: ConstantsFile, filename: str=None, **kwargs: Any):
        self._wv_length_ku = kwargs.pop(
            'wv_length_ku_chd', None
        )
        self._chirp_slope_ku = kwargs.pop(
            'chirp_slope_ku_chd', None
        )

        self.cst = cst

        super().__init__(filename, **kwargs)
