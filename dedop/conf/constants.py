from .auxiliary_file_reader import *


class ConstantsFile(AuxiliaryFileReader):
    """
    class for loading the Constants file
    """
    _id = "CST"
    _fileversion = 0

    c = AuxiliaryParameter(
        "c_cst",
        "speed of light",
        param_type=float)
    pi = AuxiliaryParameter(
        "pi_cst",
        "Pi number",
        param_type=float)
    semi_major_axis = AuxiliaryParameter(
        "semi_major_axis_cst",
        "semi-major axis of WGS84 ellipsoid",
        param_type=float)
    semi_minor_axis = AuxiliaryParameter(
        "semi_minor_axis_cst",
        "semi-minor axis of WGS84 ellipsoid",
        param_type=float)
    earth_radius = AuxiliaryParameter(
        "earth_radius_cst",
        "radius of the earth",
        param_type=float)
    flat_coeff = AuxiliaryParameter(
        "flat_coeff_cst",
        "flattening coefficient of the WGS84 ellipsoid",
        param_type=float)
    sec_in_day = AuxiliaryParameter(
        "sec_in_day_cst",
        "number of seconds in a day",
        param_type=float)

    def __init__(self, filename: str=None, **kwargs: Any):
        super().__init__(filename, **kwargs)
