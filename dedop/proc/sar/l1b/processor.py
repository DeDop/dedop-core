from .surface_locations import SurfaceLocationAlgorithm
from .surface_location_data import SurfaceLocationData

class L1BProcessor:
    def __init__(self, source, osv):
        self.source = source
        self.osv = osv
        self.surf_locs = []
        self.source_isps = []

    def surface_locations(self):
        sla = SurfaceLocationAlgorithm()

        for isp in self.source:
            self.source_isps.append(isp)
            if sla.process_surface_location(
                    self.surf_locs, self.source_isps):
                loc = sla.get_surface()
                self.new_surface(loc, first=sla.first_surf)

    def new_surface(self, loc_data, first=False):
        if first:
            surf = self._first_surface(loc_data)
        else:
            surf = self._new_surface(loc_data)
        self.surf_locs.append(surf)
        return surf

    def _first_surface(self, loc_data):
        return SurfaceLocationData(loc_data, data=self.source_isps[-1])

    def _new_surface(self, loc_data):
        osv = self.osv.get_record(loc_data['time_surf'])
        return SurfaceLocationData(loc_data, data=osv)

