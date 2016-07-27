from scipy import sqrt, arctan, arctan2, sin, cos
from numpy.linalg import norm
from typing import Sequence, Tuple


from .geo_error import GeolocationError
from dedop.conf import ConstantsFile

COORD_ITERS = 10
GEODETIC_ERR = 1e-9

def ecef2lla(ecef: Sequence[float], cst: ConstantsFile) -> Tuple[float, float, float]:
    """
    converts a cartesian (x, y, z) earth-centred
     earth-fixed coordinate to a radial (lat, lon, alt)
     coordinate.
    """

    x, y, z = ecef

    lat = 0.
    lon = 0.
    alt = 0.

    # for x and y are both zero, calculate
    #    the geodetic vector now
    if (x == 0.) and (y == 0.):
        # set latitude
        lon = 0.
        # set altitude - deduct radius of earth
        #   from the z-coordinate
        alt = abs(z) - cst.semi_major_axis * (1. - cst.flat_coeff)

        # set the longitude
        if (z > 0.):
            lat = cst.pi / 2.
        elif (z < 0.):
            lat = -cst.pi / 2.
        else:
            # if everything is 0, coordinate is the centre of the earth
            raise GeolocationError("invalid ECEF coordinates: {}".format(ecef))
        return lat, lon, alt
    # otherwise, convert through iteration

    # compute accentricity squared (e^2)
    ecc_sqr = cst.flat_coeff * (2. - cst.flat_coeff)

    # first iteration - E-W curvature equals semi-major axis
    x0 = cst.semi_major_axis

    rad_xy = norm([x, y])

    alt_est = norm(ecef) - cst.semi_major_axis * sqrt(1. - cst.flat_coeff)
    tmp = 1. - ecc_sqr * x0 / (x0 + alt_est)

    lat_est = arctan(z / (rad_xy * tmp))

    # now iterate until geodetic coordinates are within GEODETIC_ERR
    #   (or for COORD_ITERS number of iterations)
    max_iters = True

    for iter_count in range(COORD_ITERS):
        sin_sqr_lat = sin(lat_est) * sin(lat_est)
        xn = cst.semi_major_axis / sqrt(1. - ecc_sqr * sin_sqr_lat)

        alt = rad_xy / cos(lat_est) - x0
        tmp = 1. - ecc_sqr * xn / (xn + alt)

        lat = arctan(z / (rad_xy * tmp))

        # compute latitude error
        lat_err = abs(lat - lat_est)
        # and altitude error
        alt_err = abs(alt - alt_est) / cst.semi_major_axis

        # update estimations
        x0 = xn
        lat_est = lat
        alt_est = alt

        if (lat_err < GEODETIC_ERR) and (alt_err < GEODETIC_ERR):
            max_iters = False
            break
    if max_iters:
        raise RuntimeWarning("MAX_ITERS reached in ecef2lla")

    if (x == 0.):
        if (y == 0.):
            lon = 0.
        elif (y > 0.):
            lon = cst.pi / 2.
        elif (y < 0.):
            lon = -cst.pi / 2.
    else:
        lon = arctan2(y, x)
    return lat, lon, alt