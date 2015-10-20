from unittest import TestCase
from  dedop.core.param import Parameter


class ParameterTest(TestCase):
    def test_that_ctor_checks_validity(self):
        with self.assertRaises(ValueError) as e:
            Parameter(None)
        self.assertEqual(str(e.exception), '"name" must not be None')

        with self.assertRaises(ValueError) as e:
            Parameter('a', None)
        self.assertEqual(str(e.exception), '"data_type" must not be None')

    def test_that_ctor_derives_data_type(self):
        self.assertEqual(Parameter('name', int).data_type, int)
        self.assertEqual(Parameter('name', default_value=0.5).data_type, float)
        self.assertEqual(Parameter('name', default_value='None').data_type, str)

    def test_that_name_and_data_type_are_read_only(self):
        with self.assertRaises(AttributeError) as e:
            Parameter('a', str).name = 'b'
        self.assertEqual(str(e.exception), 'can\'t set attribute')

        with self.assertRaises(AttributeError) as e:
            Parameter('a', str).data_type = float
        self.assertEqual(str(e.exception), 'can\'t set attribute')
