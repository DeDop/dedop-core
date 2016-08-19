from .auxiliary_file_reader import *


class ConfigurationFile(AuxiliaryFileReader):
    """
    class for loading the Configuration File
    """
    _id = "CNF"

    def __init__(self, filename: str=None, **kwargs: Any):
        super().__init__(filename, **kwargs)

    # Processing and Testing

    pu_seed = \
        AuxiliaryParameter("pu_seed_cnf")
    flag_doppler_range_correction = \
        AuxiliaryParameter("flag_doppler_range_correction_cnf")
    n_samples_fitting_raw = \
        AuxiliaryParameter("n_samples_fitting_raw_cnf")
    zero_freq_sample_number_sar = \
        AuxiliaryParameter("zero_freq_sample_number_sar_cnf")
    num_lobes_int_cal1 = \
        AuxiliaryParameter("num_lobes_int_cal1_cnf")
    sigma_alt_surf_th = \
        AuxiliaryParameter("sigma_alt_surf_th_cnf")
    n_samples_fitting_rmc = \
        AuxiliaryParameter("n_samples_fitting_rmc_cnf")
    k_fact_int_cal1 = \
        AuxiliaryParameter("k_fact_int_cal1_cnf")
    N_beams_sub_stack = \
        AuxiliaryParameter("N_beams_sub_stack_cnf")
    thermal_noise_flag = \
        AuxiliaryParameter("thermal_noise_flag_cnf")
    left_avoided_samples_cal2 = \
        AuxiliaryParameter("left_avoided_samples_cal2_cnf")
    num_samp_out_wfm = \
        AuxiliaryParameter("num_samp_out_wfm_cnf")
    flag_cal1_power = \
        AuxiliaryParameter("flag_cal1_power_cnf")
    thermal_noise_first_range_bin = \
        AuxiliaryParameter("thermal_noise_first_range_bin_cnf")
    flag_azimuth_processing_method = \
        AuxiliaryParameter("flag_azimuth_processing_method_cnf")
    flag_window_delay_alignment_method = \
        AuxiliaryParameter("flag_window_delay_alignment_method_cnf")
    parameter_fitting_flag = \
        AuxiliaryParameter("parameter_fitting_flag_cnf")
    flag_cal2_correction = \
        AuxiliaryParameter("flag_cal2_correction_cnf")
    flag_avoid_zeros_in_multilooking = \
        AuxiliaryParameter("flag_avoid_zeros_in_multilooking_cnf")
    zp_fact_range = \
        AuxiliaryParameter("zp_fact_range_cnf")
    flag_antenna_weighting = \
        AuxiliaryParameter("flag_antenna_weighting_cnf")
    sigma_z_seed = \
        AuxiliaryParameter("sigma_z_seed_cnf")
    min_num_contributing_looks = \
        AuxiliaryParameter("min_num_contributing_looks_cnf")
    roughness_seed = \
        AuxiliaryParameter("roughness_seed_cnf")
    zero_freq_sample_number_lrm = \
        AuxiliaryParameter("zero_freq_sample_number_lrm_cnf")
    flag_remove_doppler_ambiguities = \
        AuxiliaryParameter("flag_remove_doppler_ambiguities_cnf")
    step_avg_cal1_pulse = \
        AuxiliaryParameter("step_avg_cal1_pulse_cnf")
    flag_postphase_azimuth_processing = \
        AuxiliaryParameter("flag_postphase_azimuth_processing_cnf")
    flag_surface_weighting = \
        AuxiliaryParameter("flag_surface_weighting_cnf")
    right_avoided_samples_cal2 = \
        AuxiliaryParameter("right_avoided_samples_cal2_cnf")
    n_looks_stack = \
        AuxiliaryParameter("N_looks_stack_cnf")
    flag_cal1_source = \
        AuxiliaryParameter("flag_cal1_source_cnf")
    decimation_fact_range_l1bs = \
        AuxiliaryParameter("decimation_fact_range_l1bs_cnf")
    width_avg_cal1_pulse = \
        AuxiliaryParameter("width_avg_cal1_pulse_cnf")
    flag_slant_range_correction = \
        AuxiliaryParameter("flag_slant_range_correction_cnf")
    flag_uso_correction = \
        AuxiliaryParameter("flag_uso_correction_cnf")
    max_fitting_iterations = \
        AuxiliaryParameter("max_fitting_iterations_cnf")
    flag_l1bs_file = \
        AuxiliaryParameter("flag_l1bs_file_cnf")
    zero_pad_fact_cal1 = \
        AuxiliaryParameter("zero_pad_fact_cal1_cnf")
    flag_cal1_corrections = \
        AuxiliaryParameter("flag_cal1_corrections_cnf")
    thermal_noise_width = \
        AuxiliaryParameter("thermal_noise_width_cnf")
    flag_azimuth_weighting = \
        AuxiliaryParameter("flag_azimuth_weighting_cnf")
    epoch_seed = \
        AuxiliaryParameter("epoch_seed_cnf")
    min_lat = \
        AuxiliaryParameter("min_lat_cnf", optional=True)
    max_lat = \
        AuxiliaryParameter("max_lat_cnf", optional=True)
    min_lon = \
        AuxiliaryParameter("min_lon_cnf", optional=True)
    max_lon = \
        AuxiliaryParameter("max_lon_cnf", optional=True)
