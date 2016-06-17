from ...proc.geo import lla2ecef
from ...proc.functions import angle_between
from ...conf import CharacterisationFile, ConstantsFile

from collections import OrderedDict
from enum import Enum
from typing import Dict, Any

import numpy as np

class IspPid(Enum):
    isp_null = 0
    isp_cal1_instr = 1
    isp_cal1_lrm = 2
    isp_cal1_sar = 3
    isp_cal1_rmc = 4
    isp_cal2 = 5
    isp_echo_lrm = 6
    isp_echo_sar = 7
    isp_echo_rmc = 8
    isp_echo_cal = 9

class InstrumentSourcePacket:
    """
    The base InstrumentSourcePacket (ISP) class

    Each ISP contains the data from one position in the
    satellite's orbit
    """
    @property
    def isp_pid(self):
        """
        the process id of the ISP
        """
        return self["isp_pid"]

    @isp_pid.setter
    def isp_pid(self, value):
        self["isp_pid"] = value

    @isp_pid.deleter
    def isp_pid(self):
        del self["isp_pid"]


    @property
    def time_sar_ku(self):
        """
        The time_sar_ku property of the ISP
        """
        return self["time_sar_ku"]

    @time_sar_ku.setter
    def time_sar_ku(self, value):
        self["time_sar_ku"] = value

    @time_sar_ku.deleter
    def time_sar_ku(self):
        del self["time_sar_ku"]

    @property
    def days(self):
        """
        The days property of the ISP
        """
        return self["days"]

    @days.setter
    def days(self, value):
        self["days"] = value

    @days.deleter
    def days(self):
        del self["days"]

    @property
    def seconds(self):
        """
        The seconds property of the ISP
        """
        return self["seconds"]

    @seconds.setter
    def seconds(self, value):
        self["seconds"] = value

    @seconds.deleter
    def seconds(self):
        del self["seconds"]

    @property
    def seq_count_sar_ku_fbr(self):
        """
        The seq_count_sar_ku_fbr property of the ISP
        """
        return self["seq_count_sar_ku_fbr"]

    @seq_count_sar_ku_fbr.setter
    def seq_count_sar_ku_fbr(self, value):
        self["seq_count_sar_ku_fbr"] = value

    @seq_count_sar_ku_fbr.deleter
    def seq_count_sar_ku_fbr(self):
        del self["seq_count_sar_ku_fbr"]

    @property
    def inst_id_sar_isp(self):
        """
        The inst_id_sar_isp property of the ISP
        """
        return self["inst_id_sar_isp"]

    @inst_id_sar_isp.setter
    def inst_id_sar_isp(self, value):
        self["inst_id_sar_isp"] = value

    @inst_id_sar_isp.deleter
    def inst_id_sar_isp(self):
        del self["inst_id_sar_isp"]

    @property
    def pri_sar_pre_dat(self):
        """
        The pri_sar_pre_dat property of the ISP
        """
        return self["pri_sar_pre_dat"]

    @pri_sar_pre_dat.setter
    def pri_sar_pre_dat(self, value):
        self["pri_sar_pre_dat"] = value

    @pri_sar_pre_dat.deleter
    def pri_sar_pre_dat(self):
        del self["pri_sar_pre_dat"]

    @property
    def ambiguity_order_sar(self):
        """
        The ambiguity_order_sar property of the ISP
        """
        return self["ambiguity_order_sar"]

    @ambiguity_order_sar.setter
    def ambiguity_order_sar(self, value):
        self["ambiguity_order_sar"] = value

    @ambiguity_order_sar.deleter
    def ambiguity_order_sar(self):
        del self["ambiguity_order_sar"]

    @property
    def burst_sar_ku(self):
        """
        The burst_sar_ku property of the ISP
        """
        return self["burst_sar_ku"]

    @burst_sar_ku.setter
    def burst_sar_ku(self, value):
        self["burst_sar_ku"] = value

    @burst_sar_ku.deleter
    def burst_sar_ku(self):
        del self["burst_sar_ku"]

    @property
    def lat_sar_sat(self):
        """
        The lat_sar_sat property of the ISP
        """
        return self["lat_sar_sat"]

    @lat_sar_sat.setter
    def lat_sar_sat(self, value):
        self["lat_sar_sat"] = value

    @lat_sar_sat.deleter
    def lat_sar_sat(self):
        del self["lat_sar_sat"]

    @property
    def lon_sar_sat(self):
        """
        The lon_sar_sat property of the ISP
        """
        return self["lon_sar_sat"]

    @lon_sar_sat.setter
    def lon_sar_sat(self, value):
        self["lon_sar_sat"] = value

    @lon_sar_sat.deleter
    def lon_sar_sat(self):
        del self["lon_sar_sat"]

    @property
    def alt_sar_sat(self):
        """
        The alt_sar_sat property of the ISP
        """
        return self["alt_sar_sat"]

    @alt_sar_sat.setter
    def alt_sar_sat(self, value):
        self["alt_sar_sat"] = value

    @alt_sar_sat.deleter
    def alt_sar_sat(self):
        del self["alt_sar_sat"]

    @property
    def geodetic_sat(self):
        """
        The Lat, Lon, and Alt of the satellite position
        """
        return np.asmatrix([self.lat_sar_sat,
                            self.lon_sar_sat,
                            self.alt_sar_sat]).T

    @geodetic_sat.setter
    def geodetic_sat(self, value):
        self.lat_sar_sat,\
         self.lon_sar_sat,\
         self.alt_sar_sat = value

    @property
    def alt_rate_sat_sar(self):
        """
        The alt_rate_sar_sat property of the ISP
        """
        return self["alt_rate_sat_sar"]

    @alt_rate_sat_sar.setter
    def alt_rate_sat_sar(self, value):
        self["alt_rate_sat_sar"] = value

    @alt_rate_sat_sar.deleter
    def alt_rate_sat_sar(self):
        del self["alt_rate_sat_sar"]

    @property
    def x_vel_sat_sar(self):
        """
        The x_vel_sat_sar property of the ISP
        """
        return self["x_vel_sat_sar"]

    @x_vel_sat_sar.setter
    def x_vel_sat_sar(self, value):
        self["x_vel_sat_sar"] = value

    @x_vel_sat_sar.deleter
    def x_vel_sat_sar(self):
        del self["x_vel_sat_sar"]

    @property
    def y_vel_sat_sar(self):
        """
        The y_vel_sat_sar property of the ISP
        """
        return self["y_vel_sat_sar"]

    @y_vel_sat_sar.setter
    def y_vel_sat_sar(self, value):
        self["y_vel_sat_sar"] = value

    @y_vel_sat_sar.deleter
    def y_vel_sat_sar(self):
        del self["y_vel_sat_sar"]

    @property
    def z_vel_sat_sar(self):
        """
        The z_vel_sat_sar property of the ISP
        """
        return self["z_vel_sat_sar"]

    @z_vel_sat_sar.setter
    def z_vel_sat_sar(self, value):
        self["z_vel_sat_sar"] = value

    @z_vel_sat_sar.deleter
    def z_vel_sat_sar(self):
        del self["z_vel_sat_sar"]

    @property
    def vel_sat_sar(self):
        """
        The Lat, Lon, and Alt of the satellite position
        """
        return np.asmatrix([self.x_vel_sat_sar,
                            self.y_vel_sat_sar,
                            self.z_vel_sat_sar]).T

    @vel_sat_sar.setter
    def vel_sat_sar(self, value):
        self.x_vel_sat_sar, \
         self.y_vel_sat_sar, \
         self.z_vel_sat_sar = value

    @property
    def roll_sar(self):
        """
        The roll_sar property of the ISP
        """
        return self["roll_sar"]

    @roll_sar.setter
    def roll_sar(self, value):
        self["roll_sar"] = value

    @roll_sar.deleter
    def roll_sar(self):
        del self["roll_sar"]

    @property
    def pitch_sar(self):
        """
        The pitch_sar property of the ISP
        """
        return self["pitch_sar"]

    @pitch_sar.setter
    def pitch_sar(self, value):
        self["pitch_sar"] = value

    @pitch_sar.deleter
    def pitch_sar(self):
        del self["pitch_sar"]

    @property
    def yaw_sar(self):
        """
        The yaw_sar property of the ISP
        """
        return self["yaw_sar"]

    @yaw_sar.setter
    def yaw_sar(self, value):
        self["yaw_sar"] = value

    @yaw_sar.deleter
    def yaw_sar(self):
        del self["yaw_sar"]

    @property
    def orientation_sar(self):
        """
        The roll, pitch and yaw of the satellite position
        """
        return np.asmatrix([self.roll_sar,
                            self.pitch_sar,
                            self.yaw_sar]).T

    @orientation_sar.setter
    def orientation_sar(self, value):
        self.roll_sar, \
         self.pitch_sar, \
         self.yaw_sar = value

    @property
    def h0_sar(self):
        """
        The h0_sar property of the ISP
        """
        return self["h0_sar"]

    @h0_sar.setter
    def h0_sar(self, value):
        self["h0_sar"] = value

    @h0_sar.deleter
    def h0_sar(self):
        del self["h0_sar"]

    @property
    def t0_sar(self):
        """
        The t0_sar property of the ISP
        """
        return self["t0_sar"]

    @t0_sar.setter
    def t0_sar(self, value):
        self["t0_sar"] = value

    @t0_sar.deleter
    def t0_sar(self):
        del self["t0_sar"]

    @property
    def cor2_sar(self):
        """
        The cor2_sar property of the ISP
        """
        return self["cor2_sar"]

    @cor2_sar.setter
    def cor2_sar(self, value):
        self["cor2_sar"] = value

    @cor2_sar.deleter
    def cor2_sar(self):
        del self["cor2_sar"]

    @property
    def win_delay_sar_ku(self):
        """
        The win_delay_sar_ku property of the ISP
        """
        return self["win_delay_sar_ku"]

    @win_delay_sar_ku.setter
    def win_delay_sar_ku(self, value):
        self["win_delay_sar_ku"] = value

    @win_delay_sar_ku.deleter
    def win_delay_sar_ku(self):
        del self["win_delay_sar_ku"]

    @property
    def x_sar_surf(self):
        """
        The x-coordinate of the ECEF vector for the
        surface position below the satellite
        """
        return self["x_sar_surf"]

    @x_sar_surf.setter
    def x_sar_surf(self, value):
        self["x_sar_surf"] = value

    @x_sar_surf.deleter
    def x_sar_surf(self):
        del self["x_sar_surf"]

    @property
    def y_sar_surf(self):
        """
        The y-coordinate of the ECEF vector for the
        surface position below the satellite
        """
        return self["y_sar_surf"]

    @y_sar_surf.setter
    def y_sar_surf(self, value):
        self["y_sar_surf"] = value

    @y_sar_surf.deleter
    def y_sar_surf(self):
        del self["y_sar_surf"]

    @property
    def z_sar_surf(self):
        """
        The z-coordinate of the ECEF vector for the
        surface position below the satellite
        """
        return self["z_sar_surf"]

    @z_sar_surf.setter
    def z_sar_surf(self, value):
        self["z_sar_surf"] = value

    @z_sar_surf.deleter
    def z_sar_surf(self):
        del self["z_sar_surf"]

    @property
    def sar_surf(self):
        """
        The ECEF vector for the surface position
        below the satellite
        """
        return np.asmatrix([self.x_sar_surf,
                            self.y_sar_surf,
                            self.z_sar_surf]).T

    @sar_surf.setter
    def sar_surf(self, value):
        self.x_sar_surf, \
         self.y_sar_surf, \
         self.z_sar_surf = value

    @property
    def x_sar_sat(self):
        """
        The x-coordinate of the ECEF vector for the
        position of the satellite
        """
        return self["x_sar_sat"]

    @x_sar_sat.setter
    def x_sar_sat(self, value):
        self["x_sar_sat"] = value

    @x_sar_sat.deleter
    def x_sar_sat(self):
        del self["x_sar_sat"]

    @property
    def y_sar_sat(self):
        """
        The y-coordinate of the ECEF vector for the
        position of the satellite
        """
        return self["y_sar_sat"]

    @y_sar_sat.setter
    def y_sar_sat(self, value):
        self["y_sar_sat"] = value

    @y_sar_sat.deleter
    def y_sar_sat(self):
        del self["y_sar_sat"]

    @property
    def z_sar_sat(self):
        """
        The z-coordinate of the ECEF vector for the
        position of the satellite
        """
        return self["z_sar_sat"]

    @z_sar_sat.setter
    def z_sar_sat(self, value):
        self["z_sar_sat"] = value

    @z_sar_sat.deleter
    def z_sar_sat(self):
        del self["z_sar_sat"]

    @property
    def pos_sar_sat(self):
        """
        The ECEF vector for the position of the satellite
        """
        return np.asmatrix([self.x_sar_sat,
                            self.y_sar_sat,
                            self.z_sar_sat]).T

    @pos_sar_sat.setter
    def pos_sar_sat(self, value):
        self.x_sar_sat, \
        self.y_sar_sat, \
        self.z_sar_sat = value

    @property
    def seq_count_sar(self):
        """
        The sequence number of the ISP
        """
        return self._seq_count_sar

    @property
    def beam_angles_list(self):
        """
        The computed list of beam angles
        """
        return self["beam_angles_list"]

    @beam_angles_list.setter
    def beam_angles_list(self, value):
        self["beam_angles_list"] = value

    @beam_angles_list.deleter
    def beam_angles_list(self):
        del self["beam_angles_list"]

    @property
    def beam_angles_trend(self):
        """
        the trend direction of the ISP's beam angles
        """
        return self["beam_angles_trend"]

    @beam_angles_trend.setter
    def beam_angles_trend(self, value):
        self["beam_angles_trend"] = value

    @beam_angles_trend.deleter
    def beam_angles_trend(self):
        del self["beam_angles_trend"]

    @property
    def waveform_cor_sar(self):
        """
        The corrected SAR waveform
        """
        return self["waveform_cor_sar"]

    @waveform_cor_sar.setter
    def waveform_cor_sar(self, value):
        self["waveform_cor_sar"] = value

    @waveform_cor_sar.deleter
    def waveform_cor_sar(self):
        del self["waveform_cor_sar"]

    @property
    def doppler_angle_sar_sat(self):
        """
        the doppler_angle_sar_sat property
        """
        return self["doppler_angle_sar_sat"]

    @doppler_angle_sar_sat.setter
    def doppler_angle_sar_sat(self, value):
        self["doppler_angle_sar_sat"] = value

    @doppler_angle_sar_sat.deleter
    def doppler_angle_sar_sat(self):
        del self["doppler_angle_sar_sat"]

    @property
    def beams_focused(self):
        """
        the focused beams
        """
        return self["beams_focused"]

    @beams_focused.setter
    def beams_focused(self, value):
        self["beams_focused"] = value

    @beams_focused.deleter
    def beams_focused(self):
        del self["beams_focused"]

    @property
    def burst_processed(self):
        """varaible for tracking whether burst processing has been performed"""
        return self._burst_processed

    @burst_processed.setter
    def burst_processed(self, value):
        self._burst_processed = value

    @property
    def counter(self):
        return self._counter


    def __init__(self, cst: ConstantsFile, chd: CharacterisationFile,
                 seq_num: int=None, *dicts: Dict[str, Any], **values: Any):
        self._data = OrderedDict()
        self._counter = seq_num

        self._seq_count_sar = seq_num
        self._beam_angles_trend = None
        self._burst_processed = False

        self.isp_pid = IspPid.isp_null

        for values_group in dicts:
            self._data.update(values_group)
        self._data.update(values)

        self.cst = cst
        self.chd = chd

    def __setitem__(self, key: str, value: Any) -> None:
        if not hasattr(self.__class__, key):
            raise KeyError("{} has no attribute '{}'".format(self, key))
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def compute_location_sar_surf(self) -> None:
        lla = (
            self.lat_sar_sat,
            self.lon_sar_sat,
            self.alt_sar_sat
        )
        x, y, z = lla2ecef(lla, self.cst)

        self.x_sar_sat = x
        self.y_sar_sat = y
        self.z_sar_sat = z

        lat_sar_surf = self.lat_sar_sat
        lon_sar_surf = self.lon_sar_sat
        alt_sar_surf = self.alt_sar_sat - self.win_delay_sar_ku * self.cst.c / 2

        lla = (lat_sar_surf, lon_sar_surf, alt_sar_surf)
        x, y, z = lla2ecef(lla, self.cst)

        self.x_sar_surf = x
        self.y_sar_surf = y
        self.z_sar_surf = z

    def calculate_beam_angles_trend(self, prev_beam_angles_list_size: int, prev_beam_angles_trend: int) -> None:
        """
        computes the beam angles trend of the ISP

        :param prev_beam_angles_list_size: the size of the beam angles list of the previous ISP
        :param prev_beam_angles_trend: the trend of the beam angles of the previous ISP
        """

        beam_angles_list_size = len(self.beam_angles_list)

        if beam_angles_list_size == self.chd.n_ku_pulses_burst:
            self.beam_angles_trend = 0
            return

        if prev_beam_angles_list_size == -1 or beam_angles_list_size > prev_beam_angles_list_size:
            self.beam_angles_trend = 1
        elif beam_angles_list_size < prev_beam_angles_list_size:
            self.beam_angles_trend = -1
        else:
            self.beam_angles_trend = prev_beam_angles_trend

    def compute_doppler_angle(self) -> None:
        """
        calculate the doppler angle
        """
        alt_surf = self.alt_sar_sat - self.chd.mean_sat_alt
        surf_geodetic = np.array([
            self.lat_sar_sat,
            self.lon_sar_sat,
            alt_surf
        ])

        surf_cartesian = np.asmatrix(lla2ecef(surf_geodetic, self.cst))

        # n vector - sat position normal to surface
        n = np.asmatrix(
            surf_cartesian.T - self.pos_sar_sat
        )
        # v vector - sat velocty (cartesian)
        v = self.vel_sat_sar
        # vector perpendicular to plane nv
        w = np.cross(n.T, v.T)
        # vector perpendicular to plane nw
        m = np.cross(w, n.T)
        # angle between v and m
        self.doppler_angle_sar_sat = angle_between(v, m)