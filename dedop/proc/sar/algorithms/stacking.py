import numpy as np
from ....conf import cst
from ..base_algorithm import BaseAlgorithm

class StackingAlgorithm(BaseAlgorithm):

    def __call__(self, working_surface_location):

        stack_all_size = len(working_surface_location.stack_all_bursts)

        if (stack_all_size <= self.n_looks_stack):
            data_stack_size = stack_all_size

            stack_elements_to_remove = 0
            stack_begin_offset = 0
        else:
            data_stack_size = self.n_looks_stack

            stack_elements_to_remove = stack_all_size - self.n_looks_stack

            look_angles_all = np.zeros((stack_all_size,))

            for stack_index in range(stack_all_size):
                stack_beam_index = working_surface_location.stack_all_beam_indicies[stack_index]

                stack_burst = working_surface_location.stack_all_bursts[stack_index]

                beam_angle = stack_burst.beam_angle_list[stack_beam_index]

                doppler_angle_beam = stack_burst.doppler_angle_sat_sar

                look_angle_beam = cst.pi / 2 + doppler_angle_beam - beam_angle

                look_angles_all[stack_index] = look_angle_beam

            look_angles_all_indicies = np.argsort(np.abs(look_angles_all))
            stack_begin_offset = look_angles_all_indicies[stack_elements_to_remove]

            self.stack_bursts = np.zeros((self.n_looks_stack,))
            self.beams_surf = np.zeros((self.n_looks_stack,))
            self.beam_angles_surf = np.zeros((self.n_looks_stack,))
            self.t0_surf = np.zeros((self.n_looks_stack,))
            self.doppler_angles_surf = np.zeros((self.n_looks_stack,))
            self.look_angles_surf = np.zeros((self.n_looks_stack,))
            self.pointing_angles_surf = np.zeros((self.n_looks_stack,))

            for stack_index in range(stack_all_size - stack_elements_to_remove):
                stack_beam_index =\
                    working_surface_location.stack_all_beam_indicies[
                        stack_index + stack_begin_offset
                    ]

                stack_burst =\
                    working_surface_location.stack_all_bursts[
                        stack_index + stack_begin_offset
                    ]

                beam_focused = stack_burst.beams_focused[stack_beam_index]
                beam_angle = stack_burst.beam_angle_list[stack_beam_index]
                t0_beam = stack_burst.t0_sar
                doppler_angle_beam = stack_burst.doppler_angle_sat_sar
                look_angle_beam = cst.pi / 2 + doppler_angle_beam - beam_angle
                pointing_angle_beam = look_angle_beam - stack_burst.pitch_sar

                self.stack_bursts[stack_index] = stack_burst
                self.beams_surf[stack_index] = beam_focused
                self.beam_angles_surf[stack_index] = beam_angle
                self.t0_surf[stack_index] = t0_beam
                self.doppler_angles_surf[stack_index] = doppler_angle_beam
                self.look_angles_surf[stack_index] = look_angle_beam
                self.pointing_angles_surf[stack_index] = pointing_angle_beam



