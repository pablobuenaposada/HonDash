from unittest import TestCase

from devices.time import Time


class TestTime(TestCase):
    def test_get_time(self):
        t = Time()
        self.assertRegexpMatches(t.get_time(), '\d{2}:\d{2}:\d{2}')
