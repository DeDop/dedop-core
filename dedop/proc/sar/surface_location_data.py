import numpy as np
from numpy.linalg import norm
from enum import Enum
from collections import OrderedDict


class SurfaceLocationData:
    """
    Class for storing data relating to a surface location
    """

    @property
    def surface_counter(self):
        """
        The sequence number of the Surface Location
        """
        return self._surface_counter

    @property
    def time_surf(self):
        """
        the time_surf property of the surface location
        """
        return self["time_surf"]

    @time_surf.setter
    def time_surf(self, value):
        self["time_surf"] = value

    @time_surf.deleter
    def time_surf(self):
        del self["time_surf"]

    @property
    def win_delay_surf(self):
        """
        the win_delay_surf property of the surface location
        """
        return self["win_delay_surf"]

    @win_delay_surf.setter
    def win_delay_surf(self, value):
        self["win_delay_surf"] = value

    @win_delay_surf.deleter
    def win_delay_surf(self):
        del self["win_delay_surf"]

    @property
    def x_surf(self):
        """
        the x_surf property of the surface location
        """
        return self["x_surf"]

    @x_surf.setter
    def x_surf(self, value):
        self["x_surf"] = value

    @x_surf.deleter
    def x_surf(self):
        del self["x_surf"]

    @property
    def y_surf(self):
        """
        the y_surf property of the surface location
        """
        return self["y_surf"]

    @y_surf.setter
    def y_surf(self, value):
        self["y_surf"] = value

    @y_surf.deleter
    def y_surf(self):
        del self["y_surf"]

    @property
    def z_surf(self):
        """
        the z_surf property of the surface location
        """
        return self["z_surf"]

    @z_surf.setter
    def z_surf(self, value):
        self["z_surf"] = value

    @z_surf.deleter
    def z_surf(self):
        del self["z_surf"]

    @property
    def ecef_surf(self):
        """
        The ECEF position vector of the surface location
        """
        return [self.x_surf, self.y_surf, self.z_surf]

    @ecef_surf.setter
    def ecef_surf(self, value):
        self.x_surf, self.y_surf, self.z_surf = value

    @property
    def lat_surf(self):
        """
        the lat_surf property of the surface location
        """
        return self["lat_surf"]

    @lat_surf.setter
    def lat_surf(self, value):
        self["lat_surf"] = value

    @lat_surf.deleter
    def lat_surf(self):
        del self["lat_surf"]

    @property
    def lon_surf(self):
        """
        the lon_surf property of the surface location
        """
        return self["lon_surf"]

    @lon_surf.setter
    def lon_surf(self, value):
        self["lon_surf"] = value

    @lon_surf.deleter
    def lon_surf(self):
        del self["lon_surf"]

    @property
    def alt_surf(self):
        """
        the alt_surf property of the surface location
        """
        return self["alt_surf"]

    @alt_surf.setter
    def alt_surf(self, value):
        self["alt_surf"] = value

    @alt_surf.deleter
    def alt_surf(self):
        del self["alt_surf"]

    @property
    def lla_surf(self):
        """
        The geodetic position vector of the
         surface location
        """
        return [self.lat_surf,
                self.lon_surf,
                self.alt_surf]

    @lla_surf.setter
    def lla_surf(self, value):
        self.lat_surf, \
         self.lon_surf, \
         self.alt_surf = value

    @property
    def x_sat(self):
        """
        the x_sat property of the surface location
        """
        return self["x_sat"]

    @x_sat.setter
    def x_sat(self, value):
        self["x_sat"] = value

    @x_sat.deleter
    def x_sat(self):
        del self["x_sat"]

    @property
    def y_sat(self):
        """
        the y_sat property of the surface location
        """
        return self["y_sat"]

    @y_sat.setter
    def y_sat(self, value):
        self["y_sat"] = value

    @y_sat.deleter
    def y_sat(self):
        del self["y_sat"]

    @property
    def z_sat(self):
        """
        the z_sat property of the surface location
        """
        return self["z_sat"]

    @z_sat.setter
    def z_sat(self, value):
        self["z_sat"] = value

    @z_sat.deleter
    def z_sat(self):
        del self["z_sat"]

    @property
    def ecef_sat(self):
        """
        The ECEF position vector of the surface location
        """
        return [self.x_sat, self.y_sat, self.z_sat]

    @ecef_sat.setter
    def ecef_sat(self, value):
        self.x_sat, self.y_sat, self.z_sat = value

    @property
    def lat_sat(self):
        """
        the lat_sat property of the surface location
        """
        return self["lat_sat"]

    @lat_sat.setter
    def lat_sat(self, value):
        self["lat_sat"] = value

    @lat_sat.deleter
    def lat_sat(self):
        del self["lat_sat"]

    @property
    def lon_sat(self):
        """
        the lon_sat property of the surface location
        """
        return self["lon_sat"]

    @lon_sat.setter
    def lon_sat(self, value):
        self["lon_sat"] = value

    @lon_sat.deleter
    def lon_sat(self):
        del self["lon_sat"]

    @property
    def alt_sat(self):
        """
        the alt_sat property of the surface location
        """
        return self["alt_sat"]

    @alt_sat.setter
    def alt_sat(self, value):
        self["alt_sat"] = value

    @alt_sat.deleter
    def alt_sat(self):
        del self["alt_sat"]

    @property
    def lla_sat(self):
        """
        The geodetic position vector of the
         surface location
        """
        return [self.lat_sat,
                self.lon_sat,
                self.alt_sat]

    @lla_sat.setter
    def lla_sat(self, value):
        self.lat_sat, \
         self.lon_sat, \
         self.alt_sat = value

    @property
    def x_vel_sat(self):
        """
        the x_vel_sat property of the surface location
        """
        return self["x_vel_sat"]

    @x_vel_sat.setter
    def x_vel_sat(self, value):
        self["x_vel_sat"] = value

    @x_vel_sat.deleter
    def x_vel_sat(self):
        del self["x_vel_sat"]

    @property
    def y_vel_sat(self):
        """
        the y_vel_sat property of the surface location
        """
        return self["y_vel_sat"]

    @y_vel_sat.setter
    def y_vel_sat(self, value):
        self["y_vel_sat"] = value

    @y_vel_sat.deleter
    def y_vel_sat(self):
        del self["y_vel_sat"]

    @property
    def z_vel_sat(self):
        """
        the z_vel_sat property of the surface location
        """
        return self["z_vel_sat"]

    @z_vel_sat.setter
    def z_vel_sat(self, value):
        self["z_vel_sat"] = value

    @z_vel_sat.deleter
    def z_vel_sat(self):
        del self["z_vel_sat"]

    @property
    def vel_sat(self):
        """
        The velocity vector of the satellite above the
         surface location
        """
        return [self.x_vel_sat,
                self.y_vel_sat,
                self.z_vel_sat]

    @vel_sat.setter
    def vel_sat(self, value):
        self.x_vel_sat,\
         self.y_vel_sat,\
         self.z_vel_sat = value

    @property
    def alt_rate_sat(self):
        """
        the alt_rate_sat property of the surface location
        """
        return self["alt_rate_sat"]

    @alt_rate_sat.setter
    def alt_rate_sat(self, value):
        self["alt_rate_sat"] = value

    @alt_rate_sat.deleter
    def alt_rate_sat(self):
        del self["alt_rate_sat"]

    @property
    def roll_sat(self):
        """
        the roll_sat property of the surface location
        """
        return self["roll_sat"]

    @roll_sat.setter
    def roll_sat(self, value):
        self["roll_sat"] = value

    @roll_sat.deleter
    def roll_sat(self):
        del self["roll_sat"]

    @property
    def pitch_sat(self):
        """
        the pitch_sat property of the surface location
        """
        return self["pitch_sat"]

    @pitch_sat.setter
    def pitch_sat(self, value):
        self["pitch_sat"] = value

    @pitch_sat.deleter
    def pitch_sat(self):
        del self["pitch_sat"]

    @property
    def yaw_sat(self):
        """
        the yaw_sat property of the surface location
        """
        return self["yaw_sat"]

    @yaw_sat.setter
    def yaw_sat(self, value):
        self["yaw_sat"] = value

    @yaw_sat.deleter
    def yaw_sat(self):
        del self["yaw_sat"]

    @property
    def orientation_sat(self):
        """
        The roll, pitch and yaw of the satellite's
         orientation above the surface location
        """
        return [self.roll_sat,
                self.pitch_sat,
                self.yaw_sat]

    @orientation_sat.setter
    def orientation_sat(self, value):
        self.roll_sat, \
         self.pitch_sat, \
         self.yaw_sat = value

    @property
    def angular_azimuth_beam_resolution(self):
        """
        the angular_azimuth_beam_resolution property of the surface location
        """
        return self["angular_azimuth_beam_resolution"]

    @angular_azimuth_beam_resolution.setter
    def angular_azimuth_beam_resolution(self, value):
        self["angular_azimuth_beam_resolution"] = value

    @angular_azimuth_beam_resolution.deleter
    def angular_azimuth_beam_resolution(self):
        del self["angular_azimuth_beam_resolution"]

    @property
    def surface_type(self):
        """
        the surface_type property of the surface location
        """
        return self["surface_type"]

    @surface_type.setter
    def surface_type(self, value):
        self["surface_type"] = value

    @surface_type.deleter
    def surface_type(self):
        del self["surface_type"]

    @property
    def stack_all_beams_indices(self):
        """
        the stack_all_beams_indices property of the surface location
        """
        return self["stack_all_beams_indices"]

    @stack_all_beams_indices.setter
    def stack_all_beams_indices(self, value):
        self["stack_all_beams_indices"] = value

    @stack_all_beams_indices.deleter
    def stack_all_beams_indices(self):
        del self["stack_all_beams_indices"]

    @property
    def stack_all_bursts(self):
        """
        the stack_all_bursts property of the surface location
        """
        return self["stack_all_bursts"]

    @stack_all_bursts.setter
    def stack_all_bursts(self, value):
        self["stack_all_bursts"] = value

    @stack_all_bursts.deleter
    def stack_all_bursts(self):
        del self["stack_all_bursts"]

    @property
    def data_stack_size(self):
        """
        The number of bursts in the stack
        """
        try:
            return self["data_stack_size"]
        except KeyError:
            self["data_stack_size"] =\
                len(self.stack_all_bursts)
            return self["data_stack_size"]

    @data_stack_size.setter
    def data_stack_size(self, value):
        self["data_stack_size"] = value

    @data_stack_size.deleter
    def data_stack_size(self):
        del self["data_stack_size"]

    @property
    def stack_bursts(self):
        """
        the stack_bursts property of the surface location
        """
        return self["stack_bursts"]

    @stack_bursts.setter
    def stack_bursts(self, value):
        self["stack_bursts"] = value

    @stack_bursts.deleter
    def stack_bursts(self):
        del self["stack_bursts"]

    @property
    def beam_angles_surf(self):
        """
        the beam_angles_surf property of the surface location
        """
        return self["beam_angles_surf"]

    @beam_angles_surf.setter
    def beam_angles_surf(self, value):
        self["beam_angles_surf"] = value

    @beam_angles_surf.deleter
    def beam_angles_surf(self):
        del self["beam_angles_surf"]

    @property
    def surf_sat_vector(self):
        """
        the surf_sat_vector property of the surface location
        """
        return self["surf_sat_vector"]

    @surf_sat_vector.setter
    def surf_sat_vector(self, value):
        self["surf_sat_vector"] = value

    @surf_sat_vector.deleter
    def surf_sat_vector(self):
        del self["surf_sat_vector"]

    @property
    def t0_surf(self):
        """
        the t0_surf property of the surface location
        """
        return self["t0_surf"]

    @t0_surf.setter
    def t0_surf(self, value):
        self["t0_surf"] = value

    @t0_surf.deleter
    def t0_surf(self):
        del self["t0_surf"]

    @property
    def beams_surf(self):
        """
        the beams_surf property of the surface location
        """
        return self["beams_surf"]

    @beams_surf.setter
    def beams_surf(self, value):
        self["beams_surf"] = value

    @beams_surf.deleter
    def beams_surf(self):
        del self["beams_surf"]

    @property
    def beams_geo_corr(self):
        """
        the beams_geo_corr property of the surface location
        """
        return self["beams_geo_corr"]

    @beams_geo_corr.setter
    def beams_geo_corr(self, value):
        self["beams_geo_corr"] = value

    @beams_geo_corr.deleter
    def beams_geo_corr(self):
        del self["beams_geo_corr"]

    @property
    def doppler_corrections(self):
        """
        The doppler_corrections array
        """
        return self["doppler_corrections"]

    @doppler_corrections.setter
    def doppler_corrections(self, value):
        self["doppler_corrections"] = value

    @doppler_corrections.deleter
    def doppler_corrections(self):
        del self["doppler_corrections"]

    @property
    def slant_range_corrections(self):
        """
        The slant_range_corrections array
        """
        return self["slant_range_corrections"]

    @slant_range_corrections.setter
    def slant_range_corrections(self, value):
        self["slant_range_corrections"] = value

    @slant_range_corrections.deleter
    def slant_range_corrections(self):
        del self["slant_range_corrections"]

    @property
    def win_delay_corrections(self):
        """
        The win_delay_corrections array
        """
        return self["win_delay_corrections"]

    @win_delay_corrections.setter
    def win_delay_corrections(self, value):
        self["win_delay_corrections"] = value

    @win_delay_corrections.deleter
    def win_delay_corrections(self):
        del self["win_delay_corrections"]

    @property
    def beams_range_compr(self):
        """
        the range-compressed beams array
        """
        return self["beams_range_compr"]

    @beams_range_compr.setter
    def beams_range_compr(self, value):
        self["beams_range_compr"] = value

    @beams_range_compr.deleter
    def beams_range_compr(self):
        del self["beams_range_compr"]


    def __init__(self, cst, chd, surf_num=None, *dicts, **values):
        self._surface_counter = surf_num
        self._data = OrderedDict()
        self._data["surface_type"] = SurfaceType.surface_null

        for values_group in dicts:
            self._data.update(values_group)
        self._data.update(values)

        self.cst = cst
        self.chd = chd

    def __setitem__(self, key, value):
        if not hasattr(self.__class__, key):
            raise KeyError("{} has no attribute '{}'".format(self, key))
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def compute_angular_azimuth_beam_resolution(self, pri_sar):
        vel_sat = np.array([self.x_vel_sat,
                            self.y_vel_sat,
                            self.z_vel_sat]).T
        self.angular_azimuth_beam_resolution = np.arcsin(
            self.cst.c / (2. * self.chd.freq_ku * norm(vel_sat) *
                     self.chd.n_ku_pulses_burst * pri_sar)
        )

    def compute_surf_sat_vector(self):
        self.surf_sat_vector =\
            np.asarray(self.ecef_surf, dtype=np.float64) -\
            np.asarray(self.ecef_sat,  dtype=np.float64)

class SurfaceType(Enum):
    surface_null = 0
    surface_raw = 1
    surface_rmc = 2