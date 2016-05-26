from ..input_dataset import InputDataset
from ..packet import InstrumentSourcePacket

import netCDF4 as nc
from enum import Enum


class L1ADimensions(Enum):
    echo_sample_ind = "echo_sample_ind"
    sar_ku_pulse_burst_ind = "sar_ku_pulse_burst_ind"
    sar_c_pulse_burst_ind = "sar_c_pulse_burst_ind"
    ltm_max_ind = "ltm_max_ind"
    time_l1a_echo_sar_ku = "time_l1a_echo_sar_ku"
    time_l1a_echo_plrm = "time_l1a_echo_plrm"


class L1AVariables(Enum):
    echo_sample_ind = "echo_sample_ind"
    sar_ku_pulse_burst_ind = "sar_ku_pulse_burst_ind"
    sar_c_pulse_burst_ind = "sar_c_pulse_burst_ind"
    ltm_max_ind = "ltm_max_ind"
    time_l1a_echo_sar_ku = "time_l1a_echo_sar_ku"
    UTC_day_l1a_echo_sar_ku = "UTC_day_l1a_echo_sar_ku"
    UTC_sec_l1a_echo_sar_ku = "UTC_sec_l1a_echo_sar_ku"
    UTC_time_20hz_l1a_echo_sar_ku = "UTC_time_20hz_l1a_echo_sar_ku"
    isp_coarse_time_l1a_echo_sar_ku = "isp_coarse_time_l1a_echo_sar_ku"
    isp_fine_time_l1a_echo_sar_ku = "isp_fine_time_l1a_echo_sar_ku"
    flag_time_status_l1a_echo_sar_ku = "flag_time_status_l1a_echo_sar_ku"
    sral_fine_time_l1a_echo_sar_ku = "sral_fine_time_l1a_echo_sar_ku"
    lat_l1a_echo_sar_ku = "lat_l1a_echo_sar_ku"
    lon_l1a_echo_sar_ku = "lon_l1a_echo_sar_ku"
    surf_type_l1a_echo_sar_ku = "surf_type_l1a_echo_sar_ku"
    burst_count_prod_l1a_echo_sar_ku = "burst_count_prod_l1a_echo_sar_ku"
    seq_count_l1a_echo_sar_ku = "seq_count_l1a_echo_sar_ku"
    burst_count_cycle_l1a_echo_sar_ku = "burst_count_cycle_l1a_echo_sar_ku"
    nav_bul_status_l1a_echo_sar_ku = "nav_bul_status_l1a_echo_sar_ku"
    nav_bul_source_l1a_echo_sar_ku = "nav_bul_source_l1a_echo_sar_ku"
    oper_instr_l1a_echo_sar_ku = "oper_instr_l1a_echo_sar_ku"
    SAR_mode_l1a_echo_sar_ku = "SAR_mode_l1a_echo_sar_ku"
    cl_gain_l1a_echo_sar_ku = "cl_gain_l1a_echo_sar_ku"
    acq_stat_l1a_echo_sar_ku = "acq_stat_l1a_echo_sar_ku"
    dem_eeprom_l1a_echo_sar_ku = "dem_eeprom_l1a_echo_sar_ku"
    weighting_l1a_echo_sar_ku = "weighting_l1a_echo_sar_ku"
    loss_track_l1a_echo_sar_ku = "loss_track_l1a_echo_sar_ku"
    h0_nav_dem_l1a_echo_sar_ku = "h0_nav_dem_l1a_echo_sar_ku"
    h0_applied_l1a_echo_sar_ku = "h0_applied_l1a_echo_sar_ku"
    cor2_nav_dem_l1a_echo_sar_ku = "cor2_nav_dem_l1a_echo_sar_ku"
    cor2_applied_l1a_echo_sar_ku = "cor2_applied_l1a_echo_sar_ku"
    dh0_l1a_echo_sar_ku = "dh0_l1a_echo_sar_ku"
    agccode_ku_l1a_echo_sar_ku = "agccode_ku_l1a_echo_sar_ku"
    agccode_c_l1a_echo_sar_ku = "agccode_c_l1a_echo_sar_ku"
    alt_l1a_echo_sar_ku = "alt_l1a_echo_sar_ku"
    orb_alt_rate_l1a_echo_sar_ku = "orb_alt_rate_l1a_echo_sar_ku"
    x_pos_l1a_echo_sar_ku = "x_pos_l1a_echo_sar_ku"
    y_pos_l1a_echo_sar_ku = "y_pos_l1a_echo_sar_ku"
    z_pos_l1a_echo_sar_ku = "z_pos_l1a_echo_sar_ku"
    x_vel_l1a_echo_sar_ku = "x_vel_l1a_echo_sar_ku"
    y_vel_l1a_echo_sar_ku = "y_vel_l1a_echo_sar_ku"
    z_vel_l1a_echo_sar_ku = "z_vel_l1a_echo_sar_ku"
    roll_sat_pointing_l1a_echo_sar_ku = "roll_sat_pointing_l1a_echo_sar_ku"
    pitch_sat_pointing_l1a_echo_sar_ku = "pitch_sat_pointing_l1a_echo_sar_ku"
    yaw_sat_pointing_l1a_echo_sar_ku = "yaw_sat_pointing_l1a_echo_sar_ku"
    roll_sral_mispointing_l1a_echo_sar_ku = "roll_sral_mispointing_l1a_echo_sar_ku"
    pitch_sral_mispointing_l1a_echo_sar_ku = "pitch_sral_mispointing_l1a_echo_sar_ku"
    yaw_sral_mispointing_l1a_echo_sar_ku = "yaw_sral_mispointing_l1a_echo_sar_ku"
    range_ku_l1a_echo_sar_ku = "range_ku_l1a_echo_sar_ku"
    int_path_cor_ku_l1a_echo_sar_ku = "int_path_cor_ku_l1a_echo_sar_ku"
    uso_cor_l1a_echo_sar_ku = "uso_cor_l1a_echo_sar_ku"
    cog_cor_l1a_echo_sar_ku = "cog_cor_l1a_echo_sar_ku"
    agc_ku_l1a_echo_sar_ku = "agc_ku_l1a_echo_sar_ku"
    scale_factor_ku_l1a_echo_sar_ku = "scale_factor_ku_l1a_echo_sar_ku"
    sig0_cal_ku_l1a_echo_sar_ku = "sig0_cal_ku_l1a_echo_sar_ku"
    i_meas_ku_l1a_echo_sar_ku = "i_meas_ku_l1a_echo_sar_ku"
    q_meas_ku_l1a_echo_sar_ku = "q_meas_ku_l1a_echo_sar_ku"
    gprw_meas_ku_l1a_echo_sar_ku = "gprw_meas_ku_l1a_echo_sar_ku"
    cal2_ku_ind_l1a_echo_sar_ku = "cal2_ku_ind_l1a_echo_sar_ku"
    burst_power_cor_ku_l1a_echo_sar_ku = "burst_power_cor_ku_l1a_echo_sar_ku"
    burst_phase_cor_ku_l1a_echo_sar_ku = "burst_phase_cor_ku_l1a_echo_sar_ku"
    cal1_ku_ind_l1a_echo_sar_ku = "cal1_ku_ind_l1a_echo_sar_ku"
    time_l1a_echo_plrm = "time_l1a_echo_plrm"
    i2q2_meas_ku_l1a_echo_plrm = "i2q2_meas_ku_l1a_echo_plrm"
    i2q2_meas_c_l1a_echo_plrm = "i2q2_meas_c_l1a_echo_plrm"


