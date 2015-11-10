from ctypes import *
from collections import namedtuple
from .packet import CryosatPacket


CHD = namedtuple('CHD', 'n_ku_pulses_burst n_samples_sar')
chd = CHD(64, 256)


class ModeStruct(Structure):
    _fields_ = [
        ('mode', c_int16, 6),
        ('sar_in_deg_case', c_int16, 1),
        ('_reserved1', c_int16, 1),
        ('cal4', c_int16, 1),
        ('platform_cont', c_int16, 2),
        ('_reserved2', c_int16, 5),
    ]


class InstrConfigStruct(Structure):
    _fields_ = [
        ('rx_in_use', c_int32, 2),
        ('siral_id', c_int32, 1),
        ('_reserved1', c_int32, 1),
        ('bandwidth', c_int32, 2),
        ('_reserved2', c_int32, 2),
        ('tracking_mode', c_int32, 2),
        ('ext_calibration', c_int32, 1),
        ('_reserved3', c_int32, 1),
        ('loop_stat', c_int32, 1),
        ('loss_echo', c_int32, 1),
        ('real_time_error', c_int32, 1),
        ('echo_sat_error', c_int32, 1),
        ('rx_band_attenuation', c_int32, 1),
        ('cycle_report', c_int32, 1),
        ('star_tracker_1', c_int32, 1),
        ('star_tracker_2', c_int32, 1),
        ('star_tracker_3', c_int32, 1),
        ('_reserved4', c_int32, 1),
    ]


class ConfiDataStruct(Structure):
    _fields_ = [
        ('block_degraded', c_uint32, 1),
        ('blank_block', c_uint32, 1),
        ('datation_degraded', c_uint32, 1),
        ('orbit_prop_error', c_uint32, 1),
        ('orbit_file_change', c_uint32, 1),
        ('orbit_discon', c_uint32, 1),
        ('echo_sat', c_uint32, 1),
        ('other_echo_error', c_uint32, 1),

        ('rx1_error_for_sarin', c_uint32, 1),
        ('rx2_error_for_sarin', c_uint32, 1),
        ('window_delay_inconsistency', c_uint32, 1),
        ('agc_inconsistency', c_uint32, 1),
        ('cal1_correction_miss', c_uint32, 1),
        ('cal1_correction_from_ipf_db', c_uint32, 1),
        ('doris_uso_correction', c_uint32, 1),
        ('complex_cal_correction+_from_ipf_db', c_uint32, 1),

        ('trk_echo_error', c_uint32, 1),
        ('echo_rx1_error', c_uint32, 1),
        ('echo_rx2_error', c_uint32, 1),
        ('nmp_inconsistency', c_uint32, 1),
        ('azimuth_cal_missing', c_uint32, 1),
        ('azimuth_cal_from_ipf_db', c_uint32, 1),
        ('range_window_cal_function_mising', c_uint32, 1),
        ('range_window_cal_function_from_ipf_db', c_uint32, 1),

        ('_reserved1', c_uint32, 1),
        ('cal2_correction_missing', c_uint32, 1),
        ('cal2_correction_from_ipf_db', c_uint32, 1),
        ('power_scaling_error_lrm_only', c_uint32, 1),
        ('attitude_correction_missing', c_uint32, 1),
        ('attitude_interpolation_error', c_uint32, 1),
        ('_reserved2', c_uint32, 1),
        ('phase_peturbation', c_uint32, 1),
    ]


class CryosatTimeOrbit(Structure):
    _fields_ = [
        ('days', c_int32),
        ('seconds', c_uint32),
        ('microseconds', c_uint32),
        ('uso_correction', c_uint32),
        ('mode_id_cr', ModeStruct),
        ('source_seq_count_sar_ku_fbr', c_uint16),
        ('ins_configuration', InstrConfigStruct),
        ('burst_sar_ku', c_uint32),
        ('lat_sar_sat', c_int32),
        ('lon_sar_sat', c_int32),
        ('alt_sar_sat', c_int32),
        ('alt_rate_sar_sat', c_int32),
        ('x_vel_sat_sar', c_int32),
        ('y_vel_sat_sar', c_int32),
        ('z_vel_sat_sar', c_int32),
        ('real_beam_direction', c_int32 * 3),
        ('inferometer_baseline', c_int32 * 3),
        ('confidence_data', ConfiDataStruct)
    ]


