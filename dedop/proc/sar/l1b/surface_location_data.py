from ....io.consts import cst, chd

import numpy as np
from numpy.linalg import norm

class SurfaceLocationData:
    def __init__(self, location_data, data):
        self.time_surf = location_data['time_surf']

        self.x_surf = location_data['x_surf']
        self.y_surf = location_data['y_surf']
        self.z_surf = location_data['z_surf']

        self.lat_surf = location_data['lat_surf']
        self.lon_surf = location_data['lon_surf']
        self.alt_surf = location_data['alt_surf']

        self.x_sat = data.x_sar_sat
        self.y_sat = data.y_sar_sat
        self.z_sat = data.z_sar_sat

        self.lat_sat = data.lat_sar_sat
        self.lon_sat = data.lon_sar_sat
        self.alt_sat = data.alt_sar_sat

        self.x_vel_sat = data.x_vel_sat_sar
        self.y_vel_sat = data.y_vel_sat_sar
        self.z_vel_sat = data.z_vel_sat_sar

        self.alt_rate_sat = data.alt_rate_sat_sar

        self.roll_sat = data.roll_sar
        self.pitch_sat = data.pitch_sar
        self.yaw_sat = data.yaw_sar

        self.compute_angular_azimuth_beam_resolution()
        self.compute_surf_sat_vector()

    def compute_angular_azimuth_beam_resolution(self):
        vel_sat = np.array([self.x_vel_sat,
                            self.y_vel_sat,
                            self.z_vel_sat]).T
        self.angular_azimuth_beam_resolution = np.arcsin(
            cst.c / (2. * chd.freq_ku * norm(vel_sat) *
                     chd.N_ku_pulses_burst * chd.pri_sar)
        )

    def compute_surf_sat_vector(self):
        self.surf_sat = np.array([self.x_surf - self.x_sat,
                                  self.y_surf - self.y_sat,
                                  self.z_surf - self.z_sat]).T