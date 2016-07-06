import numpy as np
from typing import Optional, Tuple

from dedop.model import SurfaceType, SurfaceData
from ..base_algorithm import BaseAlgorithm
from ....util.parameter import Parameter


@Parameter("rmc_margin", default_value=6)
@Parameter("flag_avoid_zeros_in_multilooking", default_value=0)
class StackMaskingAlgorithm(BaseAlgorithm):

    def __call__(self, working_surface_location: SurfaceData) -> None:
        rmc_mask = self.compute_rmc_mask(working_surface_location)
        geom_mask = self.compute_geometry_mask(working_surface_location)
        ambig_mask = self.compute_ambiguity_mask(working_surface_location)

        stack_mask, stack_mask_vector = self.combine_masks(
            geom_mask, ambig_mask, rmc_mask
        )
        self.beams_masked = self.apply_mask(working_surface_location, stack_mask)
        self.stack_mask_vector = stack_mask_vector

    def compute_rmc_mask(self, working_surface_location: SurfaceData) -> Optional[np.ndarray]:
        """
        Computes the RMC mask, if there is an RMC burst in the stack
        """
        sample_start_max = self.chd.n_samples_sar // 2 + 1
        if 1 <= self.chd.i_sample_start <= sample_start_max:
            i_sample_start = self.chd.i_sample_start - 1
        else:
            i_sample_start = 0


        if working_surface_location.surface_type == SurfaceType.surface_rmc:
            rmc_beam_mask = np.zeros(
                (self.chd.n_samples_sar * self.zp_fact_range), dtype=np.int8
            )

            start = i_sample_start * self.zp_fact_range
            end = (i_sample_start + self.chd.n_samples_sar // 2
                   - self.rmc_margin) * self.zp_fact_range
            rmc_beam_mask[int(start):int(end)] = 1

            return rmc_beam_mask
        return None


    def compute_geometry_mask(self, working_surface_location: SurfaceData) -> np.ndarray:
        geom_mask = np.zeros(
            (self.n_looks_stack, self.chd.n_samples_sar * self.zp_fact_range),
            dtype=np.int8
        )

        for beam_index in range(working_surface_location.data_stack_size):
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
        ambi_mask = np.zeros(
            (self.n_looks_stack, self.chd.n_samples_sar * self.zp_fact_range),
            dtype=np.int8
        )
        ## TODO: to be defined
        ambi_mask[:, :] = 1

        return ambi_mask

    def combine_masks(self, geom_mask: np.ndarray, ambig_mask: np.ndarray,
                      rmc_mask: Optional[np.ndarray]=None) -> Tuple[np.ndarray, np.ndarray]:
        stack_size, beam_size = geom_mask.shape
        stack_mask = np.zeros((stack_size, beam_size))
        stack_mask_vector = np.zeros((stack_size))

        for beam_index in range(stack_size):
            stack_mask[beam_index, :] = geom_mask[beam_index, :] * ambig_mask[beam_index, :]

            if rmc_mask is not None:
                stack_mask[beam_index, :] *= rmc_mask[:]

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

    def apply_mask(self, working_surface_location: SurfaceData, stack_mask: np.ndarray) -> np.ndarray:
        output = working_surface_location.beams_range_compr *\
                 stack_mask[:working_surface_location.data_stack_size, :]

        if self.flag_avoid_zeros_in_multilooking:
            invalid = np.flatnonzero(stack_mask == 0)
            output[invalid] = np.NaN

        return output
