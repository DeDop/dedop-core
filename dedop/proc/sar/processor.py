from typing import Optional, Sequence, Dict, Any, List

from .algorithms import *
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile, WorkspaceConfig
from dedop.model import SurfaceData, L1AProcessingData
from dedop.data.input import InputDataset
from dedop.data.output import L1BSWriter, L1BWriter
from dedop.util.monitor import Monitor


class L1BProcessor:
    """
    class for the L1B Processing chain
    """
    _chd_file = "common/chd.json"
    _cst_file = "common/cst.json"

    @property
    def surf_locs(self) -> List[SurfaceData]:
        """
        the queue of currently working Surface Locations
        """
        return self._surfaces

    @property
    def source_isps(self) -> List[L1AProcessingData]:
        """
        the queue of processing L1A Packets
        """
        return self._packets

    def __init__(self, name: str, configuration: WorkspaceConfig):
        """
        initialise the processor
        """
        # store conf objects
        self.cst = ConstantsFile(configuration.cst_file)
        self.chd = CharacterisationFile(self.cst, configuration.chd_file)
        self.cnf = ConfigurationFile(configuration.cnf_file)

        # store file objects
        self.l1b_file = L1BWriter(filename=configuration.l1b_output, chd=self.chd, cnf=self.cnf)
        if configuration.l1bs_output is not None:
            self.l1bs_file = L1BSWriter(filename=configuration.l1bs_output, chd=self.chd)  # , cnf=self.cnf)
        else:
            self.l1bs_file = None
        # init. surface & packets arrays
        self._surfaces = []
        self._packets = []
        self.min_surfs = 64 + 16  # 16 elem. margin

        # set defaults for beam angles
        self.beam_angles_list_size_prev = -1
        self.beam_angles_trend_prev = -1

        # initialise the algorithm classes
        self.surface_locations_algorithm =\
            SurfaceLocationAlgorithm(self.chd, self.cst)
        self.beam_angles_algorithm =\
            BeamAnglesAlgorithm(self.chd, self.cst)
        self.azimuth_processing_algorithm =\
            AzimuthProcessingAlgorithm(self.chd, self.cst)
        self.stack_gathering_algorithm =\
            StackGatheringAlgorithm(self.chd, self.cst)
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

    def process(self, l1a_file: InputDataset, monitor: Monitor=None) -> None:
        """
        runs the L1B Processing Chain
        """
        self.l1a_file = l1a_file

        running = True
        surface_processing = False

        self.beam_angles_list_size_prev = -1
        self.beam_angles_trend_prev = -1

        while running:
            input_packet = next(self.l1a_file)

            if input_packet is not None:
                new_surface = self.surface_locations(input_packet)

                if new_surface is None:
                    continue

            if surface_processing or len(self.surf_locs) >= self.min_surfs:
                surface_processing = True

                working_loc = self.surf_locs[0]

                for processed_packet in self.source_isps:
                    if not processed_packet.burst_processed:

                        self.beam_angles(self.surf_locs, processed_packet, working_loc)

                        self.azimuth_processing(processed_packet)

                        processed_packet.burst_processed = True

                        if not self.beam_angles_algorithm.work_location_seen:
                            break

                stack = self.stack_gathering(working_loc)

                self.geometry_corrections(working_loc, stack)
                self.range_compression(working_loc)
                self.stack_masking(working_loc)
                self.multilooking(working_loc)
                self.sigma_zero_scaling(working_loc)

                if self.l1b_file is not None:
                    self.l1b_file.write_record(working_loc)
                if self.l1bs_file is not None:
                    self.l1bs_file.write_record(working_loc)

                self.clear_old_records(working_loc)


            if not self.surf_locs:
                running = False

    def clear_old_records(self, current_surface: SurfaceData) -> None:
        """
        removes outdated packets & surfaces from the buffers
        """
        while self.source_isps:
            if self.source_isps[0].counter == current_surface.stack_all_bursts[0].counter:
                break
            else:
                self.source_isps.pop(0)

        self.surf_locs.pop(0)

    def surface_locations(self, packet: L1AProcessingData) -> Optional[SurfaceData]:
        """
        call the surface locations algortihm and return the new location
        (if one is found)
        """
        self.source_isps.append(packet)

        if self.surface_locations_algorithm(self.surf_locs, self.source_isps):
            loc = self.surface_locations_algorithm.get_surface()
            return self.new_surface(loc)
        return None

    def beam_angles(self, surfaces: Sequence[SurfaceData], packet: L1AProcessingData,
                    working_surface_location: SurfaceData) -> None:
        """
        call the beam angles algorithm and store the results
        """
        self.beam_angles_algorithm(surfaces, packet, working_surface_location)

        packet.beam_angles_list = self.beam_angles_algorithm.beam_angles
        packet.surfaces_seen_list = self.beam_angles_algorithm.surfaces_seen

        packet.calculate_beam_angles_trend(
            self.beam_angles_list_size_prev,
            self.beam_angles_trend_prev
        )
        self.beam_angles_list_size_prev =\
            len(packet.beam_angles_list)
        self.beam_angles_trend_prev =\
            packet.beam_angles_trend

        last_index = 0

        for seen_surface_index, seen_surface_counter in enumerate(packet.surfaces_seen_list):
            for curr_surface in surfaces[last_index:]:
                last_index += 1

                if curr_surface.surface_counter == seen_surface_counter:

                    curr_surface.add_stack_beam_index(
                        seen_surface_index,
                        packet.beam_angles_trend,
                        len(packet.beam_angles_list)
                    )

                    curr_surface.add_stack_burst(packet)

                    break

    def azimuth_processing(self, packet: L1AProcessingData) -> None:
        """
        call the azimuth processing algorithm and store the results
        """
        self.azimuth_processing_algorithm(packet, self.chd.wv_length_ku)
        packet.beams_focused = self.azimuth_processing_algorithm.beams_focused

    def geometry_corrections(self, working_surface_location: SurfaceData, stack) -> None:
        """
        call the geometry correction algorithm and store the results
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

    def range_compression(self, working_surface_location: SurfaceData) -> None:
        """
        call the range compression algorithm and store the results
        """
        self.range_compression_algorithm(working_surface_location)

        working_surface_location.beams_range_compr =\
            self.range_compression_algorithm.beam_range_compr
        working_surface_location.beams_range_compr_iq =\
            self.range_compression_algorithm.beam_range_compr_iq

    def stack_gathering(self, working_surface_location: SurfaceData) -> None:
        """
        call the stack_gathering algorithm and store the results in the
        working surface location object
        """
        self.stack_gathering_algorithm(working_surface_location)

        working_surface_location.stack_bursts =\
            self.stack_gathering_algorithm.stack_bursts
        working_surface_location.beams_surf =\
            self.stack_gathering_algorithm.beams_surf
        working_surface_location.beam_angles_surf =\
            self.stack_gathering_algorithm.beam_angles_surf
        working_surface_location.t0_surf =\
            self.stack_gathering_algorithm.t0_surf
        working_surface_location.doppler_angles_surf =\
            self.stack_gathering_algorithm.doppler_angles_surf
        working_surface_location.look_angles_surf =\
            self.stack_gathering_algorithm.look_angles_surf
        working_surface_location.pointing_angles_surf =\
            self.stack_gathering_algorithm.pointing_angles_surf
        working_surface_location.look_index_surf =\
            self.stack_gathering_algorithm.look_index_surf
        working_surface_location.look_counter_surf =\
            self.stack_gathering_algorithm.look_counter_surf

        working_surface_location.closest_burst_index =\
            self.stack_gathering_algorithm.closest_burst_index

    def stack_masking(self, working_surface_location: SurfaceData) -> None:
        """
        call the stack masking algorithm and store the results
        """
        self.stack_masking_algorithm(working_surface_location)

        # store results in working surface location
        working_surface_location.beams_masked =\
            self.stack_masking_algorithm.beams_masked
        working_surface_location.stack_mask_vector =\
            self.stack_masking_algorithm.stack_mask_vector

    def multilooking(self, working_surface_location: SurfaceData) -> None:
        """
        call the multilooking algorithm and store the results in the
        surface location object
        """
        self.multilooking_algorithm(working_surface_location)

        working_surface_location.stack_std =\
            self.multilooking_algorithm.stack_std
        working_surface_location.stack_skewness =\
            self.multilooking_algorithm.stack_skewness
        working_surface_location.stack_kurtosis =\
            self.multilooking_algorithm.stack_kurtosis

        working_surface_location.waveform_multilooked =\
            self.multilooking_algorithm.waveform_multilooked

    def sigma_zero_scaling(self, working_surface_location: SurfaceData) -> None:
        """
        call the sigma0 scaling algorithm and store the results in the
        surface location object
        """
        self.sigma_zero_algorithm(
            working_surface_location, self.chd.wv_length_ku, self.chd.chirp_slope_ku
        )
        working_surface_location.sigma0_scaling_factor =\
            self.sigma_zero_algorithm.sigma0_scaling_factor

    def new_surface(self, loc_data: Dict[str, Any]) -> SurfaceData:
        """
        create a new surface location object from the provided data,
        and add it to the list of surface locations
        """
        if not self.surf_locs:
            index = 0
        else:
            index = self.surf_locs[-1].surface_counter + 1

        surf = SurfaceData(
            self.cst, self.chd, index, **loc_data
        )
        self.add_surface(surf)
        surf.compute_surf_sat_vector()
        surf.compute_angular_azimuth_beam_resolution(
            self.chd.pri_sar
        )
        return surf

    def add_surface(self, surface: SurfaceData) -> None:
        self.surf_locs.append(surface)
