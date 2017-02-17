import numpy as np
from typing import Dict, Sequence

from dedop.model import SurfaceData, L1AProcessingData
from ..base_algorithm import BaseAlgorithm
from dedop.proc.functions import *
from dedop.proc.geo import lla2ecef, ecef2lla, normalize
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile


class SurfaceLocationAlgorithm(BaseAlgorithm):
    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile, cnf: ConfigurationFile):
        self.first_surf = False
        self.new_surf = False

        self.time_surf = 0
        self.x_surf = 0
        self.y_surf = 0
        self.z_surf = 0
        self.lat_surf = 0
        self.lon_surf = 0
        self.alt_surf = 0
        self.x_sat = 0
        self.y_sat = 0
        self.z_sat = 0
        self.lat_sat = 0
        self.lon_sat = 0
        self.alt_sat = 0
        self.x_vel_sat = 0
        self.y_vel_sat = 0
        self.z_vel_sat = 0
        self.alt_rate_sat = 0
        self.roll_sat = 0
        self.pitch_sat = 0
        self.yaw_sat = 0
        self.win_delay_surf = 0
        self.prev_tai = 0
        self.prev_utc_days = 0
        self.prev_utc_secs = 0
        self.curr_day_length = 0

        super().__init__(chd, cst, cnf)

    def get_surface(self) -> Dict[str, float]:
        """
        get dictionary of parameters for new surface

        :return: data for surface
        """
        return {
            'time_surf': self.time_surf,
            'x_surf': self.x_surf,
            'y_surf': self.y_surf,
            'z_surf': self.z_surf,
            'lat_surf': self.lat_surf,
            'lon_surf': self.lon_surf,
            'alt_surf': self.alt_surf,
            'x_sat': self.x_sat,
            'y_sat': self.y_sat,
            'z_sat': self.z_sat,
            'lat_sat': self.lat_sat,
            'lon_sat': self.lon_sat,
            'alt_sat': self.alt_sat,
            'x_vel_sat': self.x_vel_sat,
            'y_vel_sat': self.y_vel_sat,
            'z_vel_sat': self.z_vel_sat,
            'alt_rate_sat': self.alt_rate_sat,
            'roll_sat': self.roll_sat,
            'pitch_sat': self.pitch_sat,
            'yaw_sat': self.yaw_sat,
            'win_delay_surf': self.win_delay_surf,
            'prev_tai': self.prev_tai,
            'prev_utc_days': self.prev_utc_days,
            'prev_utc_secs': self.prev_utc_secs,
            'curr_day_length': self.curr_day_length
        }

    def store_first_location(self, isps: Sequence[L1AProcessingData]) -> None:
        """
        define values for first surface (directly beneath the ISP)

        :param isps: list of input bursts
        """
        isp_record = isps[-1]

        self.time_surf = isp_record.time_sar_ku

        self.lat_surf = normalize(isp_record.lat_sar_sat, self.cst)
        self.lon_surf = normalize(isp_record.lon_sar_sat, self.cst)
        self.alt_surf = isp_record.alt_sar_sat -\
                        isp_record.win_delay_sar_ku * self.cst.c / 2.

        surf = lla2ecef(
            [self.lat_surf, self.lon_surf, self.alt_surf], self.cst
        )
        self.x_surf = surf[0]
        self.y_surf = surf[1]
        self.z_surf = surf[2]

        self.x_sat = isp_record.x_sar_sat
        self.y_sat = isp_record.y_sar_sat
        self.z_sat = isp_record.z_sar_sat

        self.lat_sat = isp_record.lat_sar_sat
        self.lon_sat = isp_record.lon_sar_sat
        self.alt_sat = isp_record.alt_sar_sat

        self.x_vel_sat = isp_record.x_vel_sat_sar
        self.y_vel_sat = isp_record.y_vel_sat_sar
        self.z_vel_sat = isp_record.z_vel_sat_sar

        self.alt_rate_sat = isp_record.alt_rate_sat_sar

        self.roll_sat = isp_record.roll_sar
        self.pitch_sat = isp_record.pitch_sar
        self.yaw_sat = isp_record.yaw_sar

        self.win_delay_surf = isp_record.win_delay_sar_ku

    def __call__(self, locs: Sequence[SurfaceData], isps: Sequence[L1AProcessingData], force_new: bool=False) -> bool:
        """
        attempt to compute new surface location

        :param locs: current surface locations
        :param isps: current bursts
        :param force_new: flag to force a new surface directly beneath burst
        :return: 'True' if new surface was created
        """
        if (not locs) or force_new:
            self.first_surf = True
            self.new_surf = True

            self.store_first_location(isps)
        else:
            self.first_surf = False
            self.new_surf = self.find_new_location(locs, isps)
        return self.new_surf

    def find_new_location(self, locs: Sequence[SurfaceData], isps: Sequence[L1AProcessingData]) -> bool:
        """
        attempt to find a new surface location

        :param locs: current surface locations
        :param isps: current bursts
        :return: 'True' if surface is created
        """
        surface = locs[-1]
        isp_curr = isps[-1]
        isp_prev = isps[-2]

        ground_surf_orbit_vector = np.matrix(
            [[isp_curr.x_sar_surf - surface.x_sat,],
             [isp_curr.y_sar_surf - surface.y_sat,],
             [isp_curr.z_sar_surf - surface.z_sat,]],
            dtype=np.float64
        )
        ground_surf_orbit_angle = angle_between(
            surface.surf_sat_vector, ground_surf_orbit_vector
        )
        if ground_surf_orbit_angle < surface.angular_azimuth_beam_resolution:
            return False

        ground_surf_orbit_vector_prev = np.matrix(
            [[isp_prev.x_sar_surf - surface.x_sat,],
             [isp_prev.y_sar_surf - surface.y_sat,],
             [isp_prev.z_sar_surf - surface.z_sat,]],
            dtype=np.float64
        )
        try:
            ground_surf_orbit_angle_prev = angle_between(
                surface.surf_sat_vector, ground_surf_orbit_vector_prev
            )
        except RuntimeWarning:
            print(isp_curr.counter)

        # compute alpha - the ratio of the position of the surface
        #   between the two ISP readings
        alpha = (surface.angular_azimuth_beam_resolution - ground_surf_orbit_angle_prev) /\
                (ground_surf_orbit_angle - ground_surf_orbit_angle_prev)

        self.time_surf = isp_prev.time_sar_ku +\
            alpha * (isp_curr.time_sar_ku - isp_prev.time_sar_ku)
        self.x_surf = isp_prev.x_sar_surf +\
            alpha * (isp_curr.x_sar_surf - isp_prev.x_sar_surf)
        self.y_surf = isp_prev.y_sar_surf +\
            alpha * (isp_curr.y_sar_surf - isp_prev.y_sar_surf)
        self.z_surf = isp_prev.z_sar_surf +\
            alpha * (isp_curr.z_sar_surf - isp_prev.z_sar_surf)

        surf_loc_cart = np.array([self.x_surf,
                                  self.y_surf,
                                  self.z_surf])
        surf_loc_geod = ecef2lla(surf_loc_cart, self.cst)
        self.lat_surf = surf_loc_geod[0]
        self.lon_surf = surf_loc_geod[1]
        self.alt_surf = surf_loc_geod[2]

        self.x_sat = isp_prev.x_sar_sat +\
            alpha * (isp_curr.x_sar_sat - isp_prev.x_sar_sat)
        self.y_sat = isp_prev.y_sar_sat + \
            alpha * (isp_curr.y_sar_sat - isp_prev.y_sar_sat)
        self.z_sat = isp_prev.z_sar_sat + \
            alpha * (isp_curr.z_sar_sat - isp_prev.z_sar_sat)

        sat_loc_cart = np.array([self.x_sat,
                                 self.y_sat,
                                 self.z_sat])
        sat_loc_geod = ecef2lla(sat_loc_cart, self.cst)
        self.lat_sat = sat_loc_geod[0]
        self.lon_sat = sat_loc_geod[1]
        self.alt_sat = sat_loc_geod[2]

        self.x_vel_sat = isp_prev.x_vel_sat_sar + \
            alpha * (isp_curr.x_vel_sat_sar - isp_prev.x_vel_sat_sar)
        self.y_vel_sat = isp_prev.y_vel_sat_sar + \
            alpha * (isp_curr.y_vel_sat_sar - isp_prev.y_vel_sat_sar)
        self.z_vel_sat = isp_prev.z_vel_sat_sar + \
            alpha * (isp_curr.z_vel_sat_sar - isp_prev.z_vel_sat_sar)

        self.alt_rate_sat = isp_prev.alt_rate_sat_sar + \
            alpha * (isp_curr.alt_rate_sat_sar - isp_prev.alt_rate_sat_sar)

        self.roll_sat = isp_prev.roll_sar + \
                     alpha * (isp_curr.roll_sar - isp_prev.roll_sar)
        self.pitch_sat = isp_prev.pitch_sar + \
                     alpha * (isp_curr.pitch_sar - isp_prev.pitch_sar)
        self.yaw_sat = isp_prev.yaw_sar + \
                     alpha * (isp_curr.yaw_sar - isp_prev.yaw_sar)

        self.win_delay_surf = (self.alt_sat - self.alt_surf) * 2. / self.cst.c

        self.prev_tai = isp_prev.time_sar_ku
        self.prev_utc_days = isp_prev.days
        self.prev_utc_secs = isp_prev.seconds
        self.curr_day_length = self.cst.sec_in_day +\
            (isp_curr.leap_secs_since_2000 - isp_prev.leap_secs_since_2000)

        return True
