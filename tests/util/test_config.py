import os.path
from io import StringIO
from unittest import TestCase

from dedop.util.config import get_config_value, get_config_path, get_config, read_python_config


class PythonConfigTest(TestCase):
    def test_get_config_value(self):
        with self.assertRaises(ValueError) as e:
            get_config_value(None)
        self.assertEqual(str(e.exception), 'name must be given')

        with self.assertRaises(ValueError) as e:
            get_config_value('')
        self.assertEqual(str(e.exception), 'name must be given')

        value = get_config_value('_im_not_in_', 'Yes!')
        self.assertEqual(value, 'Yes!')

    def test_get_config_path(self):
        value = get_config_path('_im_not_in_', '~/dedop-workspaces')
        self.assertIsNotNone(value)
        self.assertTrue(value.endswith('dedop-workspaces'))
        self.assertNotIn('~', value)

    def test_get_config(self):
        config = get_config()
        self.assertIsNotNone(config)

    def test_read_python_config_file(self):
        config = read_python_config(StringIO("import os.path\n"
                                             "root_dir = os.path.join('user', 'home', 'norman')"))
        self.assertIn('root_dir', config)
        self.assertEqual(config['root_dir'], os.path.join('user', 'home', 'norman'))
