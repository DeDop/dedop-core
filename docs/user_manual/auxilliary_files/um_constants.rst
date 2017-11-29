===========================
Constants Parameters
===========================

The Constants file (CST.json) contains the values of various physical constants required by
the Dedop processor. Although this file can be editted either via the Dedop Studio interface
or with the command ``dedop config edit``, it should generally not be nessicary to do so.

Constants
---------

- c_cst
    - value: float
    - description: speed of light
- pi_cst
    - value: float
    - description: Pi number
- semi_major_axis_cst
    - value: float
    - description: semi-major axis of WGS84 ellipsoid
- semi_minor_axis_cst
    - value: float
    - description: semi-minor axis of WGS84 ellipsoid
- earth_radius_cst
    - value: float
    - description: radius of the earth
- flat_coeff_cst
    - value: float
    - description: flattening coefficient of the WGS84 ellipsoid
- sec_in_day_cst
    - value: float
    - description: number of seconds in a day