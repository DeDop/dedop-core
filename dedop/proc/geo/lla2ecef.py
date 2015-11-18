from scipy import cos, sin, sqrt, pi
import numpy as np


def lla2ecef(lla, f=None, re=None, radians=True):
    """
    convert LLA (longitude, latitude, altitude) coordinates
    to ECEF (Earth-centred, Earth-fixed) XYZ coordinates.

    INPUTS:
        lla:	the LLA coordinate vector (or collection of vectors)
        [f]:	the flattening of the reference ellipsoid
        [Re]:	the equatorial radius (semi-major axis) of the reference ellipsoid

    if 'f' or 'Re' are omitted, the WGS84 model is used

    OUTPUTS:
        xyz:	The ECEF vector (or collection of vectors)
    """

    # set default values for WGS84
    a = 6378137.      # semi-major axis of the earth [m]
    b = 6356752.3145  # semi-minor axis of the earth [m]

    if f is not None and re is not None:
        # optional ref. ellipsoid has been provided:
        # set semi-major axis:
        a = re
        # set semi-minor axis:
        b = (1 - f) * re

    # check if 'lla' is 1D:
    dims = len(lla.shape)
    if dims == 1:
        lla = np.reshape(lla, (1, 3))

    # convert lat & lon into radians
    if not radians:
        lat = lla[:, 0] / 180.0 * pi
        lon = lla[:, 1] / 180.0 * pi
    else:
        lat = lla[:, 0]
        lon = lla[:, 1]
    alt = lla[:, 2]

    xyz = np.zeros(lla.shape)

    # calc. n (prime vertical of curvatures)
    n = a ** 2 / sqrt(
        (a * cos(lat) ** 2) +
        (b * sin(lon) ** 2)
    )
    # calc. e - eccentricity
    e = (b ** 2) / (a ** 2)

    # calc. coords
    xyz[:, 0] = (n + alt) * cos(lat) * cos(lon)
    xyz[:, 1] = (n + alt) * cos(lat) * sin(lon)
    xyz[:, 2] = (n * e + alt) * sin(lat)

    return xyz
