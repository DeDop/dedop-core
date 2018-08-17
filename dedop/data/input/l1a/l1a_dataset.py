from enum import Enum
from math import log10, radians
from typing import Iterator

import netCDF4 as nc
import numpy as np

from dedop.conf import ConfigurationFile, CharacterisationFile, ConstantsFile
from dedop.model.l1a_processing_data import L1AProcessingData, PacketPid
from ..input_dataset import InputDataset
from .enums import L1AVariables, L1ADimensions

from ..netcdf_reader import NetCDFReader

class L1AGlobals:
    __slots__ = [
        "mission_name",
        "altimeter_sensor_name",
        "gnss_sensor_name",
        "doris_sensor_name",
        "references",
        "acq_station_name",
        "xref_altimeter_level0",
        "xref_navatt_level0",
        "xref_altimeter_orbit",
        "xref_doris_uso",
        "xref_altimeter_ltm_lrm_cal1",
        "xref_altimeter_ltm_sar_cal1",
        "xref_altimeter_ltm_ku_cal2",
        "xref_altimeter_ltm_c_cal2",
        "xref_altimeter_characterisation",
        "xref_time_correlation",
        "xref_platform",
        "history",
        "product_name"
    ]

    def __init__(self, **attrs):
        self.mission_name =\
            attrs.get('mission_name')
        self.altimeter_sensor_name =\
            attrs.get('altimeter_sensor_name')
        self.gnss_sensor_name =\
            attrs.get('gnss_sensor_name')
        self.doris_sensor_name =\
            attrs.get('doris_sensor_name')
        self.references =\
            attrs.get('references')
        self.acq_station_name =\
            attrs.get('acq_station_name')
        self.xref_altimeter_level0 =\
            attrs.get('xref_altimeter_level0')
        self.xref_navatt_level0 =\
            attrs.get('xref_navatt_level0')
        self.xref_altimeter_orbit =\
            attrs.get('xref_altimeter_orbit')
        self.xref_doris_uso =\
            attrs.get('xref_doris_uso')
        self.xref_altimeter_ltm_lrm_cal1 =\
            attrs.get('xref_altimeter_ltm_lrm_cal1')
        self.xref_altimeter_ltm_sar_cal1 =\
            attrs.get('xref_altimeter_ltm_sar_cal1')
        self.xref_altimeter_ltm_ku_cal2 =\
            attrs.get('xref_altimeter_ltm_ku_cal2')
        self.xref_altimeter_ltm_c_cal2 =\
            attrs.get('xref_altimeter_ltm_c_cal2')
        self.xref_altimeter_characterisation =\
            attrs.get('xref_altimeter_characterisation')
        self.xref_time_correlation =\
            attrs.get('xref_time_correlation')
        self.xref_platform =\
            attrs.get('xref_platform')
        self.history =\
            attrs.get('history')
        self.product_name =\
            attrs.get('product_name')

    def get_l1b_product_name(self):
        return self.product_name.replace('_A__', '____')

    def get_l1bs_product_name(self):
        return self.product_name.replace('_A__', '_BS_')


