from enum import Enum

import numpy as np
from math import degrees

from dedop.model import SurfaceData
from .netcdf_writer import NetCDFWriter
from ...conf import CharacterisationFile, ConfigurationFile, ConstantsFile


class L1BDimensions(Enum):
    time_l1b_echo_sar_ku = 'time_l1b_echo_sar_ku'
    echo_sample_ind = 'echo_sample_ind'
    max_multi_stack_ind = 'max_multi_stack_ind'


class L1BVariables(Enum):
    time_l1b_echo_sar_ku = 'time_l1b_echo_sar_ku'
    UTC_day_l1b_echo_sar_ku = 'UTC_day_l1b_echo_sar_ku'
    UTC_sec_l1b_echo_sar_ku = 'UTC_sec_l1b_echo_sar_ku'
    GPS_time_l1b_echo_sar_ku = 'GPS_time_l1b_echo_sar_ku'
    isp_coarse_time_l1b_echo_sar_ku = 'isp_coarse_time_l1b_echo_sar_ku'
    isp_fine_time_l1b_echo_sar_ku = 'isp_fine_time_l1b_echo_sar_ku'
    sral_fine_time_l1b_echo_sar_ku = 'sral_fine_time_l1b_echo_sar_ku'
    lat_l1b_echo_sar_ku = 'lat_l1b_echo_sar_ku'
    lon_l1b_echo_sar_ku = 'lon_l1b_echo_sar_ku'
    alt_l1b_echo_sar_ku = 'alt_l1b_echo_sar_ku'
    orb_alt_rate_l1b_echo_sar_ku = 'orb_alt_rate_l1b_echo_sar_ku'
    flag_time_status_l1b_echo_sar_ku = 'flag_time_status_l1b_echo_sar_ku'
    time_time_corr_val_l1b_echo_sar_ku = 'time_time_corr_val_l1b_echo_sar_ku'
    flag_man_pres_l1b_echo_sar_ku = 'flag_man_pres_l1b_echo_sar_ku'
    flag_man_thrust_l1b_echo_sar_ku = 'flag_man_thrust_l1b_echo_sar_ku'
    flag_man_plane_l1b_echo_sar_ku = 'flag_man_plane_l1b_echo_sar_ku'
    flag_gnss_status_l1b_echo_sar_ku = 'flag_gnss_status_l1b_echo_sar_ku'
    x_pos_l1b_echo_sar_ku = 'x_pos_l1b_echo_sar_ku'
    y_pos_l1b_echo_sar_ku = 'y_pos_l1b_echo_sar_ku'
    z_pos_l1b_echo_sar_ku = 'z_pos_l1b_echo_sar_ku'
    x_vel_l1b_echo_sar_ku = 'x_vel_l1b_echo_sar_ku'
    y_vel_l1b_echo_sar_ku = 'y_vel_l1b_echo_sar_ku'
    z_vel_l1b_echo_sar_ku = 'z_vel_l1b_echo_sar_ku'
    nav_bul_status_l1b_echo_sar_ku = 'nav_bul_status_l1b_echo_sar_ku'
    nav_bul_source_l1b_echo_sar_ku = 'nav_bul_source_l1b_echo_sar_ku'
    nav_bul_coarse_time_l1b_echo_sar_ku = 'nav_bul_coarse_time_l1b_echo_sar_ku'
    nav_bul_fine_time_l1b_echo_sar_ku = 'nav_bul_fine_time_l1b_echo_sar_ku'
    seq_count_l1b_echo_sar_ku = 'seq_count_l1b_echo_sar_ku'
    isp_time_status_echo_sar_ku = 'isp_time_status_echo_sar_ku'
    oper_instr_l1b_echo_sar_ku = 'oper_instr_l1b_echo_sar_ku'
    SAR_mode_l1b_echo_sar_ku = 'SAR_mode_l1b_echo_sar_ku'
    cl_gain_l1b_echo_sar_ku = 'cl_gain_l1b_echo_sar_ku'
    acq_stat_l1b_echo_sar_ku = 'acq_stat_l1b_echo_sar_ku'
    dem_eeprom_l1b_echo_sar_ku = 'dem_eeprom_l1b_echo_sar_ku'
    weighting_l1b_echo_sar_ku = 'weighting_l1b_echo_sar_ku'
    loss_track_l1b_echo_sar_ku = 'loss_track_l1b_echo_sar_ku'
    h0_nav_dem_l1b_echo_sar_ku = 'h0_nav_dem_l1b_echo_sar_ku'
    h0_applied_l1b_echo_sar_ku = 'h0_applied_l1b_echo_sar_ku'
    cor2_nav_dem_l1b_echo_sar_ku = 'cor2_nav_dem_l1b_echo_sar_ku'
    cor2_applied_l1b_echo_sar_ku = 'cor2_applied_l1b_echo_sar_ku'
    dh0_l1b_echo_sar_ku = 'dh0_l1b_echo_sar_ku'
    agccode_ku_l1b_echo_sar_ku = 'agccode_ku_l1b_echo_sar_ku'
    surf_type_l1b_echo_sar_ku = 'surf_type_l1b_echo_sar_ku'
    range_ku_l1b_echo_sar_ku = 'range_ku_l1b_echo_sar_ku'
    uso_cor_l1b_echo_sar_ku = 'uso_cor_l1b_echo_sar_ku'
    int_path_cor_ku_l1b_echo_sar_ku = 'int_path_cor_ku_l1b_echo_sar_ku'
    range_rate_l1b_echo_sar_ku = 'range_rate_l1b_echo_sar_ku'
    agc_ku_l1b_echo_sar_ku = 'agc_ku_l1b_echo_sar_ku'
    scale_factor_ku_l1b_echo_sar_ku = 'scale_factor_ku_l1b_echo_sar_ku'
    agc_cor_ku_l1b_echo_sar_ku = 'agc_cor_ku_l1b_echo_sar_ku'
    sig0_cal_ku_l1b_echo_sar_ku = 'sig0_cal_ku_l1b_echo_sar_ku'
    nb_stack_l1b_echo_sar_ku = 'nb_stack_l1b_echo_sar_ku'
    max_stack_l1b_echo_sar_ku = 'max_stack_l1b_echo_sar_ku'
    stdev_stack_l1b_echo_sar_ku = 'stdev_stack_l1b_echo_sar_ku'
    skew_stack_l1b_echo_sar_ku = 'skew_stack_l1b_echo_sar_ku'
    kurt_stack_l1b_echo_sar_ku = 'kurt_stack_l1b_echo_sar_ku'
    beam_ang_l1b_echo_sar_ku = 'beam_ang_l1b_echo_sar_ku'
    look_ang_l1b_echo_sar_ku = 'look_ang_l1b_echo_sar_ku'
    beam_form_l1b_echo_sar_ku = 'beam_form_l1b_echo_sar_ku'
    i2q2_meas_ku_l1b_echo_sar_ku = 'i2q2_meas_ku_l1b_echo_sar_ku'
    roll_sat_pointing_l1b_echo_sar_ku = 'roll_sat_pointing_l1b_echo_sar_ku'
    pitch_sat_pointing_l1b_echo_sar_ku = 'pitch_sat_pointing_l1b_echo_sar_ku'
    yaw_sat_pointing_l1b_echo_sar_ku = 'yaw_sat_pointing_l1b_echo_sar_ku'
    start_look_angle_stack_l1b_echo_sar_ku = 'start_look_angle_stack_l1b_echo_sar_ku'
    stop_look_angle_stack_l1b_echo_sar_ku = 'stop_look_angle_stack_l1b_echo_sar_ku'
    start_beam_ang_stack_l1b_echo_sar_ku = 'start_beam_ang_stack_l1b_echo_sar_ku'
    stop_beam_ang_stack_l1b_echo_sar_ku = 'stop_beam_ang_stack_l1b_echo_sar_ku'
    stack_mask_vector_l1b_echo_sar_ku = 'stack_mask_vector_l1b_echo_sar_ku'
    i2q2_scale_factor_l1b_echo_sar_ku = 'i2q2_scale_factor_l1b_echo_sar_ku'
    stack_scale_factor_ku_l1b_echo_sar_ku = 'stack_scale_factor_ku_l1b_echo_sar_ku'


