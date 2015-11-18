from .surface_locations import SurfaceLocationAlgorithm
from .surface_location_data import SurfaceLocationData

class L1BProcessor:
    def __init__(self, source):
        self.source = source
        self.surf_locs = []
        self.source_isps = []

    def surface_locations(self):
        sla = SurfaceLocationAlgorithm()

        for isp in self.source:
            self.source_isps.append(isp)
            if sla.process_surface_location(
                    self.surf_locs, self.source_isps):
                loc = sla.get_surface()
                yield self.new_surface(loc, first=sla.first_surf)


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
        time = loc_data['time_surf']
        data = self.source.get_interpolated(time)
        return SurfaceLocationData(loc_data, data)

