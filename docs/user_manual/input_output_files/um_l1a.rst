===============
L1A Input Files
===============

File Description
----------------

The Dedop processor reads Level 1A Sentinel-3 format data files. These files are in the netCDF4 (.nc)
format, and must have the correct dimensions and variables as described in this page. If the format
of the input file being processed does not match the format described here, Dedop may be unable to
read the file.

Input files can be added to a workspace via the command ``dedop input add``, or passed directly to the
processor at run-time by using the ``-i`` parameter of the ``dedop run`` command.

Dimensions
----------

- echo_sample_ind
    - description: the number of samples per echo
- sar_ku_pulse_burst_ind
    - description: the number of Ku-band pulses in a SAR burst
- sar_c_pulse_burst_ind
    - description: the number of C-band pulses in a SAR burst
- ltm_max_ind
    - description: Maximum number of LTM Cal1 or Cal2 tables
- time_l1a_echo_sar_ku
    - description: the along-track time of SAR bursts
- time_l1a_echo_plrm
    - description: the along-track time of PLRM bursts


Variables
---------

- echo_sample_ind
    - description: the echo sample index
- sar_ku_pulse_burst_ind
    - description: the SAR Ku-band burst index
- sar_c_pulse_burst_ind
    - description: the SAR C-band burst index
- ltm_max_ind
    - description: Maximum number of LTM Cal1 or Cal2 tables
- time_l1a_echo_sar_ku
    - description: the time of the SAR Ku-band burst
- UTC_day_l1a_echo_sar_ku
    - description: the UTC day number of the burst
- UTC_sec_l1a_echo_sar_ku
    - description: the number of seconds of the current UTC day of the burst
- UTC_time_20hz_l1a_echo_sar_ku
    - description: UTC of the 20 Hz measurement
- isp_coarse_time_l1a_echo_sar_ku
    - description: ISP coarse time
- isp_fine_time_l1a_echo_sar_ku
    - description: ISP fine time
- flag_time_status_l1a_echo_sar_ku
    - description: time status flag
- sral_fine_time_l1a_echo_sar_ku
    - description: ISP SRAL fine datation
- lat_l1a_echo_sar_ku
    - description: the latitude (degrees north) for the current burst
- lon_l1a_echo_sar_ku
    - description: the longitude (degrees east) for the corrent burst
- surf_type_l1a_echo_sar_ku
    - description: the surface type flag
- burst_count_prod_l1a_echo_sar_ku
    - description: bursts counter within the product
- seq_count_l1a_echo_sar_ku
    - description: the source sequence counter index
- burst_count_cycle_l1a_echo_sar_ku
    - description: bursts counter within the tracking cycle
- nav_bul_status_l1a_echo_sar_ku
    - description: navigation bulletin status
- nav_bul_source_l1a_echo_sar_ku
    - description: navigation bulletin source identifier
- oper_instr_l1a_echo_sar_ku
    - description: the instrument flag
- SAR_mode_l1a_echo_sar_ku
    - description: SAR mode identifier
- cl_gain_l1a_echo_sar_ku
    - description: tracking configuration - closed loop gain
- acq_stat_l1a_echo_sar_ku
    - description: tracking configuration - acquisition status
- dem_eeprom_l1a_echo_sar_ku
    - description: tracking configuration - DEM EEPROM read access
- weighting_l1a_echo_sar_ku
    - description: altimeter configuration - weighting function
- loss_track_l1a_echo_sar_ku
    - description: loss of track criterion
- h0_nav_dem_l1a_echo_sar_ku
    - description: altitude command H0 computed with nav DEM
- h0_applied_l1a_echo_sar_ku
    - description: applied altitude command H0
- cor2_nav_dem_l1a_echo_sar_ku
    - description: altitude command COR2 computed with nav DEM
- cor2_applied_l1a_echo_sar_ku
    - description: applied altitude command COR2
- dh0_l1a_echo_sar_ku
    - description: distance error computed on the echo of the cycle (N-2) in open loop mode
- agccode_ku_l1a_echo_sar_ku
    - description: AGCCODE for ku band
- agccode_c_l1a_echo_sar_ku
    - description: AGCCODE for c band
- alt_l1a_echo_sar_ku
    - description: the altitude of the current burst
- orb_alt_rate_l1a_echo_sar_ku
    - description: the altitude rate of the current burst
- x_pos_l1a_echo_sar_ku
    - description: the ECEF x-coordinate of the current burst
- y_pos_l1a_echo_sar_ku
    - description: the ECEF y-coordinate of the current burst
- z_pos_l1a_echo_sar_ku
    - description: the ECEF z-coordinate of the current burst
- x_vel_l1a_echo_sar_ku
    - description: the ECEF x-velocity of the current burst
- y_vel_l1a_echo_sar_ku
    - description: the ECEF y-velocity of the current burst
- z_vel_l1a_echo_sar_ku
    - description: the ECEF z-velocity of the current burst
- roll_sat_pointing_l1a_echo_sar_ku
    - description: the roll (degrees) of the satellite at the current burst
- pitch_sat_pointing_l1a_echo_sar_ku
    - description: the pitch (degrees) of the satellite at the current burst
- yaw_sat_pointing_l1a_echo_sar_ku
    - description: the yaw (degrees) of the satellite at the current burst
- roll_sral_mispointing_l1a_echo_sar_ku
    - description: SRAL mispointing angle - roll
- pitch_sral_mispointing_l1a_echo_sar_ku
    - description: SRAL mispointing angle - pitch
- yaw_sral_mispointing_l1a_echo_sar_ku
    - description: SRAL mispointing angle - yaw
- range_ku_l1a_echo_sar_ku
    - description: the receiving window range
- int_path_cor_ku_l1a_echo_sar_ku
    - description: the internal path correction
- uso_cor_l1a_echo_sar_ku
    - description: the USO correction
- cog_cor_l1a_echo_sar_ku
    - description: the Centre-of-Gravity correction
- agc_ku_l1a_echo_sar_ku
    - description: the AGC correction
- scale_factor_ku_l1a_echo_sar_ku
    - description: the sigma-0 scaling factor
- sig0_cal_ku_l1a_echo_sar_ku
    - description: internal calibration correction on Sigma0 for ku band
- i_meas_ku_l1a_echo_sar_ku
    - description: the i-component of the measured waveform
- q_meas_ku_l1a_echo_sar_ku
    - description: the q-component of the measured waveform
- gprw_meas_ku_l1a_echo_sar_ku
    - description: ku band samples of the normalized GPRW (cal2)
- cal2_ku_ind_l1a_echo_sar_ku
    - description: the CAL2 index
- burst_power_cor_ku_l1a_echo_sar_ku
    - description: the power of the burst
- burst_phase_cor_ku_l1a_echo_sar_ku
    - description: the phase of the burst
- cal1_ku_ind_l1a_echo_sar_ku
    - description: the CAL1 index