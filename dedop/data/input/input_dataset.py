from typing import Iterator

from dedop.model.l1a_processing_data import L1AProcessingData
from ...conf import ConstantsFile, CharacterisationFile, ConfigurationFile

from math import radians

class InputDataset:
    def __init__(self, dataset, cst: ConstantsFile, chd: CharacterisationFile, cnf: ConfigurationFile):
        self._dset = dataset
        self.cst = cst
        self.chd = chd
        self.cnf = cnf

    def close(self) -> None:
        self._dset.close()

    def in_range(self, packet: L1AProcessingData) -> bool:
        """checks if the location of the packet is
            within the range defined by the min & max
            longitudes & latitudes defined in the CNF"""
        lat = packet.lat_sar_sat
        lon = packet.lon_sar_sat

        if self.cnf.min_lat is not None and lat < radians(self.cnf.min_lat):
            return False
        if self.cnf.max_lat is not None and lat > radians(self.cnf.max_lat):
            return False
        if self.cnf.min_lon is not None and lon < radians(self.cnf.min_lon):
            return False
        if self.cnf.max_lon is not None and lon > radians(self.cnf.max_lon):
            return False

        return True

    def __iter__(self) -> Iterator[L1AProcessingData]:
        for packet in self._dset:
            if not self.in_range(packet):
                continue
            yield packet

    def __getitem__(self, index: int) -> L1AProcessingData:
        return self._dset[index]
