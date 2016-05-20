from .constants_reader import *


class CharacterisationFile(ConstantsFileReader):
    """
    class for loading the Characterisation File
    """

    _filename = "chd.json"
    
    @property
    def pitch_bias(self):
        """Pitch bias measured in-flight"""
        return self["pitch_bias_chd"].value
    
    @property
    def n_samples_sar(self):
        """Number of samples per each SAR pulse"""
        return self["N_samples_sar_chd"].value

    @property
    def power_tx_ant_ku(self):
        """Antenna SSPA RF Peak Transmitted Power in Ku band"""
        return self["power_tx_ant_ku_chd"].value

    @property
    def onboard_proc_sar_raw(self):
        """Combination of on-board fixed digital gains for the SAR Raw digital
            chain from ADC converter to TM (it includes ADC, FFTs, beta)"""
        return self["onboard_proc_sar_raw_chd"].value
    
    @property
    def yaw_bias(self):
        """Yaw bias measured in-flight"""
        return self["yaw_bias_chd"].value

    @property
    def freq_ku(self):
        """Emitted frequency in Ku-band"""
        return self["freq_ku_chd"].value

    @property
    def rfu_rx_gain_ground(self):
        """Combination of RFU gains in the receiving chain"""
        return self["rfu_rx_gain_ground_chd"].value
    
    @property
    def pulse_length(self):
        """Pulse length"""
        return self["pulse_length_chd"].value

    @property
    def bw_ku(self):
        """Ku-band bandwidth"""
        return self["bw_ku_chd"].value
    
    @property
    def n_ku_pulses_burst(self):
        """Number of Ku-band pulses per burst"""
        return self["N_ku_pulses_burst_chd"].value
    
    @property
    def cai_cor2_unit_conv(self):
        """Factor that converts CAI to COR2 units"""
        return self["cai_cor2_unit_conv_chd"].value

    @property
    def h0_cor2_unit_conv(self):
        """Factor that converts HO to COR2 units"""
        return self["h0_cor2_unit_conv_chd"].value
    
    @property
    def i_sample_start(self):
        """The RMC ASIC truncates the time domain burst and keeps only the range
            gates with indexes going from (i_sample_start_chd) to
            (i_sample_start_chd + N_samples_sar_chd/2-1)"""
        return self["i_sample_start_chd"].value
    
    @property
    def fai_shift_number(self):
        """Number of fai shifts to complete one sample in LRM and SAR science
            waveforms"""
        return self["fai_shift_number_chd"].value
    
    @property
    def t0_h0_unit_conv(self):
        """Factor that converts T0 to H0 units"""
        return self["T0_h0_unit_conv_chd"].value
    
    @property
    def antenna_gain_ku(self):
        """Antenna gain for Ku-band"""
        return self["antenna_gain_ku_chd"].value

    @property
    def roll_bias(self):
        """Roll bias measured in-flight"""
        return self["roll_bias_chd"].value

    @property
    def pri_T0_unit_conv(self):
        """Factor that converts PRI to T0 units"""
        return self["pri_T0_unit_conv_chd"].value
    
    def __init__(self, filename=None):
        if filename is None:
            filename = self._filename
        super().__init__(filename)