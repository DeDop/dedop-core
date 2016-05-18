from tests.testing import TestDataLoader
from dedop.proc.sar.algorithms import Sigma0ScalingFactorAlgorithm
from dedop.proc.sar.surface_location_data import SurfaceLocationData
from dedop.io.input.packet import InstrumentSourcePacket
from dedop.conf import ConstantsFile, CharacterisationFile

import unittest
import numpy as np

class Sigma0ScalingFactorAlgorithmTests(unittest.TestCase):
    cst_file = 'test_data/common/cst.json'
    chd_file = 'test_data/common/chd.json'

    inputs_01 = 'test_data/proc/sigma0_scaling_factor_algorithm/' \
               'sigma0_scaling_factor_algorithm_01/input/inputs.txt'
    expected_01 = 'test_data/proc/sigma0_scaling_factor_algorithm/' \
                  'sigma0_scaling_factor_algorithm_01/expected/expected.txt'

    def setUp(self):
        self.cst = ConstantsFile(self.cst_file)
        self.chd = CharacterisationFile(self.chd_file)
        self.sigma0_algorithm =\
            Sigma0ScalingFactorAlgorithm(self.chd, self.cst)

    def test_sigma0_algorithm_01(self):
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        data_stack_size = input_data['data_stack_size']

        isps = []

        x_vel = input_data['x_vel_sat_sar']
        y_vel = input_data['y_vel_sat_sar']
        z_vel = input_data['z_vel_sat_sar']
        pri_sar = input_data['pri_sar_pre_dat']

        for stack_index in range(data_stack_size):
            isp = InstrumentSourcePacket(
                self.cst, self.chd,
                x_vel_sat_sar=x_vel[stack_index],
                y_vel_sat_sar=y_vel[stack_index],
                z_vel_sat_sar=z_vel[stack_index],
                pri_sar_pre_dat=pri_sar[stack_index]
            )
            isps.append(isp)

        working_loc = SurfaceLocationData(
            self.cst, self.chd,
            data_stack_size=data_stack_size,
            range_sat_surf=input_data['range_sat_surf'],
            stack_bursts=np.asarray(isps)
        )
        self.sigma0_algorithm.zp_fact_range = input_data['zp_fact_range_cnf']
        sig0_scale_factor = self.sigma0_algorithm(
            working_loc,
            input_data['wv_length_ku'],
            input_data['chirp_slope_ku']
        )
        self.assertAlmostEqual(
            expected['sigma0_scaling_factor'], sig0_scale_factor,
        )