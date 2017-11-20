from enum import Enum

import numpy as np
from math import degrees

from dedop.model import SurfaceData
from .netcdf_writer import NetCDFWriter
from dedop.conf import CharacterisationFile, ConfigurationFile, ConstantsFile


class L1BSDimensions(Enum):
    time_l1bs_echo_sar_ku = 'time_l1bs_echo_sar_ku'
    echo_sample_ind = 'echo_sample_ind'
    max_multi_stack_ind = 'max_multi_stack_ind'


class L1BSVariables(Enum):
    time_l1bs_echo_sar_ku = 'time_l1bs_echo_sar_ku'
    UTC_day_l1bs_echo_sar_ku = 'UTC_day_l1bs_echo_sar_ku'
    UTC_sec_l1bs_echo_sar_ku = 'UTC_sec_l1bs_echo_sar_ku'
    lat_l1bs_echo_sar_ku = 'lat_l1bs_echo_sar_ku'
    lon_l1bs_echo_sar_ku = 'lon_l1bs_echo_sar_ku'
    surf_type_l1bs_echo_sar_ku = 'surf_type_l1bs_echo_sar_ku'
    records_count_l1bs_echo_sar_ku = 'records_count_l1bs_echo_sar_ku'
    alt_l1bs_echo_sar_ku = 'alt_l1bs_echo_sar_ku'
    orb_alt_rate_l1bs_echo_sar_ku = 'orb_alt_rate_l1bs_echo_sar_ku'
    x_pos_l1bs_echo_sar_ku = 'x_pos_l1bs_echo_sar_ku'
    y_pos_l1bs_echo_sar_ku = 'y_pos_l1bs_echo_sar_ku'
    z_pos_l1bs_echo_sar_ku = 'z_pos_l1bs_echo_sar_ku'
    x_vel_l1bs_echo_sar_ku = 'x_vel_l1bs_echo_sar_ku'
    y_vel_l1bs_echo_sar_ku = 'y_vel_l1bs_echo_sar_ku'
    z_vel_l1bs_echo_sar_ku = 'z_vel_l1bs_echo_sar_ku'
    meas_x_pos_l1bs_echo_sar_ku = 'meas_x_pos_l1bs_echo_sar_ku'
    meas_y_pos_l1bs_echo_sar_ku = 'meas_y_pos_l1bs_echo_sar_ku'
    meas_z_pos_l1bs_echo_sar_ku = 'meas_z_pos_l1bs_echo_sar_ku'
    roll_sat_pointing_l1bs_echo_sar_ku = 'roll_sat_pointing_l1bs_echo_sar_ku'
    pitch_sat_pointing_l1bs_echo_sar_ku = 'pitch_sat_pointing_l1bs_echo_sar_ku'
    yaw_sat_pointing_l1bs_echo_sar_ku = 'yaw_sat_pointing_l1bs_echo_sar_ku'
    roll_sral_mispointing_l1bs_echo_sar_ku = 'roll_sral_mispointing_l1bs_echo_sar_ku'
    pitch_sral_mispointing_l1bs_echo_sar_ku = 'pitch_sral_mispointing_l1bs_echo_sar_ku'
    yaw_sral_mispointing_l1bs_echo_sar_ku = 'yaw_sral_mispointing_l1bs_echo_sar_ku'
    range_ku_l1bs_echo_sar_ku = 'range_ku_l1bs_echo_sar_ku'
    int_path_cor_ku_l1bs_echo_sar_ku = 'int_path_cor_ku_l1bs_echo_sar_ku'
    uso_cor_l1bs_echo_sar_ku = 'uso_cor_l1bs_echo_sar_ku'
    cog_cor_l1bs_echo_sar_ku = 'cog_cor_l1bs_echo_sar_ku'
    agccode_ku_l1bs_echo_sar_ku = 'agccode_ku_l1bs_echo_sar_ku'
    agc_ku_l1bs_echo_sar_ku = 'agc_ku_l1bs_echo_sar_ku'
    scale_factor_ku_l1bs_echo_sar_ku = 'scale_factor_ku_l1bs_echo_sar_ku'
    sig0_cal_ku_l1bs_echo_sar_ku = 'sig0_cal_ku_l1bs_echo_sar_ku'
    snr_ku_l1bs_echo_sar_ku = 'snr_ku_l1bs_echo_sar_ku'
    i2q2_meas_ku_l1bs_echo_sar_ku = 'i2q2_meas_ku_l1bs_echo_sar_ku'
    nb_stack_l1bs_echo_sar_ku = 'nb_stack_l1bs_echo_sar_ku'
    max_stack_l1bs_echo_sar_ku = 'max_stack_l1bs_echo_sar_ku'
    max_loc_stack_l1bs_echo_sar_ku = 'max_loc_stack_l1bs_echo_sar_ku'
    stdev_stack_l1bs_echo_sar_ku = 'stdev_stack_l1bs_echo_sar_ku'
    skew_stack_l1bs_echo_sar_ku = 'skew_stack_l1bs_echo_sar_ku'
    kurt_stack_l1bs_echo_sar_ku = 'kurt_stack_l1bs_echo_sar_ku'
    beam_ang_l1bs_echo_sar_ku = 'beam_ang_l1bs_echo_sar_ku'
    beam_form_l1bs_echo_sar_ku = 'beam_form_l1bs_echo_sar_ku'
    burst_start_ind_l1bs_echo_sar_ku = 'burst_start_ind_l1bs_echo_sar_ku'
    burst_stop_ind_l1bs_echo_sar_ku = 'burst_stop_ind_l1bs_echo_sar_ku'
    iq_scale_factor_l1bs_echo_sar_ku = 'iq_scale_factor_l1bs_echo_sar_ku'
    i_echoes_ku_l1bs_echo_sar_ku = 'i_echoes_ku_l1bs_echo_sar_ku'
    q_echoes_ku_l1bs_echo_sar_ku = 'q_echoes_ku_l1bs_echo_sar_ku'
    start_look_angle_stack_l1bs_echo_sar_ku = 'start_look_angle_stack_l1bs_echo_sar_ku'
    stop_look_angle_stack_l1bs_echo_sar_ku = 'stop_look_angle_stack_l1bs_echo_sar_ku'
    start_beam_ang_stack_l1bs_echo_sar_ku = 'start_beam_ang_stack_l1bs_echo_sar_ku'
    stop_beam_ang_stack_l1bs_echo_sar_ku = 'stop_beam_ang_stack_l1bs_echo_sar_ku'
    power_var_stack_l1bs_echo_sar_ku = 'power_var_stack_l1bs_echo_sar_ku'


