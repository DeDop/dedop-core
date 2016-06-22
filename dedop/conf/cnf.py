from .constants_reader import *

class ConfigurationFile(ConstantsFileReader):
    """
    class for loading the Configuration File
    """
    # Processing and Testing

    @property
    def pu_seed(self):
        """Pu initial seed"""
        return self["pu_seed_cnf"]

    @property
    def flag_doppler_range_correction(self):
        """Flag that activates the Doppler range correction in the geometry
            corrections: Deactivated (false); Activated (true)"""
        return self["flag_doppler_range_correction_cnf"]

    @property
    def n_samples_fitting_raw(self):
        """Number of samples (without zero padding) of the RAW L1B waveform to
            fit"""
        return self["n_samples_fitting_raw_cnf"]

    @property
    def zero_freq_sample_number_sar(self):
        """Sample number of the ZERO frequency position in SAR mode"""
        return self["zero_freq_sample_number_sar_cnf"]

    @property
    def num_lobes_int_cal1(self):
        """Number of secondary lobes to interpolate at each side in addition to the
            main lobe [0,4]"""
        return self["num_lobes_int_cal1_cnf"]

    @property
    def sigma_alt_surf_th(self):
        """Threshold that determines whether a surface has low or high
            variability"""
        return self["sigma_alt_surf_th_cnf"]

    @property
    def n_samples_fitting_rmc(self):
        """Number of samples (without zero padding) of the RMC L1B waveform to
            fit"""
        return self["n_samples_fitting_rmc_cnf"]

    @property
    def k_fact_int_cal1(self):
        """Interpolation samples ratio"""
        return self["k_fact_int_cal1_cnf"]

    @property
    def N_beams_sub_stack(self):
        """Number of beams per sub-stack"""
        return self["N_beams_sub_stack_cnf"]

    @property
    def thermal_noise_flag(self):
        """Estimate thermal noise (1) ; Set thermal noise to 0 (0)"""
        return self["thermal_noise_flag_cnf"]

    @property
    def left_avoided_samples_cal2(self):
        """Number of CAL2 samples to be avoided at the left spectrum edge for the
            normalisation"""
        return self["left_avoided_samples_cal2_cnf"]

    @property
    def num_samp_out_wfm(self):
        """Number of PTR waveform samples shown in CAL1 L1B output file"""
        return self["num_samp_out_wfm_cnf"]

    @property
    def flag_cal1_power(self):
        """Flag that indicates the CAL1 power type: CAL1 L1B total power (0); CAL1
            L1B max power (1)"""
        return self["flag_cal1_power_cnf"]

    @property
    def thermal_noise_first_range_bin(self):
        """First range bin (from 0, without zero padding) of the thermal noise
            estimation window"""
        return self["thermal_noise_first_range_bin_cnf"]

    @property
    def flag_azimuth_processing_method(self):
        """Flag that indicates the azimuth processing method:
            Surface dependant (0); Approximate (1); Exact (2)"""
        return self["flag_azimuth_processing_method_cnf"]

    @property
    def flag_window_delay_alignment_method(self):
        """Flag to indicate the window delay alignment method:
            Surface dependent (0); Beam max integrated power (1);
            Satellite position above surface (2); Look angle 0 (3);
            Doppler angle 0 (4)"""
        return self["flag_window_delay_alignment_method_cnf"]

    @property
    def parameter_fitting_flag(self):
        """Fit sigma_z parameter (0) ; fit roughness parameter (1)"""
        return self["parameter_fitting_flag_cnf"]

    @property
    def flag_cal2_correction(self):
        """Flag that activates the CAL2 corrections:
            Deactivated (false); Activated (true)"""
        return self["flag_cal2_correction_cnf"]

    @property
    def flag_avoid_zeros_in_multilooking(self):
        """Flag that indicates if the samples set to zero in the beams will be
            avoided when averaging in multi-looking: No (false); Yes (true)"""
        return self["flag_avoid_zeros_in_multilooking_cnf"]

    @property
    def zp_fact_range(self):
        """Zero padding factor used during range compression"""
        return self["zp_fact_range_cnf"]

    @property
    def flag_antenna_weighting(self):
        """Flag that activates the antenna weighting:
            Deactivated (false); Activated (true)"""
        return self["flag_antenna_weighting_cnf"]

    @property
    def sigma_z_seed(self):
        """Sigma_z initial seed"""
        return self["sigma_z_seed_cnf"]

    @property
    def min_num_contributing_looks(self):
        """Minimum number of contributing looks in the L1B record in order to fit
            the waveform of that record"""
        return self["min_num_contributing_looks_cnf"]

    @property
    def roughness_seed(self):
        """Roughness initial seed"""
        return self["roughness_seed_cnf"]

    @property
    def zero_freq_sample_number_lrm(self):
        """Sample number of the ZERO frequency position in LRM mode"""
        return self["zero_freq_sample_number_lrm_cnf"]

    @property
    def flag_remove_doppler_ambiguities(self):
        """Flag that indicates if the Doppler ambiguities will be removed:
            No (false); Yes (true)"""
        return self["flag_remove_doppler_ambiguities_cnf"]

    @property
    def step_avg_cal1_pulse(self):
        """Time elapsed between two consecutive output records in CAL1 Pulse mode"""
        return self["step_avg_cal1_pulse_cnf"]

    @property
    def flag_postphase_azimuth_processing(self):
        """Flag that activates the post-phase azimuth corrections:
            Deactivated (false); Activated (true)"""
        return self["flag_postphase_azimuth_processing_cnf"]

    @property
    def flag_surface_weighting(self):
        """Flag that activates the surface weighting:
            Deactivated (false); Activated (true)"""
        return self["flag_surface_weighting_cnf"]

    @property
    def right_avoided_samples_cal2(self):
        """Number of CAL2 samples to be avoided at the right spectrum edge for the
            normalisation"""
        return self["right_avoided_samples_cal2_cnf"]

    @property
    def N_looks_stack(self):
        """Number of looks in 1 stack"""
        return self["N_looks_stack_cnf"]

    @property
    def flag_cal1_source(self):
        """Flag that indicates the CAL1 corrections source:
            CAL1 L1B (0); CAL1 on-ground (1)"""
        return self["flag_cal1_source_cnf"]

    @property
    def decimation_fact_range_l1bs(self):
        """Decimation factor in range dimension applied in the waveforms in the
            L1B-S product"""
        return self["decimation_fact_range_l1bs_cnf"]

    @property
    def width_avg_cal1_pulse(self):
        """Width of the Running Window Averaging in CAL1 Pulse mode"""
        return self["width_avg_cal1_pulse_cnf"]

    @property
    def flag_slant_range_correction(self):
        """Flag that activates the slant range correction in the geometry
            corrections: Deactivated (false); Activated (true)"""
        return self["flag_slant_range_correction_cnf"]

    @property
    def flag_uso_correction(self):
        """Flag that activates the USO correction:
            Deactivated (false); Activated (true)"""
        return self["flag_uso_correction_cnf"]

    @property
    def max_fitting_iterations(self):
        """Maximum number of iterations allowed in the fitting routine"""
        return self["max_fitting_iterations_cnf"]

    @property
    def flag_l1bs_file(self):
        """Flag that activates the writing of the L1B-S file:
            Deactivated (false); Activated (true)"""
        return self["flag_l1bs_file_cnf"]

    @property
    def zero_pad_fact_cal1(self):
        """Zero Padding Factor"""
        return self["zero_pad_fact_cal1_cnf"]

    @property
    def flag_cal1_corrections(self):
        """Flag that activates the CAL1 corrections:
            Deactivated (false); Activated (true)"""
        return self["flag_cal1_corrections_cnf"]

    @property
    def thermal_noise_width(self):
        """Width of the thermal noise estimation window (without zero padding)"""
        return self["thermal_noise_width_cnf"]

    @property
    def flag_azimuth_weighting(self):
        """Flag that activates the azimuth weighting:
            Deactivated (false); Activated (true)"""
        return self["flag_azimuth_weighting_cnf"]

    @property
    def epoch_seed(self):
        """Epoch initial seed (without zero padding)"""
        return self["epoch_seed_cnf"]
