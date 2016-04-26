import numpy as np
from ..base_algorithm import BaseAlgorithm

class StackingAlgorithm(BaseAlgorithm):

    def __call__(self, working_surface_location):
        """
        Call the stacking algorithm

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
                look_angles_all_indices[stack_elements_to_remove:]
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

        # rmc_burst_in_stack = False

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

            self.stack_bursts[stack_index] = stack_burst
            self.beams_surf[stack_index, :] = beam_focused
            self.beam_angles_surf[stack_index] = beam_angle
            self.t0_surf[stack_index] = t0_beam
            self.doppler_angles_surf[stack_index] = doppler_angle_beam
            self.look_angles_surf[stack_index] = look_angle_beam
            self.pointing_angles_surf[stack_index] = pointing_angle_beam

            # TODO: implement this once surface types are done
            # if not rmc_burst_in_stack and stack_burst.isp_pid == IspPid.isp_echo_rmc:
            #     rmc_burst_in_stack = True