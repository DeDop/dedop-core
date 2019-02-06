import datetime
import os
import time
from typing import Optional, Sequence, Dict, Any, List
from netCDF4 import getlibversion

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.conf.enums import OutputFormat
from dedop.data.input.l1a import L1ADataset
from dedop.data.output import L1BSWriter, L1BWriter, L1BWriterExtended
from dedop.model import SurfaceData, L1AProcessingData
from dedop.model.processor import BaseProcessor
from dedop.util.monitor import Monitor
from dedop.util.time import iso_format
from dedop.version import __version__

from .algorithms import *
from .cal import *


class L1BProcessor(BaseProcessor):
    """
    class for the L1B Processing chain
    """

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

    def __init__(self, name: str, cnf_file: str, cst_file: str, chd_file: str, out_path: str,
                 skip_l1bs: bool = True):
        """
        initialise the processor
        """

        if not name:
            raise ValueError('name must be given')
        if not cnf_file:
            raise ValueError('cnf_file must be given')
        if not cst_file:
            raise ValueError('cst_file must be given')
        if not chd_file:
            raise ValueError('chd_file must be given')
        if out_path is None:
            raise ValueError('out_path must be given')

        # store conf objects
        self.cst = ConstantsFile(cst_file)
        self.chd = CharacterisationFile(self.cst, chd_file)
        self.cnf = ConfigurationFile(cnf_file)

        self.skip_l1bs = skip_l1bs
        self.out_path = out_path
        self.name = name
        self.l1a_file = None

        # init. surface & packets arrays
        self._surfaces = []
        self._packets = []
        self.surfaces_count = 0
        self.min_surfs = 64 + 16  # 16 elem. margin

        # set defaults for beam angles
        self.beam_angles_list_size_prev = -1
        self.beam_angles_trend_prev = -1

        # initialise the algorithm classes
        self.surface_locations_algorithm = \
            SurfaceLocationAlgorithm(self.chd, self.cst, self.cnf)
        self.beam_angles_algorithm = \
            BeamAnglesAlgorithm(self.chd, self.cst, self.cnf)
        self.azimuth_processing_algorithm = \
            AzimuthProcessingAlgorithm(self.chd, self.cst, self.cnf)
        self.stack_gathering_algorithm = \
            StackGatheringAlgorithm(self.chd, self.cst, self.cnf)
        self.geometry_corrections_algorithm = \
            GeometryCorrectionsAlgorithm(self.chd, self.cst, self.cnf)
        self.range_compression_algorithm = \
            RangeCompressionAlgorithm(self.chd, self.cst, self.cnf)
        self.stack_masking_algorithm = \
            StackMaskingAlgorithm(self.chd, self.cst, self.cnf)
        self.multilooking_algorithm = \
            MultilookingAlgorithm(self.chd, self.cst, self.cnf)
        self.sigma_zero_algorithm = \
            Sigma0ScalingFactorAlgorithm(self.chd, self.cst, self.cnf)

        # init. the calibrations
        self.cal1_algorithm =\
            CAL1Algorithm(self.chd, self.cst, self.cnf)
        self.cal2_algorithm =\
            CAL2Algorithm(self.chd, self.cst, self.cnf)

        # set threshold for gaps
        self.gap_threshold = self.chd.bri_sar * 1.5

    def process(self, l1a_file: str, monitor: Monitor = Monitor.NULL) -> int:
        """
        runs the L1B Processing Chain
        """
        self.l1a_file = L1ADataset(l1a_file, chd=self.chd, cst=self.cst, cnf=self.cnf)

        print('processing %s using "%s"' % (self.l1a_file.file_path, self.name))

        t0 = time.time()

        with monitor.starting('processing', total_work=len(self.l1a_file)):
            status = self._process(l1a_file, monitor)

        dt = time.time() - t0

        print('produced %s' % self.l1b_file.file_path)
        if self.l1bs_file is not None:
            print('produced %s' % self.l1bs_file.file_path)

        print('processing took %s' % str(datetime.timedelta(seconds=dt)))

        return status

    def _process(self, l1a_file, monitor):
        running = True
        surface_processing = False
        status = -1
        self.beam_angles_list_size_prev = -1
        self.beam_angles_trend_prev = -1
        self.surfaces_count = 0

        # find base name of input file
        l1a_base, _ = os.path.splitext(os.path.basename(l1a_file))
        if l1a_base.startswith('L1A'):
            l1a_base = l1a_base[len('L1A'):]

        l1a_base_part = ''
        if l1a_base:
            l1a_base_part = '_%s' % l1a_base

        name_part = ''
        if self.name:
            name_part = '_%s' % self.name

        # create l1b-s output path
        l1bs_name = 'L1BS%s%s.nc' % (l1a_base_part, name_part)
        l1bs_path = os.path.join(self.out_path, l1bs_name)

        # create l1b output path
        l1b_name = 'L1B%s%s.nc' % (l1a_base_part, name_part)
        l1b_path = os.path.join(self.out_path, l1b_name)

        # create output file objects
        writerCls = L1BWriter if self.cnf.output_format == OutputFormat.s3 else L1BWriterExtended
        self.l1b_file = writerCls(filename=l1b_path, chd=self.chd, cnf=self.cnf, cst=self.cst)
        if not self.skip_l1bs:
            self.l1bs_file = L1BSWriter(filename=l1bs_path, chd=self.chd, cnf=self.cnf, cst=self.cst)
        else:
            self.l1bs_file = None

        # open output files
        self.l1b_file.open()
        if self.l1bs_file is not None:
            self.l1bs_file.open()

        prev_time = None
        gap_processing = False
        gap_resume = False
        sub_monitor = None
        any_surface = False

        index = -1

        while running:
            index += 1

            if monitor.is_cancelled():
                running = False

            # if a gap has been encountered, then the current lists of input packets & surfaces need to be processed
            #  before reading another input.
            if not gap_processing:

                # monitor.progress(1)

                # if this is the first iteration after finishing a gap, then the next packet has already been read
                #  so another one should not be retrieved from the L1A
                if not gap_resume:
                    # input_packet = next(self.l1a_file)
                    try:
                        input_packet = next(self.l1a_file)
                    except StopIteration:
                        input_packet = None
                        if not surface_processing:
                            break
                            # raise Exception("insufficient input records")
                    else:
                        monitor.progress(1)

                if input_packet is not None:
                    # apply calibrations
                    self.cal1_algorithm(input_packet)
                    self.cal2_algorithm(input_packet)

                    # check if there is a gap (or if this is the first packet & prev_time has not been set)
                    if prev_time is None or input_packet.time_sar_ku - prev_time < self.gap_threshold:

                        prev_time = input_packet.time_sar_ku
                        new_surface = self.surface_locations(input_packet, force_new=gap_resume)

                        gap_resume = False

                        if new_surface is None:
                            continue

                    else:
                        gap_processing = True
                        prev_time = None
                        sub_monitor = monitor.child(1)
                        sub_monitor.start("processing gap", len(self.surf_locs))

            elif sub_monitor is not None:
                sub_monitor.progress(1, len(self.surf_locs))

            if surface_processing or len(self.surf_locs) >= self.min_surfs or gap_processing:
                surface_processing = True

                working_loc = self.surf_locs[0]

                for processed_packet in self.source_isps:
                    if not processed_packet.burst_processed:

                        self.beam_angles(self.surf_locs, processed_packet, working_loc)

                        self.azimuth_processing(processed_packet)

                        processed_packet.burst_processed = True

                        if not self.beam_angles_algorithm.work_location_seen:
                            break

                self.stack_gathering(working_loc)

                # if the current surface doesn't have enough contributing bursts, then
                #  it should not be written to the outputs - and so the rest of the processing
                #  is not needed
                if working_loc.data_stack_size < (self.cnf.n_looks_stack // 2):
                    del self.surf_locs[0]  # remove this surface from the queue
                else:
                    self.geometry_corrections(working_loc)
                    self.range_compression(working_loc)
                    self.stack_masking(working_loc)
                    self.multilooking(working_loc)
                    self.sigma_zero_scaling(working_loc)

                    if self.l1b_file is not None:
                        self.l1b_file.write_record(working_loc)
                    if self.l1bs_file is not None:
                        self.l1bs_file.write_record(working_loc)

                    self.clear_old_records(working_loc)
                    any_surface = True

            if not self.surf_locs:
                if gap_processing:
                    # all the remaining surfaces & bursts before the gap have been processed
                    gap_processing = False  # end gap mode
                    gap_resume = True  # next iteration will be the first after the gap
                    surface_processing = False  # require min. number of surfaces again
                    sub_monitor.done()
                else:
                    # the end of the input has been reached
                    running = False
                    status = None

        l1a_globals = self.l1a_file.read_globals()

        ctime = iso_format()
        ftime = iso_format(self.l1a_file.first_time())
        ltime = iso_format(self.l1a_file.last_time())
        # close output files
        self.l1b_file.write_globals(
            title='DeDop SRAL Level 1 Measurement',
            mission_name=l1a_globals.mission_name,
            altimeter_sensor_name=l1a_globals.altimeter_sensor_name,
            gnss_sensor_name=l1a_globals.gnss_sensor_name,
            doris_sensor_name=l1a_globals.doris_sensor_name,
            references=l1a_globals.references,
            acq_station_name=l1a_globals.acq_station_name,
            xref_altimeter_level0=l1a_globals.xref_altimeter_level0,
            xref_navatt_level0=l1a_globals.xref_navatt_level0,
            xref_altimeter_orbit=l1a_globals.xref_altimeter_orbit,
            xref_doris_uso=l1a_globals.xref_doris_uso,
            xref_altimeter_ltm_lrm_cal1=l1a_globals.xref_altimeter_ltm_lrm_cal1,
            xref_altimeter_ltm_sar_cal1=l1a_globals.xref_altimeter_ltm_sar_cal1,
            xref_altimeter_ltm_ku_cal2=l1a_globals.xref_altimeter_ltm_ku_cal2,
            xref_altimeter_ltm_c_cal2=l1a_globals.xref_altimeter_ltm_c_cal2,
            xref_altimeter_characterisation=l1a_globals.xref_altimeter_characterisation,
            xref_time_correlation=l1a_globals.xref_time_correlation,
            semi_major_ellipsoid_axis=self.cst.semi_major_axis,
            ellipsoid_flattening=self.cst.flat_coeff,
            netcdf_version=getlibversion(),
            product_name=l1a_globals.get_l1b_product_name(),
            institution='isardSAT',
            source='DeDop {}'.format(__version__),
            history=l1a_globals.history,
            contact='http://www.dedop.org/',
            creation_time=ctime,
            first_meas_time=ftime,
            last_meas_time=ltime
        )
        self.l1b_file.close()
        if self.l1bs_file is not None:
            self.l1bs_file.write_globals(
                title='DeDop SRAL Level 1BS Measurement',
                mission_name=l1a_globals.mission_name,
                altimeter_sensor_name=l1a_globals.altimeter_sensor_name,
                gnss_sensor_name=l1a_globals.gnss_sensor_name,
                doris_sensor_name=l1a_globals.doris_sensor_name,
                references=l1a_globals.references,
                acq_station_name=l1a_globals.acq_station_name,
                xref_altimeter_level0=l1a_globals.xref_altimeter_level0,
                xref_navatt_level0=l1a_globals.xref_navatt_level0,
                xref_altimeter_orbit=l1a_globals.xref_altimeter_orbit,
                xref_doris_uso=l1a_globals.xref_doris_uso,
                xref_altimeter_ltm_lrm_cal1=l1a_globals.xref_altimeter_ltm_lrm_cal1,
                xref_altimeter_ltm_sar_cal1=l1a_globals.xref_altimeter_ltm_sar_cal1,
                xref_altimeter_ltm_ku_cal2=l1a_globals.xref_altimeter_ltm_ku_cal2,
                xref_altimeter_ltm_c_cal2=l1a_globals.xref_altimeter_ltm_c_cal2,
                xref_altimeter_characterisation=l1a_globals.xref_altimeter_characterisation,
                xref_platform=l1a_globals.xref_platform,
                xref_time_correlation=l1a_globals.xref_time_correlation,
                semi_major_ellipsoid_axis=self.cst.semi_major_axis,
                ellipsoid_flattening=self.cst.flat_coeff,
                netcdf_version=getlibversion(),
                product_name=l1a_globals.get_l1bs_product_name(),
                institution='isardSAT',
                source='DeDop {}'.format(__version__),
                history=l1a_globals.history,
                contact='http://www.dedop.org/',
                creation_time=ctime,
                first_meas_time=ftime,
                last_meas_time=ltime
            )
            self.l1bs_file.close()

        if not any_surface:
            raise Exception("insufficient input records to create output data")

        return status

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

    def surface_locations(self, packet: L1AProcessingData, force_new: bool=False) -> Optional[SurfaceData]:
        """
        call the surface locations algorithm and return the new location
        (if one is found)
        """
        self.source_isps.append(packet)

        if self.surface_locations_algorithm(self.surf_locs, self.source_isps, force_new=force_new):
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
        self.beam_angles_list_size_prev = \
            len(packet.beam_angles_list)
        self.beam_angles_trend_prev = \
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

    def geometry_corrections(self, working_surface_location: SurfaceData) -> None:
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

        working_surface_location.beams_range_compr = \
            self.range_compression_algorithm.beam_range_compr
        working_surface_location.beams_range_compr_iq = \
            self.range_compression_algorithm.beam_range_compr_iq

    def stack_gathering(self, working_surface_location: SurfaceData) -> None:
        """
        call the stack_gathering algorithm and store the results in the
        working surface location object
        """
        self.stack_gathering_algorithm(working_surface_location)

        working_surface_location.data_stack_size = \
            self.stack_gathering_algorithm.data_stack_size
        working_surface_location.stack_bursts = \
            self.stack_gathering_algorithm.stack_bursts
        working_surface_location.beams_surf = \
            self.stack_gathering_algorithm.beams_surf
        working_surface_location.beam_angles_surf = \
            self.stack_gathering_algorithm.beam_angles_surf
        working_surface_location.t0_surf = \
            self.stack_gathering_algorithm.t0_surf
        working_surface_location.doppler_angles_surf = \
            self.stack_gathering_algorithm.doppler_angles_surf
        working_surface_location.look_angles_surf = \
            self.stack_gathering_algorithm.look_angles_surf
        working_surface_location.pointing_angles_surf = \
            self.stack_gathering_algorithm.pointing_angles_surf
        working_surface_location.look_index_surf = \
            self.stack_gathering_algorithm.look_index_surf
        working_surface_location.look_counter_surf = \
            self.stack_gathering_algorithm.look_counter_surf

        working_surface_location.closest_burst_index = \
            self.stack_gathering_algorithm.closest_burst_index

    def stack_masking(self, working_surface_location: SurfaceData) -> None:
        """
        call the stack masking algorithm and store the results
        """
        self.stack_masking_algorithm(working_surface_location)

        # store results in working surface location
        working_surface_location.beams_masked = \
            self.stack_masking_algorithm.beams_masked
        working_surface_location.stack_mask_vector = \
            self.stack_masking_algorithm.stack_mask_vector
        working_surface_location.stack_mask =\
            self.stack_masking_algorithm.stack_mask

    def multilooking(self, working_surface_location: SurfaceData) -> None:
        """
        call the multilooking algorithm and store the results in the
        surface location object
        """
        self.multilooking_algorithm(working_surface_location)

        working_surface_location.stack_max = \
            self.multilooking_algorithm.stack_max
        working_surface_location.stack_std = \
            self.multilooking_algorithm.stack_std
        working_surface_location.stack_skewness = \
            self.multilooking_algorithm.stack_skewness
        working_surface_location.stack_kurtosis = \
            self.multilooking_algorithm.stack_kurtosis

        working_surface_location.n_beams_start_stop = \
            self.multilooking_algorithm.n_beams_start_stop
        working_surface_location.start_look_angle = \
            self.multilooking_algorithm.start_look_angle
        working_surface_location.stop_look_angle = \
            self.multilooking_algorithm.stop_look_angle
        working_surface_location.start_doppler_angle = \
            self.multilooking_algorithm.start_doppler_angle
        working_surface_location.stop_doppler_angle = \
            self.multilooking_algorithm.stop_doppler_angle
        working_surface_location.start_pointing_angle = \
            self.multilooking_algorithm.start_pointing_angle
        working_surface_location.stop_pointing_angle = \
            self.multilooking_algorithm.stop_pointing_angle
        working_surface_location.start_beam_angle = \
            self.multilooking_algorithm.start_beam_angle
        working_surface_location.stop_beam_angle = \
            self.multilooking_algorithm.stop_beam_angle
        working_surface_location.start_burst_index = \
            self.multilooking_algorithm.start_burst_index
        working_surface_location.stop_burst_index = \
            self.multilooking_algorithm.stop_burst_index

        working_surface_location.stack_mask_vector_start_stop = \
            self.multilooking_algorithm.stack_mask_vector_start_stop
        working_surface_location.beam_angles_start_stop = \
            self.multilooking_algorithm.beam_angles_start_stop
        working_surface_location.look_angles_start_stop = \
            self.multilooking_algorithm.look_angles_start_stop

        working_surface_location.waveform_multilooked = \
            self.multilooking_algorithm.waveform_multilooked

    def sigma_zero_scaling(self, working_surface_location: SurfaceData) -> None:
        """
        call the sigma0 scaling algorithm and store the results in the
        surface location object
        """
        working_surface_location.sigma0_scaling_factor = self.sigma_zero_algorithm(
            working_surface_location, self.chd.wv_length_ku, self.chd.chirp_slope_ku
        )
        working_surface_location.sigma0_scaling_factor_beam =\
            self.sigma_zero_algorithm.sigma0_scaling_factor_beam

    def new_surface(self, loc_data: Dict[str, Any]) -> SurfaceData:
        """
        create a new surface location object from the provided data,
        and add it to the list of surface locations
        """
        surf = SurfaceData(
            self.cst, self.chd, self.surfaces_count, **loc_data
        )
        self.surfaces_count += 1
        self.add_surface(surf)
        surf.compute_surf_sat_vector()
        surf.compute_angular_azimuth_beam_resolution(
            self.chd.pri_sar
        )
        return surf

    def add_surface(self, surface: SurfaceData) -> None:
        """
        add a surface to the list

        :param surface: the surface
        """
        self.surf_locs.append(surface)
