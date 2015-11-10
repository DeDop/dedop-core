class InstrumentSourcePacket:
    days = None
    seconds = None
    process_id = None
    seq_count_sar_ku_fbr = None
    inst_id_sar_isp = None
    pri_sar = None
    ambiguity_order_sar = None
    burst_sar_ku = None
    burst_sar_ku_fbr = None
    lat_sar_sat = None
    lon_sar_sat = None
    alt_sar_sat = None
    alt_rate_sar_sat = None
    x_vel_sat_sar = None
    y_vel_sat_sar = None
    z_vel_sat_sar = None
    roll_sar = None
    pitch_sar = None
    yaw_sar = None
    h0_sar = None
    cor2_sar = None

    def __init__(self, packet_num):
        self.seq_count_sar = packet_num