class L1BSWriter(NetCDFWriter):
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
            L1BSDimensions.time_l1bs_echo_sar_ku, None
        )
        self.define_dimension(
            L1BSDimensions.echo_sample_ind, chd.n_samples_sar * cnf.zp_fact_range
        )
        self.define_dimension(
            L1BSDimensions.max_multi_stack_ind, cnf.n_looks_stack
        )
        # create variable definitions
        self.define_variable(
            L1BSVariables.time_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="UTC: l1bs_echo_Sar_ku mode",
            calendar="gregorian",
            units="seconds since 2000-01-01 00:00:00.0"
        )
        self.define_variable(
            L1BSVariables.UTC_day_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="day UTC: l1bs_echo_sar_ku mode",
            units="days since 2000-01-01 00:00:00.0",
            fill_value=32767
        )
        self.define_variable(
            L1BSVariables.UTC_sec_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="seconds in the day UTC: l1bs_echo_sar_ku mode",
            units="seconds in the day",
            fill_value=1.84467440737096e19
        )
        # lat/lon
        self.define_variable(
            L1BSVariables.lat_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="latitude: l1bs_echo_sar_ku mode",
            units="degrees_north",
            scale_factor=1e-6,
            add_offset=0,
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.lon_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="longitude: l1bs_echo_sar_ku mode",
            units="degrees_east",
            scale_factor=1e-6,
            add_offset=0,
            fill_value=2147483647
        )
        # surf type
        self.define_variable(
            L1BSVariables.surf_type_l1bs_echo_sar_ku,
            np.int8,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="altimeter surface type: l1bs_echo_sar_ku mode",
            flag_values=(0x00, 0x01, 0x02, 0x03),
            flag_meanings=(
                "open_ocean_or_semi-enclosed_seas",
                "enclosed_seas_or_lakes",
                "continental_ice",
                "land"
            ),
            fill_value=127,
            comment="value closest in time to the reference measurement"
        )

        self.define_variable(
            L1BSVariables.records_count_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="l1b record counters within the product: l1bs_echo_sar_ku mode",
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.alt_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="altitude of satellite: l1bs_echo_sar_ku mode",
            units="m",
            scale_factor=1e-4,
            add_offset=700000,
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.orb_alt_rate_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="orbital altitude rate: l1bs_echo_sar_ku mode",
            scale_factor=1e-2,
            add_offset=0,
            units='m/s',
            fill_value=32767
        )
        self.define_variable(
            L1BSVariables.x_pos_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite altitude - x component: l1bs_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.y_pos_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite altitude - y component: l1bs_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.z_pos_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite altitude - z component: l1bs_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.x_vel_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite velocity - x component: l1bs_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.y_vel_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite velocity - y component: l1bs_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.z_vel_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite velocity - z component: l1bs_echo_sar_ku mode",
            units="m/s",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.meas_x_pos_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="measurement altitude - x component: l1bs_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.meas_y_pos_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="measurement altitude - y component: l1bs_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.meas_z_pos_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="measurement altitude - z component: l1bs_echo_sar_ku mode",
            units="m",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.roll_sat_pointing_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite pointing angle - roll: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BSVariables.pitch_sat_pointing_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite pointing angle - pitch: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BSVariables.yaw_sat_pointing_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="satellite pointing angle - yaw: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BSVariables.roll_sral_mispointing_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="SRAL mispointing angle - roll: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BSVariables.pitch_sral_mispointing_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="SRAL mispointing angle - pitch: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BSVariables.yaw_sral_mispointing_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="SRAL mispointing angle - yaw: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="degrees",
            fill_value=32767,
            comment="value for the closest in time from the burst time tag, given " \
                    "in the nadir pointing reference frame."
        )
        self.define_variable(
            L1BSVariables.range_ku_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="corrected range for ku band: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=700000,
            units="m",
            comment="Distance between the altimeter reference point and the surface height " \
                    "associated to a range gate used as a reference inside the tracking window " \
                    "(reference tracking point), corrected for USO frequency drift and internal" \
                    "path correction",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.int_path_cor_ku_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="internal path correction for ku band: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="m",
            comment="Value the closest in time from the burst time lag",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.uso_cor_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="USO frequency drift correction: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="m",
            fill_value=2147483647,
            comment="value the closest in time from the burst time tag"
        )
        self.define_variable(
            L1BSVariables.cog_cor_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="distance antenna-CoG correction: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="m",
            comment="Distance in the z-component between the centre of mass of the satellite " \
                    "and the altimeter antenna reference point",
            fill_value=32767
        )
        self.define_variable(
            L1BSVariables.agccode_ku_l1bs_echo_sar_ku,
            np.int8,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="AGCCODE for ku band: l1bs_echo_sar_ku mode",
            units="dB",
            fill_value=127
        )
        self.define_variable(
            L1BSVariables.agc_ku_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="corrected AGC for ku band: l1bs_echo_sar_ku mode",
            scale_factor=1e-2,
            add_offset=0,
            units="dB",
            comment="AGC corrected for instrumental errors - value the closest in time to the reference measurement",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.scale_factor_ku_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="scaling factor for sigma0 evaluation for ku band: l1bs_echo_sar_ku mode",
            scale_factor=1e-2,
            add_offset=0,
            units="dB",
            comment="scaling factor corrected for AGC instrumental errors and internal calibration",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.sig0_cal_ku_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="internal calibration correction on Sigma0 for ku band: l1bs_echo_sar_ku mode",
            scale_factor=1e-2,
            add_offset=0,
            units="dB",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.snr_ku_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="snr estimation for ku band: l1bs_echo_sar_ku mode",
            scale_factor=1e-2,
            add_offset=0,
            units="dB",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.i2q2_meas_ku_l1bs_echo_sar_ku,
            np.uint32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,
             L1BSDimensions.echo_sample_ind),
            long_name="I2+Q2 measurement for ku band: l1bs_echo_sar_ku mode",
            comment="the echo is corrected for Doppler range effect, phase/power burst calibration " \
                    "and GPRW effect. The echo is scaled using the correctied AGC (agc_ku_l1b_echo_sar_ku)",
            scale_factor=1e-3,
            add_offset=0,
            units="count",
            fill_value=4294967295
        )
        self.define_variable(
            L1BSVariables.nb_stack_l1bs_echo_sar_ku,
            np.uint16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="number of waveforms summed in stack: l1bs_echo_sar_ku mode",
            units="count",
            fill_value=65535
        )
        self.define_variable(
            L1BSVariables.max_stack_l1bs_echo_sar_ku,
            np.uint32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="maximum power of stack: l1bs_echo_sar_ku mode",
            scale_factor=1e-4,
            add_offset=0,
            units="FFT power unit",
            fill_value=4294967295
        )
        self.define_variable(
            L1BSVariables.max_loc_stack_l1bs_echo_sar_ku,
            np.uint16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="location of the maximum power of stack: l1bs_echo_sar_ku mode",
            units="count",
            fill_value=65535
        )
        self.define_variable(
            L1BSVariables.stdev_stack_l1bs_echo_sar_ku,
            np.uint32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="standard deviation of stack: l1bs_echo_sar_ku mode",
            scale_factor=1e-6,
            add_offset=0,
            units="rad",
            fill_value=4294967295
        )
        self.define_variable(
            L1BSVariables.skew_stack_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="skewness of stack: l1bs_echo_sar_ku mode",
            scale_factor=1e-6,
            add_offset=0,
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.kurt_stack_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="kurtosis of stack: l1bs_echo_sar_ku mode",
            scale_factor=1e-6,
            add_offset=0,
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.beam_ang_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,
             L1BSDimensions.max_multi_stack_ind),
            long_name="doppler beam angles in stack: l1bs_echo_sar_ku mode",
            comment="the useful values of the table are the first nb_stack_l1bs_echo_sar_ku values",
            scale_factor=1e-6,
            add_offset=1.57,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BSVariables.beam_form_l1bs_echo_sar_ku,
            np.uint8,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="flag on beam formation quality in stack: l1bs_echo_sar_ku mode",
            scale_factor=1e-2,
            add_offset=0,
            units="percent",
            fill_value=65535
        )
        self.define_variable(
            L1BSVariables.burst_start_ind_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="burst start index for stack building: l1bs_echo_sar_ku mode",
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.burst_stop_ind_l1bs_echo_sar_ku,
            np.int32,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="burst stop index for stack building: l1bs_echo_sar_ku mode",
            units="count",
            fill_value=2147483647
        )
        self.define_variable(
            L1BSVariables.iq_scale_factor_l1bs_echo_sar_ku,
            np.float64,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="dynamic scale factor for I/Q waveforms i_echoes_ku_l1bs_echo_sar_ku and"
                      "q_echos_ku_l1bs_echo_sar_ku",
            comment="dynamic scale factor for I/Q waveforms i_echoes_ku_l1bs_echo_sar_ku and"
                    "q_echos_ku_l1bs_echo_sar_ku",
            fill_value=18446744073709551616
        )
        self.define_variable(
            L1BSVariables.i_echoes_ku_l1bs_echo_sar_ku,
            np.int8,
            (L1BSDimensions.time_l1bs_echo_sar_ku,
             L1BSDimensions.max_multi_stack_ind,
             L1BSDimensions.echo_sample_ind),
            long_name="fully calibrated ky band echoes, i measurements aligned"\
                      " within the stack: l1bs_echo_sar_ku mode",
            units="count",
            fill_value=-128,
            comment="Fully calibrate ku band echoes, I values (300*128 samples) in the frequency domain, " \
                    "and aligned within the stack. The useful echoes of the table are the first " \
                    "nb_stack_l1bs_echo_sar_ku echos."
        )
        self.define_variable(
            L1BSVariables.q_echoes_ku_l1bs_echo_sar_ku,
            np.int8,
            (L1BSDimensions.time_l1bs_echo_sar_ku,
             L1BSDimensions.max_multi_stack_ind,
             L1BSDimensions.echo_sample_ind),
            long_name="fully calibrated ky band echoes, q measurements aligned" \
                      " within the stack: l1bs_echo_sar_ku mode",
            units="count",
            fill_value=-128,
            comment="Fully calibrate ku band echoes, Q values (300*128 samples) in the frequency domain, " \
                    "and aligned within the stack. The useful echoes of the table are the first " \
                    "nb_stack_l1bs_echo_sar_ku echos."
        )
        self.define_variable(
            L1BSVariables.start_look_angle_stack_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="start look angle in stack: l1bs_echo_sar_ku mode",
            scale_factor=1e-6,
            add_offset=1.57,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BSVariables.stop_look_angle_stack_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="stop look angle in stack: l1bs_echo_sar_ku mode",
            scale_factor=1e-6,
            add_offset=1.57,
            units="rad",
            fill_value=32767
        )
        self.define_variable(
            L1BSVariables.power_var_stack_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,
             L1BSDimensions.max_multi_stack_ind),
            long_name="power variations within the stack: l1bs_echo_sar_ku mode",
            comment="The useful values of the table are the first nb_stack_l1bs_echo_sar_ku values, " \
                    "one value of power for each individual echo",
            units="FFT power unit",
            fill_value=32767
        )
        self.define_variable(
            L1BSVariables.start_beam_ang_stack_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="start doppler beam angle in stack: l1bs_echo_sar_ku mode",
            units="rad",
            fill_value=32767,
            scale_factor=1e-6,
            add_offset=1.57
        )
        self.define_variable(
            L1BSVariables.stop_beam_ang_stack_l1bs_echo_sar_ku,
            np.int16,
            (L1BSDimensions.time_l1bs_echo_sar_ku,),
            long_name="stop doppler beam angle in stack: l1bs_echo_sar_ku mode",
            units="rad",
            fill_value=32767,
            scale_factor=1e-6,
            add_offset=1.57
        )

    def write_record(self, surface_location_data: SurfaceData) -> None:
        """
        output a record the L1B-S file.
        """

        closest_burst = surface_location_data.closest_burst
        stack_end = surface_location_data.data_stack_size-1
        time_interval = surface_location_data.time_surf - surface_location_data.prev_tai
        utc_secs = surface_location_data.prev_utc_secs + time_interval

        if utc_secs > surface_location_data.curr_day_length:
            utc_secs -= surface_location_data.curr_day_length
            utc_days = surface_location_data.prev_utc_days + 1
        else:
            utc_days = surface_location_data.prev_utc_days

        scale_factor = pow(10, -closest_burst.agc_ku / 10)

        stack_i = np.real(surface_location_data.beams_range_compr_iq)
        stack_q = np.imag(surface_location_data.beams_range_compr_iq)
        max_iq = max(np.max(np.abs(stack_i)), np.max(np.abs(stack_q)))

        dynamic_scale = max_iq / 127.

        super().write_record(
            time_l1bs_echo_sar_ku=surface_location_data.time_surf,
            UTC_day_l1bs_echo_sar_ku=utc_days,
            UTC_sec_l1bs_echo_sar_ku=utc_secs,
            lat_l1bs_echo_sar_ku=degrees(surface_location_data.lat_surf),
            lon_l1bs_echo_sar_ku=degrees(surface_location_data.lon_surf),
            surf_type_l1bs_echo_sar_ku=surface_location_data.surface_type.value,
            records_count_l1bs_echo_sar_ku=surface_location_data.surface_counter,
            alt_l1bs_echo_sar_ku=surface_location_data.alt_sat,
            orb_alt_rate_l1bs_echo_sar_ku=surface_location_data.alt_rate_sat,
            x_pos_l1bs_echo_sar_ku=surface_location_data.x_sat,
            y_pos_l1bs_echo_sar_ku=surface_location_data.y_sat,
            z_pos_l1bs_echo_sar_ku=surface_location_data.z_sat,
            x_vel_l1bs_echo_sar_ku=surface_location_data.x_vel_sat,
            y_vel_l1bs_echo_sar_ku=surface_location_data.y_vel_sat,
            z_vel_l1bs_echo_sar_ku=surface_location_data.z_vel_sat,
            meas_x_pos_l1bs_echo_sar_ku=surface_location_data.x_surf,
            meas_y_pos_l1bs_echo_sar_ku=surface_location_data.y_surf,
            meas_z_pos_l1bs_echo_sar_ku=surface_location_data.z_surf,
            roll_sat_pointing_l1bs_echo_sar_ku=surface_location_data.roll_sat,
            pitch_sat_pointing_l1bs_echo_sar_ku=surface_location_data.pitch_sat,
            yaw_sat_pointing_l1bs_echo_sar_ku=surface_location_data.yaw_sat,
            roll_sral_mispointing_l1bs_echo_sar_ku=closest_burst.roll_sral_mispointing,
            pitch_sral_mispointing_l1bs_echo_sar_ku=closest_burst.pitch_sral_mispointing,
            yaw_sral_mispointing_l1bs_echo_sar_ku=closest_burst.yaw_sral_mispointing,
            range_ku_l1bs_echo_sar_ku=surface_location_data.win_delay_surf * self.cst.c / 2.,
            int_path_cor_ku_l1bs_echo_sar_ku=closest_burst.int_path_cor_ku,
            uso_cor_l1bs_echo_sar_ku=closest_burst.uso_cor,
            cog_cor_l1bs_echo_sar_ku=closest_burst.cog_cor,
            agccode_ku_l1bs_echo_sar_ku=closest_burst.agccode_ku,
            agc_ku_l1bs_echo_sar_ku=closest_burst.agc_ku,
            scale_factor_ku_l1bs_echo_sar_ku=surface_location_data.sigma0_scaling_factor,
            sig0_cal_ku_l1bs_echo_sar_ku=closest_burst.sig0_cal_ku,
            snr_ku_l1bs_echo_sar_ku=None,
            i2q2_meas_ku_l1bs_echo_sar_ku=surface_location_data.waveform_multilooked*scale_factor,
            nb_stack_l1bs_echo_sar_ku=surface_location_data.data_stack_size,
            max_stack_l1bs_echo_sar_ku=surface_location_data.stack_max,
            max_loc_stack_l1bs_echo_sar_ku=None,
            stdev_stack_l1bs_echo_sar_ku=surface_location_data.stack_std,
            skew_stack_l1bs_echo_sar_ku=surface_location_data.stack_skewness,
            kurt_stack_l1bs_echo_sar_ku=surface_location_data.stack_kurtosis,
            beam_ang_l1bs_echo_sar_ku=surface_location_data.beam_angles_surf,
            beam_form_l1bs_echo_sar_ku=None,
            burst_start_ind_l1bs_echo_sar_ku=surface_location_data.stack_bursts[0].source_seq_count,
            burst_stop_ind_l1bs_echo_sar_ku=surface_location_data.stack_bursts[stack_end].source_seq_count,
            iq_scale_factor_l1bs_echo_sar_ku=dynamic_scale,
            i_echoes_ku_l1bs_echo_sar_ku=stack_i/dynamic_scale,
            q_echoes_ku_l1bs_echo_sar_ku=stack_q/dynamic_scale,
            start_look_angle_stack_l1bs_echo_sar_ku=surface_location_data.look_angles_surf[0],
            stop_look_angle_stack_l1bs_echo_sar_ku=surface_location_data.look_angles_surf[stack_end],
            start_beam_ang_stack_l1bs_echo_sar_ku=surface_location_data.beam_angles_surf[0],
            stop_beam_ang_stack_l1bs_echo_sar_ku=surface_location_data.beam_angles_surf[stack_end]
        )
