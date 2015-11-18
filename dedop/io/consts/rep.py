# ########################################################
# --------------------------------------------------------
# Created by isardSAT S.L. 
# --------------------------------------------------------
# JasonCS 
# This code implements the algorithm as described in the
# isardSAT_JasonCS_DPM_JC-DS-ISR-SY-0006_v5a_20130605
#
# ---------------------------------------------------------
# Objective: Define Repositori Parameters
# 
# INPUTs : - 
# OUTPUTs: -
#
# ----------------------------------------------------------
#
# ########################################################
from .chd import N_ku_pulses_burst, N_samples_sar
import numpy as np

power_var_cal1_sar_ku = 0
burst_phase_array_cor_cal1_sar = np.zeros((1,N_ku_pulses_burst))
wfm_cal2_science_sar = np.ones((1,N_samples_sar))
