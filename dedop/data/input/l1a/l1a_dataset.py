from enum import Enum
from math import log10, radians
from typing import Iterator

import netCDF4 as nc

from dedop.conf import ConfigurationFile, CharacterisationFile, ConstantsFile
from dedop.model.l1a_processing_data import L1AProcessingData, PacketPid
from ..input_dataset import InputDataset
from .enums import L1AVariables, L1ADimensions

from ..netcdf_reader import NetCDFReader


class L1ADataset(InputDataset):
    def __init__(self, filename: str, cst: ConstantsFile, chd: CharacterisationFile, cnf: ConfigurationFile):
        """
        The L1ADataset class reads L1A NetCDF data files.
        """
        dset = NetCDFReader(filename)
        super().__init__(dset, cst=cst, chd=chd, cnf=cnf)

        self._file_path = filename
        self._last_index = 0

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def max_index(self) -> int:
        """get size of primary dimension"""
        dim = self._dset.dimensions[
            L1ADimensions.time_l1a_echo_sar_ku.value
        ]
        return dim.size

    def __getitem__(self, index: int) -> L1AProcessingData:
        # convert scale factor to linear value
        agc = self.get_value(L1AVariables.agc_ku_l1a_echo_sar_ku, index)
        scale_factor = pow(10., -agc / 20.)
        # construct waveform
        waveform = (self.get_value(L1AVariables.i_meas_ku_l1a_echo_sar_ku, index) +
                    1j * self.get_value(L1AVariables.q_meas_ku_l1a_echo_sar_ku, index)) / scale_factor
        packet = L1AProcessingData(
            self.cst, self.chd, index,
            isp_pid=PacketPid.echo_sar,
            time_sar_ku=self.get_value(L1AVariables.time_l1a_echo_sar_ku, index),
            isp_coarse_time=self.get_value(L1AVariables.isp_coarse_time_l1a_echo_sar_ku, index),
            isp_fine_time=self.get_value(L1AVariables.isp_fine_time_l1a_echo_sar_ku, index),
            sral_fine_time=self.get_value(L1AVariables.sral_fine_time_l1a_echo_sar_ku, index),
            days=self.get_value(L1AVariables.UTC_day_l1a_echo_sar_ku, index),
            seconds=self.get_value(L1AVariables.UTC_sec_l1a_echo_sar_ku, index),
            inst_id_sar_isp=0,
            pri_sar_pre_dat=self.chd.pri_sar,
            ambiguity_order_sar=0,
            burst_sar_ku=self.get_value(L1AVariables.burst_count_prod_l1a_echo_sar_ku, index),
            lat_sar_sat=radians(self.get_value(L1AVariables.lat_l1a_echo_sar_ku, index)),
            lon_sar_sat=radians(self.get_value(L1AVariables.lon_l1a_echo_sar_ku, index)),
            alt_sar_sat=self.get_value(L1AVariables.alt_l1a_echo_sar_ku, index),
            alt_rate_sat_sar=self.get_value(L1AVariables.orb_alt_rate_l1a_echo_sar_ku, index),
            x_vel_sat_sar=self.get_value(L1AVariables.x_vel_l1a_echo_sar_ku, index),
            y_vel_sat_sar=self.get_value(L1AVariables.y_vel_l1a_echo_sar_ku, index),
            z_vel_sat_sar=self.get_value(L1AVariables.z_vel_l1a_echo_sar_ku, index),
            roll_sar=radians(self.get_value(L1AVariables.roll_sral_mispointing_l1a_echo_sar_ku, index)),
            pitch_sar=radians(self.get_value(L1AVariables.pitch_sral_mispointing_l1a_echo_sar_ku, index)),
            yaw_sar=radians(self.get_value(L1AVariables.yaw_sral_mispointing_l1a_echo_sar_ku, index)),
            h0_sar=self.get_value(L1AVariables.h0_applied_l1a_echo_sar_ku, index),
            t0_sar=self.chd.t0_nom,  # * (1. + 2. * self.uso_cor_l1a_echo_sar_ku[index] / self.cst.c),
            uso_cor=self.get_value(L1AVariables.uso_cor_l1a_echo_sar_ku, index),
            cor2_sar=self.get_value(L1AVariables.cor2_applied_l1a_echo_sar_ku, index),
            win_delay_sar_ku=self.get_value(L1AVariables.range_ku_l1a_echo_sar_ku, index) * 2 / self.cst.c,
            x_sar_sat=self.get_value(L1AVariables.x_pos_l1a_echo_sar_ku, index),
            y_sar_sat=self.get_value(L1AVariables.y_pos_l1a_echo_sar_ku, index),
            z_sar_sat=self.get_value(L1AVariables.z_pos_l1a_echo_sar_ku, index),
            waveform_cor_sar=waveform,
            beams_focused=None,
            flag_time_status=self.get_value(L1AVariables.flag_time_status_l1a_echo_sar_ku, index),
            nav_bul_status=self.get_value(L1AVariables.nav_bul_status_l1a_echo_sar_ku, index),
            nav_bul_source=self.get_value(L1AVariables.nav_bul_source_l1a_echo_sar_ku, index),
            source_seq_count=self.get_value(L1AVariables.seq_count_l1a_echo_sar_ku, index),
            oper_instr=self.get_value(L1AVariables.oper_instr_l1a_echo_sar_ku, index),
            SAR_mode=self.get_value(L1AVariables.SAR_mode_l1a_echo_sar_ku, index),
            cl_gain=self.get_value(L1AVariables.cl_gain_l1a_echo_sar_ku, index),
            acq_stat=self.get_value(L1AVariables.acq_stat_l1a_echo_sar_ku, index),
            dem_eeprom=self.get_value(L1AVariables.dem_eeprom_l1a_echo_sar_ku, index),
            loss_track=self.get_value(L1AVariables.loss_track_l1a_echo_sar_ku, index),
            h0_nav_dem=self.get_value(L1AVariables.h0_nav_dem_l1a_echo_sar_ku, index),
            h0_applied=self.get_value(L1AVariables.h0_applied_l1a_echo_sar_ku, index),
            cor2_nav_dem=self.get_value(L1AVariables.cor2_nav_dem_l1a_echo_sar_ku, index),
            cor2_applied=self.get_value(L1AVariables.cor2_applied_l1a_echo_sar_ku, index),
            dh0=self.get_value(L1AVariables.dh0_l1a_echo_sar_ku, index),
            agccode_ku=self.get_value(L1AVariables.agccode_ku_l1a_echo_sar_ku, index),
            range_ku=self.get_value(L1AVariables.range_ku_l1a_echo_sar_ku, index),
            int_path_cor_ku=self.get_value(L1AVariables.int_path_cor_ku_l1a_echo_sar_ku, index),
            agc_ku=self.get_value(L1AVariables.agc_ku_l1a_echo_sar_ku, index),
            sig0_cal_ku=self.get_value(L1AVariables.sig0_cal_ku_l1a_echo_sar_ku, index),
            surf_type=self.get_value(L1AVariables.surf_type_l1a_echo_sar_ku, index)
        )
        packet.compute_location_sar_surf()
        packet.compute_doppler_angle()
        return packet

    def __iter__(self) -> Iterator[L1AProcessingData]:
        for index in range(self.max_index):
            packet = self[index]
            if self.in_range(packet):
                yield self[index]

    def __next__(self) -> L1AProcessingData:
        if self._last_index == self.max_index:
            return None
        while not self.in_range(self[self._last_index]):
            self._last_index += 1
            if self._last_index == self.max_index:
                return None
        packet = self[self._last_index]
        self._last_index += 1

        return packet

    def get_value(self, varname, index):
        return self._dset.get_value(varname, index)

    def __getattr__(self, variable_name: str) -> nc.Variable:
        """
        return the requested variable from the netCDF file
        """
        var = self._dset.variables[variable_name]
        var.set_auto_mask(False)
        return var
