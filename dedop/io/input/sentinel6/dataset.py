from ..input_dataset import InputDataset
import netCDF4 as ncdf

from .packet import Sentinel6Packet

class Sentinel6Dataset(InputDataset):
    @property
    def l1_mode_id_ku(self):
        return self._dset['l1_mode_id_ku']

    @property
    def time_day_ku(self):
        return self._dset['time_day_ku']

    @property
    def time_seconds_ku(self):
        return self._dset['time_seconds_ku']

    @property
    def tm_source_sequence_counter_ku(self):
        return self._dset['tm_source_sequence_counter_ku']

    @property
    def burst_counter_ku(self):
        return self._dset['burst_counter_ku']

    @property
    def latitude_ku(self):
        return self._dset['latitude_ku']

    @property
    def longitude_ku(self):
        return self._dset['longitude_ku']

    @property
    def com_altitude_ku(self):
        return self._dset['com_altitude_ku']

    @property
    def com_altitude_rate_ku(self):
        return self._dset['com_altitude_rate_ku']

    @property
    def com_velocity_vector_ku(self):
        return self._dset['com_velocity_vector_ku']

    @property
    def satellite_mispointing_ku(self):
        return self._dset['satellite_mispointing_ku']

    @property
    def mispointing_bias_ku(self):
        return self._dset['mispointing_bias_ku']

    @property
    def l1_instrument_configuration_ku(self):
        return self._dset['l1_instrument_configuration_ku']

    @property
    def l1a_mcd_ku(self):
        return self._dset['l1a_mcd_ku']

    @property
    def altimeter_range_calibrated_ku(self):
        return self._dset['altimeter_range_calibrated_ku']

    @property
    def range_corr_internal_delay_ku(self):
        return self._dset['range_corr_internal_delay_ku']

    @property
    def range_corr_com_ku(self):
        return self._dset['range_corr_com_ku']

    @property
    def attenuator_calibrated_ku(self):
        return self._dset['attenuator_calibrated_ku']

    @property
    def altimeter_power_drift_ku(self):
        return self._dset['altimeter_power_drift_ku']

    @property
    def power_corr_digital_processing_ku(self):
        return self._dset['power_corr_digital_processing_ku']

    @property
    def power_scaling_to_antenna_ku(self):
        return self._dset['power_scaling_to_antenna_ku']

    @property
    def altimeter_clock_ku(self):
        return self._dset['altimeter_clock_ku']

    @property
    def tm_h0_ku(self):
        return self._dset['tm_h0_ku']

    @property
    def tm_cor2_ku(self):
        return self._dset['tm_cor2_ku']

    @property
    def cai_ku(self):
        return self._dset['cai_ku']

    @property
    def fai_ku(self):
        return self._dset['fai_ku']

    @property
    def tm_pri_ku(self):
        return self._dset['tm_pri_ku']

    @property
    def tm_ambiguity_rank_ku(self):
        return self._dset['tm_ambiguity_rank_ku']

    @property
    def tm_nimp_ku(self):
        return self._dset['tm_nimp_ku']

    @property
    def tm_burst_num_ku(self):
        return self._dset['tm_burst_num_ku']

    @property
    def i_samples_ku(self):
        return self._dset['i_samples_ku']

    @property
    def q_samples_ku(self):
        return self._dset['q_samples_ku']

    @property
    def i_scale_factor_ku(self):
        return self._dset['i_scale_factor_ku']

    @property
    def q_scale_factor_ku(self):
        return self._dset['q_scale_factor_ku']

    @property
    def snr_estimation_ku(self):
        return self._dset['snr_estimation_ku']

    def __init__(self, filename):
        dset = ncdf.Dataset(filename)
        InputDataset.__init__(self, dset)

    def __getitem__(self, index):
        return Sentinel6Packet(index, self)