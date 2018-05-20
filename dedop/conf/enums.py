from enum import Enum


class AzimuthWindowingMethod(Enum):
    disabled = "none"
    boxcar = "boxcar"
    hanning = "hanning"
    hamming = "hamming"

class AzimuthProcessingMethod(Enum):
    """
    Enum for azimuth processing method selection flag
    """

    approximate = "approx"
    exact = "exact"


class AzimuthWeighting(Enum):
    """
    Enum for azimuth weighting toggle flag
    """

    enabled = 1
    disabled = 0

class OutputFormat(Enum):
    """
    Enum for output format option
    """

    s3 = 'sentinel-3'
    extended = 'extended'
