import numpy as np
from numpy.linalg import norm
from enum import Enum

class SurfaceLocationData():
    def __init__(self, data, cst, chd):
        self.time_surf = data.get('time_surf', None)

        self.x_surf = data.get('x_surf', None)
        self.y_surf = data.get('y_surf', None)
        self.z_surf = data.get('z_surf', None)

        self.lat_surf = data.get('lat_surf', None)
        self.lon_surf = data.get('lon_surf', None)
        self.alt_surf = data.get('alt_surf', None)

        self.x_sat = data.get('x_sar_sat', None)
        self.y_sat = data.get('y_sar_sat', None)
        self.z_sat = data.get('z_sar_sat', None)

        self.lat_sat = data.get('lat_sar_sat', None)
        self.lon_sat = data.get('lon_sar_sat', None)
        self.alt_sat = data.get('alt_sar_sat', None)

        self.x_vel_sat = data.get('x_vel_sat_sar', None)
        self.y_vel_sat = data.get('y_vel_sat_sar', None)
        self.z_vel_sat = data.get('z_vel_sat_sar', None)

        self.alt_rate_sat = data.get('alt_rate_sat_sar', None)

        self.roll_sat = data.get('roll_sar', None)
        self.pitch_sat = data.get('pitch_sar', None)
        self.yaw_sat = data.get('yaw_sar', None)

        self.pri_sar = data.get('pri_sar_pre_dat', None)

        self.compute_angular_azimuth_beam_resolution(cst, chd)
        self.compute_surf_sat_vector()

    def compute_angular_azimuth_beam_resolution(self, cst, chd):
        vel_sat = np.array([self.x_vel_sat,
                            self.y_vel_sat,
                            self.z_vel_sat]).T
        self.angular_azimuth_beam_resolution = np.arcsin(
            cst.c / (2. * chd.freq_ku * norm(vel_sat) *
                     chd.n_ku_pulses_burst * self.pri_sar)
        )

    def compute_surf_sat_vector(self):
        self.surf_sat_vector = np.array([self.x_surf - self.x_sat,
                                  self.y_surf - self.y_sat,
                                  self.z_surf - self.z_sat]).T

class SurfaceType(Enum):
    surface_rmc = 1