class CryosatMeasurement(Structure):
    _fields_ = [
        ('win_delay_sar_ku', c_int64),
        ('h0_comp_sar_isp', c_int32),
        ('cor2_comp_sar_isp', c_int32),
        ('h0_sar_isp', c_int32),
        ('cor2_sar_isp', c_int32),
        ('att1_science', c_int32),
        ('att2_science', c_int32),
        ('tot_fixed_gain_1', c_int32),
        ('tot_fixed_gain_1', c_int32),
        ('transmit_power', c_int32),
        ('doppler_range_correction', c_int32),
        ('instrument_range_correction_tx_rx', c_int32),
        ('instrument_range_correction', c_int32),
        ('instrument_sigma0_correction_tx_rx', c_int32),
        ('instrument_sigma0_correction_rx', c_int32),
        ('internal_phase_correction', c_int32),
        ('external_phase_correction', c_int32),
        ('noise_power', c_int32),
        ('phase_slope_correction', c_int32),
        ('_reserved1', c_char * 4)
    ]


class CorrectionFlags(Structure):
    _fields_ = [
        ('flags_1', c_int32, 1),
        ('flags_2', c_int32, 1),
        ('flags_3', c_int32, 1),
        ('flags_4', c_int32, 1),
        ('flags_5', c_int32, 1),
        ('flags_6', c_int32, 1),
        ('flags_7', c_int32, 1),
        ('flags_8', c_int32, 1),
        ('flags_9', c_int32, 1),
        ('flags_10', c_int32, 1),
        ('flags_11', c_int32, 1),
        ('flags_12', c_int32, 1),
        ('flags_13', c_int32, 20),
    ]


class CryosatCorrections(Structure):
    _fields_ = [
        ('dry_tropo_correction', c_int32),
        ('wet_tropo_correction', c_int32),
        ('inverse_baro_correction', c_int32),
        ('dynamic_atmospheric_correction', c_int32),
        ('gim_iono_correction', c_int32),
        ('ocean_equilibrium_tide', c_int32),
        ('long_period_tide_height', c_int32),
        ('ocean_loading_tide', c_int32),
        ('solid_earth_tide', c_int32),
        ('geocentric_polar_tide', c_int32),
        ('surface_type_flag', c_int32),
        ('_reserved1', c_uint8 * 4),
        ('correction_status_flags', CorrectionFlags),
        ('correction_error_flags', CorrectionFlags),
        ('_reserved2', c_uint8 * 4),
    ]


class CryosatWaveforms(Structure):
    _fields_ = [
        ('wfm_iq_sar_ku_fbr_aux_1', c_int8 * chd.n_ku_pulses_burst * chd.n_samples_sar * 2),
        ('wfm_iq_sar_ku_fbr_aux_2', c_int8 * chd.n_ku_pulses_burst * chd.n_samples_sar * 2),
        ('nimp_sar_isp', c_uint16),
        ('_reserved', c_uint16)
    ]


class CryosatRecord(Structure):
    _fields_ = [
        ('time_orbit', CryosatTimeOrbit * 20),
        ('measurements', CryosatMeasurement * 20),
        ('corrections', CryosatCorrections),
        ('waveforms', CryosatWaveforms * 20),
    ]

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(20)
            return [self[i] for i in range(start, stop, step)]
        return self.measurements[index],\
               self.time_orbit[index],\
               self.waveforms[index],\
               self.corrections

    def __iter__(self):
        for i in range(20):
            yield self[i]
