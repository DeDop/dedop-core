from math import acos

import numpy as np
from numpy.linalg import norm
from typing import Sequence, Tuple

from dedop.model import SurfaceData, L1AProcessingData
from ..base_algorithm import BaseAlgorithm


class BeamAnglesAlgorithm(BaseAlgorithm):
    """
    Class for finding beam angles
    """

    def __call__(self, surface_locations: Sequence[SurfaceData], isp_record: L1AProcessingData,
                 work_location: SurfaceData):
        """
        compute the beam angles between the provided list of surfaces and the given burst

        :param surface_locations: list of surface locations
        :param isp_record: current burst
        :param work_location: working surface location
        """
        self.work_location_seen = False
        self.beam_angles = []
        self.surfaces_seen = []

        curr_location_seen = False

        # the q angles define the max. & min. view angle for satellite
        # at the position of the burst
        q_min = acos(self.cst.c / self.chd.pri_sar / 4. /
                     self.chd.freq_ku / isp_record.vel_sat_sar_norm)
        q_max = self.cst.pi - q_min

        for surface in surface_locations:
            prev_location_seen = curr_location_seen

            beam_angle, curr_location_seen =\
                self.compute_beam_angle(surface, isp_record, q_min, q_max)
            if curr_location_seen:
                self.beam_angles.append(beam_angle)
                self.surfaces_seen.append(surface.surface_counter)

                if len(self.beam_angles) > self.chd.n_ku_pulses_burst:
                    self.beam_angles.pop(0)
                    self.surfaces_seen.pop(0)
                if work_location == surface:
                    self.work_location_seen = True

            elif prev_location_seen:
                break

    @staticmethod
    def compute_beam_angle(surface: SurfaceData, isp_record: L1AProcessingData,
                           q_min: float, q_max: float) -> Tuple[float, bool]:
        """
        computes the beam angle for the specified surface.
        """

        # create vector from satellite position to surface
        surf_burst = np.matrix([
            surface.x_surf - isp_record.x_sar_sat,
            surface.y_surf - isp_record.y_sar_sat,
            surface.z_surf - isp_record.z_sar_sat
        ])
        # compute angle between surface vector and satellite's velocity
        # vector
        beam_angle = acos(
            np.dot(surf_burst, isp_record.vel_sat_sar) /
            (norm(surf_burst) * isp_record.vel_sat_sar_norm)
        )

        beam_angle_tangent = beam_angle - isp_record.doppler_angle_sar_sat
        # if the angle is within the q-range, it can be seen
        if q_min <= beam_angle_tangent <= q_max:
            location_seen = True
        else:
            location_seen = False

        return beam_angle, location_seen
