===========================
Characterisation Parameters
===========================

The Characterisation file (CHD.json) describes the parameters of the instrument from which the input
data being processed have been obtained. the default characterisation parameter values are suitable
for processing data from Sentinel-3. In general, it should not be nessicary to edit this file. If you
wish to process Cryosat-2 data that has been adapted into the Sentinel-3 L1A format, a suitable set of
values can be created either through the `Dedop Studio` interface, or by adding the ``--cryosat-adapted``
flag to the ``dedop config add`` command.

Parameter Descriptions
----------------------

- mean_sat_alt_chd
    - value: float
    - units: metres
    - description: mean altitude of the satellite
- N_samples_sar_chd
    - value: integer
    - description: number of samples per each SAR pulse
- N_ku_pulses_burst_chd
    - value: integer
    - description: number of ku-band pulses per burst
- freq_ku_chd
    - value: float
    - units: Hz
    - description: emitted frequency in Ku-band
- pulse_length_chd
    - value: float
    - units: s
    - description: pulse length
- bw_ku_chd
    - value: float
    - units: Hz
    - description: Ku-band bandwidth
- power_tx_ant_ku_chd
    - value: float
    - units: dB
    - description: Antenna SSPA RF Peak Transmitted Power in Ku band
- antenna_gain_ku_chd
    - value: float
    - units: dB
    - description: Antenna gain for Ku-band
- uso_freq_nom_chd
    - value: float
    - units: Hz
    - description: USO nominal frequency
- alt_freq_multiplier_chd
    - value: float
    - description: Factor to convert from USO frequency to altimeter frequency
- prf_sar_chd
    - value: float
    - units: Hz
    - description: pulse repetition frequency
- brf_sar_chd
    - value: float
    - units: Hz
    - description: burst repetition frequency
- antenna_weights_chd
    - value: float array(250)
    - description: array of antenna weights
- antenna_angles_chd
    - value: float array(250)
    - units: radians
    - description: array of antenna angles
- antenna_angles_spacing_chd
    - value: float
    - units: radians
    - description: spacing between antenna angles

NB: the parameters ``antenna_weights_chd``, ``antenna_angles_chd``, and ``antenna_angles_spacing_chd``
are optional, and do not need to be included in the CHD file unless the ``flag_antenna_wieghting_cnf``
flag in the CNF file is set to ``true``.