class L1ADataset(InputDataset):
    @property
    def max_index(self):
        # get size of primary dimension
        dim = self._dset.dimensions[
            L1ADimensions.time_l1a_echo_sar_ku.value
        ]
        return dim.size

    def __init__(self, filename, cst, chd):
        dset = nc.Dataset(filename)
        super().__init__(dset, cst, chd)

    def __getitem__(self, index):
        return InstrumentSourcePacket(
            self.cst, self.chd, self.echo_sample_ind[index],
            isp_pid=None,
            time_sar_ku=self.time_l1a_echo_sar_ku[index],
            days=self.UTC_day_l1a_echo_sar_ku[index],
            seconds=self.UTC_sec_l1a_echo_sar_ku[index],
            process_id=None,
            inst_id_sar_isp=None,
            pri_sar_pre_dat=None,
            ambiguity_order_sar=None,
            burst_sar_ku=None,
            burst_sar_ku_fbr=None,
            lat_sar_sat=self.lat_l1a_echo_sar_ku[index],
            lon_sar_sat=self.lon_l1a_echo_sar_ku[index],
            alt_sar_sat=self.alt_l1a_echo_sar_ku[index],
            alt_rate_sar_sat=self.orb_alt_rate_l1a_echo_sar_ku[index],
            x_vel_sar_sat=self.x_vel_l1a_echo_sar_ku[index],
            y_vel_sar_sat=self.y_vel_l1a_echo_sar_ku[index],
            z_vel_sar_sat=self.z_vel_l1a_echo_sar_ku[index],
            roll_sar=self.roll_sat_pointing_l1a_echo_sar_ku[index],
            pitch_sar=self.pitch_sat_pointing_l1a_echo_sar_ku[index],
            yaw_sar=self.yaw_sat_pointing_l1a_echo_sar_ku[index],
            h0_sar=None,
            t0_sar=None,
            cor2_sar=None,
            win_delay_sar_ku=self.range_ku_l1a_echo_sar_ku[index] * 2 / self.cst.c,
            x_sar_sat=self.x_pos_l1a_echo_sar_ku[index],
            y_sar_sat=self.y_pos_l1a_echo_sar_ku[index],
            z_sar_sat=self.z_pos_l1a_echo_sar_ku[index],
            waveform_cor_sar=None,
            doppler_angle_sar_sat=None,
            beams_focused=None
        )

    def __iter__(self):
        for index in range(self.max_index):
            return self[index]

    def __getattr__(self, variable_name):
        """
        return the requested variable from the netCDF file
        """
        return self._dset.variables[variable_name]
