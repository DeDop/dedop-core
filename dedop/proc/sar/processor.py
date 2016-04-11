from .surface_location_data import SurfaceLocationData
from .algorithms import *

from ...util.parameter import Parameter


@Parameter("N_looks_stack")
class L1BProcessor:
    """
    class for the L1B Processing chain
    """

    def __init__(self, source):
        self.source = source
        self.surf_locs = []
        self.source_isps = []
        self.min_surfs = 8

        self.surface_locations_algorithm = SurfaceLocationAlgorithm()
        self.beam_angles_algorithm = BeamAnglesAlgorithm()
        self.azimuth_processing_algorithm = AzimuthProcessingAlgorithm()
        self.stacking_algorithm = StackingAlgorithm()
        self.geometry_corrections_algorithm = GeometryCorrectionsAlgorithm()
        self.range_compression_algorithm = RangeCompressionAlgorithm()
        self.stack_masking_algorithm = StackMaskingAlgorithm()

    def process(self):
        """
        runs the L1B Processing Chain
        """
        running = True
        surface_processing = False

        while running:
            isp = next(self.source)

            if isp is not None:
                #  pre. datation
                #  pre WD
                #  final burst dat.
                #  onboard rev.
                #  final WD
                #  Instr. Gain
                #  Wav. Correction

                new_surface = self.surface_locations(isp)

                if new_surface is None:
                    continue

            if surface_processing or len(self.surf_locs) >= self.min_surfs:
                surface_processing = True

                working_loc = self.surf_locs.pop(0)

                for processed_isp in self.source_isps:
                    if not processed_isp.burst_processed:

                        self.beam_angles(self.surf_locs, processed_isp, working_loc)

                        self.azimuth_processing(processed_isp)

                        processed_isp.burst_processed = True

                stack = self.stacking(working_loc)

                self.geometry_corrections(working_loc, stack)
                self.range_compression(working_loc)
                self.stack_masking(working_loc)

            if not self.surf_locs:
                running = False


    def surface_locations(self, isp):
        self.source_isps.append(isp)
        if self.surface_locations_algorithm(self.surf_locs, self.source_isps):
            loc = self.surface_locations_algorithm.get_surface()
            return self.new_surface(loc, first=self.surface_locations_algorithm.first_surf)
        return None

    def beam_angles(self, surfaces, isp, working_surface_location):
        self.beam_angles_algorithm(surfaces, isp, working_surface_location)

    def azimuth_processing(self, isp):
        self.azimuth_processing_algorithm(isp)

    def geometry_corrections(self, working_surface_location, stack):
        self.geometry_corrections_algorithm(working_surface_location, stack, self.N_looks_stack)

    def range_compression(self, working_surface_location):
        working_surface_location.beams_range_compr = self.range_compression_algorithm(working_surface_location)

    def stacking(self, working_surface_location):
        self.stacking_algorithm(working_surface_location)

    def stack_masking(self, working_surface_location):
        self.stack_masking_algorithm(working_surface_location)

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

