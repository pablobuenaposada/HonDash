from unittest import TestCase

from devices.time import Time


class TestTime(TestCase):
    def test_get_time(self):
        t = Time()
        self.assertRegex(t.get_time(), r'\d{2}:\d{2}:\d{2}')
