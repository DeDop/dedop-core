from .sar.l1b import L1BProcessor
from ..io.input.osv import OSVDataSet

def main(source):
    l1b = L1BProcessor(source, OSVDataSet(source))
    for s in l1b.surface_locations():
        print(s)