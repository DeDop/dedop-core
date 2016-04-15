from .packet import InstrumentSourcePacket

class InputDataset:
    def __init__(self, dataset, cst):
        self._dset = dataset
        self.cst = cst

    def close(self):
        self._dset.close()

    def __iter__(self):
        for packet in self._dset:
            yield packet

    def __getitem__(self, index):
        return self._dset[index]

    def get_interpolated(self, time):
        params = ["days", "seconds", "process_id", "seq_count_sar_ku_fbr", "inst_id_sar_isp",
                  "pri_sar", "ambiguity_order_sar", "burst_sar_ku", "burst_sar_ku_fbr", "lat_sar_sat",
                  "lon_sar_sat", "alt_sar_sat", "alt_rate_sat_sar", "x_vel_sat_sar", "y_vel_sat_sar",
                  "z_vel_sat_sar", "roll_sar", "pitch_sar", "yaw_sar", "h0_sar", "cor2_sar", "time_sar_ku"]

        prev_packet = self[0]
        next_packet = None
        for packet in self:
            if packet.time_sar_ku < time:
                prev_packet = packet
            else:
                next_packet = packet
                break
        vals = {}
        t_diff = next_packet.time_sar_ku - prev_packet.time_sar_ku
        if t_diff <= 0:
            return next_packet
        fract = (time - prev_packet.time_sar_ku) / t_diff

        for pname in params:
            v1 = getattr(prev_packet, pname)
            v2 = getattr(next_packet, pname)
            if (v1 is None) or (v2 is None):
                continue
            vals[pname] = v1 + (v2 - v1) * fract
        return InstrumentSourcePacket(None, **vals)
