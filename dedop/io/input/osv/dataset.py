from ..packet import InstrumentSourcePacket

import numpy as np
from scipy.interpolate import splrep, splev


class OSVDataSet:
    """
    class for retrieving orbit position information
    """
    # below is a list of the variables returned each time the get_interpolated
    #  function is called.
    params = ["days", "seconds", "process_id", "seq_count_sar_ku_fbr", "inst_id_sar_isp",
              "pri_sar", "ambiguity_order_sar", "burst_sar_ku", "burst_sar_ku_fbr", "lat_sar_sat",
              "lon_sar_sat", "alt_sar_sat", "alt_rate_sat_sar", "x_vel_sat_sar", "y_vel_sat_sar",
              "z_vel_sat_sar", "roll_sar", "pitch_sar", "yaw_sar", "h0_sar", "cor2_sar"]

    def __init__(self, input_dataset, window_size=10):
        self._dset = input_dataset
        self.window_size = window_size

    def get_interpolated(self, time, linear=False):
        """
        returns the values at the specified time using either
        linear or spline-based interpolation
        """
        if linear:
            return self._get_lin_interpolated(time)
        return self._get_spline_interpolated(time)

    def _get_spline_interpolated(self, time):
        """
        returns values at the specified time using spline
        interpolation
        """
        window = []
        remaining = int(self.window_size / 2)

        for packet in self._dset:
            window.append(packet)
            if len(window) > self.window_size:
                window.pop(0)
            if packet.time_sar_ku > time:
                remaining -= 1
                if remaining <= 0 and len(window) == self.window_size:
                    break

        t = np.array([p.time_sar_ku for p in window])
        vals = {'time_sar_ku': time}
        for pname in self.params:
            var = np.array([getattr(p, pname) for p in window])
            spline = splrep(t, var)
            vals[pname] = splev(time, spline)
        return InstrumentSourcePacket(None, **vals)

    def _get_lin_interpolated(self, time):
        """
        returns the values at the specified time using linear
        interpolation
        """
        prev_packet = self._dset[0]
        next_packet = None
        for packet in self._dset:
            if packet.time_sar_ku < time:
                prev_packet = packet
            else:
                next_packet = packet
                break
        vals = {'time_sar_ku': time}
        t_diff = next_packet.time_sar_ku - prev_packet.time_sar_ku
        if t_diff <= 0:
            return next_packet
        fract = (time - prev_packet.time_sar_ku) / t_diff

        for pname in self.params:
            v1 = getattr(prev_packet, pname)
            v2 = getattr(next_packet, pname)
            if (v1 is None) or (v2 is None):
                continue
            vals[pname] = v1 + (v2 - v1) * fract
        return InstrumentSourcePacket(None, **vals)
