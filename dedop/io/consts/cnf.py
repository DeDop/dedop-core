# ########################################################
# --------------------------------------------------------
# Created by isardSAT S.L. 
# --------------------------------------------------------
# JasonCS 
# This code implements the algorithm as described in the
# isardSAT_JasonCS_DPM_JC-DS-ISR-SY-0006_v5a_20130605
#
# ---------------------------------------------------------
# Objective: Define Configuration parameters
# 
# INPUTs : - 
# OUTPUTs: -
#
# ----------------------------------------------------------
#
# ########################################################

## Processing and testing

processing_algorithms_flag  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# Tag 0. Deactivate Doppler Range Correction: no(0)/yes(1)
# Tag 1. Deactivate Slant Range Correction:no(0)/yes(1)
# Tag 2. Deactivate Pre-phase on Azimuth Processing: no(0)/yes(1)
# Tag 3. Deactivate Post-phase on Azimuth Processing: no(0)/yes(1)
# Tag 4. Force Exact Method on Azimuth Processing: no(0)/yes(1)
# Tag 5. Deactivate CAL1 Corrections:no(0)/yes(1)
# Tag 6. Deactivate USO Corrections:yes(0)/no(1)
# Tag 7. Deactivate CAL2 Corrections:no(0)/yes(1)
# Tag 8. Deactivate CAL1 chain:no(0)/yes(1)
# Tag 9. Deactivate CAL2 chain:no(0)/yes(1)
# Tag 10. Deactivate Multi-looking threshold: no(0)/yes(1)
# Tag 11. Deactivate antenna weigthing: no(0)/yes(1) 
# Tag 12. Deactivate surface weighting: no(0)/yes(1)
flag_alignment = 1 # On board altitude rate alignment activated(1) This should be included in the Tag 13.

testing_brk_flag = [0, 0, 1, 1, 1]
# Tag 0: LRM Breakpoint no(0)/yes(1)
# Tag 1: CAL1 Breakpoint no(0)/yes(1)
# Tag 2: SAR L1A Breakpoint no(0)/yes(1)
# Tag 3: SAR Ku waveforms Breakpoint no(0)/yes(1)
# Tag 4: SAR Ku stack Breakpoint no(0)/yes(1)

## SAR Ku
clock_unit_conv = 256
cor2_bit_shift = 4

sigma_alt_surf_th = 1000 #AZIMUTH PROCESSING (HIGH OR LOW VARIABILITY)
zp_fact_range = 2
N_surf_samp_interpol = 20
N_points_spline_surf = 10
smooth_fact_surf_pos = 0
# N_points_spline_orbit = 10
N_points_spline_orbit = N_points_spline_surf
smooth_fact_orbit_pos = 0
smooth_fact_orbit_vel = 0
accu_orbit_alt = 0
accu_orbit_lat = 0.0001
N_beams_sub_stack = 5

#SURFACE LOCATIONS (HIGH OR LOW ROUGHNESS)
sigma_alt_surf_geoloc_th = 100 * N_surf_samp_interpol
range_index1 = 12
range_index2 = 16
k_noise_top = 7
k_noise_floor = 0
trp_flag = 0 #chooses wether to execute the TRP special processing
trp_flag_method = 1 #chooses which method is used for this TRP special processing
                     #1: nearest surface location is replaced with the TRP position
                     #2: surface locations to be replaced are forced

#Force azimuth processing exact method no(0)/yes(1)
force_exact_method = 0

# Add a random error in the pointing
random_pointing_error       = [0,0,0]
                                #[0,0,0] no error added
                                #[1,0,0] added in the roll
                                #[0,1,0] added in the pitch
                                #[0,0,1] added in the yaw
                                #[1,1,0] added in the roll & pitch
                                #[0,1,1] added in the pitch & yaw
                                #[1,0,1] added in the roll & yaw
                                #[1,1,1] added in the roll & pitch & yaw
                                
bias_pointing_error         = [0,0,0]
                                #[0,0,0] no error added
                                #[1,0,0] added in the roll
                                #[0,1,0] added in the pitch
                                #[0,0,1] added in the yaw
                                #[1,1,0] added in the roll & pitch
                                #[0,1,1] added in the pitch & yaw
                                #[1,0,1] added in the roll & yaw
                                #[1,1,1] added in the roll & pitch & yaw
                                
harmonic_pointing_error     = [0,0,0]
                                #[0,0,0] no error added
                                #[1,0,0] added in the roll
                                #[0,1,0] added in the pitch
                                #[0,0,1] added in the yaw
                                #[1,1,0] added in the roll & pitch
                                #[0,1,1] added in the pitch & yaw
                                #[1,0,1] added in the roll & yaw
                                #[1,1,1] added in the roll & pitch & yaw
                                
                                
#For Multilooking consider zeros in averaging no(0)/yes(1)
use_zeros = 0
delete_ambiguities=1
