from unittest import TestCase, mock

from devices.kpro import Kpro


class TestKpro(TestCase):

    def setUp(self):
        # we are not unit testing USB features and find() may raise a
        # `usb.core.NoBackendError` e.g. on Docker
        with mock.patch('usb.core.find') as m_find:
            m_find.return_value = None
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

    def test_afr_v4_valid(self):
        self.kpro.version = 4
        self.kpro.data0[16] = 0
        self.kpro.data0[17] = 128
        self.assertEquals(self.kpro.afr(), 14.7)

    def test_afr_v2_valid(self):
        self.kpro.version = 2
        self.kpro.data0[18] = 0
        self.kpro.data0[19] = 128
        self.assertEquals(self.kpro.afr(), 14.7)

    def test_afr_v4_division_by_zero(self):
        self.kpro.version = 4
        self.kpro.data0[18] = 0
        self.kpro.data0[19] = 0
        self.assertEqual(self.kpro.afr(), 0)
