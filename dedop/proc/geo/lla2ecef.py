from scipy import cos, sin, sqrt, radians
from typing import Sequence, Tuple

from dedop.conf import ConstantsFile


def lla2ecef(lla: Sequence[float], cst: ConstantsFile, lla_as_degrees: bool=False) -> Tuple[float, float, float]:
    """
    converts LLA (Latitude, Longitude, Altitude) coordinates
    to ECEF (Earth-Centre, Earth-First) XYZ coordinates.
    """

    lat, lon, alt = lla
    if lla_as_degrees:
        lat = radians(lat)
        lon = radians(lon)

    a = cst.semi_major_axis
    b = cst.semi_minor_axis
    # calc. ellipsoid flatness
    f = (a - b) / a
    # calc. eccentricity
    e = sqrt(f * (2 - f))

    # Calculate length of the normal to the ellipsoid
    N = a / sqrt(1 - (e * sin(lat)) ** 2)
    # Calculate ecef coordinates
    x = (N + alt) * cos(lat) * cos(lon)
    y = (N + alt) * cos(lat) * sin(lon)
    z = (N * (1 - e ** 2) + alt) * sin(lat)
    # Return the ecef coordinates
    return x, y, z
