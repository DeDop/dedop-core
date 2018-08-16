import numpy as np
from numpy.linalg import norm
from enum import Enum
from collections import OrderedDict

from dedop.conf import CharacterisationFile, ConstantsFile
from .l1a_processing_data import L1AProcessingData

from typing import Any, Tuple, Sequence


class SurfaceType(Enum):
    surface_null = 0
    surface_raw = 1
    surface_rmc = 2


class SurfaceData:
    """
    Class for storing data relating to a surface location
    """

    @property
    def sigma0_scaling_factor_beam(self) -> np.ndarray:
        """
        per-beam values for sigma-0 scaling factor
        """
        return self['sigma0_scaling_factor_beam']
    
    @sigma0_scaling_factor_beam.setter
    def sigma0_scaling_factor_beam(self, value: np.ndarray) -> None:
        self['sigma0_scaling_factor_beam'] = value

    @sigma0_scaling_factor_beam.deleter
    def sigma0_scaling_factor_beam(self) -> None:
        del self['sigma0_scaling_factor_beam']

    @property
    def focus_target_distance(self) -> float:
        """
        the distance from the surface position to the target
        focus location given in the CNF
        """
        return self["focus_target_distance"]

    @focus_target_distance.setter
    def focus_target_distance(self, value: float):
        self["focus_target_distance"] = value

    @focus_target_distance.deleter
    def focus_target_distance(self) -> None:
        del self["focus_target_distance"]

    @property
    def target_focused(self) -> bool:
        if "target_focused" not in self._data:
            self._data["target_focused"] = False
        return self["target_focused"]

    @target_focused.setter
    def target_focused(self, value: bool) -> None:
        self["target_focused"] = value

    @target_focused.deleter
    def target_focused(self) -> None:
        del self["target_focused"]

    @property
    def surface_counter(self) -> int:
        """
        The sequence number of the Surface Location
        """
        return self._surface_counter

    @property
    def time_surf(self) -> float:
        """
        the time_surf property of the surface location
        """
        return self["time_surf"]

    @time_surf.setter
    def time_surf(self, value: float) -> None:
        self["time_surf"] = value

    @time_surf.deleter
    def time_surf(self) -> None:
        del self["time_surf"]

    @property
    def win_delay_surf(self) -> float:
        """
        the win_delay_surf property of the surface location
        """
        return self["win_delay_surf"]

    @win_delay_surf.setter
    def win_delay_surf(self, value: float) -> None:
        self["win_delay_surf"] = value

    @win_delay_surf.deleter
    def win_delay_surf(self) -> None:
        del self["win_delay_surf"]

    @property
    def x_surf(self) -> float:
        """
        the x_surf property of the surface location
        """
        return self["x_surf"]

    @x_surf.setter
    def x_surf(self, value: float) -> None:
        self["x_surf"] = value

    @x_surf.deleter
    def x_surf(self) -> None:
        del self["x_surf"]

    @property
    def y_surf(self) -> float:
        """
        the y_surf property of the surface location
        """
        return self["y_surf"]

    @y_surf.setter
    def y_surf(self, value: float) -> None:
        self["y_surf"] = value

    @y_surf.deleter
    def y_surf(self) -> None:
        del self["y_surf"]

    @property
    def z_surf(self) -> float:
        """
        the z_surf property of the surface location
        """
        return self["z_surf"]

    @z_surf.setter
    def z_surf(self, value: float) -> None:
        self["z_surf"] = value

    @z_surf.deleter
    def z_surf(self) -> None:
        del self["z_surf"]

    @property
    def ecef_surf(self) -> Tuple[float, float, float]:
        """
        The ECEF position vector of the surface location
        """
        return self.x_surf, self.y_surf, self.z_surf

    @ecef_surf.setter
    def ecef_surf(self, value: Sequence[float]) -> None:
        self.x_surf, self.y_surf, self.z_surf = value

    @property
    def lat_surf(self) -> float:
        """
        the lat_surf property of the surface location
        """
        return self["lat_surf"]

    @lat_surf.setter
    def lat_surf(self, value: float) -> None:
        self["lat_surf"] = value

    @lat_surf.deleter
    def lat_surf(self) -> None:
        del self["lat_surf"]

    @property
    def lon_surf(self) -> float:
        """
        the lon_surf property of the surface location
        """
        return self["lon_surf"]

    @lon_surf.setter
    def lon_surf(self, value: float) -> None:
        self["lon_surf"] = value

    @lon_surf.deleter
    def lon_surf(self) -> None:
        del self["lon_surf"]

    @property
    def alt_surf(self) -> float:
        """
        the alt_surf property of the surface location
        """
        return self["alt_surf"]

    @alt_surf.setter
    def alt_surf(self, value: float) -> None:
        self["alt_surf"] = value

    @alt_surf.deleter
    def alt_surf(self) -> None:
        del self["alt_surf"]

    @property
    def lla_surf(self) -> Tuple[float]:
        """
        The geodetic position vector of the
         surface location
        """
        return self.lat_surf, self.lon_surf, self.alt_surf

    @lla_surf.setter
    def lla_surf(self, value: Sequence[float]) -> None:
        self.lat_surf, self.lon_surf, self.alt_surf = value

    @property
    def x_sat(self) -> float:
        """
        the x_sat property of the surface location
        """
        return self["x_sat"]

    @x_sat.setter
    def x_sat(self, value: float) -> None:
        self["x_sat"] = value

    @x_sat.deleter
    def x_sat(self) -> None:
        del self["x_sat"]

    @property
    def y_sat(self) -> float:
        """
        the y_sat property of the surface location
        """
        return self["y_sat"]

    @y_sat.setter
    def y_sat(self, value: float) -> None:
        self["y_sat"] = value

    @y_sat.deleter
    def y_sat(self) -> None:
        del self["y_sat"]

    @property
    def z_sat(self) -> float:
        """
        the z_sat property of the surface location
        """
        return self["z_sat"]

    @z_sat.setter
    def z_sat(self, value: float) -> None:
        self["z_sat"] = value

    @z_sat.deleter
    def z_sat(self) -> None:
        del self["z_sat"]

    @property
    def ecef_sat(self) -> Tuple[float]:
        """
        The ECEF position vector of the surface location
        """
        return self.x_sat, self.y_sat, self.z_sat

    @ecef_sat.setter
    def ecef_sat(self, value: Sequence[float]) -> None:
        self.x_sat, self.y_sat, self.z_sat = value

    @property
    def lat_sat(self) -> None:
        """
        the lat_sat property of the surface location
        """
        return self["lat_sat"]

    @lat_sat.setter
    def lat_sat(self, value: float) -> None:
        self["lat_sat"] = value

    @lat_sat.deleter
    def lat_sat(self) -> None:
        del self["lat_sat"]

    @property
    def lon_sat(self) -> float:
        """
        the lon_sat property of the surface location
        """
        return self["lon_sat"]

    @lon_sat.setter
    def lon_sat(self, value: float) -> None:
        self["lon_sat"] = value

    @lon_sat.deleter
    def lon_sat(self) -> None:
        del self["lon_sat"]

    @property
    def alt_sat(self) -> float:
        """
        the alt_sat property of the surface location
        """
        return self["alt_sat"]

    @alt_sat.setter
    def alt_sat(self, value: float) -> None:
        self["alt_sat"] = value

    @alt_sat.deleter
    def alt_sat(self) -> None:
        del self["alt_sat"]

    @property
    def lla_sat(self) -> Tuple[float]:
        """
        The geodetic position vector of the
         surface location
        """
        return self.lat_sat, self.lon_sat, self.alt_sat

    @lla_sat.setter
    def lla_sat(self, value: Sequence[float]) -> None:
        self.lat_sat, self.lon_sat, self.alt_sat = value

    @property
    def x_vel_sat(self) -> float:
        """
        the x_vel_sat property of the surface location
        """
        return self["x_vel_sat"]

    @x_vel_sat.setter
    def x_vel_sat(self, value: float) -> None:
        self["x_vel_sat"] = value

    @x_vel_sat.deleter
    def x_vel_sat(self) -> None:
        del self["x_vel_sat"]

    @property
    def y_vel_sat(self) -> float:
        """
        the y_vel_sat property of the surface location
        """
        return self["y_vel_sat"]

    @y_vel_sat.setter
    def y_vel_sat(self, value: float) -> None:
        self["y_vel_sat"] = value

    @y_vel_sat.deleter
    def y_vel_sat(self) -> None:
        del self["y_vel_sat"]

    @property
    def z_vel_sat(self) -> float:
        """
        the z_vel_sat property of the surface location
        """
        return self["z_vel_sat"]

    @z_vel_sat.setter
    def z_vel_sat(self, value: float) -> None:
        self["z_vel_sat"] = value

    @z_vel_sat.deleter
    def z_vel_sat(self) -> None:
        del self["z_vel_sat"]

    @property
    def vel_sat(self) -> Tuple[float]:
        """
        The velocity vector of the satellite above the
         surface location
        """
        return self.x_vel_sat, self.y_vel_sat, self.z_vel_sat

    @vel_sat.setter
    def vel_sat(self, value: Sequence[float]) -> None:
        self.x_vel_sat, self.y_vel_sat, self.z_vel_sat = value

    @property
    def alt_rate_sat(self) -> float:
        """
        the alt_rate_sat property of the surface location
        """
        return self["alt_rate_sat"]

    @alt_rate_sat.setter
    def alt_rate_sat(self, value: float) -> None:
        self["alt_rate_sat"] = value

    @alt_rate_sat.deleter
    def alt_rate_sat(self) -> None:
        del self["alt_rate_sat"]

    @property
    def roll_sat(self) -> float:
        """
        the roll_sat property of the surface location
        """
        return self["roll_sat"]

    @roll_sat.setter
    def roll_sat(self, value: float) -> None:
        self["roll_sat"] = value

    @roll_sat.deleter
    def roll_sat(self) -> None:
        del self["roll_sat"]

    @property
    def pitch_sat(self) -> float:
        """
        the pitch_sat property of the surface location
        """
        return self["pitch_sat"]

    @pitch_sat.setter
    def pitch_sat(self, value: float) -> None:
        self["pitch_sat"] = value

    @pitch_sat.deleter
    def pitch_sat(self) -> None:
        del self["pitch_sat"]

    @property
    def yaw_sat(self) -> None:
        """
        the yaw_sat property of the surface location
        """
        return self["yaw_sat"]

    @yaw_sat.setter
    def yaw_sat(self, value: float) -> None:
        self["yaw_sat"] = value

    @yaw_sat.deleter
    def yaw_sat(self) -> None:
        del self["yaw_sat"]

    @property
    def orientation_sat(self) -> Tuple[float]:
        """
        The roll, pitch and yaw of the satellite's
         orientation above the surface location
        """
        return self.roll_sat, self.pitch_sat, self.yaw_sat

    @orientation_sat.setter
    def orientation_sat(self, value: Sequence[float]) -> None:
        self.roll_sat, self.pitch_sat, self.yaw_sat = value

    @property
    def angular_azimuth_beam_resolution(self) -> float:
        """
        the angular_azimuth_beam_resolution property of the surface location
        """
        return self["angular_azimuth_beam_resolution"]

    @angular_azimuth_beam_resolution.setter
    def angular_azimuth_beam_resolution(self, value: float) -> None:
        self["angular_azimuth_beam_resolution"] = value

    @angular_azimuth_beam_resolution.deleter
    def angular_azimuth_beam_resolution(self) -> None:
        del self["angular_azimuth_beam_resolution"]

    @property
    def surface_type(self) -> SurfaceType:
        """
        the surface_type property of the surface location
        """
        return self["surface_type"]

    @surface_type.setter
    def surface_type(self, value: SurfaceType) -> None:
        self["surface_type"] = value

    @surface_type.deleter
    def surface_type(self) -> None:
        del self["surface_type"]

    @property
    def stack_all_beams_indices(self) -> np.ndarray:
        """
        the stack_all_beams_indices property of the surface location
        """
        return self["stack_all_beams_indices"]

    @stack_all_beams_indices.setter
    def stack_all_beams_indices(self, value: np.ndarray):
        self["stack_all_beams_indices"] = value

    @stack_all_beams_indices.deleter
    def stack_all_beams_indices(self) -> None:
        del self["stack_all_beams_indices"]

    @property
    def stack_all_beams_indices_abs(self) -> np.ndarray:
        """
        the stack_all_beams_indices_abs property of the surface location
        """
        return self["stack_all_beams_indices_abs"]

    @stack_all_beams_indices_abs.setter
    def stack_all_beams_indices_abs(self, value: np.ndarray) -> None:
        self["stack_all_beams_indices_abs"] = value

    @stack_all_beams_indices_abs.deleter
    def stack_all_beams_indices_abs(self) -> None:
        del self["stack_all_beams_indices_abs"]

    @property
    def stack_all_bursts(self) -> np.ndarray:
        """
        the stack_all_bursts property of the surface location
        """
        return self["stack_all_bursts"]

    @stack_all_bursts.setter
    def stack_all_bursts(self, value: np.ndarray) -> None:
        self["stack_all_bursts"] = value

    @stack_all_bursts.deleter
    def stack_all_bursts(self) -> None:
        del self["stack_all_bursts"]

    @property
    def data_stack_size(self) -> int:
        """
        The number of bursts in the stack
        """
        return self["data_stack_size"]

    @data_stack_size.setter
    def data_stack_size(self, value: int) -> None:
        self["data_stack_size"] = value

    @data_stack_size.deleter
    def data_stack_size(self) -> None:
        del self["data_stack_size"]

    @property
    def stack_bursts(self) -> np.ndarray:
        """
        the stack_bursts property of the surface location
        """
        return self["stack_bursts"]

    @stack_bursts.setter
    def stack_bursts(self, value: np.ndarray) -> None:
        self["stack_bursts"] = value

    @stack_bursts.deleter
    def stack_bursts(self) -> None:
        del self["stack_bursts"]

    @property
    def beam_angles_surf(self) -> np.ndarray:
        """
        the beam_angles_surf property of the surface location
        """
        return self["beam_angles_surf"]

    @beam_angles_surf.setter
    def beam_angles_surf(self, value: np.ndarray) -> None:
        self["beam_angles_surf"] = value

    @beam_angles_surf.deleter
    def beam_angles_surf(self) -> None:
        del self["beam_angles_surf"]

    @property
    def surf_sat_vector(self) -> np.ndarray:
        """
        the surf_sat_vector property of the surface location
        """
        return self["surf_sat_vector"]

    @surf_sat_vector.setter
    def surf_sat_vector(self, value: np.ndarray) -> None:
        self["surf_sat_vector"] = value

    @surf_sat_vector.deleter
    def surf_sat_vector(self) -> None:
        del self["surf_sat_vector"]

    @property
    def t0_surf(self) -> float:
        """
        the t0_surf property of the surface location
        """
        return self["t0_surf"]

    @t0_surf.setter
    def t0_surf(self, value: float) -> None:
        self["t0_surf"] = value

    @t0_surf.deleter
    def t0_surf(self) -> None:
        del self["t0_surf"]

    @property
    def beams_surf(self) -> np.ndarray:
        """
        the beams_surf property of the surface location
        """
        return self["beams_surf"]

    @beams_surf.setter
    def beams_surf(self, value: np.ndarray) -> None:
        self["beams_surf"] = value

    @beams_surf.deleter
    def beams_surf(self) -> None:
        del self["beams_surf"]

    @property
    def beams_geo_corr(self) -> np.ndarray:
        """
        the beams_geo_corr property of the surface location
        """
        return self["beams_geo_corr"]

    @beams_geo_corr.setter
    def beams_geo_corr(self, value: np.ndarray) -> None:
        self["beams_geo_corr"] = value

    @beams_geo_corr.deleter
    def beams_geo_corr(self) -> None:
        del self["beams_geo_corr"]

    @property
    def doppler_corrections(self) -> np.ndarray:
        """
        The doppler_corrections array
        """
        return self["doppler_corrections"]

    @doppler_corrections.setter
    def doppler_corrections(self, value: np.ndarray) -> None:
        self["doppler_corrections"] = value

    @doppler_corrections.deleter
    def doppler_corrections(self) -> None:
        del self["doppler_corrections"]

    @property
    def slant_range_corrections(self) -> np.ndarray:
        """
        The slant_range_corrections array
        """
        return self["slant_range_corrections"]

    @slant_range_corrections.setter
    def slant_range_corrections(self, value: np.ndarray) -> None:
        self["slant_range_corrections"] = value

    @slant_range_corrections.deleter
    def slant_range_corrections(self) -> None:
        del self["slant_range_corrections"]

    @property
    def win_delay_corrections(self) -> np.ndarray:
        """
        The win_delay_corrections array
        """
        return self["win_delay_corrections"]

    @win_delay_corrections.setter
    def win_delay_corrections(self, value: np.ndarray) -> None:
        self["win_delay_corrections"] = value

    @win_delay_corrections.deleter
    def win_delay_corrections(self) -> None:
        del self["win_delay_corrections"]

    @property
    def beams_range_compr(self) -> np.ndarray:
        """
        the range-compressed beams array
        """
        return self["beams_range_compr"]

    @beams_range_compr.setter
    def beams_range_compr(self, value: np.ndarray) -> None:
        self["beams_range_compr"] = value

    @beams_range_compr.deleter
    def beams_range_compr(self) -> None:
        del self["beams_range_compr"]

    @property
    def beams_range_compr_iq(self) -> np.ndarray:
        """
        the range-compressed beams array
        """
        return self["beams_range_compr_iq"]

    @beams_range_compr_iq.setter
    def beams_range_compr_iq(self, value: np.ndarray) -> None:
        self["beams_range_compr_iq"] = value

    @beams_range_compr_iq.deleter
    def beams_range_compr_iq(self) -> None:
        del self["beams_range_compr_iq"]

    @property
    def beams_masked(self) -> np.ndarray:
        """
        the result of the masking applied to the beams
        """
        return self['beams_masked']

    @beams_masked.setter
    def beams_masked(self, value: np.ndarray) -> None:
        self['beams_masked'] = value

    @beams_masked.deleter
    def beams_masked(self) -> None:
        del self['beams_masked']

    @property
    def look_angles_surf(self) -> np.ndarray:
        """
        the look_angles_surf property
        """
        return self['look_angles_surf']

    @look_angles_surf.setter
    def look_angles_surf(self, value: np.ndarray) -> None:
        self['look_angles_surf'] = value

    @look_angles_surf.deleter
    def look_angles_surf(self) -> None:
        del self['look_angles_surf']

    @property
    def pointing_angles_surf(self) -> np.ndarray:
        """
        the pointing_angles_surf property
        """
        return self['pointing_angles_surf']

    @pointing_angles_surf.setter
    def pointing_angles_surf(self, value: np.ndarray) -> None:
        self['pointing_angles_surf'] = value

    @pointing_angles_surf.deleter
    def pointing_angles_surf(self) -> None:
        del self['pointing_angles_surf']

    @property
    def stack_mask_vector(self) -> np.ndarray:
        """
        the stack_mask_vector property
        """
        return self['stack_mask_vector']

    @stack_mask_vector.setter
    def stack_mask_vector(self, value: np.ndarray) -> None:
        self['stack_mask_vector'] = value

    @stack_mask_vector.deleter
    def stack_mask_vector(self) -> None:
        del self['stack_mask_vector']

    @property
    def stack_mask(self) -> np.ndarray:
        """
        the stack_mask property
        """
        return self['stack_mask']

    @stack_mask.setter
    def stack_mask(self, value: np.ndarray) -> None:
        self['stack_mask'] = value

    @stack_mask.deleter
    def stack_mask(self) -> None:
        del self['stack_mask']

    @property
    def doppler_angles_surf(self) -> np.ndarray:
        """
        the doppler_angles_surf property
        """
        return self['doppler_angles_surf']

    @doppler_angles_surf.setter
    def doppler_angles_surf(self, value: np.ndarray) -> None:
        self['doppler_angles_surf'] = value

    @doppler_angles_surf.deleter
    def doppler_angles_surf(self) -> None:
        del self['doppler_angles_surf']

    @property
    def stack_mask(self) -> np.ndarray:
        """
        the stack_mask property
        """
        return self['stack_mask']

    @stack_mask.setter
    def stack_mask(self, value: np.ndarray) -> None:
        self['stack_mask'] = value

    @stack_mask.deleter
    def stack_mask(self) -> None:
        del self['stack_mask']

    @property
    def range_sat_surf(self) -> float:
        """
        the range_sat_surf property
        """
        return self['range_sat_surf']

    @range_sat_surf.setter
    def range_sat_surf(self, value: float) -> None:
        self['range_sat_surf'] = value

    @range_sat_surf.deleter
    def range_sat_surf(self) -> float:
        del self['range_sat_surf']

    @property
    def closest_burst_index(self) -> int:
        """index of the burst closest to the surface position"""
        return self['closest_burst_index']

    @closest_burst_index.setter
    def closest_burst_index(self, value: int) -> None:
        self['closest_burst_index'] = value

    @closest_burst_index.deleter
    def closest_burst_index(self) -> None:
        del self['closest_burst_index']

    @property
    def closest_burst(self) -> L1AProcessingData:
        """the closest bursts to the surface position"""
        return self.stack_bursts[self.closest_burst_index]

    @property
    def sigma0_scaling_factor(self) -> float:
        """the sigma-nought scaling factor"""
        return self["sigma0_scaling_factor"]

    @sigma0_scaling_factor.setter
    def sigma0_scaling_factor(self, value: float) -> None:
        self["sigma0_scaling_factor"] = value

    @sigma0_scaling_factor.deleter
    def sigma0_scaling_factor(self) -> None:
        del self["sigma0_scaling_factor"]

    @property
    def stack_std(self) -> float:
        """the standard deviation of the gaussian fit for the stack"""
        return self["stack_std"]

    @stack_std.setter
    def stack_std(self, value: float) -> None:
        self["stack_std"] = value

    @stack_std.deleter
    def stack_std(self) -> None:
        del self["stack_std"]

    @property
    def stack_max(self) -> float:
        """the maximum value of the gaussian fit for the stack"""
        return self["stack_max"]

    @stack_max.setter
    def stack_max(self, value: float) -> None:
        self["stack_max"] = value

    @stack_max.deleter
    def stack_max(self) -> None:
        del self["stack_max"]

    @property
    def stack_skewness(self) -> float:
        """the skewness of the gaussian fit for the stack"""
        return self["stack_skewness"]

    @stack_skewness.setter
    def stack_skewness(self, value: float) -> None:
        self["stack_skewness"] = value

    @stack_skewness.deleter
    def stack_skewness(self) -> None:
        del self["stack_skewness"]

    @property
    def stack_kurtosis(self) -> float:
        """the kurtosis of the fit for the stack"""
        return self["stack_kurtosis"]

    @stack_kurtosis.setter
    def stack_kurtosis(self, value):
        self["stack_kurtosis"] = value

    @stack_kurtosis.deleter
    def stack_kurtosis(self):
        del self["stack_kurtosis"]

    @property
    def waveform_multilooked(self) -> np.ndarray:
        """the final waveform after multilooking"""
        return self["waveform_multilooked"]

    @waveform_multilooked.setter
    def waveform_multilooked(self, value: np.ndarray) -> None:
        self["waveform_multilooked"] = value

    @waveform_multilooked.deleter
    def waveform_multilooked(self) -> None:
        del self["waveform_multilooked"]

    @property
    def gps_time_surf(self) -> float:
        return self.time_surf + 20 * 365 * 86400 - 19

    @property
    def prev_tai(self):
        return self["prev_tai"]

    @property
    def prev_utc_days(self):
        return self["prev_utc_days"]

    @property
    def prev_utc_secs(self):
        return self["prev_utc_secs"]

    @property
    def curr_day_length(self):
        return self["curr_day_length"]

    @property
    def n_beams_start_stop(self) -> float:
        return self["n_beams_start_stop"]

    @n_beams_start_stop.setter
    def n_beams_start_stop(self, value: int) -> None:
        self["n_beams_start_stop"] = value

    @property
    def start_look_angle(self) -> int:
        return self["start_look_angle"]

    @start_look_angle.setter
    def start_look_angle(self, value: float) -> None:
        self["start_look_angle"] = value

    @property
    def stop_look_angle(self) -> float:
        return self["stop_look_angle"]

    @stop_look_angle.setter
    def stop_look_angle(self, value: float) -> None:
        self["stop_look_angle"] = value

    @property
    def start_doppler_angle(self) -> float:
        return self["start_doppler_angle"]

    @start_doppler_angle.setter
    def start_doppler_angle(self, value: float) -> None:
        self["start_doppler_angle"] = value

    @property
    def stop_doppler_angle(self) -> float:
        return self["stop_doppler_angle"]

    @stop_doppler_angle.setter
    def stop_doppler_angle(self, value: float) -> None:
        self["stop_doppler_angle"] = value

    @property
    def start_pointing_angle(self) -> float:
        return self["start_pointing_angle"]

    @start_pointing_angle.setter
    def start_pointing_angle(self, value: float) -> None:
        self["start_pointing_angle"] = value

    @property
    def stop_pointing_angle(self) -> float:
        return self["stop_pointing_angle"]

    @stop_pointing_angle.setter
    def stop_pointing_angle(self, value: float) -> None:
        self["stop_pointing_angle"] = value

    @property
    def stack_mask_vector_start_stop(self) -> np.ndarray:
        return self["stack_mask_vector_start_stop"]

    @stack_mask_vector_start_stop.setter
    def stack_mask_vector_start_stop(self, value: np.ndarray) -> None:
        self["stack_mask_vector_start_stop"] = value

    @property
    def start_beam_angle(self) -> float:
        return self["start_beam_angle"]

    @start_beam_angle.setter
    def start_beam_angle(self, value: float) -> None:
        self["start_beam_angle"] = value

    @property
    def stop_beam_angle(self) -> float:
        return self["stop_beam_angle"]

    @stop_beam_angle.setter
    def stop_beam_angle(self, value: float) -> None:
        self["stop_beam_angle"] = value

    @property
    def start_burst_index(self) -> float:
        return self["start_burst_index"]

    @start_burst_index.setter
    def start_burst_index(self, value: float) -> None:
        self["start_burst_index"] = value

    @property
    def stop_burst_index(self) -> float:
        return self["stop_burst_index"]

    @stop_burst_index.setter
    def stop_burst_index(self, value: float) -> None:
        self["stop_burst_index"] = value

    @property
    def beam_angles_start_stop(self) -> np.ndarray:
        return self["beam_angles_start_stop"]

    @beam_angles_start_stop.setter
    def beam_angles_start_stop(self, value: np.ndarray) -> None:
        self["beam_angles_start_stop"] = value

    @property
    def look_angles_start_stop(self) -> np.ndarray:
        return self["look_angles_start_stop"]

    @look_angles_start_stop.setter
    def look_angles_start_stop(self, value: np.ndarray) -> None:
        self["look_angles_start_stop"] = value

    def __init__(self, cst: ConstantsFile, chd: CharacterisationFile, surf_num: int=None,
                 *dicts: dict, **values: Any):
        """
        initialize the SurfaceData instance

        :param cst: ConstantsFile object containing data from the chosen cst file
        :param chd: CharacterisationFile object containing data from the chosen chd file
        :param surf_num: optional integer counter for identifying surface
        :param dicts: array of dictionaries containing data definitions
        :param values: keyword arguments for data definitions
        """
        # set surface id
        self._surface_counter = surf_num
        # create empty data container
        self._data = OrderedDict()
        # set default values
        self._data["surface_type"] = SurfaceType.surface_null
        self.stack_all_beams_indices = []
        self.stack_all_beams_indices_abs = []
        self.stack_all_bursts = []

        # get values from dictionaries
        for values_group in dicts:
            self.set_values(**values_group)
        # get values from keyword arguments
        self.set_values(**values)

        # get conf file objects
        self.cst = cst
        self.chd = chd

    def set_values(self, **values: Any) -> None:
        """
        sets a number of data values from keyword arguments
        """
        for propname, value in values.items():
            self[propname] = value

    def __setitem__(self, key: str, value: Any) -> None:
        if not hasattr(self.__class__, key):
            raise KeyError("{} has no attribute '{}'".format(self, key))
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def compute_angular_azimuth_beam_resolution(self, pri_sar: float) -> None:
        vel_sat = np.array([self.x_vel_sat,
                            self.y_vel_sat,
                            self.z_vel_sat]).T
        self.angular_azimuth_beam_resolution = np.arcsin(
            self.cst.c / (2. * self.chd.freq_ku * norm(vel_sat) * self.chd.n_ku_pulses_burst * pri_sar)
        )

    def compute_surf_sat_vector(self) -> None:
        self.surf_sat_vector =\
            np.asarray(self.ecef_surf, dtype=np.float64) -\
            np.asarray(self.ecef_sat,  dtype=np.float64)

    def add_stack_beam_index(self, beam_index: int, beam_angle_trend: int, beam_angles_list_size: int) -> None:
        self.stack_all_beams_indices.append(beam_index)

        if beam_angle_trend == 1:
            self.stack_all_beams_indices_abs.append(
                beam_index + self.chd.n_ku_pulses_burst -
                beam_angles_list_size - self.chd.n_ku_pulses_burst // 2
            )
        else:
            self.stack_all_beams_indices_abs.append(
                beam_index - self.chd.n_ku_pulses_burst // 2
            )

    def add_stack_burst(self, packet: L1AProcessingData):
        self.stack_all_bursts.append(packet)
