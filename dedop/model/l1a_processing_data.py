from dedop.proc.geo import lla2ecef
from dedop.proc.functions import angle_between
from dedop.conf import CharacterisationFile, ConstantsFile

from collections import OrderedDict
from enum import Enum
from typing import Dict, Any

import numpy as np

class PacketPid(Enum):
    null = 0
    cal1_instr = 1
    cal1_lrm = 2
    cal1_sar = 3
    cal1_rmc = 4
    cal2 = 5
    echo_lrm = 6
    echo_sar = 7
    echo_rmc = 8
    echo_cal = 9

class L1AProcessingData:
    """
    The base L1AProcessingData (ISP) class

    Each packet contains the data from one position in the
    satellite's orbit
    """
    @property
    def isp_pid(self):
        """
        the process id of the packet
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
        The time_sar_ku property of the packet
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
        The days property of the packet
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
        The seconds property of the packet
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
        The seq_count_sar_ku_fbr property of the packet
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
        The inst_id_sar_isp property of the packet
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
        The pri_sar_pre_dat property of the packet
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
        The ambiguity_order_sar property of the packet
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
        The burst_sar_ku property of the packet
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
        The lat_sar_sat property of the packet
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
        The lon_sar_sat property of the packet
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
        The alt_sar_sat property of the packet
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
        The alt_rate_sar_sat property of the packet
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
        The x_vel_sat_sar property of the packet
        """
        return self._vel_sat_sar[0, 0]

    @x_vel_sat_sar.setter
    def x_vel_sat_sar(self, value):
        self._vel_sat_sar[0, 0] = value

    @property
    def y_vel_sat_sar(self):
        """
        The y_vel_sat_sar property of the packet
        """
        return self._vel_sat_sar[1, 0]

    @y_vel_sat_sar.setter
    def y_vel_sat_sar(self, value):
        self._vel_sat_sar[1, 0] = value

    @property
    def z_vel_sat_sar(self):
        """
        The z_vel_sat_sar property of the packet
        """
        return self.vel_sat_sar[2, 0]

    @z_vel_sat_sar.setter
    def z_vel_sat_sar(self, value):
        self._vel_sat_sar[2, 0] = value

    @property
    def vel_sat_sar(self):
        """
        The Lat, Lon, and Alt of the satellite position
        """
        return self._vel_sat_sar

    @vel_sat_sar.setter
    def vel_sat_sar(self, value):
        self._vel_sat_sar[0, 0] = value[0]
        self._vel_sat_sar[1, 0] = value[1]
        self._vel_sat_sar[2, 0] = value[2]

    @property
    def roll_sar(self):
        """
        The roll_sar property of the packet
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
        The pitch_sar property of the packet
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
        The yaw_sar property of the packet
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
        The h0_sar property of the packet
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
        The t0_sar property of the packet
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
        The cor2_sar property of the packet
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
        The win_delay_sar_ku property of the packet
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
        The sequence number of the packet
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
        the trend direction of the packet's beam angles
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
        """variable for tracking whether burst processing has been performed"""
        return self._burst_processed

    @burst_processed.setter
    def burst_processed(self, value):
        self._burst_processed = value

    @property
    def counter(self):
        return self._counter

    @property
    def isp_coarse_time(self):
        return self["isp_coarse_time"]

    @property
    def isp_fine_time(self):
        return self["isp_fine_time"]

    @property
    def sral_fine_time(self):
        return self["sral_fine_time"]

    @property
    def flag_time_status(self):
        return self["flag_time_status"]
    
    @property
    def nav_bul_status(self):
        return self["nav_bul_status"]
    
    @property
    def nav_bul_source(self):
        return self["nav_bul_source"]
    
    @property
    def source_seq_count(self):
        return self["source_seq_count"]
    
    @property
    def oper_instr(self):
        return self["oper_instr"]
    
    @property
    def SAR_mode(self):
        return self["SAR_mode"]
    
    @property
    def cl_gain(self):
        return self["cl_gain"]
    
    @property
    def acq_stat(self):
        return self["acq_stat"]
    
    @property
    def dem_eeprom(self):
        return self["dem_eeprom"]
    
    @property
    def loss_track(self):
        return self["loss_track"]
    
    @property
    def h0_nav_dem(self):
        return self["h0_nav_dem"]
    
    @property
    def h0_applied(self):
        return self["h0_applied"]
    
    @property
    def cor2_nav_dem(self):
        return self["cor2_nav_dem"]
    
    @property
    def cor2_applied(self):
        return self["cor2_applied"]
    
    @property
    def dh0(self):
        return self["dh0"]
    
    @property
    def agccode_ku(self):
        return self["agccode_ku"]
    
    @property
    def range_ku(self):
        return self["range_ku"]
    
    @property
    def int_path_cor_ku(self):
        return self["int_path_cor_ku"]
    
    @property
    def agc_ku(self):
        return self["agc_ku"]
    
    @property
    def sig0_cal_ku(self):
        return self["sig0_cal_ku"]

    @property
    def uso_cor(self):
        return self["uso_cor"]

    @property
    def surf_type(self):
        return self["surf_type"]

    @property
    def roll_sral_mispointing(self):
        return self["roll_sral_mispointing"]

    @property
    def pitch_sral_mispointing(self):
        return self["pitch_sral_mispointing"]

    @property
    def yaw_sral_mispointing(self):
        return self["yaw_sral_mispointing"]

    @property
    def cog_cor(self):
        return self["cog_cor"]

    # CAL 1 & CAL 2
    @property
    def cal1_power(self) -> np.ndarray:
        """
        CAL1 power correction
        """
        return self["cal1_power"]

    @cal1_power.setter
    def cal1_power(self, value: np.ndarray) -> None:
        self["cal1_power"] = value

    @cal1_power.deleter
    def cal1_power(self) -> None:
        del self["cal1_power"]

    @property
    def cal1_phase(self) -> np.ndarray:
        """
        CAL1 phase correction
        """
        return self["cal1_phase"]

    @cal1_phase.setter
    def cal1_phase(self, value: np.ndarray) -> None:
        self["cal1_phase"] = value

    @cal1_phase.deleter
    def cal1_phase(self) -> None:
        del self["cal1_phase"]

    @property
    def cal2_array(self) -> np.ndarray:
        """
        CAL2 correction
        """
        return self["cal2_array"]

    @cal2_array.setter
    def cal2_array(self, value: np.ndarray) -> None:
        self["cal2_array"] = value

    @cal2_array.deleter
    def cal2_array(self) -> None:
        del self["cal2_array"]

    @property
    def leap_secs_since_2000(self):
        return self.time_sar_ku - (self.days * self.cst.sec_in_day + self.seconds)

    @property
    def h(self) -> np.ndarray:
        total_num_pulses_rc =\
            round(self.chd.n_bursts_cycle/self.pri_sar_pre_dat, 0)

        h = math.floor(self.h0_sar * self.chd.h0_cor2_unit_conv)
        h += self.cor2_applied *\
             np.arange(self.chd.n_ku_pulses_burst)/total_num_pulses_rc
        return h

    @property
    def cai(self):
        return (self.h / self.chd.cai_cor2_unit_conv).astype(int)

    @property
    def fai(self):
        return (self.h - self.cai*self.chd.cai_cor2_unit_conv) /\
                self.chd.h0_cor2_unit_conv

    @property
    def vel_sat_sar_norm(self):
        if self._vel_sat_norm is None:
            self._vel_sat_norm = np.linalg.norm(
                self.vel_sat_sar
            )
        return self._vel_sat_norm

    def __init__(self, cst: ConstantsFile, chd: CharacterisationFile,
                 seq_num: int=None, *dicts: Dict[str, Any], **values: Any):
        self._data = OrderedDict()
        self._counter = seq_num

        self._seq_count_sar = seq_num
        self._beam_angles_trend = None
        self._burst_processed = False
        self._vel_sat_norm = None
        x_vel = values.pop('x_vel_sat_sar', 0)
        y_vel = values.pop('y_vel_sat_sar', 0)
        z_vel = values.pop('z_vel_sat_sar', 0)
        self._vel_sat_sar = np.matrix([[x_vel], [y_vel], [z_vel]], dtype=np.float64)

        self.isp_pid = PacketPid.null

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
        computes the beam angles trend of the packet

        :param prev_beam_angles_list_size: the size of the beam angles list of the previous packet
        :param prev_beam_angles_trend: the trend of the beam angles of the previous packet
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

        if self.doppler_angle_sar_sat < self.cst.pi / 2:
            self.doppler_angle_sar_sat *= -1