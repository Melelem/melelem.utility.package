from unittest import TestCase

from melelem.utilities.builtins import (
    count_decimal_places
)


class BuiltinsTests(TestCase):
    def test_count_decimal_places(self):
        # 1 decimal place.
        decimal_place_count = count_decimal_places(0.1)
        self.assertEqual(decimal_place_count, 1)

        # 3 decimal places.
        decimal_place_count = count_decimal_places(0.111)
        self.assertEqual(decimal_place_count, 3)

        # Integer (1 decimal place).
        decimal_place_count = count_decimal_places(1)
        self.assertEqual(decimal_place_count, 1)
