from unittest import TestCase
from unittest.mock import patch

from soffos.utilities.lazy_loader import LazyLoader


class LazyLoaderTests(TestCase):
    def setUp(self):
        self.value = 'Hello World!'
        self.load = lambda: self.value
        self.lazy_loader = LazyLoader(self.load)

    def test_init(self):
        self.assertIsNone(self.lazy_loader._value)
        self.assertEqual(self.lazy_loader._load, self.load)

    def test_lazy_load(self):
        value = self.lazy_loader.lazy_load()
        self.assertEqual(value, self.value)

    def test_lazy_load__called_once(self):
        with patch.object(self.lazy_loader, '_load') as _load:
            _load.return_value = self.value

            # First call = load value and return.
            value = self.lazy_loader.lazy_load()
            self.assertEqual(value, self.value)

            # Second call = return cached value.
            value = self.lazy_loader.lazy_load()
            self.assertEqual(value, self.value)

            # Assert load only called once.
            _load.assert_called_once()
