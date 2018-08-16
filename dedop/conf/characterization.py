from .auxiliary_file_reader import *
from .constants import ConstantsFile

from typing import Any
from math import radians


class CharacterisationFile(AuxiliaryFileReader):
    """
    class for loading the Characterisation File
    """
    _id = "CHD"
    _fileversion = 1

    mean_sat_alt = AuxiliaryParameter(
        "mean_sat_alt_chd",
        """mean altitude of the satellite""",
        param_type=float)

    n_samples_sar = AuxiliaryParameter(
        "N_samples_sar_chd",
        """number of samples per each SAR pulse""",
        param_type=int)
    n_ku_pulses_burst = AuxiliaryParameter(
        "N_ku_pulses_burst_chd",
        """number of ku-band pulses per burst""",
        param_type=int)

    freq_ku = AuxiliaryParameter(
        "freq_ku_chd",
        """emitted frequency in Ku-band""",
        param_type=float)
    pulse_length = AuxiliaryParameter(
        "pulse_length_chd",
        """pulse length""",
        param_type=float)
    bw_ku = AuxiliaryParameter(
        "bw_ku_chd",
        """Ku-band bandwidth""",
        param_type=float)

    power_tx_ant_ku = AuxiliaryParameter(
        "power_tx_ant_ku_chd",
        """antenna SSPA RF peak transmitted power in Ku band""",
        param_type=float)
    antenna_gain_ku = AuxiliaryParameter(
        "antenna_gain_ku_chd",
        """antenna gain for ku-band""",
        param_type=float)

    uso_freq_nom = AuxiliaryParameter(
        "uso_freq_nom_chd",
        """USO frequency nominal value""",
        param_type=float)
    alt_freq_multiplier = AuxiliaryParameter(
        "alt_freq_multiplier_chd",
        param_type=float)

    prf_sar = AuxiliaryParameter(
        "prf_sar_chd",
        """pulse repetition frequency""",
        param_type=float)
    brf_sar = AuxiliaryParameter(
        "brf_sar_chd",
        """burst repetition frequency""",
        param_type=float)

    antenna_weights = AuxiliaryParameterArray(
        "antenna_weights_chd",
        """array of antenna weights""",
        param_type=np.float64, shape=(250,)
    )
    antenna_angles = AuxiliaryParameterArray(
        "antenna_angles_chd",
        """array of antenna angles""",
        param_type=np.float64, shape=(250,)
    )
    antenna_angles_spacing = AuxiliaryParameter(
        "antenna_angles_spacing_chd",
        """spacing between antenna angles""",
        param_type=float)

    # look angle mask params
    look_angle_mask_min = AuxiliaryParameter(
        "look_angle_mask_min_chd",
        cast_type=radians,
        optional=True
    )
    look_angle_mask_max = AuxiliaryParameter(
        "look_angle_mask_max_chd",
        cast_type=radians,
        optional=True
    )

    ptr_width = AuxiliaryParameter(
        "ptr_width_chd",
        param_type=float
    )
    fft_step_freq_ku = AuxiliaryParameter(
        "fft_step_freq_ku_chd",
        param_type=float
    )
    ratio_trc_ku = AuxiliaryParameter(
        "ratio_trc_ku_chd",
        param_type=float
    )

    @property
    def pri_sar(self):
        return 1. / self.prf_sar

    @property
    def bri_sar(self):
        return 1. / self.brf_sar

    @property
    def chirp_slope_ku(self) -> float:
        """the chirp slope for the Ku-band (derived parameter)"""
        if self._chirp_slope_ku is None:
            self._chirp_slope_ku = self.bw_ku / self.pulse_length
        return self._chirp_slope_ku

    @property
    def wv_length_ku(self) -> float:
        """the Ku-band wavelength (derived parameter)"""
        if self._wv_length_ku is None:
            self._wv_length_ku = self.cst.c / self.freq_ku
        return self._wv_length_ku

    @property
    def t0_nom(self):
        return 1. / (self.uso_freq_nom * self.alt_freq_multiplier)

    def __init__(self, cst: ConstantsFile, filename: str=None, **kwargs: Any):
        """
        create a new CharacterisationFile object
        """
        self._wv_length_ku = kwargs.pop(
            'wv_length_ku_chd', None
        )
        self._chirp_slope_ku = kwargs.pop(
            'chirp_slope_ku_chd', None
        )

        self.cst = cst
        super().__init__(filename, **kwargs)
