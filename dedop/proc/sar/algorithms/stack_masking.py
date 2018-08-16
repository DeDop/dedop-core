import numpy as np
from typing import Tuple

from dedop.model import SurfaceData
from ..base_algorithm import BaseAlgorithm
from ....util.parameter import Parameter


@Parameter("flag_stack_masking", data_type=bool)
class StackMaskingAlgorithm(BaseAlgorithm):

    def __call__(self, working_surface_location: SurfaceData) -> None:
        """
        apply stack masking algorithm

        :param working_surface_location: current surface location
        :return:
        """

        if self.flag_stack_masking:
            geom_mask = self.compute_geometry_mask(working_surface_location)
            ambig_mask = self.compute_ambiguity_mask(working_surface_location)
            angle_mask = self.compute_angle_mask(working_surface_location)

            stack_mask, stack_mask_vector = self.combine_masks(
                geom_mask, ambig_mask, angle_mask
            )
            self.beams_masked = self.apply_mask(working_surface_location, stack_mask)
        else:
            stack_mask, stack_mask_vector = self.default_mask()
            self.beams_masked = working_surface_location.beams_range_compr

        self.stack_mask_vector = stack_mask_vector
        self.stack_mask = stack_mask

    def default_mask(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        returns an empty (all 1s) mask and corresponding mask vector
        """
        beam_size = self.chd.n_samples_sar * self.zp_fact_range
        mask = np.ones(
            (self.n_looks_stack, beam_size),
            dtype=np.float64
        )
        mask_vector = np.ones(
            (self.n_looks_stack,),
            dtype=np.float64
        ) * (beam_size - 1)

        return mask, mask_vector

    def compute_geometry_mask(self, working_surface_location: SurfaceData) -> np.ndarray:
        """
        create the geometry mask

        :param working_surface_location: current surface
        :return: geometry mask
        """
        geom_mask = np.zeros(
            (self.n_looks_stack, self.chd.n_samples_sar * self.zp_fact_range),
            dtype=np.float64
        )
        max_stack = min(working_surface_location.data_stack_size, self.n_looks_stack)
        for beam_index in range(max_stack):
            shift = working_surface_location.doppler_corrections[beam_index] +\
                    working_surface_location.slant_range_corrections[beam_index] +\
                    working_surface_location.win_delay_corrections[beam_index]

            shift_coarse = np.round(shift)

            if shift_coarse > 0:
                start = shift_coarse * self.zp_fact_range
                end = self.chd.n_samples_sar * self.zp_fact_range

            else:
                start = 0
                end = (self.chd.n_samples_sar - abs(shift_coarse)) * self.zp_fact_range
            if start < end:
                geom_mask[beam_index, int(start):int(end)] = 1

        return geom_mask

    def compute_ambiguity_mask(self, working_surface_location: SurfaceData) -> np.ndarray:
        """
        create the ambiguity mask (TODO: not yet implemented)

        :param working_surface_location: current surface
        :return: ambiguity mask
        """
        ambi_mask = np.zeros(
            (self.n_looks_stack, self.chd.n_samples_sar * self.zp_fact_range),
            dtype=np.float64
        )
        # TODO: to be defined
        ambi_mask[:, :] = 1

        return ambi_mask

    def compute_angle_mask(self, working_surface_location: SurfaceData) -> np.ndarray:
        """
        create the look angle mask
        """
        angle_mask = np.ones(
            (self.n_looks_stack, self.chd.n_samples_sar * self.zp_fact_range),
            dtype=np.float64
        )
        if self.chd.look_angle_mask_min is None or\
           self.chd.look_angle_mask_max is None:
            return angle_mask

        max_stack = min(working_surface_location.data_stack_size, self.n_looks_stack)
        for beam_index in range(max_stack):

            look_angle = working_surface_location.look_angles_surf[beam_index]
            angle_mask[beam_index, :] = (self.chd.look_angle_mask_min < look_angle < self.chd.look_angle_mask_max)

        return angle_mask

    @staticmethod
    def combine_masks(geom_mask: np.ndarray, ambig_mask: np.ndarray, angle_mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        stack_size, beam_size = geom_mask.shape
        stack_mask = np.zeros((stack_size, beam_size), dtype=np.float64)
        stack_mask_vector = np.zeros((stack_size,), dtype=np.float64)

        for beam_index in range(stack_size):
            stack_mask[beam_index, :] = geom_mask[beam_index, :] * ambig_mask[beam_index, :] *\
                                        angle_mask[beam_index, :]

            # now we must find the start position of any trailing
            # zeros in this row of the mask. This index will be
            # stored in the stack_mask_vector

            if stack_mask[beam_index, -1] == 1.:
                # check if the right-most value of the mask is a 1.
                # if so, then we don't need to search backwards, and
                # instead we store the largest index of the row.

                stack_mask_vector[beam_index] = beam_size - 1
            else:
                # if there's at least one trailing zero, we need
                # to search backwards until we find the first '1'.
                # This gives us the starting index of the trailing
                # zeros

                # get a reversed view of the row of the mask
                backwards = np.flipud(stack_mask[beam_index, :])
                # search forwards through the reversed view
                for i, value in enumerate(backwards):
                    # if we've found a one, then the store the previous
                    # index.
                    if value == 1.:
                        stack_mask_vector[beam_index] = beam_size - i
                        break

        return stack_mask, stack_mask_vector

    @staticmethod
    def apply_mask(working_surface_location: SurfaceData, stack_mask: np.ndarray) -> np.ndarray:
        output = working_surface_location.beams_range_compr *\
                 stack_mask[:working_surface_location.data_stack_size, :]

        return output
