import numpy as np
from numpy.linalg import norm
from math import cos, sqrt

from ....conf import cst, chd
from ..base_algorithm import BaseAlgorithm

APPROXIMATE_METHOD = 'approx'
EXACT_METHOD = 'exact'

class AzimuthProcessingAlgorithm(BaseAlgorithm):

    def __call__(self, isps, method=EXACT_METHOD):
        """
        :param isps:
        :param wavelength_ku:
        :param method:
        :return:
        """
        wavelength_ku = chd.wv_length_ku

        # azimuth processing with approx. method
        if method == APPROXIMATE_METHOD:
            self.computeApproximateMethod(isps, wavelength_ku)
        # azimuth processing with exact method
        elif method == EXACT_METHOD:
            self.computeExactMethod(isps, wavelength_ku)
        # throw an error if the method isn't valid
        else:
            raise ValueError("Method '{}' is not valid - must be '{}' or '{}'".format(
                method, APPROXIMATE_METHOD, EXACT_METHOD
            ))

    def computeApproximateMethod(self, isp, wavelength_ku):
        """
        :param isps:
        :param wavelength_ku:
        :return:
        """

        # create empty fft waveforms
        waveform_fft_azimuth = np.zeros(
            (chd.N_samples_sar, chd.N_ku_pulses_burst), dtype=complex
        )
        waveform_phase_shift = np.zeros(
            (chd.N_samples_sar, chd.N_ku_pulses_burst), dtype=complex
        )

        # the azimuth processing is done only once, using the beam
        # angle phase of the beam pointing to the nadir (considered
        # the central beam)
        nadir_beam_angle = self.getNadirBeamAngle(isp)

        # use the nadir beam angle to compute the phase shift
        self.computePhaseShift(
            isp, nadir_beam_angle, wavelength_ku, waveform_phase_shift
        )
        # compute the azimuth FFTs
        self.computeFftAzimuthDimension(
            waveform_phase_shift, waveform_fft_azimuth
        )

        # the result is the focused beams. If the list of beam angles
        # is increasing in size, then the useful first beams are in the
        # output of the waveform_fft_azimuth (because the first part of the
        # waveform_fft_azimuth beams point to surfaces that are before the
        # first surface). This way we will always have the beams in the same
        # position as the corresponding beam angle in the beam angle/surfaces
        # seen lists.
        if isp.beam_angles_trend == 1:
            beams_offset = 64 - len(isp.beam_angles_list)
        else:
            beams_offset = 0
        self.beams_focused = waveform_fft_azimuth[beams_offset:]

    def computeExactMethod(self, isp, wavelength_ku):
        # create empty fft waveforms
        waveform_fft_azimuth = np.zeros(
            (chd.N_samples_sar, chd.N_ku_pulses_burst), dtype=complex
        )
        waveform_phase_shift = np.zeros(
            (chd.N_samples_sar, chd.N_ku_pulses_burst), dtype=complex
        )

        for beam_index, beam_angle_value in enumerate(isp.beam_angles_list):
            self.computePhaseShift(
                isp, beam_angle_value, wavelength_ku, waveform_phase_shift
            )

            self.computeFftAzimuthDimension(
                waveform_phase_shift, waveform_fft_azimuth
            )
            self.beams_focused[beam_index, :] =\
                waveform_fft_azimuth[chd.N_ku_pulses_burst // 2, :]


    def computePhaseShift(self, isp, nadir_beam_angle, wavelength_ku, waveform_phase_shift):
        """
        :param isp:
        :param nadir_beam_angle:
        :param wavelength_ku:
        :param waveform_phase_shift:
        :return:
        """
        for pulse_index in range(chd.N_ku_pulses_burst):
            beam_angle_phase = np.exp(-2j *\
                2. * cst.pi * wavelength_ku *\
                norm(isp.vel_sat_sar) *\
                cos(nadir_beam_angle) *\
                isp.pri_sar * pulse_index
            )
            waveform_phase_shift[pulse_index, :] =\
                beam_angle_phase * isp.waveform_cor_sar[pulse_index, :]

    def computeFftAzimuthDimension(self, waveform_phase_shift, waveform_fft_azimuth):
        """
        :param waveform_phase_shift:
        :param waveform_fft_azimuth:
        :return:
        """
        for sample_index in range(chd.N_samples_sar):
            out_fft = np.fft.fft(
                waveform_phase_shift[:, sample_index]
            )

            for pulse_index in range(chd.N_ku_pulses_burst):
                pulse_index_shifted =\
                    pulse_index + (chd.N_ku_pulses_burst // 2) % chd.N_ku_pulses_burst
                waveform_fft_azimuth[pulse_index, sample_index] =\
                    sqrt(chd.N_ku_pulses_burst) * out_fft[pulse_index_shifted]

    def getNadirBeamAngle(self, isp):
        """
        :param isp:
        :return:
        """
        beam_angles_list_size = len(isp.beam_angles_list)
        nadir_beam_index = 0

        if isp.beam_angles_trend == 1:
            nadir_beam_index = beam_angles_list_size - chd.N_ku_pulses_burst // 2

        elif isp.beam_angles_trend == -1:
            if beam_angles_list_size <= (chd.N_ku_pulses_burst // 2):
                nadir_beam_index = beam_angles_list_size - 1
            else:
                nadir_beam_index = chd.N_ku_pulses_burst // 2

        elif isp.beam_angles_trend == 0:
            nadir_beam_index = chd.N_ku_pulses_burst // 2

        nadir_beam_angle = isp.beam_angles_list[nadir_beam_index]
        return nadir_beam_angle