class L1ADataset(InputDataset):
    def __init__(self, filename: str, cst: ConstantsFile, chd: CharacterisationFile, cnf: ConfigurationFile):
        """
        The L1ADataset class reads L1A NetCDF data files.
        """
        dset = NetCDFReader(filename)
        super().__init__(dset, cst=cst, chd=chd, cnf=cnf)

        self._file_path = filename

        if self._roi_enabled():
            lats = dset.get_variable(L1AVariables.lat_l1a_echo_sar_ku)[:]
            lons = dset.get_variable(L1AVariables.lon_l1a_echo_sar_ku)[:]

            roi_filter = np.ones(lats.shape, dtype=bool)
            if self.cnf.min_lat is not None:
                roi_filter = np.logical_and(
                    roi_filter, lats >= self.cnf.min_lat
                )
            if self.cnf.min_lon is not None:
                roi_filter = np.logical_and(
                    roi_filter, lons >= self.cnf.min_lon
                )
            if self.cnf.max_lat is not None:
                roi_filter = np.logical_and(
                    roi_filter, lats <= self.cnf.max_lat
                )
            if self.cnf.max_lon is not None:
                roi_filter = np.logical_and(
                    roi_filter, lons <= self.cnf.max_lon
                )
            self._roi_filter = roi_filter
            indexes = np.argwhere(roi_filter)
            self._start_index = indexes.min()
            self._final_index = indexes.max()
        else:
            self._roi_filter = None
            self._start_index = 0
            self._final_index = self._get_data_size()

        self._last_index = self._start_index

    def _roi_enabled(self) -> bool:
        return self.cnf.min_lat is not None or\
               self.cnf.min_lon is not None or\
               self.cnf.max_lat is not None or\
               self.cnf.max_lon is not None

    def _check_roi(self, index) -> bool:
        if self._roi_filter is None:
            return True
        return self._roi_filter[index]

    def _get_data_size(self) -> int:
        dim = self._dset.dimensions[
            L1ADimensions.time_l1a_echo_sar_ku.value
        ]
        return dim.size

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def max_index(self) -> int:
        """get size of primary dimension"""
        return self._final_index - self._start_index

    def first_time(self) -> float:
        return self.get_value(L1AVariables.time_l1a_echo_sar_ku, self._start_index)

    def last_time(self) -> float:
        return self.get_value(L1AVariables.time_l1a_echo_sar_ku, self._final_index-1)

    def __len__(self):
        return self._final_index - self._start_index

    def __getitem__(self, index: int) -> L1AProcessingData:
        # convert scale factor to linear value
        agc = self.get_value(L1AVariables.agc_ku_l1a_echo_sar_ku, index)
        scale_factor = pow(10., -agc / 20.)
        # construct waveform
        waveform = (self.get_value(L1AVariables.i_meas_ku_l1a_echo_sar_ku, index) +
                    1j * self.get_value(L1AVariables.q_meas_ku_l1a_echo_sar_ku, index)) / scale_factor
        zcog = np.cos(self.get_value(L1AVariables.pitch_sat_pointing_l1a_echo_sar_ku, index)) *\
               self.get_value(L1AVariables.cog_cor_l1a_echo_sar_ku, index)
        range = self.get_value(L1AVariables.range_ku_l1a_echo_sar_ku, index) + zcog

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
            roll_sral_mispointing=self.get_value(L1AVariables.roll_sral_mispointing_l1a_echo_sar_ku, index),
            pitch_sral_mispointing=self.get_value(L1AVariables.pitch_sral_mispointing_l1a_echo_sar_ku, index),
            yaw_sral_mispointing=self.get_value(L1AVariables.yaw_sral_mispointing_l1a_echo_sar_ku, index),
            cog_cor=self.get_value(L1AVariables.cog_cor_l1a_echo_sar_ku, index),
            h0_sar=self.get_value(L1AVariables.h0_applied_l1a_echo_sar_ku, index),
            t0_sar=self.chd.t0_nom,  # * (1. + 2. * self.uso_cor_l1a_echo_sar_ku[index] / self.cst.c),
            uso_cor=self.get_value(L1AVariables.uso_cor_l1a_echo_sar_ku, index),
            cor2_sar=self.get_value(L1AVariables.cor2_applied_l1a_echo_sar_ku, index),
            win_delay_sar_ku=range * 2 / self.cst.c,
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
            surf_type=self.get_value(L1AVariables.surf_type_l1a_echo_sar_ku, index),
            # CAL 1 & CAL 2
            cal1_power=self.get_value(L1AVariables.burst_power_cor_ku_l1a_echo_sar_ku, index),
            cal1_phase=self.get_value(L1AVariables.burst_phase_cor_ku_l1a_echo_sar_ku, index),
            cal2_array=self.get_value(L1AVariables.gprw_meas_ku_l1a_echo_sar_ku, index)[self.cnf.flag_cal2_table_index, :]
        )

        packet.compute_location_sar_surf()
        packet.compute_doppler_angle()
        return packet

    def __iter__(self) -> Iterator[L1AProcessingData]:
        for index in range(self._start_index, self._final_index):
            if self._check_roi(index) and self.is_valid(self[index]):
                yield self[index]
            else:
                yield None

    def __next__(self) -> L1AProcessingData:
        if self._last_index >= self._final_index:
            raise StopIteration()
        # while not self.in_range(self[self._last_index]):
        #     self._last_index += 1
        #     if self._last_index == self.max_index:
        #         return None
        if not self._check_roi(self._last_index):
            self._last_index += 1
            return None
        packet = self[self._last_index]
        self._last_index += 1

        if not self.is_valid(packet):
            return None
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

    def read_globals(self) -> L1AGlobals:
        return L1AGlobals(**self._dset.read_globals())
