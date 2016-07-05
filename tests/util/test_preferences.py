from unittest import TestCase

from dedop.util.preferences import Preferences

TEST_PREFS = '_test.prefs'


class PreferencesTest(TestCase):
    def setUp(self):
        import os
        if os.path.exists(TEST_PREFS):
            os.remove(TEST_PREFS)

    def test_get_and_set(self):
        preferences = Preferences('_test', dir_path='.')

        self.assertEqual(None, preferences.get('x', None))
        self.assertEqual('Ok', preferences.get('x', 'Ok'))

        preferences.set('x', 7.3)
        self.assertEqual(7.3, preferences.get('x', None))
        self.assertEqual(7.3, preferences.get('x', 'Ok'))

        self.assertEqual(None, preferences.get('x.y.z', None))
        self.assertEqual('Ok', preferences.get('x.y.z', 'Ok'))

        preferences.set('x.y.z', 7.3)
        self.assertEqual(7.3, preferences.get('x.y.z', None))
        self.assertEqual(7.3, preferences.get('x.y.z', 'Ok'))

        self.assertEqual({'z': 7.3}, preferences.get('x.y', None))
        self.assertEqual({'y': {'z': 7.3}}, preferences.get('x', None))

    def test_store_and_load(self):
        preferences = Preferences('_test', dir_path='.')

        preferences.set('window.bounds', [0, 0, 200, 100])
        preferences.set('last_dirs.configs', '/home/norman/configs')
        preferences.set('last_dirs.products', '/home/norman/products')

        preferences.store()

        preferences2 = Preferences('_test', dir_path='.')
        preferences2.load()

        self.assertEqual(preferences.data, preferences2.data)