class L1BWriterExtended(NetCDFWriter):
    """
    class for writing L1B netCDF files
    """
    def __init__(self, chd: CharacterisationFile, cnf: ConfigurationFile, cst: ConstantsFile, filename: str):
        """
        Initialize the L1BWriter Instance

        :param filename: the path of the output file to write
        """
        super().__init__(filename)
        self.chd = chd
        self.cnf = cnf
        self.cst = cst

        # create dimension definitions
        self.define_dimension(
            L1BDimensions.time_l1b_echo_sar_ku, None
        )
        self.define_dimension(
            L1BDimensions.echo_sample_ind, chd.n_samples_sar * cnf.zp_fact_range
        )
        self.define_dimension(
            L1BDimensions.max_multi_stack_ind, cnf.n_looks_stack
        )
        # create variable definitions
        self.define_variable(
            L1BVariables.time_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="UTC: l1b_echo_Sar_ku mode",
            calendar="gregorian",
            units="seconds since 2000-01-01 00:00:00.0"
        )
        self.define_variable(
            L1BVariables.UTC_day_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="day UTC: l1b_echo_sar_ku mode",
            units="days since 2000-01-01 00:00:00.0",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.UTC_sec_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="seconds in the day UTC: l1b_echo_sar_ku mode",
            units="seconds in the day",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.GPS_time_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="GPS time: l1b_echo_sar_ku mode",
            calendar="gregorian",
            units="seconds since 1980-01-06 00:00:00.0",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.isp_coarse_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP coarse time: l1b_echo_sar_ku mode",
            units="second",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.isp_fine_time_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP fine time: l1b_echo_sar_ku mode",
            units="2^-24 second",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.sral_fine_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP SRAL fine datation: l1b_echo_sar_ku mode",
            units="137.5*10^-9 second",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.lat_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="latitude: l1b_echo_sar_ku mode",
            standard_name="latitude",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="degrees_north",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.lon_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="longitude: l1b_echo_sar_ku mode",
            standard_name="longitude",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="degrees_east",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.alt_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altitude of satellite: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=700000.,
            units="m",
            fill_value=2147483647,
        )
        self.define_variable(
            L1BVariables.orb_alt_rate_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="orbital altitude rate: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="m/s",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.flag_time_status_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="time status flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="flag indicating if the time is synchronized or not with "
                    "GPS time",
            flag_meanings=(
                "synchronization",
                "no_synchronization"
            )
        )
        self.define_variable(
            L1BVariables.time_time_corr_val_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="time correlation validity flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01, 0x02),
            comment="flag indicating if the time correlation information is "
                    "valid provided by OBSE, valid provided by Ground Segment "
                    "or invalid",
            flag_meanings=(
                "valid_obsw",
                "valid_ground_segment",
                "invalid"
            )
        )
        self.define_variable(
            L1BVariables.flag_man_pres_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="manoeuvre presence flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "no_manoeuvre",
                "ongoing_manoeuvre"
            )
        )
        self.define_variable(
            L1BVariables.flag_man_thrust_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="manoeuvre thrust flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "no_thrust",
                "ongoing_thrust"
            )
        )
        self.define_variable(
            L1BVariables.flag_man_plane_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="manoeuvre plane flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "in_plane",
                "out_of_plane"
            )
        )
        self.define_variable(
            L1BVariables.flag_gnss_status_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="validty flag for the navigation message from the gnss receiver: l1b_echo_sar_ku mode",
            comment="indicating if the navigation message from the GNSS receiver is valid "
                    "or not valid/available",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "valid",
                "invalid_unavailable"
            )
        )
        self.define_variable(
            L1BVariables.x_pos_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite altitude - x component: l1b_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.y_pos_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite altitude - y component: l1b_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.z_pos_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite altitude - z component: l1b_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.x_vel_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite velocity - x component: l1b_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.y_vel_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite velocity - y component: l1b_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.z_vel_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite velocity - z component: l1b_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.nav_bul_status_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin status: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("ok", "ko"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.nav_bul_source_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin source identifier: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("gps", "doris"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.nav_bul_coarse_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin coarse time: l1b_echo_sar_ku mode",
            units="second",
            comment="value the closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.nav_bul_fine_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin fine time: l1b_echo_sar_ku mode",
            units="2^-24 second",
            comment="value the closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.seq_count_l1b_echo_sar_ku,
            np.uint16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="sequence count: l1b_echo_sar_ku mode",
            comment="value the closest in time to the reference measurement",
            fill_value=65535
        )
        self.define_variable(
            L1BVariables.isp_time_status_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP time status: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("SRAL_OBT_extrapolated",
                           "SRAL_OBT_updated_wth_SMU_OBT"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.oper_instr_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="operating instrument: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="Instrument A stands for SRAL Nominal and instrument B stands for SRAL Redundant",
            flag_meanings=("A", "B"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.SAR_mode_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="SAR mode identifier: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01, 0x02),
            comment="the values closest in time to the reference measurement",
            flag_meanings=(
                "closed_loop",
                "open_loop",
                "open_loop_fixed_gain"
            ),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.cl_gain_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="tracking_configuration - closed loop gain: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="the value closest in time to the reference measurement",
            flag_meanings=(
                "Nominal_value",
                "Nominal_value_with_back-off"
            ),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.acq_stat_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="tracking configuration - acquisition status: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=(
                "no_aquisition",
                "acquisition"
            ),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.dem_eeprom_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="tracking configuration - DEM EEPROM read access: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("enabled", "disabled"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.weighting_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altimeter configuration - weighting function: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("enabled", "disabled"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.loss_track_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="loss of track criterion: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("normal", "loss_of_track"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.h0_nav_dem_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altitude command H0 computed with nav DEM: l1b_echo_sar_ku mode",
            units="3.125/64*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.h0_applied_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="applied altitude command H0: l1b_echo_sar_ku mode",
            units="3.125/64*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.cor2_nav_dem_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altitude command COR2 computed with nav DEM: l1b_echo_sar_ku mode",
            units="3.125/1024*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.cor2_applied_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="applied altitude command COR2: l1b_echo_sar_ku mode",
            units="3.125/1024*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.dh0_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            # TODO: confirm this long_name is correct - field is truncated in PDFS.
            long_name="distance error computed on the echo of the cycle (N-2)"
                      " in open loop mode (current cycle): l1b_echo_sar_ku mode",
            units="3.125/64*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.agccode_ku_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="AGCCODE for ku band: l1b_echo_sar_ku mode",
            units="dB",
            comments="value closest in time to the reference measurement",
            fill_value=127
        )
        self.define_variable(
            L1BVariables.surf_type_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altimeter surface type: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01, 0x02, 0x03),
            comments="value closest in time to the reference measurement",
            flag_meanings=(
                "open_ocean_or_semi-enclosed_seas",
                "enclosed_seas_or_lakes",
                "continental_ice",
                "land"
            )
        )
        self.define_variable(
            L1BVariables.range_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="corrected range for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=700000.0,
            units="m",
            comment="reference range corrected for USO frequency drift and internal path correction",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.uso_cor_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="USO frequency drift correction: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=0.00,
            units="m",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.int_path_cor_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="internal path correction for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=0.00,
            units="m",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.range_rate_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="range rate: l1b_echo_sar_ku mode",
            scale_factor=1.0e-03,
            add_offset=0.00,
            units="m/s",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.agc_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="corrected AGC for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            comment="AGC corrected for instrumental errors - value the closest in time to the"
                    "reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.scale_factor_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="scaling factor for sigma0 evaluation for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            comment="scaling factor corrected for AGC instrumental errors and internal calibration",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.agc_cor_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="correction for instrument errors on AGC for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.sig0_cal_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="internal calibration correction on Sigma0 for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.nb_stack_l1b_echo_sar_ku,
            np.uint16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="number of waveforms summed in stack: l1b_echo_sar_ku mode",
            units="count",
            fill_value=65535
        )
        self.define_variable(
            L1BVariables.max_stack_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="maximum power of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="FFT power unit",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.stdev_stack_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="standard deviation of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="rad",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.skew_stack_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="skewness of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.kurt_stack_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="kurtosis of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.beam_ang_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,
             L1BDimensions.max_multi_stack_ind),
            long_name="doppler beam angles in stack: l1b_echo_sar_ku mode",
            comment="the useful values of the table are the first n_useful values where n_useful is"
                    "the number of waveforms summed in the stack",
            scale_factor=1.0e-06,
            add_offset=1.57,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.look_ang_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,
             L1BDimensions.max_multi_stack_ind),
            long_name="doppler look angles in stack: l1b_echo_sar_ku mode",
            comment="the useful values of the table are the first n_useful values where n_useful is"
                    "the number of waveforms summed in the stack",
            scale_factor=1.0e-06,
            add_offset=1.57,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.beam_form_l1b_echo_sar_ku,
            np.uint16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="flag on beam formation quality in stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="percent",
            fill_value=65535
        )
        self.define_variable(
            L1BVariables.i2q2_meas_ku_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,
             L1BDimensions.echo_sample_ind),
            long_name="I2+Q2 measurement for ku band: l1b_echo_sar_ku mode",
            comment="the echo is corrected for Doppler range effect, phase/power burst calibration "
                    "and GPRW effect. The echo is scaled using the i2q2_scale_factor_l1b_echo_sar_ku value",
            units="count",
            scale_factor=1./4294967294.,
            add_offset=0,
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.i2q2_scale_factor_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="I2+Q2 dynamic scale factor: l1b_echo_sar_ku mode",
            comment="Scale factor for the i2q2_meas_ku_l1b_echo_sar_ku waveform. The waveform should "
                    "be multiplied by this value after reading.",
            units="count"
        )
        # attitude vars
        self.define_variable(
            L1BVariables.roll_sat_pointing_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite pointing angle - roll: l1b_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BVariables.pitch_sat_pointing_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite pointing angle - pitch: l1b_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BVariables.yaw_sat_pointing_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite pointing angle - yaw: l1b_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )

        # beam & look angles
        self.define_variable(
            L1BVariables.start_look_angle_stack_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="start look angle in stack: l1b_echo_sar_ku mode",
            scale_factor=1e-6,
            add_offset=0,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.stop_look_angle_stack_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="stop look angle in stack: l1b_echo_sar_ku mode",
            scale_factor=1e-6,
            add_offset=0,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.start_beam_ang_stack_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="start doppler beam angle in stack: l1b_echo_sar_ku mode",
            units="rad",
            fill_value=32767,
            scale_factor=1e-6,
            add_offset=1.57
        )
        self.define_variable(
            L1BVariables.stop_beam_ang_stack_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="stop doppler beam angle in stack: l1b_echo_sar_ku mode",
            units="rad",
            fill_value=32767,
            scale_factor=1e-6,
            add_offset=1.57
        )
        # stack mask vector
        self.define_variable(
            L1BVariables.stack_mask_vector_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,
             L1BDimensions.max_multi_stack_ind),
            long_name="stack mask vector: l1b_echo_sar_ku mode",
            units="count",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.stack_scale_factor_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,
             L1BDimensions.max_multi_stack_ind),
            long_name="per-beam values for scaling factor for sigma0 evaluation for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            comment="scaling factor corrected for AGC instrumental errors and internal calibration (per-beam)",
            fill_value=2147483647
        )

    def write_record(self, surface_location_data: SurfaceData) -> None:
        """
        output a record to the L1B file.
        """

        closest_burst = surface_location_data.closest_burst

        time_interval = surface_location_data.time_surf - surface_location_data.prev_tai
        utc_secs = surface_location_data.prev_utc_secs + time_interval

        if utc_secs > surface_location_data.curr_day_length:
            utc_secs -= surface_location_data.curr_day_length
            utc_days = surface_location_data.prev_utc_days + 1
        else:
            utc_days = surface_location_data.prev_utc_days

        # scale_factor = pow(10, -closest_burst.agc_ku / 10)
        scale_factor = surface_location_data.waveform_multilooked.max()

        # import matplotlib.pyplot as plt
        # plt.plot(surface_location_data.waveform_multilooked)
        # plt.show()

        super().write_record(
            time_l1b_echo_sar_ku=surface_location_data.time_surf,
            UTC_day_l1b_echo_sar_ku=utc_days,
            UTC_sec_l1b_echo_sar_ku=utc_secs,
            GPS_time_l1b_echo_sar_ku=surface_location_data.gps_time_surf,
            isp_coarse_time_l1b_echo_sar_ku=closest_burst.isp_coarse_time,
            isp_fine_time_l1b_echo_sar_ku=closest_burst.isp_fine_time,
            sral_fine_time_l1b_echo_sar_ku=closest_burst.sral_fine_time,
            lat_l1b_echo_sar_ku=degrees(surface_location_data.lat_surf),
            lon_l1b_echo_sar_ku=degrees(surface_location_data.lon_surf),
            alt_l1b_echo_sar_ku=surface_location_data.alt_sat,
            orb_alt_rate_l1b_echo_sar_ku=surface_location_data.alt_rate_sat,
            flag_time_status_l1b_echo_sar_ku=closest_burst.flag_time_status,
            #  flag_time_corr_val_l1b_echo_sar_ku=None,  # closest_burst.flag_time_corr,
            flag_man_pres_l1b_echo_sar_ku=None,  # closest_burst.flag_man_pres,
            flag_man_thrust_l1b_echo_sar_ku=None,  # closest_burst.flag_man_thrust,
            flag_man_plane_l1b_echo_sar_ku=None,  # closest_burst.flag_man_plane,
            flag_gnss_status_l1b_echo_sar_ku=None,  # closest_burst.flag_gnss_status,
            x_pos_l1b_echo_sar_ku=surface_location_data.x_sat,
            y_pos_l1b_echo_sar_ku=surface_location_data.y_sat,
            z_pos_l1b_echo_sar_ku=surface_location_data.z_sat,
            x_vel_l1b_echo_sar_ku=surface_location_data.x_vel_sat,
            y_vel_l1b_echo_sar_ku=surface_location_data.y_vel_sat,
            z_vel_l1b_echo_sar_ku=surface_location_data.z_vel_sat,
            roll_sat_pointing_l1b_echo_sar_ku=surface_location_data.roll_sat,
            pitch_sat_pointing_l1b_echo_sar_ku=surface_location_data.pitch_sat,
            yaw_sat_pointing_l1b_echo_sar_ku=surface_location_data.yaw_sat,
            nav_bul_status_l1b_echo_sar_ku=closest_burst.nav_bul_status,
            nav_bul_source_l1b_echo_sar_ku=closest_burst.nav_bul_source,
            nav_bul_coarse_time_l1b_echo_sar_ku=None,
            nav_bul_fine_time_l1b_echo_sar_ku=None,
            seq_count_l1b_echo_sar_ku=closest_burst.source_seq_count,
            #  isp_time_status_l1b_echo_sar_ku=None,  # closest_burst.isp_time_status,
            oper_instr_l1b_echo_sar_ku=closest_burst.oper_instr,
            SAR_mode_l1b_echo_sar_ku=closest_burst.SAR_mode,
            cl_gain_l1b_echo_sar_ku=closest_burst.cl_gain,
            acq_stat_l1b_echo_sar_ku=closest_burst.acq_stat,
            dem_eeprom_l1b_echo_sar_ku=closest_burst.dem_eeprom,
            weighting_l1b_echo_sar_ku=None,  # surface_location_data.cnf.flag_azimuth_weighting,
            loss_track_l1b_echo_sar_ku=closest_burst.loss_track,
            h0_nav_dem_l1b_echo_sar_ku=closest_burst.h0_nav_dem,
            h0_applied_l1b_echo_sar_ku=closest_burst.h0_applied,
            cor2_nav_dem_l1b_echo_sar_ku=closest_burst.cor2_nav_dem,
            cor2_applied_l1b_echo_sar_ku=closest_burst.cor2_applied,
            dh0_l1b_echo_sar_ku=closest_burst.dh0,
            agccode_ku_l1b_echo_sar_ku=closest_burst.agccode_ku,
            surf_type_l1b_echo_sar_ku=closest_burst.surf_type,
            range_ku_l1b_echo_sar_ku=surface_location_data.win_delay_surf * self.cst.c / 2.,
            uso_cor_l1b_echo_sar_ku=closest_burst.uso_cor,
            int_path_cor_ku_l1b_echo_sar_ku=closest_burst.int_path_cor_ku,
            range_rate_l1b_echo_sar_ku=None,  # closest_burst.range_rate,
            agc_ku_l1b_echo_sar_ku=closest_burst.agc_ku,
            scale_factor_ku_l1b_echo_sar_ku=surface_location_data.sigma0_scaling_factor,
            agc_cor_ku_l1b_echo_sar_ku=closest_burst.agc_ku - closest_burst.agccode_ku,
            sig0_cal_ku_l1b_echo_sar_ku=closest_burst.sig0_cal_ku,
            nb_stack_l1b_echo_sar_ku=surface_location_data.n_beams_start_stop,
            max_stack_l1b_echo_sar_ku=surface_location_data.stack_max,
            stdev_stack_l1b_echo_sar_ku=surface_location_data.stack_std,
            skew_stack_l1b_echo_sar_ku=surface_location_data.stack_skewness,
            kurt_stack_l1b_echo_sar_ku=surface_location_data.stack_kurtosis,
            beam_ang_l1b_echo_sar_ku=surface_location_data.beam_angles_surf,
            look_ang_l1b_echo_sar_ku=surface_location_data.look_angles_surf,
            beam_form_l1b_echo_sar_ku=None,
            i2q2_meas_ku_l1b_echo_sar_ku=surface_location_data.waveform_multilooked/scale_factor,
            i2q2_scale_factor_l1b_echo_sar_ku=scale_factor,
            start_look_angle_stack_l1b_echo_sar_ku=surface_location_data.start_look_angle,
            stop_look_angle_stack_l1b_echo_sar_ku=surface_location_data.stop_look_angle,
            start_beam_ang_stack_l1b_echo_sar_ku=surface_location_data.start_beam_angle,
            stop_beam_ang_stack_l1b_echo_sar_ku=surface_location_data.stop_beam_angle,
            stack_mask_vector_l1b_echo_sar_ku=surface_location_data.stack_mask_vector_start_stop,
            stack_scale_factor_ku_l1b_echo_sar_ku=surface_location_data.sigma0_scaling_factor_beam
        )

