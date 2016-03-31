from ....conf import cst, chd
from ..base_algorithm import BaseAlgorithm

import numpy as np
from numpy.linalg import norm
from math import acos

class BeamAnglesAlgorithm(BaseAlgorithm):
    """
    Class for finding beam angles
    """
    def __init__(self):
        self.work_location_seen = False
        self.beam_angles = []
        self.surfaces_seen = []

        super().__init__()

    def __call__(self, surface_locations, isp_record, work_location_index):
        """

        """
        curr_location_seen = False

        for surface in surface_locations:
            prev_location_seen = curr_location_seen

            beam_angle, curr_location_seen =\
                self.compute_beam_angle(surface, isp_record)
            if curr_location_seen:
                self.beam_angles.append(beam_angle)
                self.surfaces_seen.append(surface.index)

                if len(self.beam_angles) > chd.N_ku_pulses_burst:
                    self.beam_angles.pop(0)
                    self.surfaces_seen.pop(0)
                if work_location_index == surface.index:
                    self.work_location_seen = True
            elif prev_location_seen:
                break

    def compute_beam_angle(self, surface, isp_record):
        """
        computes the beam angle for the specified surface.
        """
        # the q angles define the max. & min. view angle for satellite
        # at the position of the burst
        q_min = acos(cst.c / isp_record.pri_sar / 4. /
                     chd.freq_ku / norm(isp_record.vel_sat_sar))
        q_max = cst.pi - q_min

        # create vector from satellite position to surface
        surf_burst = np.matrix([
            [surface.x_surf - isp_record.x_sar_sat],
            [surface.y_surf - isp_record.y_sar_sat],
            [surface.z_surf - isp_record.z_sar_sat]
        ])
        # compute angle between surface vector and satellite's velocity
        # vector
        beam_angle = acos(
            np.dot(surf_burst, isp_record.vel_sat_sar) /
            (norm(surf_burst) * norm(isp_record.vel_sat_sar))
        )
        # if the angle is within the q-range, it can be seen
        if q_min <= beam_angle <= q_max:
            location_seen = True
        else:
            location_seen = False
        return beam_angle, location_seen