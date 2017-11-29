==================
L1B-S Output Files
==================

File Description
----------------

In addition to the L1B file, the dedop processor can also optionally write an L1B-S output file. This
file contains much of the same information as the L1B file, but is extended to include stack-level (per 
beam) data. The processor will produce an L1B-S file by default, but due to the large size of the file
you may wish to dissable this. To prevent the processor from creating an L1B-S file, add the ``--skip-l1bs``
argument to the ``dedop run`` command.

Dimensions
----------

- time_l1bs_echo_sar_ku
    - description: Number of L1Bs ECHO_SAR_Ku measurements
- echo_sample_ind
    - description: Number of samples in a waveform
- max_multi_stack_ind
    - description: Maximum number of multilook beams per stack

Variables
---------

- time_l1bs_echo_sar_ku
    - description: UTC Seconds since 2000-01-01 00:00:00.0
- UTC_day_l1bs_echo_sar_ku
    - description: UTC Days since 2000-01-01 00:00:00.0
- UTC_sec_l1bs_echo_sar_ku 
    - description: Seconds since the start of the current UTC day
- lat_l1bs_echo_sar_ku
    - description: Surface location (degrees North)
- lon_l1bs_echo_sar_ku
    - description: Surface location (degrees East)
- surf_type_l1bs_echo_sar_ku
    - description: Altimeter surface type (open ocean or semi-enclosed seas/enclosed seas/enclosed seas or lakes/continental ice/land)
- records_count_l1bs_echo_sar_ku
    - description: Record index
- alt_l1bs_echo_sar_ku
    - description: Altitude of surface (m)
- orb_alt_rate_l1bs_echo_sar_ku
    - description: Orbital altitude rate (m/s)
- x_pos_l1bs_echo_sar_ku
    - description: Satellite ECEF x-coordinate
- y_pos_l1bs_echo_sar_ku
    - description: Satellite ECEF y-coordinate
- z_pos_l1bs_echo_sar_ku
    - description: Satellite ECEF z-coordinate
- x_vel_l1bs_echo_sar_ku
    - description: Satellite ECEF x-velocity
- y_vel_l1bs_echo_sar_ku
    - description: Satellite ECEF y-velocity
- z_vel_l1bs_echo_sar_ku
    - description: Satellite ECEF z-velocity
- meas_x_pos_l1bs_echo_sar_ku
    - description: Surface location - ECEF x-coordinate
- meas_y_pos_l1bs_echo_sar_ku
    - description: Surface location - ECEF y-coordinate
- meas_z_pos_l1bs_echo_sar_ku
    - description: Surface location - ECEF z-coordinate
- roll_sat_pointing_l1bs_echo_sar_ku
    - description: Satellite pointing angle - roll (degrees)
- pitch_sat_pointing_l1bs_echo_sar_ku
    - description: Satellite pointing angle - pitch (degrees)
- yaw_sat_pointing_l1bs_echo_sar_ku
    - description: Satellite pointing angle - yaw (degrees)
- roll_sral_mispointing_l1bs_echo_sar_ku
    - description: SRAL mispointing angle - roll (degrees)
- pitch_sral_mispointing_l1bs_echo_sar_ku
    - description: SRAL mispointing angle - pitch (degrees)
- yaw_sral_mispointing_l1bs_echo_sar_ku
    - description: SRAL mispointing angle - yaw (degrees)
- range_ku_l1bs_echo_sar_ku
    - description: Corrected range for ku band (m)
- int_path_cor_ku_l1bs_echo_sar_ku
    - description: Internal path correction for ku band
- uso_cor_l1bs_echo_sar_ku
    - description: USO frequency drift correction
- cog_cor_l1bs_echo_sar_ku
    - description: Distance antenna-CoG correction
- agccode_ku_l1bs_echo_sar_ku
    - description: AGCCODE for ku band
- agc_ku_l1bs_echo_sar_ku
    - description: corrected AGC for ku band
- scale_factor_ku_l1bs_echo_sar_ku
    - description: scaling factor for sigma0 evaluation for ku band
- sig0_cal_ku_l1bs_echo_sar_ku
    - description: internal calibration correction on Sigma0 for ku band
- snr_ku_l1bs_echo_sar_ku
    - description: snr estimation for ku band
- i2q2_meas_ku_l1bs_echo_sar_ku
    - description: multilooked I2+Q2 measurement for ku band
- nb_stack_l1bs_echo_sar_ku
    - description: number of waveforms summed in stack
- max_stack_l1bs_echo_sar_ku
    - description: maximum power of stack
- max_loc_stack_l1bs_echo_sar_ku
    - description: Location of the maximum power of stack
- stdev_stack_l1bs_echo_sar_ku
    - description: standard deviation of stack
- skew_stack_l1bs_echo_sar_ku
    - description: skewness of stack
- kurt_stack_l1bs_echo_sar_ku
    - description: kurtosis of stack
- beam_ang_l1bs_echo_sar_ku
    - description: look angles in stack
- beam_form_l1bs_echo_sar_ku
    - description: flag on beam formation quality in stack
- burst_start_ind_l1bs_echo_sar_ku
    - description: Burst start index for stack building
- burst_stop_ind_l1bs_echo_sar_ku
    - description: Burst stop index for stack building
- iq_scale_factor_l1bs_echo_sar_ku
    - description: Dynamic scale factor for I/Q waveforms i_echoes_ku_l1bs_echo_sar_ku and q_echoes_ku_l1bs_echo_sar_ku
- i_echoes_ku_l1bs_echo_sar_ku
    - description: Fully calibrated ku band echoes, i measurements aligned within the stack
- q_echoes_ku_l1bs_echo_sar_ku
    - description: fully calibrated ku band echoes, q measurements aligned within the stack
- start_look_angle_stack_l1bs_echo_sar_ku
    - description: start look angle in stack
- stop_look_angle_stack_l1bs_echo_sar_ku
    - description: stop look angle in stack
- start_beam_ang_stack_l1bs_echo_sar_ku
    - description: start doppler beam angle in stack
- stop_beam_ang_stack_l1bs_echo_sar_ku
    - description: stop doppler beam angle in stack
- power_var_stack_l1bs_echo_sar_ku
    - description: power variations within the stack