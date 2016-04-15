from ...consts import chd, cst
from ..packet import InstrumentSourcePacket
from ....proc.geo.lla2ecef import lla2ecef

from math import atan
import numpy as np

class CryosatPacket(InstrumentSourcePacket):
    def __init__(self, index, measurement, time_orbit, waveforms, corrections, cst):
        super().__init__(index, cst)

        #  set time-orbit data
        self.days = time_orbit.days * cst.sec_in_day
        self.seconds = time_orbit.seconds
        self.microseconds = time_orbit.microseconds * 1e-6

        if time_orbit.mode.mode == 3:
            self.process_id = 57 if time_orbit.mode.cal4 else 58

        self.seq_count_sar_ku_fbr = time_orbit.source_seq_count_sar_ku_fbr

        self.inst_id_sar_isp = 0
        self.pri_sar = chd.pri_sar
        self.ambiguity_order_sar = 0

        self.burst_sar_ku = time_orbit.burst_sar_ku
        self.burst_sar_ku_fbr = time_orbit.burst_sar_ku % chd.N_bursts_cycle_sar

        if self.burst_sar_ku_fbr == 0:
            self.burst_sar_ku_fbr = 1

        self.lat_sar_sat = time_orbit.lat_sar_sat * 1e-7
        self.lon_sar_sat = time_orbit.lon_sar_sat * 1e-7
        self.alt_sar_sat = time_orbit.alt_sar_sat * 1e-3
        self.alt_rate_sar_sat = time_orbit.alt_rate_sar_sat * 1e-3

        self.x_vel_sat_sar = time_orbit.x_vel_sat_sar * 1e-3
        self.y_vel_sat_sar = time_orbit.y_vel_sat_sar * 1e-3
        self.z_vel_sat_sar = time_orbit.z_vel_sat_sar * 1e-3

        self.roll_sar = atan(time_orbit.interferometer_baseline[0]/time_orbit.interferometer_baseline[2])
        self.pitch_sar = atan(-time_orbit.real_beam_direction[1]/time_orbit.real_beam_direction[0])
        self.yaw_sar = atan(time_orbit.interferometer_baseline[1]/time_orbit.interferometer_baseline[2])

        self.mea_conf_data_sar_ku_fbr = time_orbit.confidence_data
        self.confi_block_degraded = time_orbit.confidence_data.confi_block_degraded

        #  set measurements data
        self.win_delay_sar_ku = measurement.win_delay_sar_ku * 1e-12
        self.h0_comp_sar = measurement.h0_comp_sar_isp
        self.cor2_comp_sar = measurement.cor2_comp_sar_isp
        self.h0_sar = measurement.h0_sar_isp
        self.cor2_sar = measurement.cor2_sar_isp

        self.att1_science = measurement.att1_science / 100.
        self.att2_science = measurement.att2_science / 100.
        self.att_sar_ku = 62 - self.att1_science

        self.tot_fixed_gain_1 = measurement.tot_fixed_gain_1
        self.tot_fixed_gain_2 = measurement.tot_fixed_gain_2
        self.transmit_power = measurement.transmit_power

        self.doppler_range_correction = measurement.doppler_range_correction
        self.instrument_range_correction_tx_rx = measurement.instrument_range_correction_tx_rx
        self.instrument_range_correction = measurement.instrument_range_correction
        self.instrument_sigma_correction_tx_rx = measurement.instrument_sigma_correction_tx_rx
        self.instrument_sigma_correction_rx = measurement.instrument_sigma_correction_rx
        self.internal_phase_correction = measurement.internal_range_correction
        self.external_phase_correction = measurement.external_range_correction
        self.noise_power = measurement.noise_power
        self.phase_slope_correction = measurement.phase_slope_correction

        #  set corrections data
        self.dry_tropo_correction = corrections.dry_tropo_correction
        self.wet_tropo_correction = corrections.wet_tropo_correction
        self.inverse_baro_correction = corrections.inverse_baro_correction
        self.dynamic_atmospheric_correction = corrections.dynamic_atmospheric_correction
        self.gim_iono_correction = corrections.gim_iono_correction
        self.ocean_equilibrium_tide = corrections.ocean_equilibrium_tide
        self.long_period_tide_height = corrections.long_period_tide_height
        self.ocean_loading_tide = corrections.ocean_loading_tide
        self.solid_earth_tide = corrections.solid_earth_tide
        self.geocentric_polar_tide = corrections.geocentric_polar_tide
        self.surface_type_flag = corrections.surface_type_flag
        self.correction_status_flags = corrections.correction_status_flags
        self.correction_error_flags = corrections.correction_error_flags

        #  set waveforms data
        wfm_iq_sar_ku_fbr_i_1 = waveforms.wfm_iq_sar_ku_fbr_aux_1[0::2]
        wfm_iq_sar_ku_fbr_q_1 = waveforms.wfm_iq_sar_ku_fbr_aux_1[1::2]
        wfm_iq_sar_ku_fbr_i_2 = waveforms.wfm_iq_sar_ku_fbr_aux_2[0::2]
        wfm_iq_sar_ku_fbr_q_2 = waveforms.wfm_iq_sar_ku_fbr_aux_2[1::2]

        self.wfm_iq_sar_ku_fbr_i_11 = np.zeros(chd.N_ku_pulses_burst, chd.N_samples_sar)
        self.wfm_iq_sar_ku_fbr_q_11 = np.zeros(chd.N_ku_pulses_burst, chd.N_samples_sar)
        self.wfm_iq_sar_ku_fbr_i_22 = np.zeros(chd.N_ku_pulses_burst, chd.N_samples_sar)
        self.wfm_iq_sar_ku_fbr_q_22 = np.zeros(chd.N_ku_pulses_burst, chd.N_samples_sar)

        for i_pulse in range(chd.N_ku_pulses_burst):
            index = slice(i_pulse * chd.N_samples_sar, (i_pulse + 1) * chd.N_samples_sar)
            self.wfm_iq_sar_ku_fbr_i_11[i_pulse, :] = wfm_iq_sar_ku_fbr_i_1[index]
            self.wfm_iq_sar_ku_fbr_q_11[i_pulse, :] = wfm_iq_sar_ku_fbr_q_1[index]
            self.wfm_iq_sar_ku_fbr_i_22[i_pulse, :] = wfm_iq_sar_ku_fbr_i_2[index]
            self.wfm_iq_sar_ku_fbr_q_22[i_pulse, :] = wfm_iq_sar_ku_fbr_q_2[index]
        self.nimp_sar = waveforms.nimp_sar_isp

        #  finalise
        self.win_delay_sar_ku = self.win_delay_sar_ku + self.instrument_range_correction_tx_rx / (cst.c / 2)
        self.wfm_cal_gain_corrected = self.wfm_iq_sar_ku_fbr_i_11 + 1j * self.wfm_iq_sar_ku_fbr_q_11
        self.wfm_cal_gain_corrected_2 = self.wfm_iq_sar_ku_fbr_i_22 + 1j * self.wfm_iq_sar_ku_fbr_q_22

        self.N_total_bursts_sar_ku = len(self.lat_sar_sat)
        self.time_sar_ku = self.days + self.seconds + self.microseconds

        p = lla2ecef(
            np.vstack([self.lat_sar_sat, self.lon_sar_sat, self.alt_sar_sat]),
            cst.flat_coeff, cst.semi_major_axis)
        self.x_sar_sat = p[:, 0].T
        self.y_sar_sat = p[:, 1].T
        self.z_sar_sat = p[:, 2].T
