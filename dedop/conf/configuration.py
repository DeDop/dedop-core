from dedop.conf.enums import AzimuthWindowingMethod

from .auxiliary_file_reader import *


class ConfigurationFile(AuxiliaryFileReader):
    """
    class for loading the Configuration File
    """
    _id = "CNF"

    def __init__(self, filename: str=None, **kwargs: Any):
        super().__init__(filename, **kwargs)

    # corrections flags
    flag_cal2_correction = \
        AuxiliaryParameter("flag_cal2_correction_cnf")
    flag_uso_correction = \
        AuxiliaryParameter("flag_uso_correction_cnf")
    flag_cal1_corrections = \
        AuxiliaryParameter("flag_cal1_corrections_cnf")
    flag_cal1_intraburst_corrections = \
        AuxiliaryParameter("flag_cal1_intraburst_corrections_cnf")

    # surface focusing
    flag_surface_focusing = \
        AuxiliaryParameter("flag_surface_focusing_cnf")
    surface_focusing_lat = \
        AuxiliaryParameter("surface_focusing_lat_cnf")
    surface_focusing_lon = \
        AuxiliaryParameter("surface_focusing_lon_cnf")
    surface_focusing_alt = \
        AuxiliaryParameter("surface_focusing_alt_cnf")

    # azimuth processing
    flag_azimuth_processing_method = \
        AuxiliaryParameter("flag_azimuth_processing_method_cnf")
    flag_postphase_azimuth_processing = \
        AuxiliaryParameter("flag_postphase_azimuth_processing_cnf")
    flag_azimuth_windowing_method = \
        AuxiliaryParameter("flag_azimuth_windowing_method_cnf",
                           param_type=AzimuthWindowingMethod)
    azimuth_window_width = \
        AuxiliaryParameter("azimuth_window_width_cnf")

    # geometry corrections
    flag_doppler_range_correction = \
        AuxiliaryParameter("flag_doppler_range_correction_cnf")
    flag_slant_range_correction = \
        AuxiliaryParameter("flag_slant_range_correction_cnf")
    flag_window_delay_alignment_method = \
        AuxiliaryParameter("flag_window_delay_alignment_method_cnf")
    elevation_reference_value = \
        AuxiliaryParameter("elevation_reference_value_cnf")

    # stack masking
    flag_stack_masking = \
        AuxiliaryParameter("flag_stack_masking_cnf",
                           param_type=bool)
    flag_remove_doppler_ambiguities = \
        AuxiliaryParameter("flag_remove_doppler_ambiguities_cnf",
                           param_type=bool)
    ambiguity_mask_margin = \
        AuxiliaryParameter("ambiguity_mask_margin_cnf",
                           param_type=int)

    # multilooking
    flag_avoid_zeros_in_multilooking = \
        AuxiliaryParameter("flag_avoid_zeros_in_multilooking_cnf")
    flag_surface_weighting = \
        AuxiliaryParameter("flag_surface_weighting_cnf")
    flag_antenna_weighting = \
        AuxiliaryParameter("flag_antenna_weighting_cnf",
                           param_type=float)

    # generic
    zp_fact_range = \
        AuxiliaryParameter("zp_fact_range_cnf")
    n_looks_stack = \
        AuxiliaryParameter("N_looks_stack_cnf")

    # ROI
    min_lat = \
        AuxiliaryParameter("min_lat_cnf", optional=True)
    max_lat = \
        AuxiliaryParameter("max_lat_cnf", optional=True)
    min_lon = \
        AuxiliaryParameter("min_lon_cnf", optional=True)
    max_lon = \
        AuxiliaryParameter("max_lon_cnf", optional=True)
