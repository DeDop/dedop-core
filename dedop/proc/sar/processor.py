from .surface_location_data import SurfaceLocationData
from .algorithms import *


class L1BProcessor:
    """
    class for the L1B Processing chain
    """
    _chd_file = "common/chd.json"
    _cst_file = "common/cst.json"

    def __init__(self, source, chd_file, cst_file, l1b_output, l1bs_output=None):
        """

        :param source:
        :param chd_file:
        :param cst_file:
        :param l1b_output:
        :param l1bs_output:
        """
        self.cst = cst_file
        self.chd = chd_file

        self.source = source
        self.l1b_file = l1b_output
        self.l1bs_file = l1bs_output
        self.surf_locs = []
        self.source_isps = []
        self.min_surfs = 64 + 16 # 16 elem. margin

        self.surface_locations_algorithm =\
            SurfaceLocationAlgorithm(self.chd, self.cst)
        self.beam_angles_algorithm =\
            BeamAnglesAlgorithm(self.chd, self.cst)
        self.azimuth_processing_algorithm =\
            AzimuthProcessingAlgorithm(self.chd, self.cst)
        self.stacking_algorithm =\
            StackingAlgorithm(self.chd, self.cst)
        self.geometry_corrections_algorithm =\
            GeometryCorrectionsAlgorithm(self.chd, self.cst)
        self.range_compression_algorithm =\
            RangeCompressionAlgorithm(self.chd, self.cst)
        self.stack_masking_algorithm =\
            StackMaskingAlgorithm(self.chd, self.cst)
        self.multilooking_algorithm =\
            MultilookingAlgorithm(self.chd, self.cst)
        self.sigma_zero_algorithm =\
            Sigma0ScalingFactorAlgorithm(self.chd, self.cst)

    def process(self):
        """
        runs the L1B Processing Chain
        """
        running = True
        surface_processing = False

        self.beam_angles_list_size_prev = -1
        self.beam_angles_trend_prev = -1

        while running:
            isp = next(self.source)

            if isp is not None:
                new_surface = self.surface_locations(isp)

                if new_surface is None:
                    continue

            if surface_processing or len(self.surf_locs) >= self.min_surfs:
                surface_processing = True

                working_loc = self.surf_locs[0]

                for processed_isp in self.source_isps:
                    if not processed_isp.burst_processed:

                        self.beam_angles(self.surf_locs, processed_isp, working_loc)

                        self.azimuth_processing(processed_isp)

                        processed_isp.burst_processed = True

                        if not self.beam_angles_algorithm.work_location_seen:
                            break

                stack = self.stacking(working_loc)

                self.geometry_corrections(working_loc, stack)
                self.range_compression(working_loc)
                self.stack_masking(working_loc)
                self.multilooking(working_loc)
                self.sigma_zero_scaling(working_loc)

                if self.l1b_file is not None:
                    self.l1b_file.write_record(working_loc)
                if self.l1bs_file is not None:
                    self.l1bs_file.write_record(working_loc)

                # TODO: remove old ISP processed - add counter and remove items prior to first in working surface

                while self.source_isps:
                    if self.source_isps[0].counter == working_loc.stack_all_bursts[0].counter:
                        break
                    else:
                        self.source_isps.pop(0)

                self.surf_locs.pop(0)

            if not self.surf_locs:
                running = False


    def surface_locations(self, isp):
        """
        call the surface locations algortihm and return the new location
        (if one is found)

        :param isp:
        :return:
        """
        self.source_isps.append(isp)

        if self.surface_locations_algorithm(self.surf_locs, self.source_isps):
            loc = self.surface_locations_algorithm.get_surface()
            return self.new_surface(loc)
        return None

    def beam_angles(self, surfaces, isp, working_surface_location):
        """
        call the beam angles algorithm and store the results

        :param surfaces:
        :param isp:
        :param working_surface_location:
        :return:
        """
        self.beam_angles_algorithm(surfaces, isp, working_surface_location)

        isp.beam_angles_list = self.beam_angles_algorithm.beam_angles
        isp.surfaces_seen_list = self.beam_angles_algorithm.surfaces_seen

        isp.calculate_beam_angles_trend(
            self.beam_angles_list_size_prev,
            self.beam_angles_trend_prev
        )
        self.beam_angles_list_size_prev =\
            len(isp.beam_angles_list)
        self.beam_angles_trend_prev =\
            isp.beam_angles_trend

        last_index = 0

        for seen_surface_index, seen_surface_counter in enumerate(isp.surfaces_seen_list):
            for curr_surface in surfaces[last_index:]:
                last_index += 1

                if curr_surface.surface_counter == seen_surface_counter:

                    curr_surface.add_stack_beam_index(
                        seen_surface_index,
                        isp.beam_angles_trend,
                        len(isp.beam_angles_list)
                    )

                    curr_surface.add_stack_burst(isp)

                    break

    def azimuth_processing(self, isp):
        """
        call the azimuth processing algorithm and store the results

        :param isp:
        :return:
        """
        self.azimuth_processing_algorithm(isp, self.chd.wv_length_ku)
        isp.beams_focused = self.azimuth_processing_algorithm.beams_focused

    def geometry_corrections(self, working_surface_location, stack):
        """
        call the geometry correction algorithm and store the results

        :param working_surface_location:
        :param stack:
        :return:
        """
        self.geometry_corrections_algorithm(working_surface_location, self.chd.wv_length_ku)

        working_surface_location.slant_range_corrections = \
            self.geometry_corrections_algorithm.slant_range_corrections
        working_surface_location.range_sat_surf = \
            self.geometry_corrections_algorithm.range_sat_surf
        working_surface_location.doppler_corrections = \
            self.geometry_corrections_algorithm.doppler_corrections
        working_surface_location.win_delay_corrections = \
            self.geometry_corrections_algorithm.win_delay_corrections
        working_surface_location.beams_geo_corr = \
            self.geometry_corrections_algorithm.beams_geo_corr

    def range_compression(self, working_surface_location):
        """
        call the range compression algorithm and store the results

        :param working_surface_location:
        :return:
        """
        self.range_compression_algorithm(working_surface_location)

        working_surface_location.beams_range_compr =\
            self.range_compression_algorithm.beam_range_compr
        working_surface_location.beams_range_compr_iq =\
            self.range_compression_algorithm.beam_range_compr_iq

    def stacking(self, working_surface_location):
        """
        call the stacking algorithm and store the results in the
        working surface location object

        :param working_surface_location:
        :return:
        """
        self.stacking_algorithm(working_surface_location)

        working_surface_location.stack_bursts =\
            self.stacking_algorithm.stack_bursts
        working_surface_location.beams_surf =\
            self.stacking_algorithm.beams_surf
        working_surface_location.beam_angles_surf =\
            self.stacking_algorithm.beam_angles_surf
        working_surface_location.t0_surf =\
            self.stacking_algorithm.t0_surf
        working_surface_location.doppler_angles_surf =\
            self.stacking_algorithm.doppler_angles_surf
        working_surface_location.look_angles_surf =\
            self.stacking_algorithm.look_angles_surf
        working_surface_location.pointing_angles_surf =\
            self.stacking_algorithm.pointing_angles_surf
        working_surface_location.look_index_surf =\
            self.stacking_algorithm.look_index_surf
        working_surface_location.look_counter_surf =\
            self.stacking_algorithm.look_counter_surf

    def stack_masking(self, working_surface_location):
        """
        call the stack masking algorithm and store the results

        :param working_surface_location:
        :return:
        """
        self.stack_masking_algorithm(working_surface_location)

        # store results in working surface location
        working_surface_location.beams_masked =\
            self.stack_masking_algorithm.beams_masked
        working_surface_location.stack_mask_vector =\
            self.stack_masking_algorithm.stack_mask_vector

    def multilooking(self, working_surface_location):
        """
        call the multilooking algorithm and store the results in the
        surface location object

        :param working_surface_location:
        :return:
        """
        # TODO: store results
        self.multilooking_algorithm(working_surface_location)

    def sigma_zero_scaling(self, working_surface_location):
        """
        call the sigma0 scaling algorithm and store the results in the
        surface location object

        :param working_surface_location:
        :return:
        """
        # TODO: store results
        self.sigma_zero_algorithm(
            working_surface_location, self.chd.wv_length_ku, self.chd.chirp_slope_ku
        )

    def new_surface(self, loc_data):
        """
        create a new surface location object from the provided data,
        and add it to the list of surface locations

        :param loc_data:
        :return:
        """
        if not self.surf_locs:
            index = 0
        else:
            index = self.surf_locs[-1].surface_counter + 1

        surf = SurfaceLocationData(
            self.cst, self.chd, index, **loc_data
        )
        self.surf_locs.append(surf)
        surf.compute_surf_sat_vector()
        surf.compute_angular_azimuth_beam_resolution(
            self.chd.pri_sar
        )
        return surf
