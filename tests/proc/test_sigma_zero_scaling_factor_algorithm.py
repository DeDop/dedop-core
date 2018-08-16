import unittest

import numpy as np

from dedop.conf import ConstantsFile, CharacterisationFile, ConfigurationFile
from dedop.model import SurfaceData
from dedop.model.l1a_processing_data import L1AProcessingData
from dedop.proc.sar.algorithms import Sigma0ScalingFactorAlgorithm
from tests.testing import TestDataLoader


@unittest.skip("need to update expected values for Sigma-0 tests")
class Sigma0ScalingFactorAlgorithmTests(unittest.TestCase):
    inputs_01 = 'test_data/proc/sigma0_scaling_factor_algorithm/' \
               'sigma0_scaling_factor_algorithm_01/input/inputs.txt'
    expected_01 = 'test_data/proc/sigma0_scaling_factor_algorithm/' \
                  'sigma0_scaling_factor_algorithm_01/expected/expected.txt'

    def initialise_algorithm(self, input_data):
        self.cnf = ConfigurationFile(
            zp_fact_range_cnf=input_data["zp_fact_range_cnf"]
        )
        self.cst = ConstantsFile(
            pi_cst=input_data['pi_cst'],
            earth_radius_cst=input_data['earth_radius_cst'],
            c_cst=input_data['c_cst']
        )
        self.chd = CharacterisationFile(
            self.cst,
            N_ku_pulses_burst_chd=input_data['n_ku_pulses_burst_chd'],
            N_samples_sar_chd=input_data['n_samples_sar_chd'],
            wv_length_ku_chd=input_data['wv_length_ku'],
            chirp_slope_ku_chd=input_data['chirp_slope_ku'],
            pulse_length_chd=input_data['pulse_length_chd'],
            power_tx_ant_ku_chd=input_data['power_tx_ant_ku_chd'],
            antenna_gain_ku_chd=input_data['antenna_gain_ku_chd']
        )
        self.sigma0_algorithm =\
            Sigma0ScalingFactorAlgorithm(self.chd, self.cst, self.cnf)

    def test_sigma0_algorithm_01(self):
        input_data = TestDataLoader(self.inputs_01, delim=' ')
        expected = TestDataLoader(self.expected_01, delim=' ')

        self.initialise_algorithm(input_data)

        data_stack_size = input_data['data_stack_size']

        isps = []

        x_vel = input_data['x_vel_sat_sar']
        y_vel = input_data['y_vel_sat_sar']
        z_vel = input_data['z_vel_sat_sar']
        pri_sar = input_data['pri_sar_pre_dat']

        for stack_index in range(data_stack_size):
            packet = L1AProcessingData(
                self.cst, self.chd,
                x_vel_sat_sar=x_vel[stack_index],
                y_vel_sat_sar=y_vel[stack_index],
                z_vel_sat_sar=z_vel[stack_index],
                pri_sar_pre_dat=pri_sar[stack_index]
            )
            isps.append(packet)

        working_loc = SurfaceData(
            self.cst, self.chd,
            data_stack_size=data_stack_size,
            range_sat_surf=input_data['range_sat_surf'],
            stack_bursts=np.asarray(isps)
        )
        sig0_scale_factor = self.sigma0_algorithm(
            working_loc,
            input_data['wv_length_ku'],
            input_data['chirp_slope_ku']
        )
        self.assertAlmostEqual(
            expected['sigma0_scaling_factor'], sig0_scale_factor,
        )