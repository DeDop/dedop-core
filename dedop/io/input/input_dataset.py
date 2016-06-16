from ...conf import ConstantsFile, CharacterisationFile
from typing import Iterator
from .packet import InstrumentSourcePacket

class InputDataset:
    def __init__(self, dataset, cst: ConstantsFile, chd: CharacterisationFile):
        self._dset = dataset
        self.cst = cst
        self.chd = chd

    def close(self) -> None:
        self._dset.close()

    def __iter__(self) -> Iterator[InstrumentSourcePacket]:
        for packet in self._dset:
            yield packet

    def __getitem__(self, index: int) -> InstrumentSourcePacket:
        return self._dset[index]
