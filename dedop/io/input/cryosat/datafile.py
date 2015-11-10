from .record import CryosatRecord
from .packet import CryosatPacket

import ctypes as ct
import array
from collections import namedtuple

DSD = namedtuple("DSD", "name type filename offset size num_dsr dsr_size")

class CryosatDatafile:
    def __init__(self, filename):
        self.filename = filename
        self._file = open(self.filename, 'rb')
        self.index = 0

        self.read_product_headers()

        self.item_size = ct.sizeof(CryosatRecord)
        self.data_offset = self.dsds[0].offset
        self.num_items = self.dsds[0].num_dsr

    def close(self):
        self._file.close()

    def read_product_headers(self):
        # read main product headers
        raw = array.array('B')
        raw.fromfile(self._file, 1247)

        self.product = "".join(chr(c) for c in raw[9:71])
        self.sph_size = int("".join(chr(c) for c in raw[1114:1124]))
        self.num_dsd = int("".join(chr(c) for c in raw[1141:1151]))
        # read specific product headers

        raw = array.array('B')
        raw.fromfile(self._file, self.sph_size)

        self.siral_id = chr(raw[725])
        index = 1112


        self.dsds = []
        for n in range(self.num_dsd):
            index += 9
            ds_name = "".join(
                chr(c) for c in raw[index:index+28]
            )
            index += 38
            ds_type = chr(raw[index])
            index += 12
            filename = "".join(
                chr(c) for c in raw[index:index+62]
            )
            index += 74
            ds_offset = int("".join(
                chr(c) for c in raw[index:index+21]
            ))
            index += 37
            ds_size = int("".join(
                chr(c) for c in raw[index:index+21]
            ))
            index += 37
            num_dsr = int("".join(
                chr(c) for c in raw[index:index+11]
            ))
            index += 21
            dsr_size = int("".join(
                chr(c) for c in raw[index:index+11]
            ))
            index += 52

            self.dsds.append(
                DSD(ds_name, ds_type, filename,
                    ds_offset, ds_size, num_dsr,
                    dsr_size)
            )

    def __getitem__(self, index):
        if not isinstance(index, slice):
            return self.get_packet(index)
        start, stop, stride = index.indices(self.num_items)
        return [self.get_packet(i)
                for i in range(start, stop, stride)]


    def get_record(self, index):
        if index >= self.num_items:
            return IndexError("index %d is too large" % index)
        if index < 0:
            return IndexError("Does not support negative indexing")

        self._file.seek(self.data_offset + index * self.item_size)
        raw = self._file.read(self.item_size)

        record = CryosatRecord()
        ct.memmove(ct.addressof(record), raw, self.item_size)
        return record

    def get_packet(self, index):
        i_record = int(index / 20)
        i_packet = index % 20

        record = self.get_record(i_record)
        return CryosatPacket(index, *record[i_packet])