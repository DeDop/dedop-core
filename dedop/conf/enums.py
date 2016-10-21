from enum import Enum


class AzimuthWindowingMethod(Enum):
    disabled = "none"
    boxcar = "boxcar"
    hanning = "hanning"
    hamming = "hamming"