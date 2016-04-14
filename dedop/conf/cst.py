from .constants_reader import *


class ConstantsFile(ConstantsFileReader):
    """
    class for loading the Constants file
    """

    _filename = "cst.json"

    @property
    def c(self):
        """Speed of light"""
        return self["c_cst"].value

    @property
    def semi_major_axis(self):
        """Semi-major axis of WGS84 ellipsoid"""
        return self["semi_major_axis_cst"].value

    @property
    def earth_radius(self):
        """Earth Radius"""
        return self["earth_radius_cst"].value

    @property
    def sec_in_day(self):
        """Number of seconds in a day"""
        return self["sec_in_day_cst"].value

    @property
    def pi(self):
        """Pi number"""
        return self["pi_cst"].value

    @property
    def flat_coeff(self):
        """Flattening coefficient of WGS84 ellipsoid"""
        return self["flat_coeff_cst"].value

    @property
    def semi_minor_axis(self):
        """Semi-minor axis of WGS84 ellipsoid"""
        return self["semi_minor_axis_cst"].value

    def __init__(self, filename=None):
        if filename is None:
            filename = self._filename
        super().__init__(filename)