import unittest
import netCDF4 as nc

from dedop.data.output import L1BWriter
from dedop.conf import CharacterisationFile

from tests.testing import TestDataLoader

class L1BWriterTests(unittest.TestCase):
    _output_name = 'l1b.nc'

    chd_file = "test_data/common/CHD.json"
    expected_01 = "test_data/data/l1bs_output/" \
                  "l1bs_output_01/expected/expected.txt"

    def setUp(self):
        self.chd = CharacterisationFile(
            self.chd_file
        )

        self.writer = L1BWriter(self.chd, self._output_name)
        for dim in self.writer.create_all_dimensions():
            pass
        for var in self.writer.create_all_variables():
            pass


    def test_l1bs_output_01(self):
        expected = TestDataLoader(self.expected_01)

        self.writer.close()

        output = nc.Dataset(self._output_name)

        self.assertEqual(
            output.time_seconds.scale_factor,
            expected["time_seconds_scale_factor"]
        )

        self.assertEqual(
            output.latitude.scale_factor,
            expected["latitude_scale_factor"]
        )

        self.assertEqual(
            output.com_altitude.scale_factor,
            expected["com_altitude_scale_factor"]
        )
        self.assertEqual(
            output.com_altitude.add_offset,
            expected["com_altitude_offset"]
        )

        self.assertEqual(
            output.com_altitude_rate.scale_factor,
            expected["com_altitude_rate_scale_factor"]
        )

        self.assertEqual(
            output.com_velocity_vector.scale_factor,
            expected["com_velocity_vector_scale_factor"]
        )

        self.assertEqual(
            output.satellite_mispointing.scale_factor,
            expected["satellite_mispointing_scale_factor"]
        )

        self.assertEqual(
            output.mispointing_bias.scale_factor,
            expected["mispointing_bias_scale_factor"]
        )

        self.assertEqual(
            output.altimeter_range_calibrated.scale_factor,
            expected["altimeter_range_calibrated_scale_factor"]
        )
        self.assertEqual(
            output.altimeter_range_calibrated.add_offset,
            expected["altimeter_range_calibrated_offset"]
        )

        self.assertEqual(
            output.range_corr_internal_delay.scale_factor,
            expected["range_corr_internal_delay_scale_factor"]
        )

        self.assertEqual(
            output.range_corr_com.scale_factor,
            expected["range_corr_com_scale_factor"]
        )

        self.assertEqual(
            output.range_corr_doppler.scale_factor,
            expected["range_corr_doppler_scale_factor"]
        )

        self.assertEqual(
            output.attenuator_calibrated.scale_factor,
            expected["attenuator_calibrated_scale_factor"]
        )

        self.assertEqual(
            output.altimeter_power_drift.scale_factor,
            expected["altimeter_power_drift_scale_factor"]
        )

        self.assertEqual(
            output.power_corr_digital_processing.scale_factor,
            expected["power_corr_digital_processing_scale_factor"]
        )

        self.assertEqual(
            output.power_scaling_to_antenna.scale_factor,
            expected["power_scaling_to_antenna_scale_factor"]
        )

        self.assertEqual(
            output.altimeter_clock.scale_factor,
            expected["altimeter_clock_scale_factor"]
        )
        self.assertEqual(
            output.altimeter_clock.add_offset,
            expected["altimeter_clock_offset"]
        )

        self.assertEqual(
            output.pulse_repetition_interval.scale_factor,
            expected["pulse_repetition_interval_scale_factor"]
        )

        self.assertEqual(
            output.snr_estimation.scale_factor,
            expected["snr_estimation_scale_factor"]
        )

        self.assertEqual(
            output.sigma0_scaling_factor.scale_factor,
            expected["sigma0_scaling_factor_scale_factor"]
        )

    def test_l1bs_output_02(self):
        pass
