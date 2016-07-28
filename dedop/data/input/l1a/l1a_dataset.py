from enum import Enum
from math import log10, radians
from typing import Iterator

import netCDF4 as nc

from dedop.conf import ConfigurationFile, CharacterisationFile, ConstantsFile
from dedop.model.l1a_processing_data import L1AProcessingData, PacketPid
from ..input_dataset import InputDataset


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


class L1ADataset(InputDataset):
    def __init__(self, filename: str, cst: ConstantsFile, chd: CharacterisationFile, cnf: ConfigurationFile):
        """
        The L1ADataset class reads L1A NetCDF data files.
        """
        dset = nc.Dataset(filename)
        super().__init__(dset, cst=cst, chd=chd, cnf=cnf)

        self._file_path = filename
        self._last_index = 0

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def max_index(self) -> int:
        """get size of primary dimension"""
        dim = self._dset.dimensions[
            L1ADimensions.time_l1a_echo_sar_ku.value
        ]
        return dim.size

    def __getitem__(self, index: int) -> L1AProcessingData:
        # convert scale factor to linear value
        scale_factor = 20 * log10(self.scale_factor_ku_l1a_echo_sar_ku[index])
        # construct waveform
        waveform = scale_factor * (self.i_meas_ku_l1a_echo_sar_ku[index, :, :] +
                              1j * self.q_meas_ku_l1a_echo_sar_ku[index, :, :])
        packet = L1AProcessingData(
            self.cst, self.chd, index,
            isp_pid=PacketPid.echo_sar,
            time_sar_ku=self.time_l1a_echo_sar_ku[index],
            isp_coarse_time=self.isp_coarse_time_l1a_echo_sar_ku[index],
            isp_fine_time=self.isp_fine_time_l1a_echo_sar_ku[index],
            sral_fine_time=self.sral_fine_time_l1a_echo_sar_ku[index],
            days=self.UTC_day_l1a_echo_sar_ku[index],
            seconds=self.UTC_sec_l1a_echo_sar_ku[index],
            inst_id_sar_isp=0,
            pri_sar_pre_dat=0,
            ambiguity_order_sar=0,
            burst_sar_ku=self.burst_count_prod_l1a_echo_sar_ku[index],
            lat_sar_sat=radians(self.lat_l1a_echo_sar_ku[index]),
            lon_sar_sat=radians(self.lon_l1a_echo_sar_ku[index]),
            alt_sar_sat=self.alt_l1a_echo_sar_ku[index],
            alt_rate_sat_sar=self.orb_alt_rate_l1a_echo_sar_ku[index],
            x_vel_sat_sar=self.x_vel_l1a_echo_sar_ku[index],
            y_vel_sat_sar=self.y_vel_l1a_echo_sar_ku[index],
            z_vel_sat_sar=self.z_vel_l1a_echo_sar_ku[index],
            roll_sar=radians(self.roll_sral_mispointing_l1a_echo_sar_ku[index]),
            pitch_sar=radians(self.pitch_sral_mispointing_l1a_echo_sar_ku[index]),
            yaw_sar=radians(self.yaw_sral_mispointing_l1a_echo_sar_ku[index]),
            h0_sar=self.h0_applied_l1a_echo_sar_ku[index],
            t0_sar=self.chd.t0_nom * (1. + 2. * self.uso_cor_l1a_echo_sar_ku[index] / self.cst.c),
            cor2_sar=self.cor2_applied_l1a_echo_sar_ku[index],
            win_delay_sar_ku=self.range_ku_l1a_echo_sar_ku[index] * 2 / self.cst.c,
            x_sar_sat=self.x_pos_l1a_echo_sar_ku[index],
            y_sar_sat=self.y_pos_l1a_echo_sar_ku[index],
            z_sar_sat=self.z_pos_l1a_echo_sar_ku[index],
            waveform_cor_sar=waveform,
            beams_focused=None,
            flag_time_status=self.flag_time_status_l1a_echo_sar_ku[index],
            nav_bul_status=self.nav_bul_status_l1a_echo_sar_ku[index],
            nav_bul_source=self.nav_bul_source_l1a_echo_sar_ku[index],
            source_seq_count=self.seq_count_l1a_echo_sar_ku[index],
            oper_instr=self.oper_instr_l1a_echo_sar_ku[index],
            SAR_mode=self.SAR_mode_l1a_echo_sar_ku[index],
            cl_gain=self.cl_gain_l1a_echo_sar_ku[index],
            acq_stat=self.acq_stat_l1a_echo_sar_ku[index],
            dem_eeprom=self.dem_eeprom_l1a_echo_sar_ku[index],
            loss_track=self.loss_track_l1a_echo_sar_ku[index],
            h0_nav_dem=self.h0_nav_dem_l1a_echo_sar_ku[index],
            h0_applied=self.h0_applied_l1a_echo_sar_ku[index],
            cor2_nav_dem=self.cor2_nav_dem_l1a_echo_sar_ku[index],
            cor2_applied=self.cor2_applied_l1a_echo_sar_ku[index],
            dh0=self.dh0_l1a_echo_sar_ku[index],
            agccode_ku=self.agccode_ku_l1a_echo_sar_ku[index],
            range_ku=self.range_ku_l1a_echo_sar_ku[index],
            int_path_cor_ku=self.int_path_cor_ku_l1a_echo_sar_ku[index],
            agc_ku=self.agc_ku_l1a_echo_sar_ku[index],
            sig0_cal_ku=self.sig0_cal_ku_l1a_echo_sar_ku[index]
        )
        packet.compute_location_sar_surf()
        packet.compute_doppler_angle()
        return packet

    def __iter__(self) -> Iterator[L1AProcessingData]:
        for index in range(self.max_index):
            packet = self[index]
            if self.in_range(packet):
                yield self[index]

    def __next__(self) -> L1AProcessingData:
        if self._last_index == self.max_index:
            return None
        while not self.in_range(self[self._last_index]):
            self._last_index += 1
            if self._last_index == self.max_index:
                return None
        packet = self[self._last_index]
        self._last_index += 1

        return packet

    def __getattr__(self, variable_name: str) -> nc.Variable:
        """
        return the requested variable from the netCDF file
        """
        return self._dset.variables[variable_name]
