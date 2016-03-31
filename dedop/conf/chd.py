from .constants_reader import *


class CharacterisationFile(ConstantsFileReader):
    """
    class for loading the Characterisation File
    """

    _filename = "chd.json"
    
    @property
    def pitch_bias(self):
        """Pitch bias measured in-flight"""
        return self["pitch_bias_chd"]
    
    @property
    def max_power_ref_ground_cal1_sar_c(self):
        """Maximum power of the PTR (CAL1 SAR C) waveform measured on ground"""
        return self["max_power_ref_ground_cal1_sar_c_chd"]
    
    @property
    def onboard_proc_sar_c_cal1(self):
        """Combination of on-board fixed digital gains for the CAL1 SAR C digital
            chain from ADC converter to TM (it includes ADC, FFTs, beta)"""
        return self["onboard_proc_sar_c_cal1_chd"]
    
    @property
    def max_power_ref_ground_cal1_sar_ku(self):
        """Maximum power of the PTR (CAL1 SAR Ku) waveform measured on ground"""
        return self["max_power_ref_ground_cal1_sar_ku_chd"]
    
    @property
    def onboard_proc_lrm_ku_cal1(self):
        """Combination of on-board fixed digital gains for the CAL1 LRM Ku-band
            digital chain from ADC converter to TM (it includes ADC, FFTs, alpha)"""
        return self["onboard_proc_lrm_ku_cal1_chd"]
    
    @property
    def int_delay_ground_cal1_sar_c(self):
        """Internal delay of the PTR (CAL1 SAR C) waveform measured on ground"""
        return self["int_delay_ground_cal1_sar_c_chd"]
    
    @property
    def n_samples_sar(self):
        """Number of samples per each SAR pulse"""
        return self["N_samples_sar_chd"]
    
    @property
    def onboard_proc_sar_ku_cal1(self):
        """Combination of on-board fixed digital gains for the CAL1 SAR Ku digital
            chain from ADC converter to TM (it includes ADC, FFTs, beta)"""
        return self["onboard_proc_sar_ku_cal1_chd"]
    
    @property
    def power_tx_ant_ku(self):
        """Antenna SSPA RF Peak Transmitted Power in Ku band"""
        return self["power_tx_ant_ku_chd"]
    
    @property
    def int_delay_ground_cal1_lrm_ku(self):
        """Internal delay of the PTR (CAL1 LRM Ku) waveform measured on ground"""
        return self["int_delay_ground_cal1_lrm_ku_chd"]
    
    @property
    def n_samples_lrm(self):
        """Number of samples per each LRM pulse"""
        return self["N_samples_lrm_chd"]
    
    @property
    def tx1_lrm(self):
        """Time characterised on ground to shift the telemetered time to the
            previous transmitted pulse in LRM mode"""
        return self["tx1_lrm_chd"]
    
    @property
    def alt_freq_multiplier(self):
        """Factor to convert from USO frequency to altimeter frequency"""
        return self["alt_freq_multiplier_chd"]
    
    @property
    def n_cal_pulses_burst(self):
        """Number of Calibration pulses per burst"""
        return self["N_cal_pulses_burst_chd"]
    
    @property
    def n_c_pulses_burst(self):
        """Number of C-band pulses per burst"""
        return self["N_c_pulses_burst_chd"]
    
    @property
    def antenna_beamwidth_c(self):
        """Antenna beamwidth at 3 dB for C-band"""
        return self["antenna_beamwidth_c_chd"]
    
    @property
    def onboard_proc_sar_raw(self):
        """Combination of on-board fixed digital gains for the SAR Raw digital
            chain from ADC converter to TM (it includes ADC, FFTs, beta)"""
        return self["onboard_proc_sar_raw_chd"]
    
    @property
    def z_cog(self):
        """Center of Gravity Z component in the satellite reference frame"""
        return self["z_cog_chd"]
    
    @property
    def yaw_bias(self):
        """Yaw bias measured in-flight"""
        return self["yaw_bias_chd"]
    
    @property
    def onboard_proc_lrm_c(self):
        """Combination of on-board fixed digital gains for the LRM C-band digital
            chain from ADC converter to TM (it includes ADC, FFTs, alpha)"""
        return self["onboard_proc_lrm_c_chd"]
    
    @property
    def onboard_proc_lrm_c_cal1(self):
        """Combination of on-board fixed digital gains for the CAL1 LRM C-band
            digital chain from ADC converter to TM (it includes ADC, FFTs, alpha)"""
        return self["onboard_proc_lrm_c_cal1_chd"]
    
    @property
    def freq_c(self):
        """Emitted frequency in C-band"""
        return self["freq_c_chd"]
    
    @property
    def freq_ku(self):
        """Emitted frequency in Ku-band"""
        return self["freq_ku_chd"]
    
    @property
    def ext_delay_ground_ku(self):
        """External delay between the duplexor and the antenna measured on ground
            (Ku-band)"""
        return self["ext_delay_ground_ku_chd"]
    
    @property
    def tx1_sar(self):
        """Time characterised on ground to shift the telemetered time to the
            previous transmitted pulse in SAR mode"""
        return self["tx1_sar_chd"]
    
    @property
    def total_power_ref_ground_cal1_lrm_ku(self):
        """Total power of the PTR (CAL1 LRM Ku) waveform measured on ground"""
        return self["total_power_ref_ground_cal1_lrm_ku_chd"]
    
    @property
    def total_power_ref_ground_cal1_sar_c(self):
        """Total power of the PTR (CAL1 SAR C) waveform measured on ground"""
        return self["total_power_ref_ground_cal1_sar_c_chd"]
    
    @property
    def var_dig_gain_lrm_c_cal1_ref(self):
        """Variable digital gain for the CAL1 LRM C digital chain measured
            on-ground"""
        return self["var_dig_gain_lrm_c_cal1_ref_chd"]
    
    @property
    def ext_delay_ground_c(self):
        """External delay between the duplexor and the antenna measured on ground
            (C-band)"""
        return self["ext_delay_ground_c_chd"]
    
    @property
    def x_cog(self):
        """Center of Gravity X component in the satellite reference frame"""
        return self["x_cog_chd"]
    
    @property
    def int_delay_ground_cal1_sar_ku(self):
        """Internal delay of the PTR (CAL1 SAR Ku) waveform measured on ground"""
        return self["int_delay_ground_cal1_sar_ku_chd"]
    
    @property
    def n_bursts_cycle(self):
        """Number of bursts in a tracking cycle"""
        return self["N_bursts_cycle_chd"]
    
    @property
    def attcode_ground_cal1_lrm_ku(self):
        """Calibration ATT code for CAL1 LRM Ku measured on ground"""
        return self["attcode_ground_cal1_lrm_ku_chd"]
    
    @property
    def n_ku_pulses_rc(self):
        """Number of Ku-band pulses in a radar cycle"""
        return self["N_ku_pulses_rc_chd"]
    
    @property
    def var_dig_gain_pulse_cal1_ref(self):
        """Variable digital gain for the CAL1 Pulse digital chain measured
            on-ground"""
        return self["var_dig_gain_pulse_cal1_ref_chd"]
    
    @property
    def rfu_rx_gain_ground(self):
        """Combination of RFU gains in the receiving chain"""
        return self["rfu_rx_gain_ground_chd"]
    
    @property
    def z_ant(self):
        """Antenna Z component in the satellite reference frame"""
        return self["z_ant_chd"]
    
    @property
    def attcode_ground_cal1_lrm_c(self):
        """Calibration ATT code for CAL1 C Ku measured on ground"""
        return self["attcode_ground_cal1_lrm_c_chd"]
    
    @property
    def onboard_proc_pulse_cal1(self):
        """Combination of on-board fixed digital gains for the CAL1 Pulse digital
            chain from ADC converter to TM (it includes ADC, FFTs, beta)"""
        return self["onboard_proc_pulse_cal1_chd"]
    
    @property
    def mean_sat_alt(self):
        """Mean satellite altitude"""
        return self["mean_sat_alt_chd"]
    
    @property
    def pulse_length(self):
        """Pulse length"""
        return self["pulse_length_chd"]
    
    @property
    def onboard_proc_sar_rmc(self):
        """Combination of on-board fixed digital gains for the SAR RMC digital
            chain from ADC converter to TM (it includes ADC, FFTs, delta)"""
        return self["onboard_proc_sar_rmc_chd"]
    
    @property
    def max_power_ref_ground_cal1_lrm_ku(self):
        """Maximum power of the PTR (CAL1 LRM Ku) waveform measured on ground"""
        return self["max_power_ref_ground_cal1_lrm_ku_chd"]
    
    @property
    def total_power_ref_ground_cal1_sar_ku(self):
        """Total power of the PTR (CAL1 SAR Ku) waveform measured on ground"""
        return self["total_power_ref_ground_cal1_sar_ku_chd"]
    
    @property
    def onboard_proc_pulse_cal1_ref(self):
        """Combination of fixed digital gains for the CAL1 Pulse digital chain
            from ADC converter to TM (it includes ADC, FFTs, beta) measured
            on-ground"""
        return self["onboard_proc_pulse_cal1_ref_chd"]
    
    @property
    def var_dig_gain_lrm_ku_cal1_ref(self):
        """Variable digital gain for the CAL1 LRM Ku digital chain measured
            on-ground"""
        return self["var_dig_gain_lrm_ku_cal1_ref_chd"]
    
    @property
    def bw_ku(self):
        """Ku-band bandwidth"""
        return self["bw_ku_chd"]
    
    @property
    def var_dig_gain_sar_ku_cal1_ref(self):
        """Variable digital gain for the CAL1 SAR Ku digital chain measured
            on-ground"""
        return self["var_dig_gain_sar_ku_cal1_ref_chd"]
    
    @property
    def y_ant(self):
        """Antenna Y component in the satellite reference frame"""
        return self["y_ant_chd"]
    
    @property
    def y_cog(self):
        """Center of Gravity Y component in the satellite reference frame"""
        return self["y_cog_chd"]
    
    @property
    def n_ku_pulses_burst(self):
        """Number of Ku-band pulses per burst"""
        return self["N_ku_pulses_burst_chd"]
    
    @property
    def onboard_proc_lrm_ku_cal1_ref(self):
        """Combination of fixed digital gains for the CAL1 LRM Ku-band digital
            chain from ADC converter to TM (it includes ADC, FFTs, alpha) measured
            on-ground"""
        return self["onboard_proc_lrm_ku_cal1_ref_chd"]
    
    @property
    def antenna_gain_c(self):
        """Antenna gain for C-band"""
        return self["antenna_gain_c_chd"]
    
    @property
    def cai_cor2_unit_conv(self):
        """Factor that converts CAI to COR2 units"""
        return self["cai_cor2_unit_conv_chd"]
    
    @property
    def max_power_ref_ground_cal1_lrm_c(self):
        """Maximum power of the PTR (CAL1 LRM C) waveform measured on ground"""
        return self["max_power_ref_ground_cal1_lrm_c_chd"]
    
    @property
    def h0_cor2_unit_conv(self):
        """Factor that converts HO to COR2 units"""
        return self["h0_cor2_unit_conv_chd"]
    
    @property
    def onboard_proc_lrm_ku(self):
        """Combination of on-board fixed digital gains for the LRM Ku-band digital
            chain from ADC converter to TM (it includes ADC, FFTs, alpha)"""
        return self["onboard_proc_lrm_ku_chd"]
    
    @property
    def i_sample_start(self):
        """The RMC ASIC truncates the time domain burst and keeps only the range
            gates with indexes going from (i_sample_start_chd) to
            (i_sample_start_chd + N_samples_sar_chd/2-1)"""
        return self["i_sample_start_chd"]
    
    @property
    def fine_shift_number(self):
        """Number of fine shifts to complete one sample in CAL1 LRM waveforms"""
        return self["fine_shift_number_chd"]
    
    @property
    def fai_shift_number(self):
        """Number of fai shifts to complete one sample in LRM and SAR science
            waveforms"""
        return self["fai_shift_number_chd"]
    
    @property
    def t0_h0_unit_conv(self):
        """Factor that converts T0 to H0 units"""
        return self["T0_h0_unit_conv_chd"]
    
    @property
    def power_tx_ant_c(self):
        """SSPA RF Peak Transmitted Power in C band"""
        return self["power_tx_ant_c_chd"]
    
    @property
    def antenna_gain_ku(self):
        """Antenna gain for Ku-band"""
        return self["antenna_gain_ku_chd"]
    
    @property
    def antenna_beamwidth_ku(self):
        """Antenna beamwidth at 3 dB for Ku-band"""
        return self["antenna_beamwidth_ku_chd"]
    
    @property
    def attcode_ground_cal1_sar_ku(self):
        """Calibration ATT code for CAL1 SAR Ku measured on ground"""
        return self["attcode_ground_cal1_sar_ku_chd"]
    
    @property
    def onboard_proc_sar_ku_cal1_ref(self):
        """Combination of fixed digital gains for the CAL1 SAR Ku digital chain
            from ADC converter to TM (it includes ADC, FFTs, beta) measured
            on-ground"""
        return self["onboard_proc_sar_ku_cal1_ref_chd"]
    
    @property
    def uso_nominal_freq(self):
        """USO nominal frequency"""
        return self["uso_nominal_freq_chd"]
    
    @property
    def x_ant(self):
        """Antenna X component in the satellite reference frame"""
        return self["x_ant_chd"]
    
    @property
    def attcode_ground_cal1_sar_c(self):
        """Calibration ATT code for CAL1 SAR C measured on ground"""
        return self["attcode_ground_cal1_sar_c_chd"]
    
    @property
    def onboard_proc_lrm_c_cal1_ref(self):
        """Combination of fixed digital gains for the CAL1 LRM C-band digital chain
            from ADC converter to TM (it includes ADC, FFTs, alpha) measured
            on-ground"""
        return self["onboard_proc_lrm_c_cal1_ref_chd"]
    
    @property
    def roll_bias(self):
        """Roll bias measured in-flight"""
        return self["roll_bias_chd"]
    
    @property
    def int_delay_ground_cal1_lrm_c(self):
        """Internal delay of the PTR (CAL1 LRM C) waveform measured on ground"""
        return self["int_delay_ground_cal1_lrm_c_chd"]
    
    @property
    def ins_losses_ground(self):
        """Combination of instrument power losses in the receiving chain
            (waveguides, etc.)"""
        return self["ins_losses_ground_chd"]
    
    @property
    def n_c_pulses_rc(self):
        """Number of C-band pulses in a radar cycle"""
        return self["N_c_pulses_rc_chd"]
    
    @property
    def var_dig_gain_sar_c_cal1_ref(self):
        """Variable digital gain for the CAL1 SAR C digital chain measured
            on-ground"""
        return self["var_dig_gain_sar_c_cal1_ref_chd"]
    
    @property
    def bw_c(self):
        """C-band bandwidth"""
        return self["bw_c_chd"]
    
    @property
    def pri_T0_unit_conv(self):
        """Factor that converts PRI to T0 units"""
        return self["pri_T0_unit_conv_chd"]
    
    @property
    def onboard_proc_sar_c_cal1_ref(self):
        """Combination of fixed digital gains for the CAL1 SAR C digital chain from
            ADC converter to TM (it includes ADC, FFTs, beta) measured on-ground"""
        return self["onboard_proc_sar_c_cal1_ref_chd"]
    
    @property
    def total_power_ref_ground_cal1_lrm_c(self):
        """Total power of the PTR (CAL1 LRM C) waveform measured on ground"""
        return self["total_power_ref_ground_cal1_lrm_c_chd"]

    def __init__(self, filename=None):
        if filename is None:
            filename = self._filename
        super().__init__(filename)