from unittest import mock

import pytest

from devices.kpro import constants
from devices.kpro.kpro import Kpro


class TestKpro:

    temp_sensor_argvalues = ((51, 69, 156), (40, 80, 175), (31, 91, 195))

    def setup_method(self):
        # we are not unit testing USB features so it may raise a
        # `usb.core.NoBackendError` e.g. on Docker
        with mock.patch("devices.kpro.kpro.Kpro.__init__") as m___init__:
            m___init__.return_value = None
            self.kpro = Kpro()
        self.kpro.data0 = [None for _ in range(38)]
        self.kpro.data1 = [None for _ in range(6)]
        self.kpro.data3 = [None for _ in range(82)]
        self.kpro.data4 = [None for _ in range(18)]

    def test_battery_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data1[4] = 123

        assert self.kpro.bat() == 12.3

    def test_rpm_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[2] = 100
        self.kpro.data0[3] = 100

        assert self.kpro.rpm() == 6425

    def test_tps_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[5] = 100

        assert self.kpro.tps() == 37

    def test_o2_v4_valid(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_AFR1] = 0
        self.kpro.data0[constants.KPRO4_AFR2] = 128

        assert self.kpro.o2()["afr"] == 14.7
        assert self.kpro.o2()["lambda"] == 1

    def test_o2_v23_valid(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_AFR1] = 0
        self.kpro.data0[constants.KPRO23_AFR2] = 128

        assert self.kpro.o2()["afr"] == 14.7
        assert self.kpro.o2()["lambda"] == 1

    def test_o2_v4_division_by_zero(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_AFR1] = 0
        self.kpro.data0[constants.KPRO4_AFR2] = 0

        assert self.kpro.o2()["afr"] == 0
        assert self.kpro.o2()["lambda"] == 0

    def test_vss_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[4] = 100

        assert self.kpro.vss()["kmh"] == 100
        assert self.kpro.vss()["mph"] == 62

    def test_vss_v23(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[6] = 100

        assert self.kpro.vss()["kmh"] == 100
        assert self.kpro.vss()["mph"] == 62

    @pytest.mark.parametrize("kpro_value, value_cls, value_fht", temp_sensor_argvalues)
    def test_ect_v4(self, kpro_value, value_cls, value_fht):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data1[2] = kpro_value

        assert self.kpro.ect()["celsius"] == value_cls
        assert self.kpro.ect()["fahrenheit"] == value_fht

    @pytest.mark.parametrize("kpro_value, value_cls, value_fht", temp_sensor_argvalues)
    def test_ect_v23(self, kpro_value, value_cls, value_fht):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data1[4] = kpro_value

        assert self.kpro.ect()["celsius"] == value_cls
        assert self.kpro.ect()["fahrenheit"] == value_fht

    @pytest.mark.parametrize("kpro_value, value_cls, value_fht", temp_sensor_argvalues)
    def test_iat_v4(self, kpro_value, value_cls, value_fht):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data1[3] = kpro_value

        assert self.kpro.iat()["celsius"] == value_cls
        assert self.kpro.iat()["fahrenheit"] == value_fht

    @pytest.mark.parametrize("kpro_value, value_cls, value_fht", temp_sensor_argvalues)
    def test_iat_v23(self, kpro_value, value_cls, value_fht):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data1[5] = kpro_value

        assert self.kpro.iat()["celsius"] == value_cls
        assert self.kpro.iat()["fahrenheit"] == value_fht

    def test_map_v4(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[6] = 100

        assert self.kpro.map()["bar"] == 1
        assert self.kpro.map()["mbar"] == 1000
        assert self.kpro.map()["psi"] == 14.503773773

    def test_map_v23(self):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[8] = 100

        assert self.kpro.map()["bar"] == 1
        assert self.kpro.map()["mbar"] == 1000
        assert self.kpro.map()["psi"] == 14.503773773

    @pytest.mark.parametrize("kpro_value, result", ((100, 30.0),))
    def test_cam_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_CAM] = kpro_value

        assert self.kpro.cam() == result

    @pytest.mark.parametrize("kpro_value, result", ((100, 30.0),))
    def test_cam_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_CAM] = kpro_value

        assert self.kpro.cam() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, "N"), (1, 1)))
    def test_gear_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_GEAR] = kpro_value

        assert self.kpro.gear() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, "N"), (1, 1)))
    def test_gear_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_GEAR] = kpro_value

        assert self.kpro.gear() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (32, True)))
    def test_eps_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_EPS] = kpro_value

        assert self.kpro.eps() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (32, True)))
    def test_eps_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_EPS] = kpro_value

        assert self.kpro.eps() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (16, True)))
    def test_scs_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_SCS] = kpro_value

        assert self.kpro.scs() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (16, True)))
    def test_scs_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_SCS] = kpro_value

        assert self.kpro.scs() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (1, True)))
    def test_rvslck_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_RVSLCK] = kpro_value

        assert self.kpro.rvslck() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (1, True)))
    def test_rvslck_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_RVSLCK] = kpro_value

        assert self.kpro.rvslck() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (2, True)))
    def test_bksw_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_BKSW] = kpro_value

        assert self.kpro.bksw() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (2, True)))
    def test_bksw_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_BKSW] = kpro_value

        assert self.kpro.bksw() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (4, True)))
    def test_acsw_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_ACSW] = kpro_value

        assert self.kpro.acsw() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (4, True)))
    def test_acsw_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_ACSW] = kpro_value

        assert self.kpro.acsw() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (8, True)))
    def test_accl_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_ACCL] = kpro_value

        assert self.kpro.accl() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (8, True)))
    def test_accl_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_ACCL] = kpro_value

        assert self.kpro.accl() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (64, True)))
    def test_flr_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_FLR] = kpro_value

        assert self.kpro.flr() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (64, True)))
    def test_flr_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_FLR] = kpro_value

        assert self.kpro.flr() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (128, True)))
    def test_fanc_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data0[constants.KPRO23_FANC] = kpro_value

        assert self.kpro.fanc() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (128, True)))
    def test_fanc_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data0[constants.KPRO4_FANC] = kpro_value

        assert self.kpro.fanc() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (1, True)))
    def test_ign_v23(self, kpro_value, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data4[constants.KPRO23_IGN] = kpro_value

        assert self.kpro.ign() == result

    @pytest.mark.parametrize("kpro_value, result", ((0, False), (1, True)))
    def test_ign_v4(self, kpro_value, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data4[constants.KPRO4_IGN] = kpro_value

        assert self.kpro.ign() == result

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

        assert self.kpro.analog_input(0) == 1.0009765625
        assert self.kpro.analog_input(1) == 1.0009765625
        assert self.kpro.analog_input(2) == 1.0009765625
        assert self.kpro.analog_input(3) == 1.0009765625
        assert self.kpro.analog_input(4) == 1.0009765625
        assert self.kpro.analog_input(5) == 1.0009765625
        assert self.kpro.analog_input(6) == 1.0009765625
        assert self.kpro.analog_input(7) == 1.0009765625
