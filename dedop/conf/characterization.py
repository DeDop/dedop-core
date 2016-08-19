from .auxiliary_file_reader import *
from .constants import ConstantsFile

from typing import Any


class CharacterisationFile(AuxiliaryFileReader):
    """
    class for loading the Characterisation File
    """
    _id = "CHD"

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
        """antenna gain for ku-band""")

    uso_freq_nom = AuxiliaryParameter(
        "uso_freq_nom_chd",
        """USO frequency nominal value""",
        param_type=float)
    alt_freq_multiplier = AuxiliaryParameter(
        "alt_freq_multiplier_chd",
        param_type=float)

    pri_sar = AuxiliaryParameter(
        "pri_sar_chd",
        """pulse repetition interval""",
        param_type=float)

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
