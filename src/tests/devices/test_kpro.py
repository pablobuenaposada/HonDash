from unittest import TestCase, mock

from devices.kpro import constants
from devices.kpro.kpro import Kpro


class TestKpro(TestCase):
    def setUp(self):
        # we are not unit testing USB features so it may raise a
        # `usb.core.NoBackendError` e.g. on Docker
        with mock.patch("devices.kpro.kpro.Kpro.__init__") as m___init__:
            m___init__.return_value = None
            self.kpro = Kpro()
        self.kpro.data0 = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.kpro.data1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.kpro.data3 = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]

    def test_battery_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data1[4] = 123
        self.assertEqual(self.kpro.bat(), 12.3)

    def test_rpm_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[2] = 100
        self.kpro.data0[3] = 100
        self.assertEqual(self.kpro.rpm(), 6425)

    def test_tps_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[5] = 100
        self.assertEqual(self.kpro.tps(), 37)

    def test_o2_v4_valid(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[16] = 0
        self.kpro.data0[17] = 128
        self.assertEqual(self.kpro.o2()["afr"], 14.7)
        self.assertEqual(self.kpro.o2()["lambda"], 1)

    def test_o2_v23_valid(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[18] = 0
        self.kpro.data0[19] = 128
        self.assertEqual(self.kpro.o2()["afr"], 14.7)
        self.assertEqual(self.kpro.o2()["lambda"], 1)

    def test_o2_v4_division_by_zero(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[18] = 0
        self.kpro.data0[19] = 0
        self.assertEqual(self.kpro.o2()["afr"], 0)
        self.assertEqual(self.kpro.o2()["lambda"], 0)

    def test_vss_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[4] = 100
        self.assertEqual(self.kpro.vss()["kmh"], 100)
        self.assertEqual(self.kpro.vss()["mph"], 62)

    def test_vss_v23(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[6] = 100
        self.assertEqual(self.kpro.vss()["kmh"], 100)
        self.assertEqual(self.kpro.vss()["mph"], 62)

    def test_ect_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data1[2] = 31
        self.assertEqual(self.kpro.ect()["celsius"], 90)
        self.assertEqual(self.kpro.ect()["fahrenheit"], 194)

    def test_ect_v23(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data1[4] = 31
        self.assertEqual(self.kpro.ect()["celsius"], 90)
        self.assertEqual(self.kpro.ect()["fahrenheit"], 194)

    def test_iat_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data1[3] = 31
        self.assertEqual(self.kpro.iat()["celsius"], 90)
        self.assertEqual(self.kpro.iat()["fahrenheit"], 194)

    def test_iat_v23(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data1[5] = 31
        self.assertEqual(self.kpro.iat()["celsius"], 90)
        self.assertEqual(self.kpro.iat()["fahrenheit"], 194)

    def test_map_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[6] = 100
        self.assertEqual(self.kpro.map()["bar"], 1)
        self.assertEqual(self.kpro.map()["mbar"], 1000)
        self.assertEqual(self.kpro.map()["psi"], 14.503773773)

    def test_map_v23(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[8] = 100
        self.assertEqual(self.kpro.map()["bar"], 1)
        self.assertEqual(self.kpro.map()["mbar"], 1000)
        self.assertEqual(self.kpro.map()["psi"], 14.503773773)

    def test_analog_input_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data3[66] = 52
        self.kpro.data3[67] = 3
        self.kpro.data3[68] = 52
        self.kpro.data3[69] = 3
        self.kpro.data3[70] = 52
        self.kpro.data3[71] = 3
        self.kpro.data3[72] = 52
        self.kpro.data3[73] = 3
        self.kpro.data3[74] = 52
        self.kpro.data3[75] = 3
        self.kpro.data3[76] = 52
        self.kpro.data3[77] = 3
        self.kpro.data3[78] = 52
        self.kpro.data3[79] = 3
        self.kpro.data3[80] = 52
        self.kpro.data3[81] = 3
        self.assertEqual(self.kpro.analog_input(0), 1.0009765625)
        self.assertEqual(self.kpro.analog_input(1), 1.0009765625)
        self.assertEqual(self.kpro.analog_input(2), 1.0009765625)
        self.assertEqual(self.kpro.analog_input(3), 1.0009765625)
        self.assertEqual(self.kpro.analog_input(4), 1.0009765625)
        self.assertEqual(self.kpro.analog_input(5), 1.0009765625)
        self.assertEqual(self.kpro.analog_input(6), 1.0009765625)
        self.assertEqual(self.kpro.analog_input(7), 1.0009765625)