class L1BWriter(NetCDFWriter):
    """
    class for writing L1B netCDF files
    """
    def __init__(self, chd: CharacterisationFile, cnf: ConfigurationFile, cst: ConstantsFile, filename: str):
        """
        Initialize the L1BWriter Instance
        :param filename: the path of the output file to write
        """
        super().__init__(filename)
        self.chd = chd
        self.cnf = cnf
        self.cst = cst

        # create dimension definitions
        self.define_dimension(
            L1BDimensions.time_l1b_echo_sar_ku, None
        )
        self.define_dimension(
            L1BDimensions.echo_sample_ind, chd.n_samples_sar * cnf.zp_fact_range
        )
        self.define_dimension(
            L1BDimensions.max_multi_stack_ind, cnf.n_looks_stack
        )
        # create variable definitions
        self.define_variable(
            L1BVariables.time_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="UTC: l1b_echo_Sar_ku mode",
            calendar="gregorian",
            units="seconds since 2000-01-01 00:00:00.0"
        )
        self.define_variable(
            L1BVariables.UTC_day_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="day UTC: l1b_echo_sar_ku mode",
            units="days since 2000-01-01 00:00:00.0",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.UTC_sec_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="seconds in the day UTC: l1b_echo_sar_ku mode",
            units="seconds in the day",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.GPS_time_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="GPS time: l1b_echo_sar_ku mode",
            calendar="gregorian",
            units="seconds since 1980-01-06 00:00:00.0",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.isp_coarse_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP coarse time: l1b_echo_sar_ku mode",
            units="second",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.isp_fine_time_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP fine time: l1b_echo_sar_ku mode",
            units="2^-24 second",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.sral_fine_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP SRAL fine datation: l1b_echo_sar_ku mode",
            units="137.5*10^-9 second",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.lat_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="latitude: l1b_echo_sar_ku mode",
            standard_name="latitude",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="degrees_north",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.lon_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="longitude: l1b_echo_sar_ku mode",
            standard_name="longitude",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="degrees_east",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.alt_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altitude of satellite: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=700000.,
            units="m",
            fill_value=2147483647,
        )
        self.define_variable(
            L1BVariables.orb_alt_rate_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="orbital altitude rate: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="m/s",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.flag_time_status_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="time status flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="flag indicating if the time is synchronized or not with "
                    "GPS time",
            flag_meanings=(
                "synchronization",
                "no_synchronization"
            )
        )
        self.define_variable(
            L1BVariables.time_time_corr_val_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="time correlation validity flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01, 0x02),
            comment="flag indicating if the time correlation information is "
                    "valid provided by OBSE, valid provided by Ground Segment "
                    "or invalid",
            flag_meanings=(
                "valid_obsw",
                "valid_ground_segment",
                "invalid"
            )
        )
        self.define_variable(
            L1BVariables.flag_man_pres_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="manoeuvre presence flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "no_manoeuvre",
                "ongoing_manoeuvre"
            )
        )
        self.define_variable(
            L1BVariables.flag_man_thrust_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="manoeuvre thrust flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "no_thrust",
                "ongoing_thrust"
            )
        )
        self.define_variable(
            L1BVariables.flag_man_plane_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="manoeuvre plane flag: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "in_plane",
                "out_of_plane"
            )
        )
        self.define_variable(
            L1BVariables.flag_gnss_status_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="validty flag for the navigation message from the gnss receiver: l1b_echo_sar_ku mode",
            comment="indicating if the navigation message from the GNSS receiver is valid "
                    "or not valid/available",
            flag_values=(0x00, 0x01),
            flag_meanings=(
                "valid",
                "invalid_unavailable"
            )
        )
        self.define_variable(
            L1BVariables.x_pos_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite altitude - x component: l1b_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.y_pos_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite altitude - y component: l1b_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.z_pos_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite altitude - z component: l1b_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.x_vel_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite velocity - x component: l1b_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.y_vel_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite velocity - y component: l1b_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.z_vel_l1b_echo_sar_ku,
            np.float64,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="satellite velocity - z component: l1b_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BVariables.nav_bul_status_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin status: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("ok", "ko"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.nav_bul_source_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin source identifier: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("gps", "doris"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.nav_bul_coarse_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin coarse time: l1b_echo_sar_ku mode",
            units="second",
            comment="value the closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.nav_bul_fine_time_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="navigation bulletin fine time: l1b_echo_sar_ku mode",
            units="2^-24 second",
            comment="value the closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.seq_count_l1b_echo_sar_ku,
            np.uint16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="sequence count: l1b_echo_sar_ku mode",
            comment="value the closest in time to the reference measurement",
            fill_value=65535
        )
        self.define_variable(
            L1BVariables.isp_time_status_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="ISP time status: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("SRAL_OBT_extrapolated",
                           "SRAL_OBT_updated_wth_SMU_OBT"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.oper_instr_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="operating instrument: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="Instrument A stands for SRAL Nominal and instrument B stands for SRAL Redundant",
            flag_meanings=("A", "B"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.SAR_mode_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="SAR mode identifier: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01, 0x02),
            comment="the values closest in time to the reference measurement",
            flag_meanings=(
                "closed_loop",
                "open_loop",
                "open_loop_fixed_gain"
            ),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.cl_gain_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="tracking_configuration - closed loop gain: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="the value closest in time to the reference measurement",
            flag_meanings=(
                "Nominal_value",
                "Nominal_value_with_back-off"
            ),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.acq_stat_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="tracking configuration - acquisition status: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=(
                "no_aquisition",
                "acquisition"
            ),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.dem_eeprom_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="tracking configuration - DEM EEPROM read access: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("enabled", "disabled"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.weighting_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altimeter configuration - weighting function: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("enabled", "disabled"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.loss_track_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="loss of track criterion: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01),
            comment="value the closest in time to the reference measurement",
            flag_meanings=("normal", "loss_of_track"),
            fill_value=127
        )
        self.define_variable(
            L1BVariables.h0_nav_dem_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altitude command H0 computed with nav DEM: l1b_echo_sar_ku mode",
            units="3.125/64*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.h0_applied_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="applied altitude command H0: l1b_echo_sar_ku mode",
            units="3.125/64*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.cor2_nav_dem_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altitude command COR2 computed with nav DEM: l1b_echo_sar_ku mode",
            units="3.125/1024*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.cor2_applied_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="applied altitude command COR2: l1b_echo_sar_ku mode",
            units="3.125/1024*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.dh0_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            # TODO: confirm this long_name is correct - field is truncated in PDFS.
            long_name="distance error computed on the echo of the cycle (N-2)"
                      " in open loop mode (current cycle): l1b_echo_sar_ku mode",
            units="3.125/64*10^-9 s",
            comments="value closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.agccode_ku_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="AGCCODE for ku band: l1b_echo_sar_ku mode",
            units="dB",
            comments="value closest in time to the reference measurement",
            fill_value=127
        )
        self.define_variable(
            L1BVariables.surf_type_l1b_echo_sar_ku,
            np.int8,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="altimeter surface type: l1b_echo_sar_ku mode",
            flag_values=(0x00, 0x01, 0x02, 0x03),
            comments="value closest in time to the reference measurement",
            flag_meanings=(
                "open_ocean_or_semi-enclosed_seas",
                "enclosed_seas_or_lakes",
                "continental_ice",
                "land"
            )
        )
        self.define_variable(
            L1BVariables.range_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="corrected range for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=700000.0,
            units="m",
            comment="reference range corrected for USO frequency drift and internal path correction",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.uso_cor_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="USO frequency drift correction: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=0.00,
            units="m",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.int_path_cor_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="internal path correction for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-04,
            add_offset=0.00,
            units="m",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.range_rate_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="range rate: l1b_echo_sar_ku mode",
            scale_factor=1.0e-03,
            add_offset=0.00,
            units="m/s",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.agc_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="corrected AGC for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            comment="AGC corrected for instrumental errors - value the closest in time to the"
                    "reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.scale_factor_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="scaling factor for sigma0 evaluation for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            comment="scaling factor corrected for AGC instrumental errors and internal calibration",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.agc_cor_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="correction for instrument errors on AGC for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            comment="value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.sig0_cal_ku_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="internal calibration correction on Sigma0 for ku band: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="dB",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.nb_stack_l1b_echo_sar_ku,
            np.uint16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="number of waveforms summed in stack: l1b_echo_sar_ku mode",
            units="count",
            fill_value=65535
        )
        self.define_variable(
            L1BVariables.max_stack_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="maximum power of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="FFT power unit",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.stdev_stack_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="standard deviation of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="rad",
            fill_value=4294967295
        )
        self.define_variable(
            L1BVariables.skew_stack_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="skewness of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.kurt_stack_l1b_echo_sar_ku,
            np.int32,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="kurtosis of stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BVariables.beam_ang_l1b_echo_sar_ku,
            np.int16,
            (L1BDimensions.time_l1b_echo_sar_ku,
             L1BDimensions.max_multi_stack_ind),
            long_name="doppler beam angles in stack: l1b_echo_sar_ku mode",
            comment="the useful values of the table are the first n_useful values where n_useful is"
                    "the number of waveforms summed in the stack",
            scale_factor=1.0e-06,
            add_offset=0.00,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BVariables.beam_form_l1b_echo_sar_ku,
            np.uint16,
            (L1BDimensions.time_l1b_echo_sar_ku,),
            long_name="flag on beam formation quality in stack: l1b_echo_sar_ku mode",
            scale_factor=1.0e-02,
            add_offset=0.00,
            units="percent",
            fill_value=65535
        )
        self.define_variable(
            L1BVariables.i2q2_meas_ku_l1b_echo_sar_ku,
            np.uint32,
            (L1BDimensions.time_l1b_echo_sar_ku,
             L1BDimensions.echo_sample_ind),
            long_name="I2+Q2 measurement for ku band: l1b_echo_sar_ku mode",
            comment="the echo is corrected for Doppler range effect, phase/power burst calibration"
                    "and GPRW effect. The echo is scaled using the correlated AGC (agc_ku_l1b_echo_sar_ku)",
            scale_factor=1.0e-03,
            add_offset=0.00,
            units="count",
            fill_value=4294967295
        )

    def write_record(self, surface_location_data: SurfaceData) -> None:
        """
        output a record to the L1B file.
        """

        closest_burst = surface_location_data.closest_burst

        time_interval = surface_location_data.time_surf - surface_location_data.prev_tai
        utc_secs = surface_location_data.prev_utc_secs + time_interval

        if utc_secs > surface_location_data.curr_day_length:
            utc_secs -= surface_location_data.curr_day_length
            utc_days = surface_location_data.prev_utc_days + 1
        else:
            utc_days = surface_location_data.prev_utc_days

        scale_factor = pow(10, -closest_burst.agc_ku / 10)

        super().write_record(
            time_l1b_echo_sar_ku=surface_location_data.time_surf,
            UTC_day_l1b_echo_sar_ku=utc_days,
            UTC_sec_l1b_echo_sar_ku=utc_secs,
            GPS_time_l1b_echo_sar_ku=surface_location_data.gps_time_surf,
            isp_coarse_time_l1b_echo_sar_ku=closest_burst.isp_coarse_time,
            isp_fine_time_l1b_echo_sar_ku=closest_burst.isp_fine_time,
            sral_fine_time_l1b_echo_sar_ku=closest_burst.sral_fine_time,
            lat_l1b_echo_sar_ku=degrees(surface_location_data.lat_surf),
            lon_l1b_echo_sar_ku=degrees(surface_location_data.lon_surf),
            alt_l1b_echo_sar_ku=surface_location_data.alt_sat,
            orb_alt_rate_l1b_echo_sar_ku=surface_location_data.alt_rate_sat,
            flag_time_status_l1b_echo_sar_ku=closest_burst.flag_time_status,
            #  flag_time_corr_val_l1b_echo_sar_ku=None,  # closest_burst.flag_time_corr,
            flag_man_pres_l1b_echo_sar_ku=None,  # closest_burst.flag_man_pres,
            flag_man_thrust_l1b_echo_sar_ku=None,  # closest_burst.flag_man_thrust,
            flag_man_plane_l1b_echo_sar_ku=None,  # closest_burst.flag_man_plane,
            flag_gnss_status_l1b_echo_sar_ku=None,  # closest_burst.flag_gnss_status,
            x_pos_l1b_echo_sar_ku=surface_location_data.x_sat,
            y_pos_l1b_echo_sar_ku=surface_location_data.y_sat,
            z_pos_l1b_echo_sar_ku=surface_location_data.z_sat,
            x_vel_l1b_echo_sar_ku=surface_location_data.x_vel_sat,
            y_vel_l1b_echo_sar_ku=surface_location_data.y_vel_sat,
            z_vel_l1b_echo_sar_ku=surface_location_data.z_vel_sat,
            nav_bul_status_l1b_echo_sar_ku=closest_burst.nav_bul_status,
            nav_bul_source_l1b_echo_sar_ku=closest_burst.nav_bul_source,
            nav_bul_coarse_time_l1b_echo_sar_ku=None,
            nav_bul_fine_time_l1b_echo_sar_ku=None,
            seq_count_l1b_echo_sar_ku=closest_burst.source_seq_count,
            #  isp_time_status_l1b_echo_sar_ku=None,  # closest_burst.isp_time_status,
            oper_instr_l1b_echo_sar_ku=closest_burst.oper_instr,
            SAR_mode_l1b_echo_sar_ku=closest_burst.SAR_mode,
            cl_gain_l1b_echo_sar_ku=closest_burst.cl_gain,
            acq_stat_l1b_echo_sar_ku=closest_burst.acq_stat,
            dem_eeprom_l1b_echo_sar_ku=closest_burst.dem_eeprom,
            weighting_l1b_echo_sar_ku=None,  # surface_location_data.cnf.flag_azimuth_weighting,
            loss_track_l1b_echo_sar_ku=closest_burst.loss_track,
            h0_nav_dem_l1b_echo_sar_ku=closest_burst.h0_nav_dem,
            h0_applied_l1b_echo_sar_ku=closest_burst.h0_applied,
            cor2_nav_dem_l1b_echo_sar_ku=closest_burst.cor2_nav_dem,
            cor2_applied_l1b_echo_sar_ku=closest_burst.cor2_applied,
            dh0_l1b_echo_sar_ku=closest_burst.dh0,
            agccode_ku_l1b_echo_sar_ku=closest_burst.agccode_ku,
            surf_type_l1b_echo_sar_ku=closest_burst.surf_type,
            range_ku_l1b_echo_sar_ku=surface_location_data.win_delay_surf * self.cst.c / 2.,
            uso_cor_l1b_echo_sar_ku=closest_burst.uso_cor,
            int_path_cor_ku_l1b_echo_sar_ku=closest_burst.int_path_cor_ku,
            range_rate_l1b_echo_sar_ku=None,  # closest_burst.range_rate,
            agc_ku_l1b_echo_sar_ku=closest_burst.agc_ku,
            scale_factor_ku_l1b_echo_sar_ku=surface_location_data.sigma0_scaling_factor,
            agc_cor_ku_l1b_echo_sar_ku=closest_burst.agc_ku - closest_burst.agccode_ku,
            sig0_cal_ku_l1b_echo_sar_ku=closest_burst.sig0_cal_ku,
            nb_stack_l1b_echo_sar_ku=surface_location_data.data_stack_size,
            max_stack_l1b_echo_sar_ku=surface_location_data.stack_max,
            stdev_stack_l1b_echo_sar_ku=surface_location_data.stack_std,
            skew_stack_l1b_echo_sar_ku=surface_location_data.stack_skewness,
            kurt_stack_l1b_echo_sar_ku=surface_location_data.stack_kurtosis,
            beam_ang_l1b_echo_sar_ku=-surface_location_data.look_angles_surf,
            beam_form_l1b_echo_sar_ku=None,
            i2q2_meas_ku_l1b_echo_sar_ku=surface_location_data.waveform_multilooked #*scale_factor
        )