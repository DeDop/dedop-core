from scipy import sqrt, arctan, arctan2, sin, cos
from numpy.linalg import norm
from typing import Sequence, Tuple


from .geo_error import GeolocationError
from dedop.conf import ConstantsFile

# ATK patch for newer ecef2lla():
from numpy import mod, pi, abs, logical_and
import numbers

COORD_ITERS = 10
GEODETIC_ERR = 1e-9


def ecef2lla(ecef: Sequence[float], cst: ConstantsFile) -> Tuple[float, float, float]:
    """ECEF (x, y, z) -> (Alt, Lat, Lon)

    (Lat, Lon) in radians, (Alt, x, y, z) in meters.

    ECEF: Earth-Centered, Earth-Fixed
    (Cf. http://en.wikipedia.org/wiki/ECEF)

    For input ellipsoid codes (ell_code), cf. ellipsoid_collection in
    this module.

    * More details:

    x = ECEF X-coordinate (m)
    y = ECEF Y-coordinate (m)
    z = ECEF Z-coordinate (m)
    lat = geodetic latitude (rads)
    lon = longitude (rads)
    alt = height above ellipsoid (m)
    
    Notes: This function assumes al ellipsoid model.
    Latitude is customary geodetic (not geocentric).
    
    Source: "Department of Defense World Geodetic System 1984"
        Page 4-4
        National Imagery and Mapping Agency
        Last updated June, 2004
        NIMA TR8350.2

    Initially written in Matlab by Michael Kleder, July 2005.
    https://fr.mathworks.com/matlabcentral/fileexchange/7941-convert-cartesian--ecef--coordinates-to-lat--lon--alt?s_tid=prof_contriblnk

    2006-07-10, Matlab version modified by Nicolas Bercher (for MSW
    software), TETIS lab (Cemagref), Maison de la Teledetection,
    France.

    2013-11-04, Python version modified by Nicolas Bercher (for
    AltiHydro software), LEGOS lab (CNRS), Observatoire Midi-Pyrénées,
    Toulouse, France.

    2014-11-01 ownwards: maintained by Nicolas Bercher & Along-Track
    SAS, Plougonvelin, France.

    Nicolas Bercher
    nbercher@along-track
    Since 2013-11-04.

    """

    x, y, z = ecef

    sma, inv_flatt_coeff = cst.semi_major_axis, cst.flat_coeff

    smna = (1. - inv_flatt_coeff) * sma
    e = sqrt(1. - (smna**2.)/(sma**2.))

    b   = sqrt(sma**2. * (1. - e**2.))
    ep  = sqrt((sma**2. - b**2.) / b**2.)
    p   = sqrt(x**2. + y**2.)
    th  = arctan2(sma*z, b*p)
    lon = arctan2(y, x)
    lat = arctan2((z + ep**2. * b * sin(th)**3.), (p - e**2. * sma * cos(th)**3.))
    N   = sma / sqrt(1. - e**2. * sin(lat)**2.)
    alt = p / cos(lat) - N
    
    # return lon in range [0,2*pi]
    lon = mod(lon, 2.*pi)
    
    # correct for numerical instability in altitude near exact poles:
    # (after this correction, error is about 2 millimeters, which is about
    # the same as the numerical precision of the overall function)

    if isinstance(alt, numbers.Number):
        if abs(x)<1 and abs(y)<1:
            alt = z - b
    else:
        k = logical_and(abs(x)<1, abs(y)<1)
        alt[k] = abs(z[k]) - b
    
    # NB: removed rad2deg conversion since output is expected in radians
    return lat, lon, alt
    

def ecef2lla_iterative(ecef: Sequence[float], cst: ConstantsFile) -> Tuple[float, float, float]:
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

    if x == 0.:
        if y == 0.:
            lon = 0.
        elif y > 0.:
            lon = cst.pi / 2.
        elif y < 0.:
            lon = -cst.pi / 2.
    else:
        lon = arctan2(y, x)
    return lat, lon, alt
