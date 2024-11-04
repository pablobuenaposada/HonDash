from unittest import mock
from unittest.mock import ANY, MagicMock, call

import pytest
import usb

from devices.kpro import constants
from devices.kpro.kpro import MAX_CONNECTION_RETRIES, Kpro


class TestKpro:
    temp_sensor_argvalues = ((51, 69, 156), (40, 80, 175), (31, 91, 195))

    def setup_method(self):
        # we are not unit testing USB features so it may raise a
        # `usb.core.NoBackendError` e.g. on Docker
        with mock.patch("devices.kpro.kpro.Kpro.__init__") as m___init__:
            m___init__.return_value = None
            self.kpro = Kpro()
        self.kpro.data0 = [None for _ in range(38)]
        self.kpro.data1 = [None for _ in range(7)]
        self.kpro.data3 = [None for _ in range(100)]
        self.kpro.data4 = [None for _ in range(18)]
        self.kpro.data5 = [None for _ in range(20)]

    def test_init(self):
        with mock.patch("usb.core.find"), mock.patch(
            "threading.Thread.start"
        ) as m_start:
            self.kpro = Kpro()

        assert self.kpro.status is True
        # update method in a thread has been tried to start
        assert m_start.called is True

    @pytest.mark.parametrize(
        "kpro_version, kpro_vendor_id, kpro_product_id",
        (
            (
                constants.KPRO23_ID,
                constants.KPRO23_ID_VENDOR,
                constants.KPRO23_ID_PRODUCT,
            ),
            (constants.KPRO4_ID, constants.KPRO4_ID_VENDOR, constants.KPRO4_ID_PRODUCT),
        ),
    )
    def test_init_with_all_kpro_versions(
        self, kpro_version, kpro_vendor_id, kpro_product_id
    ):
        def found_device(idVendor, idProduct):
            if idVendor == kpro_vendor_id and idProduct == kpro_product_id:
                return MagicMock()
            else:
                return None

        with mock.patch("usb.core.find") as m_find, mock.patch(
            "threading.Thread.start"
        ) as m_start:
            m_find.side_effect = found_device
            self.kpro = Kpro()

        assert self.kpro.status is True
        # update method in a thread has been tried to start
        assert m_start.called is True
        assert self.kpro.version == kpro_version

    def test_init_no_kpro_connected(self):
        with mock.patch("usb.core.find") as m_find, mock.patch(
            "threading.Thread.start"
        ) as m_start:
            m_find.return_value = None
            self.kpro = Kpro()

        assert self.kpro.status is False
        assert self.kpro.version is None
        # update method in a thread has not been tried to start
        assert m_start.called is False
        # been trying to find the two kpro versions per 10 times, so 20 times calling usb find method
        assert m_find.call_count == 20

    @pytest.mark.parametrize(
        "version, read_calls, write_calls",
        (
            (
                constants.KPRO4_ID,
                [
                    call.read(ANY, 1000),
                    call.read(ANY, 1000),
                    call.read(ANY, 1000),
                    call.read(ANY, 1000),
                    call.read(ANY, 128, 1000),
                ],
                [
                    call.write("\x40"),
                    call.write("\x60"),
                    call.write("\x61"),
                    call.write("\x62"),
                    call.write("\x65"),
                ],
            ),
            (
                constants.KPRO23_ID,
                [
                    call.read(ANY, 1000),
                    call.read(ANY, 1000),
                    call.read(ANY, 1000),
                    call.read(ANY, 1000),
                    call.read(ANY, 1000),
                ],
                [
                    call.write("\x40"),
                    call.write("\x60"),
                    call.write("\x61"),
                    call.write("\x62"),
                    call.write("\xb0"),
                ],
            ),
            (
                None,
                [call.read(ANY, 1000), call.read(ANY, 1000)],
                [
                    call.write("\x40"),
                    call.write("\x60"),
                    call.write("\x61"),
                    call.write("\x62"),
                    call.write("\xb0"),
                ],
            ),
        ),
    )
    def test__read_from_device(self, version, read_calls, write_calls):
        device = MagicMock()
        device.read = MagicMock(return_value=[])
        entry_point = MagicMock()
        entry_point_address = MagicMock()

        assert self.kpro._read_from_device(
            version, device, entry_point, entry_point_address
        ) == (
            [],
            [],
            [],
            [],
            [],
            [],
        )
        assert device.mock_calls == read_calls
        assert entry_point.mock_calls == write_calls

    def test_find_and_connect_exception(self):
        """usb exception should be caught and retry device connection MAX_CONNECTION_RETRIES times"""
        self.kpro.status = False
        with mock.patch("threading.Thread.start") as m_start, mock.patch(
            "devices.kpro.kpro.establish_connection"
        ) as m_establish_connection, mock.patch(
            "devices.kpro.kpro.find_device"
        ) as m_find_device:
            m_establish_connection.side_effect = usb.core.USBError("foo")
            m_find_device.return_value = (MagicMock(), None)
            self.kpro.find_and_connect()
        assert self.kpro.status is False
        assert m_establish_connection.call_count == MAX_CONNECTION_RETRIES
        assert m_start.called is False

    @pytest.mark.parametrize(
        "error, status_result, init_called_result",
        (
            (usb.core.USBError("foo"), False, True),
            # "(usb.core.USBError("foo", errno=60), True, False)
        ),
    )
    def test__update_exception(self, error, status_result, init_called_result):
        """in case any usb error while fetching the data"""
        self.kpro.status = True
        self.kpro.version = self.kpro.kpro_device = self.kpro.entry_point = (
            self.kpro.entry_point_address
        ) = None
        with mock.patch(
            "devices.kpro.kpro.Kpro._read_from_device"
        ) as m__read_from_device, mock.patch(
            "devices.kpro.kpro.Kpro.__init__"
        ) as m___init__:
            m__read_from_device.side_effect = error
            self.kpro._update()
        assert self.kpro.status is status_result
        assert m___init__.called is init_called_result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, 666, 0),
            (constants.KPRO23_ID, constants.KPRO23_BAT, 123, 12.3),
            (constants.KPRO4_ID, constants.KPRO4_BAT, 123, 12.3),
        ),
    )
    def test_bat(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data1[index] = value

        assert self.kpro.bat == result

    def test_eth(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data3[constants.KPRO4_ETH] = 50

        assert self.kpro.eth == 50

    def test_flt(self):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data3[constants.KPRO4_FLT] = 50

        assert self.kpro.flt == {"celsius": 50, "fahrenheit": 122.0}

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result",
        (
            (
                constants.KPRO23_ID,
                constants.KPRO23_RPM1,
                constants.KPRO23_RPM2,
                100,
                100,
                6425,
            ),
            (
                constants.KPRO4_ID,
                constants.KPRO4_RPM1,
                constants.KPRO4_RPM2,
                100,
                100,
                6425,
            ),
        ),
    )
    def test_rpm(self, version, index1, index2, value1, value2, result):
        self.kpro.version = version
        self.kpro.data0[index1] = value1
        self.kpro.data0[index2] = value2

        assert self.kpro.rpm == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_TPS, 100, 37),
            (constants.KPRO4_ID, constants.KPRO4_TPS, 100, 37),
            (None, constants.KPRO4_TPS, 666, 0),
        ),
    )
    def test_tps(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.tps == result

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result_afr, result_lambda",
        (
            (
                constants.KPRO23_ID,
                constants.KPRO23_AFR1,
                constants.KPRO23_AFR2,
                0,
                128,
                14.7,
                1,
            ),
            (
                constants.KPRO4_ID,
                constants.KPRO4_AFR1,
                constants.KPRO4_AFR2,
                0,
                128,
                14.7,
                1,
            ),
            (
                constants.KPRO4_ID,
                constants.KPRO4_AFR1,
                constants.KPRO4_AFR2,
                0,
                0,
                0,
                0,
            ),
            (
                None,
                0,
                0,
                666,
                666,
                0,
                0,
            ),
        ),
    )
    def test_o2(
        self, version, index1, index2, value1, value2, result_afr, result_lambda
    ):
        self.kpro.version = version
        self.kpro.data0[index1] = value1
        self.kpro.data0[index2] = value2

        assert self.kpro.o2["afr"] == result_afr
        assert self.kpro.o2["lambda"] == result_lambda

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result_afr, result_lambda",
        (
            (
                constants.KPRO23_ID,
                constants.KPRO23_AFR_CMD1,
                constants.KPRO23_AFR_CMD2,
                0,
                128,
                14.7,
                1,
            ),
            (
                constants.KPRO4_ID,
                constants.KPRO4_AFR_CMD1,
                constants.KPRO4_AFR_CMD2,
                0,
                128,
                14.7,
                1,
            ),
            (
                constants.KPRO4_ID,
                constants.KPRO4_AFR_CMD1,
                constants.KPRO4_AFR_CMD2,
                0,
                0,
                0,
                0,
            ),
            (
                None,
                0,
                0,
                666,
                666,
                0,
                0,
            ),
        ),
    )
    def test_o2_cmd(
        self, version, index1, index2, value1, value2, result_afr, result_lambda
    ):
        self.kpro.version = version
        self.kpro.data0[index1] = value1
        self.kpro.data0[index2] = value2

        assert self.kpro.o2_cmd["afr"] == result_afr
        assert self.kpro.o2_cmd["lambda"] == result_lambda

    @pytest.mark.parametrize(
        "version, index, value, result_kmh, result_mph",
        (
            (None, 0, None, 0, 0),
            (constants.KPRO23_ID, constants.KPRO23_VSS, 100, 100, 62),
            (constants.KPRO4_ID, constants.KPRO4_VSS, 100, 100, 62),
        ),
    )
    def test_vss(self, version, index, value, result_kmh, result_mph):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.vss["kmh"] == result_kmh
        assert self.kpro.vss["mph"] == result_mph

    @pytest.mark.parametrize(
        "version, index, values",
        (
            (None, 0, (None, 0, 0)),
            (constants.KPRO23_ID, constants.KPRO23_ECT, temp_sensor_argvalues[0]),
            (constants.KPRO23_ID, constants.KPRO23_ECT, temp_sensor_argvalues[1]),
            (constants.KPRO23_ID, constants.KPRO23_ECT, temp_sensor_argvalues[2]),
            (constants.KPRO4_ID, constants.KPRO4_ECT, temp_sensor_argvalues[0]),
            (constants.KPRO4_ID, constants.KPRO4_ECT, temp_sensor_argvalues[1]),
            (constants.KPRO4_ID, constants.KPRO4_ECT, temp_sensor_argvalues[2]),
        ),
    )
    def test_ect(self, version, index, values):
        self.kpro.version = version
        self.kpro.data1[index] = values[0]

        assert self.kpro.ect["celsius"] == values[1]
        assert self.kpro.ect["fahrenheit"] == values[2]

    @pytest.mark.parametrize(
        "version, index, values",
        (
            (None, 0, (None, 0, 0)),
            (constants.KPRO23_ID, constants.KPRO23_IAT, temp_sensor_argvalues[0]),
            (constants.KPRO23_ID, constants.KPRO23_IAT, temp_sensor_argvalues[1]),
            (constants.KPRO23_ID, constants.KPRO23_IAT, temp_sensor_argvalues[2]),
            (constants.KPRO4_ID, constants.KPRO4_IAT, temp_sensor_argvalues[0]),
            (constants.KPRO4_ID, constants.KPRO4_IAT, temp_sensor_argvalues[1]),
            (constants.KPRO4_ID, constants.KPRO4_IAT, temp_sensor_argvalues[2]),
        ),
    )
    def test_iat(self, version, index, values):
        self.kpro.version = version
        self.kpro.data1[index] = values[0]

        assert self.kpro.iat["celsius"] == values[1]
        assert self.kpro.iat["fahrenheit"] == values[2]

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, 100, (0, 0, 0)),
            (constants.KPRO23_ID, constants.KPRO23_MAP, 100, (1, 1000, 14.503773773)),
            (constants.KPRO4_ID, constants.KPRO4_MAP, 100, (1, 1000, 14.503773773)),
        ),
    )
    def test_map(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.map["bar"] == result[0]
        assert self.kpro.map["mbar"] == result[1]
        assert self.kpro.map["psi"] == result[2]

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_CAM, 100, 30.0),
            (constants.KPRO4_ID, constants.KPRO4_CAM, 100, 30.0),
        ),
    )
    def test_cam(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.cam == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_GEAR, 1, 1),
            (constants.KPRO4_ID, constants.KPRO4_GEAR, 1, 1),
        ),
    )
    def test_gear(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.gear == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.KPRO23_ID, constants.KPRO23_EPS, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_EPS, 32, True),
            (constants.KPRO4_ID, constants.KPRO4_EPS, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_EPS, 32, True),
        ),
    )
    def test_eps(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.eps == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.KPRO23_ID, constants.KPRO23_SCS, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_SCS, 16, True),
            (constants.KPRO4_ID, constants.KPRO4_SCS, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_SCS, 16, True),
        ),
    )
    def test_scs(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.scs == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.KPRO23_ID, constants.KPRO23_RVSLCK, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_RVSLCK, 1, True),
            (constants.KPRO4_ID, constants.KPRO4_RVSLCK, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_RVSLCK, 1, True),
        ),
    )
    def test_rvslck(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.rvslck == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.KPRO23_ID, constants.KPRO23_BKSW, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_BKSW, 2, True),
            (constants.KPRO4_ID, constants.KPRO4_BKSW, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_BKSW, 2, True),
        ),
    )
    def test_bksw(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.bksw == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_ACSW, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_ACSW, 4, True),
            (constants.KPRO4_ID, constants.KPRO4_ACSW, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_ACSW, 4, True),
        ),
    )
    def test_acsw(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.acsw == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_ACCL, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_ACCL, 8, True),
            (constants.KPRO4_ID, constants.KPRO4_ACCL, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_ACCL, 8, True),
        ),
    )
    def test_accl(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.accl == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_FLR, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_FLR, 64, True),
            (constants.KPRO4_ID, constants.KPRO4_FLR, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_FLR, 64, True),
        ),
    )
    def test_flr(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.flr == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_FANC, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_FANC, 128, True),
            (constants.KPRO4_ID, constants.KPRO4_FANC, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_FANC, 128, True),
        ),
    )
    def test_fanc(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data0[index] = value

        assert self.kpro.fanc == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, None, None, False),
            (constants.KPRO23_ID, constants.KPRO23_MIL, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_MIL, 9, True),
            (constants.KPRO4_ID, constants.KPRO4_MIL, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_MIL, 36, True),
        ),
    )
    def test_mil(self, version, index, value, result):
        self.kpro.version = version
        if version == constants.KPRO23_ID:
            self.kpro.data0[index] = value
        elif version == constants.KPRO4_ID:
            self.kpro.data3[index] = value

        assert self.kpro.mil == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (constants.KPRO23_ID, constants.KPRO23_ECU_TYPE, 3, "RSX - PRB"),
            (constants.KPRO23_ID, constants.KPRO23_ECU_TYPE, 0, "unknown"),
            (constants.KPRO4_ID, constants.KPRO4_ECU_TYPE, 3, "RSX - PRB"),
            (constants.KPRO4_ID, constants.KPRO4_ECU_TYPE, 0, "unknown"),
        ),
    )
    def test_ecu_type(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data4[index] = value

        assert self.kpro.ecu_type == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.KPRO23_ID, constants.KPRO23_IGN, 0, False),
            (constants.KPRO23_ID, constants.KPRO23_IGN, 1, True),
            (constants.KPRO4_ID, constants.KPRO4_IGN, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_IGN, 1, True),
        ),
    )
    def test_ign(self, version, index, value, result):
        self.kpro.version = version
        self.kpro.data4[index] = value

        assert self.kpro.ign == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.KPRO23_ID, constants.KPRO23_VTS, 2, True),
            (constants.KPRO23_ID, constants.KPRO23_VTS, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_VTS, 2, True),
            (constants.KPRO4_ID, constants.KPRO4_VTS, 0, False),
        ),
    )
    def test_vts(self, version, index, value, result):
        self.kpro.version = version
        if version == constants.KPRO23_ID:
            self.kpro.data0[index] = value
        elif version == constants.KPRO4_ID:
            self.kpro.data3[index] = value

        assert self.kpro.vts == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.KPRO23_ID, constants.KPRO23_VTP, 1, True),
            (constants.KPRO23_ID, constants.KPRO23_VTP, 0, False),
            (constants.KPRO4_ID, constants.KPRO4_VTP, 1, True),
            (constants.KPRO4_ID, constants.KPRO4_VTP, 0, False),
        ),
    )
    def test_vtp(self, version, index, value, result):
        self.kpro.version = version
        if version == constants.KPRO23_ID:
            self.kpro.data0[index] = value
        elif version == constants.KPRO4_ID:
            self.kpro.data3[index] = value

        assert self.kpro.vtp == result

    @pytest.mark.parametrize(
        "version, vtp_index, vts_index, value, result",
        (
            (None, 0, 0, 0, "off"),
            (constants.KPRO23_ID, constants.KPRO23_VTP, constants.KPRO23_VTS, 3, "on"),
            (
                constants.KPRO23_ID,
                constants.KPRO23_VTP,
                constants.KPRO23_VTS,
                2,
                "malfunction",
            ),
            (
                constants.KPRO23_ID,
                constants.KPRO23_VTP,
                constants.KPRO23_VTS,
                1,
                "malfunction",
            ),
            (constants.KPRO23_ID, constants.KPRO23_VTP, constants.KPRO23_VTS, 0, "off"),
            (constants.KPRO4_ID, constants.KPRO4_VTP, constants.KPRO4_VTS, 3, "on"),
            (
                constants.KPRO4_ID,
                constants.KPRO4_VTP,
                constants.KPRO4_VTS,
                2,
                "malfunction",
            ),
            (
                constants.KPRO4_ID,
                constants.KPRO4_VTP,
                constants.KPRO4_VTS,
                1,
                "malfunction",
            ),
            (constants.KPRO4_ID, constants.KPRO4_VTP, constants.KPRO4_VTS, 0, "off"),
        ),
    )
    def test_vtec(self, version, vtp_index, vts_index, value, result):
        self.kpro.version = version
        if version == constants.KPRO23_ID:
            self.kpro.data0[vtp_index] = value
            self.kpro.data0[vts_index] = value
        elif version == constants.KPRO4_ID:
            self.kpro.data3[vtp_index] = value
            self.kpro.data3[vts_index] = value

        assert self.kpro.vtec == result

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result",
        (
            (
                constants.KPRO23_ID,
                constants.KPRO23_SERIAL1,
                constants.KPRO23_SERIAL2,
                210,
                4,
                1234,
            ),
            (
                constants.KPRO4_ID,
                constants.KPRO4_SERIAL1,
                constants.KPRO4_SERIAL2,
                210,
                4,
                1234,
            ),
        ),
    )
    def test_serial(self, version, index1, index2, value1, value2, result):
        self.kpro.version = version
        self.kpro.data4[index1] = value1
        self.kpro.data4[index2] = value2

        assert self.kpro.serial == result

    @pytest.mark.parametrize(
        "index1, index2, value1, value2, channel, result",
        (
            (constants.KPRO4_AN0_1, constants.KPRO4_AN0_2, 3, 52, 0, 1.0009765625),
            (constants.KPRO4_AN1_1, constants.KPRO4_AN1_2, 3, 52, 1, 1.0009765625),
            (constants.KPRO4_AN2_1, constants.KPRO4_AN2_2, 3, 52, 2, 1.0009765625),
            (constants.KPRO4_AN3_1, constants.KPRO4_AN3_2, 3, 52, 3, 1.0009765625),
            (constants.KPRO4_AN4_1, constants.KPRO4_AN4_2, 3, 52, 4, 1.0009765625),
            (constants.KPRO4_AN5_1, constants.KPRO4_AN5_2, 3, 52, 5, 1.0009765625),
            (constants.KPRO4_AN6_1, constants.KPRO4_AN6_2, 3, 52, 6, 1.0009765625),
            (constants.KPRO4_AN7_1, constants.KPRO4_AN7_2, 3, 52, 7, 1.0009765625),
        ),
    )
    def test_analog_input_v4(self, index1, index2, value1, value2, channel, result):
        self.kpro.version = constants.KPRO4_ID
        self.kpro.data3[index2] = value2
        self.kpro.data3[index1] = value1

        assert self.kpro.analog_input(channel) == result

    @pytest.mark.parametrize(
        "index1, index2, value1, value2, channel, result",
        (
            (constants.KPRO3_AN0_1, constants.KPRO3_AN0_2, 3, 52, 0, 4.00390625),
            (constants.KPRO3_AN1_1, constants.KPRO3_AN1_2, 3, 52, 1, 4.00390625),
            (constants.KPRO3_AN2_1, constants.KPRO3_AN2_2, 3, 52, 2, 4.00390625),
            (constants.KPRO3_AN3_1, constants.KPRO3_AN3_2, 3, 52, 3, 4.00390625),
            (constants.KPRO3_AN4_1, constants.KPRO3_AN4_2, 3, 52, 4, 4.00390625),
            (constants.KPRO3_AN5_1, constants.KPRO3_AN5_2, 3, 52, 5, 4.00390625),
            (constants.KPRO3_AN6_1, constants.KPRO3_AN6_2, 3, 52, 6, 4.00390625),
            (constants.KPRO3_AN7_1, constants.KPRO3_AN7_2, 3, 52, 7, 4.00390625),
        ),
    )
    def test_analog_input_v3(self, index1, index2, value1, value2, channel, result):
        self.kpro.version = constants.KPRO23_ID
        self.kpro.data5[index2] = value2
        self.kpro.data5[index1] = value1

        assert self.kpro.analog_input(channel) == result

    @pytest.mark.parametrize(
        "channel, result",
        (
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
        ),
    )
    def test_analog_input_no_version(self, channel, result):
        self.kpro.version = None

        assert self.kpro.analog_input(channel) == result
