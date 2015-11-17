from .surface_locations import SurfaceLocationAlgorithm
from .surface_location_data import SurfaceLocationData
from .beam_angles import BeamAnglesAlgortihm


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
                yield self.new_surface(loc, first=sla.first_surf)

    def beam_angles(self):
        baa = BeamAnglesAlgortihm()

        for isp in self.source:
            baa.process_beam_angles(self.surf_locs, isp,
                                    self.surf_locs[-1].index)
            for i, surf_index in enumerate(baa.surfaces_seen):
                for surf in self.surf_locs:
                    if surf.index == surf_index:
                        surf.add_stack_burst(isp)
                        surf.add_stack_beam_index(i)


    def new_surface(self, loc_data, first=False):
        if first:
            surf = self._first_surface(loc_data)
        else:
            surf = self._new_surface(loc_data)
        self.surf_locs.append(surf)
        return surf

    def _first_surface(self, loc_data):
        return SurfaceLocationData(len(self.surf_locs), loc_data, data=self.source_isps[-1])

    def _new_surface(self, loc_data):
        print(loc_data)
        time = loc_data['time_surf']
        data = self.osv.get_interpolated(time)
        return SurfaceLocationData(len(self.surf_locs), loc_data, data)