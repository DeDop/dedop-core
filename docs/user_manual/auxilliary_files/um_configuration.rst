========================
Configuration Parameters
========================

The configuration of the processor is controlled via the Configuration file (CST.json). This file
is a JSON document that contains several parameters to enable, disable, or otherwise control various
features of the processor. The CNF.json file can be editted either via the Dedop Studio interface,
or from the command-line interface with the command ``dedop config edit``.

This page contains descriptions of the configuration parameters, their purposes and possible values.

Corrections Flags
-----------------

- flag_cal2_correction_cnf
    - value: boolean [true|false]
    - description: Flag that activates the CAL2 corrections: Deactivated (false); Activated (true)
- flag_uso_correction_cnf
    - value: boolean [true|false]
    - description: Flag that activates the USO correction: Deactivated (false); Activated (true)
- flag_cal1_corrections_cnf
    - value: boolean [true|false]
    - description: Flag that activates the CAL1 corrections: Deactivated (false); Activated (true)
- flag_cal1_intraburst_corrections_cnf
    - value: boolean [true|false]
    - description: Flag that activates the CAL1 intraburst corrections: Deactivated (false); Activated (true)

Surface Focusing
-----------------

- flag_surface_focusing_cnf
    - value: boolean [true|false]
    - description: Flag that activates the surface focussing: Deactivated (false); Activated (true)
- surface_focusing_lat_cnf
    - value: float [-90, 90]
    - units: degrees north
    - description: Location of the surface focusing target (latitude) (ignored unless flag_surface_focusing_cnf is 'true')
- surface_focusing_lon_cnf
    - value: float [-180, 180]
    - units: degrees east
    - description: Location of the surface focusing target (longitude) (ignored unless flag_surface_focusing_cnf is 'true')
- surface_focusing_alt_cnf
    - value: float
    - units: metres
    - description: Location of the surface focusing target (altitude) (ignored unless flag_surface_focusing_cnf is 'true')

Azimuth Processing
------------------

- flag_azimuth_processing_method_cnf
    - value: string ['approx'|'exact']
    - description: Flag that indicates the azimuth processing method: Approximate ('approx'); Exact ('exact')
- flag_postphase_azimuth_processing_cnf
    - value: boolean [true|false]
    - description: Flag that enables the post-phase azimuth processing: Deactivated (false); Activated (true)
- flag_azimuth_windowing_method_cnf
    - value: string ['none'|'boxcar'|'hamming'|'hanning']
    - description: Flag the sets the azimuth windowing method: Disabled ('none'); Boxcar ('boxcar'); Hamming ('hamming'); Hanning ('hanning')
- azimuth_window_width_cnf
    - value: integer [32, 64]
    - description: Width of Azimuth window (minimum value: 32, maximum value: 64)

Geometry Corrections
--------------------

- flag_doppler_range_correction_cnf
    - value: boolean [true|false]
    - description: Flag that activates the Doppler range correction in the geometry corrections: Deactivated (false); Activated (true)
- flag_slant_range_correction_cnf
    - value: boolean [true|false]
    - description: Flag that activates the slant range correction in the geometry corrections: Deactivated (false); Activated (true)
- flag_window_delay_alignment_method_cnf
    - value: integer [0|1|2|3|4]
    - description: Flag to indicate the window delay alignment method: Surface dependent (0); Beam max integrated power (1); Satellite position above surface (2); Look angle 0 (3); Doppler angle 0 (4)

Stack Masking
-------------

- flag_stack_masking
    - value: boolean [true|false]
    - description: Flag that activates the Stack Masking algorithm: Activated (true); Deactivated (false)
- flag_remove_doppler_ambiguities
    - value: boolean [true|false]
    - description: Flag that indicates if the Doppler ambiguities will be removed: No (false); Yes (true)

Multilooking
------------

- flag_avoid_zeros_in_multilooking
    - value: boolean [true|false]
    - description: Flag that indicates if the samples set to zero in the beams will be avoided when averaging in multi-looking: No (false); Yes (true)
- flag_surface_weighting
    - value: boolean [true|false]
    - description: Flag that activates the surface weighting: Deactivated (false); Activated (true)
- flag_antenna_weighting
    - value: boolean [true|false]
    - description: Flag that activates the antenna weighting: Deactivated (false); Activated (true)

General
-------

- zp_fact_range
    - value: integer
    - description: Zero padding factor used during range compression
- n_looks_stack
    - value: integer
    - description: Maximum number of looks in 1 stack

Region of Interest
------------------

NB: these parameters are optional, any or all of them may be omitted from the configuration
file. If you do not wish to apply a Region-of-Interest (RoI) filter, you should not include
these parameters in the configuration file. If you wish to enable the RoI filter, add whichever
parameters you intend to use to describe the RoI.

- min_lat
    - value: float [-90, 90]
    - units: degrees north
    - description: minimum latitude beneath which input records will be excluded
- max_lat
    - value: float [-90, 90]
    - units: degrees north
    - description: maximum latitude above which input records will be excluded
- min_lon
    - value: float [-180, 180]
    - units: degrees east
    - description: minimum longitude beneath which input records will be excluded
- max_lon
    - value: float [-180, 180]
    - units: degrees east
    - description: maximum longitude above which input records will be excluded