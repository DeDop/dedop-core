import numpy as np
from numpy.linalg import norm
from math import cos, sqrt
from enum import Enum

from ..base_algorithm import BaseAlgorithm

class AzimuthProessingMethods(Enum):
    dynamic = 0
    approximate = 1
    exact = 2

class AzimuthWeighting(Enum):
    enabled = 1
    disabled = 0

class AzimuthProcessingAlgorithm(BaseAlgorithm):

    def __call__(self, isps, method=AzimuthProessingMethods.dynamic, weighting=AzimuthWeighting.disabled):
        """
        Executes the azimuth processing algorithm

        :param isps: The list of InstrumentSourcePacket instances
        :param method: The method to use
        :param weighting: Azimuth weighting flag
        """
        wavelength_ku = self.chd.wv_length_ku

        if weighting == AzimuthWeighting.enabled:
            # TODO: perform azimuth weighting
            pass

        # azimuth processing with surface dependant method
        if method == AzimuthProessingMethods.dynamic:
            # TODO: change method based on surface
            self.computeApproximateMethod(isps, wavelength_ku)

        # azimuth processing with approx. method
        elif method == AzimuthProessingMethods.approximate:
            self.computeApproximateMethod(isps, wavelength_ku)
        # azimuth processing with exact method
        elif method == AzimuthProessingMethods.exact:
            self.computeExactMethod(isps, wavelength_ku)

    def computeApproximateMethod(self, isp, wavelength_ku):
        """
        Azimuth processing approximate method

        :param isps: InstrumentSourcePacket instances
        :param wavelength_ku: signal wavelength
        """

        # create empty fft waveforms
        waveform_fft_azimuth = np.zeros(
            (self.chd.n_samples_sar, self.chd.n_ku_pulses_burst), dtype=complex
        )
        waveform_phase_shift = np.zeros(
            (self.chd.n_samples_sar, self.chd.n_ku_pulses_burst), dtype=complex
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
        """
        Azimuth processing approx. method

        :param isp: InstrumentSourcePacket
        :param wavelength_ku: signal wavelength
        :return:
        """
        # create empty fft waveforms
        waveform_fft_azimuth = np.zeros(
            (self.chd.n_samples_sar, self.chd.n_ku_pulses_burst), dtype=complex
        )
        waveform_phase_shift = np.zeros(
            (self.chd.n_samples_sar, self.chd.n_ku_pulses_burst), dtype=complex
        )

        for beam_index, beam_angle_value in enumerate(isp.beam_angles_list):
            self.computePhaseShift(
                isp, beam_angle_value, wavelength_ku, waveform_phase_shift
            )

            self.computeFftAzimuthDimension(
                waveform_phase_shift, waveform_fft_azimuth
            )
            self.beams_focused[beam_index, :] =\
                waveform_fft_azimuth[self.chd.n_ku_pulses_burst // 2, :]


    def computePhaseShift(self, isp, nadir_beam_angle, wavelength_ku, waveform_phase_shift):
        """
        :param isp:
        :param nadir_beam_angle:
        :param wavelength_ku:
        :param waveform_phase_shift:
        :return:
        """
        for pulse_index in range(self.chd.n_ku_pulses_burst):
            beam_angle_phase = np.exp(-2j * \
                                      2. * self.cst.pi * wavelength_ku * \
                                      norm(isp.vel_sat_sar) * \
                                      cos(nadir_beam_angle) * \
                                      isp.pri_sar_pre_dat * pulse_index
                                      )
            waveform_phase_shift[pulse_index, :] =\
                beam_angle_phase * isp.waveform_cor_sar[pulse_index, :]

    def computeFftAzimuthDimension(self, waveform_phase_shift, waveform_fft_azimuth):
        """
        :param waveform_phase_shift:
        :param waveform_fft_azimuth:
        :return:
        """
        for sample_index in range(self.chd.n_samples_sar):
            out_fft = np.fft.fft(
                waveform_phase_shift[:, sample_index]
            )

            for pulse_index in range(self.chd.n_ku_pulses_burst):
                pulse_index_shifted =\
                    pulse_index + (self.chd.n_ku_pulses_burst // 2) % self.chd.n_ku_pulses_burst
                waveform_fft_azimuth[pulse_index, sample_index] =\
                    sqrt(self.chd.n_ku_pulses_burst) * out_fft[pulse_index_shifted]

    def getNadirBeamAngle(self, isp):
        """
        :param isp:
        :return:
        """
        beam_angles_list_size = len(isp.beam_angles_list)
        nadir_beam_index = 0

        if isp.beam_angles_trend == 1:
            nadir_beam_index = beam_angles_list_size - self.chd.n_ku_pulses_burst // 2

        elif isp.beam_angles_trend == -1:
            if beam_angles_list_size <= (self.chd.n_ku_pulses_burst // 2):
                nadir_beam_index = beam_angles_list_size - 1
            else:
                nadir_beam_index = self.chd.n_ku_pulses_burst // 2

        elif isp.beam_angles_trend == 0:
            nadir_beam_index = self.chd.n_ku_pulses_burst // 2

        nadir_beam_angle = isp.beam_angles_list[nadir_beam_index]
        return nadir_beam_angle