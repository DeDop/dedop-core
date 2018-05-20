import numpy as np

from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile
from dedop.model import SurfaceType, SurfaceData
from dedop.model import PacketPid
from ..base_algorithm import BaseAlgorithm


class StackGatheringAlgorithm(BaseAlgorithm):

    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile, cnf: ConfigurationFile):
        super().__init__(chd, cst, cnf)

        self.data_stack_size = 0
        self.surface_type = SurfaceType.surface_null
        self.closest_burst_index = 0

        self.stack_bursts = None
        self.beams_surf = None
        self.beam_angles_surf = None
        self.t0_surf = None
        self.doppler_angles_surf = None
        self.look_angles_surf = None
        self.pointing_angles_surf = None
        self.look_index_surf = None
        self.look_counter_surf = None

    def __call__(self, working_surface_location: SurfaceData) -> None:
        """
        Call the stack_gathering algorithm

        :param working_surface_location: The current surface location
        """
        # get size of stack bursts
        stack_all_size = len(working_surface_location.stack_all_bursts)

        if stack_all_size < self.n_looks_stack:
            self.data_stack_size = stack_all_size

            stack_elements_to_remove = 0
            stack_begin_offset = 0

        else:
            self.data_stack_size = self.n_looks_stack

            # calc. number of elems to remove
            stack_elements_to_remove = stack_all_size - self.n_looks_stack

            # create empty look angles array
            look_angles_all = np.empty((stack_all_size,), dtype=np.float64)

            for stack_index in range(stack_all_size):

                stack_beam_index =\
                    working_surface_location.stack_all_beams_indices[stack_index]

                stack_burst =\
                    working_surface_location.stack_all_bursts[stack_index]

                beam_angle = stack_burst.beam_angles_list[stack_beam_index]
                doppler_angle_beam = stack_burst.doppler_angle_sar_sat
                look_angle_beam = self.cst.pi / 2. + doppler_angle_beam - beam_angle

                look_angles_all[stack_index] = look_angle_beam

            # create sorted indices array
            look_angles_all_indices = np.argsort(
                np.abs(look_angles_all)
            )
            stack_begin_offset = np.min(
                #look_angles_all_indices[stack_elements_to_remove:]
                look_angles_all_indices[:self.n_looks_stack]
            )

        self.stack_bursts = np.zeros(
            (self.n_looks_stack,), dtype=object
        )
        self.beams_surf = np.zeros(
            (self.n_looks_stack, self.chd.n_samples_sar), dtype=np.complex128
        )
        self.beam_angles_surf = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.t0_surf = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.doppler_angles_surf = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.look_angles_surf = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.pointing_angles_surf = np.zeros(
            (self.n_looks_stack,), dtype=np.float64
        )
        self.look_index_surf = -128 * np.ones(
            (self.n_looks_stack,), dtype=np.int32
        )
        self.look_counter_surf = np.zeros(
            (self.n_looks_stack,), dtype=np.int32
        )

        rmc_burst_in_stack = False
        closest_burst_beam_angle = None

        for stack_index in range(stack_all_size - stack_elements_to_remove):
            stack_beam_index =\
                working_surface_location.stack_all_beams_indices[stack_index + stack_begin_offset]

            stack_burst =\
                working_surface_location.stack_all_bursts[stack_index + stack_begin_offset]

            beam_focused = stack_burst.beams_focused[stack_beam_index, :]
            beam_angle = stack_burst.beam_angles_list[stack_beam_index]
            t0_beam = stack_burst.t0_sar
            doppler_angle_beam = stack_burst.doppler_angle_sar_sat
            look_angle_beam = self.cst.pi / 2. + doppler_angle_beam - beam_angle

            pointing_angle_beam = look_angle_beam - stack_burst.pitch_sar
            look_index_beam =\
                working_surface_location.stack_all_beams_indices_abs[stack_index + stack_begin_offset]
            look_counter_beam = stack_burst.seq_count_sar

            self.stack_bursts[stack_index] = stack_burst
            self.beams_surf[stack_index, :len(beam_focused)] = beam_focused
            self.beam_angles_surf[stack_index] = beam_angle
            self.t0_surf[stack_index] = t0_beam
            self.doppler_angles_surf[stack_index] = doppler_angle_beam
            self.look_angles_surf[stack_index] = look_angle_beam
            self.pointing_angles_surf[stack_index] = pointing_angle_beam
            self.look_index_surf[stack_index] = look_index_beam
            self.look_counter_surf[stack_index] = look_counter_beam

            if not rmc_burst_in_stack and stack_burst.isp_pid == PacketPid.echo_rmc:
                rmc_burst_in_stack = True

            burst_beam_angle = abs(beam_angle - self.cst.pi / 2.)
            if closest_burst_beam_angle is None or\
               burst_beam_angle < closest_burst_beam_angle:
                closest_burst_beam_angle = burst_beam_angle
                self.closest_burst_index = stack_index

        if rmc_burst_in_stack:
            self.surface_type = SurfaceType.surface_rmc
        else:
            self.surface_type = SurfaceType.surface_raw
