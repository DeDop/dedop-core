from unittest import TestCase
from dedop.util.parameter import Parameter


class ParamFree:
    pass


@Parameter('lower', 0.0)
@Parameter('upper', 1.0)
class Range:
    pass


@Parameter('threshold', 0.0)
class Extension:
    pass


@Parameter('method', 'M1', value_set=['M1', 'M2'])
@Parameter('range', data_type=Range)
class Extension2(Extension):
    pass


class ParameterTest(TestCase):
    def test_that_ctor_checks_validity(self):
        with self.assertRaises(ValueError) as e:
            Parameter(None)
        self.assertEqual(str(e.exception), 'name must not be None or empty')

        with self.assertRaises(ValueError) as e:
            Parameter('')
        self.assertEqual(str(e.exception), 'name must not be None or empty')

        with self.assertRaises(ValueError) as e:
            Parameter('a', None)
        self.assertEqual(str(e.exception), 'data_type must not be None')

    def test_that_ctor_derives_data_type(self):
        self.assertEqual(Parameter('name', 42).data_type, int)
        self.assertEqual(Parameter('name', 0.5).data_type, float)
        self.assertEqual(Parameter('name', 'None').data_type, str)

    def test_that_name_and_data_type_are_read_only(self):
        with self.assertRaises(AttributeError) as e:
            Parameter('a', str).name = 'b'
        self.assertEqual(str(e.exception), 'can\'t set attribute')

        with self.assertRaises(AttributeError) as e:
            Parameter('a', str).data_type = float
        self.assertEqual(str(e.exception), 'can\'t set attribute')

    def test_get_parameter(self):
        parameter = Parameter.get_parameter(Extension, 'threshold')
        self.assertIsNotNone(parameter)
        self.assertEqual('threshold', parameter.name)
        parameter = Parameter.get_parameter(Extension, 'range')
        self.assertIsNone(parameter)
        parameter = Parameter.get_parameter(Extension2, 'range')
        self.assertIsNotNone(parameter)
        self.assertEqual('range', parameter.name)

    def test_get_parameters(self):
        parameters = Parameter.get_parameters(ParamFree)
        self.assertIsNotNone(parameters)
        self.assertEqual(set(), set(parameters))
        parameters = Parameter.get_parameters(Range)
        self.assertIsNotNone(parameters)
        self.assertEqual({'lower', 'upper'}, set(parameters))
        parameters = Parameter.get_parameters(Extension)
        self.assertIsNotNone(parameters)
        self.assertEqual({'threshold'}, set(parameters))
        parameters = Parameter.get_parameters(Extension2)
        self.assertIsNotNone(parameters)
        self.assertEqual({'threshold', 'method', 'range'}, set(parameters))
