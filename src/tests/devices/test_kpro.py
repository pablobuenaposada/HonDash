from unittest import TestCase

from devices.kpro import Kpro


class TestKpro(TestCase):

    def setUp(self):
        self.kpro = Kpro()
        self.kpro.data0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.kpro.data1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_battery_v4(self):
        self.kpro.version = 4
        self.kpro.data1[4] = 123
        self.assertEqual(self.kpro.bat(), 12.3)

    def test_rpm_v4(self):
        self.kpro.version = 4
        self.kpro.data0[2] = 100
        self.kpro.data0[3] = 100
        self.assertEqual(self.kpro.rpm(), 6425)

    def test_tps_v4(self):
        self.kpro.version = 4
        self.kpro.data0[5] = 100
        self.assertEqual(self.kpro.tps(), 37)
