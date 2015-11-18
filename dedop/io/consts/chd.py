# ########################################################
# --------------------------------------------------------
# Created by isardSAT S.L. 
# --------------------------------------------------------
# JasonCS 
# This code implements the algorithm as described in the
# isardSAT_JasonCS_DPM_JC-DS-ISR-SY-0006_v5a_20130605
#
# ---------------------------------------------------------
# Objective: Define characterization parameters
# 
# INPUTs : - 
# OUTPUTs: -
#
# ----------------------------------------------------------
#
# ########################################################
from .cst import *
from math import pi

## Other (not in the DPM)

alt_clock_period_sar_ku = 1/395e6 # 1/f0
wv_length_ku = 0.022084

## Main
freq_ku             = c / wv_length_ku
bw_ku               = 320 * 1e6
# freq_c              = c_cst / wv_length_c
# bw_c                = 'TBC' * 1e6

## Time patern
N_samples_sar       = 256    # SAR Samples
N_samples_rmc       = 128    # SAR RMC Samples
N_ku_pulses_burst   = 64   # SAR Ku pulses in burst
N_c_pulses_burst    = 1     # SAR C pulses in burst
N_pulses_burst          = N_ku_pulses_burst + N_c_pulses_burst
N_bursts_cycle_sar  = 7 # Bursts in a cycle
N_pri_sar_c_ku      = 0

pulse_length        = 32 * 1e-6
tx1_sar             = 0

chirp_slope_ku      = bw_ku/pulse_length


## Platform

x_ant               = 0
y_ant               = 0
z_ant               = 0
x_cog               = 0
y_cog               = 0
z_cog               = 0

x_cog_ant = x_ant - x_cog
y_cog_ant = y_ant - y_cog
z_cog_ant = z_ant - z_cog

## Antenna
#Errors of pointing from Rob presentation on requirements meeting 28/01/2015

roll_random_error       = 0.0496/180*pi #radians.
pitch_random_error      = 0.0499/180*pi #radians.
yaw_random_error        = 0.0494/180*pi #radians.
roll_bias_error         = 0.0828/180*pi #radians.
pitch_bias_error        = 0.0722/180*pi #radians.
yaw_bias_error          = 0.0068/180*pi #radians.
roll_harmonic_error     = 0.0441/180*pi #radians.
pitch_harmonic_error    = 0.0534/180*pi #radians.
yaw_harmonic_error      = 0.0250/180*pi #radians.

antenna_gain_ku             = 42.1
antenna_beamwidth_ku        = 1.35 #Degrees

## Window Delay

#SCENARIO1
ext_delay_ground = - 1000e-12
int_delay_ground = - 7000e-12
# SCENARIO3
# ext_delay_ground = 0
# int_delay_ground = 0

## AGC and waveforms scaling factor computation
agc_telem_to_meas_table_cal1 = 0
rfu_rx_gain_ground = 130
onboard_proc_sar = 66.2266
onboard_proc_rmc = -42.1
ins_losses_ground = 0
power_tx_ant_ku = 7.5

## USO CLock
uso_freq_nom = 10e6
alt_freq_multiplier = 39.5
T0_nom = 1/(uso_freq_nom * alt_freq_multiplier)

pri_T0_unit_conv = 8
h0_cor2_unit_conv = 16
T0_h0_unit_conv = 64
cai_cor2_unit_conv = 4096

i_sample_start = 1

## Weightings
azimuth_weighting_filename = []

pri_sar = 1.











