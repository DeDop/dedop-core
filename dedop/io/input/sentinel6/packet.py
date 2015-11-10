from ...consts import chd
from ..packet import InstrumentSourcePacket

class Sentinel6Packet(InstrumentSourcePacket):
    def __init__(self, index, dataset):
        InstrumentSourcePacket.__init__(self, index)

        self.days = dataset.time_day_ku[index]
        self.seconds = dataset.time_seconds_ku[index]

        self.process_id = 57 if dataset.l1_mode_ku[index] else 58

        self.seq_count_sar_ku_fbr = dataset.tm_source_sequence_counter_ku[index]

        self.inst_id_sar_isp = 0
        self.pri_sar = chd.pri_sar
        self.ambiguity_order_sar = dataset.tm_ambiguity_rank_ku[index]

        self.burst_sar_ku = dataset.burst_counter_ku[index]
        self.burst_sar_ku_fbr = dataset.tm_burst_num_ku[index]

        self.lat_sar_sat = dataset.latitude_ku[index]
        self.lon_sar_sat = dataset.longitude_ku[index]
        self.alt_sar_sat = dataset.com_altitude_ku[index]
        self.alt_rate_sar_sat = dataset.com_altitude_rate_ku[index]

        self.x_vel_sat_sar = dataset.com_velocity_vector_ku[index, 0]
        self.y_vel_sat_sar = dataset.com_velocity_vector_ku[index, 1]
        self.z_vel_sat_sar = dataset.com_velocity_vector_ku[index, 2]

        self.roll_sar = dataset.satellite_mispointing_ku[index, 0]
        self.pitch_sar = dataset.satellite_mispointing_ku[index, 1]
        self.yaw_sar = dataset.satellite_mispointing_ku[index, 2]

        self.h0_sar = dataset.tm_h0_ku[index]
        self.cor2_sar = dataset.tm_cor2_ku[index]
