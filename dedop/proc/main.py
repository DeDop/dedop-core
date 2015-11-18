from .sar.l1b import L1BProcessor

def main(source):
    l1b = L1BProcessor(source)
    for s in l1b.surface_locations():
        print(s)