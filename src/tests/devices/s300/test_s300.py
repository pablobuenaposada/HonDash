from unittest import mock
from unittest.mock import MagicMock, call

import pytest
import usb

from devices.s300 import constants
from devices.s300.s300 import MAX_CONNECTION_RETRIES, S300


class TestS300:
    temp_sensor_argvalues = ((51, 69, 156), (40, 80, 175), (31, 91, 195))

    def setup_method(self):
        # we are not unit testing USB features so it may raise a
        # `usb.core.NoBackendError` e.g. on Docker
        with mock.patch("devices.s300.s300.S300.__init__") as m___init__:
            m___init__.return_value = None
            self.s300 = S300()
        self.s300.data4 = [None for _ in range(18)]
        self.s300.data5 = [None for _ in range(21)]
        self.s300.data6 = [None for _ in range(200)]

    def test_init(self):
        with mock.patch("usb.core.find"), mock.patch(
            "threading.Thread.start"
        ) as m_start:
            self.s300 = S300()

        assert self.s300.status is True
        # update method in a thread has been tried to start
        assert m_start.called is True

    @pytest.mark.parametrize(
        "s300_version, s300_vendor_id, s300_product_id",
        ((constants.S3003_ID, constants.S3003_ID_VENDOR, constants.S3003_ID_PRODUCT),),
    )
    def test_init_with_all_s300_versions(
        self, s300_version, s300_vendor_id, s300_product_id
    ):
        def found_device(idVendor, idProduct):
            if idVendor == s300_vendor_id and idProduct == s300_product_id:
                return MagicMock()
            else:
                return None

        with mock.patch("usb.core.find") as m_find, mock.patch(
            "threading.Thread.start"
        ) as m_start:
            m_find.side_effect = found_device
            self.s300 = S300()

        assert self.s300.status is True
        # update method in a thread has been tried to start
        assert m_start.called is True
        assert self.s300.version == s300_version

    def test_init_no_s300_connected(self):
        with mock.patch("usb.core.find") as m_find, mock.patch(
            "threading.Thread.start"
        ) as m_start:
            m_find.return_value = None
            self.s300 = S300()

        assert self.s300.status is False
        assert self.s300.version is None
        # update method in a thread has not been tried to start
        assert m_start.called is False
        # been trying to find the s300 10 times
        assert m_find.call_count == 10

    @pytest.mark.parametrize(
        "version, read_calls, write_calls",
        (
            (
                constants.S3003_ID,
                [
                    call.read(0x82, 1000, 1000),
                    call.read(0x82, 128, 1000),
                    call.read(0x82, 1000),
                ],
                [
                    call.write(b"\x90"),
                    call.write(b"\xB0"),
                    call.write(b"\x40"),
                ],
            ),
            (
                None,
                [
                    call.read(0x82, 1000, 1000),
                    call.read(0x82, 128, 1000),
                    call.read(0x82, 1000),
                ],
                [
                    call.write(b"\x90"),
                    call.write(b"\xB0"),
                    call.write(b"\x40"),
                ],
            ),
        ),
    )
    def test__read_from_device(self, version, read_calls, write_calls):
        device = MagicMock()
        device.read = MagicMock(return_value=[])
        entry_point = MagicMock()

        assert ([], [], []) == self.s300._read_from_device(version, device, entry_point)
        assert device.mock_calls == read_calls
        assert entry_point.mock_calls == write_calls

    def test_find_and_connect_exception(self):
        """usb exception should be caught and retry device connection MAX_CONNECTION_RETRIES times"""
        self.s300.status = False
        with mock.patch("threading.Thread.start") as m_start, mock.patch(
            "devices.s300.s300.establish_connection"
        ) as m_establish_connection, mock.patch(
            "devices.s300.s300.find_device"
        ) as m_find_device:
            m_establish_connection.side_effect = usb.core.USBError("foo")
            m_find_device.return_value = (MagicMock(), None)
            self.s300.find_and_connect()
        assert self.s300.status is False
        assert m_establish_connection.call_count == MAX_CONNECTION_RETRIES
        assert m_start.called is False

    @pytest.mark.parametrize(
        "error, status_result, init_called_result",
        (
            (usb.core.USBError("foo"), False, True),
            # "(usb.core.USBError("foo", errno=60), True, False)
        ),
    )
    def test__update_excption(self, error, status_result, init_called_result):
        """in case any usb error while fetching the data"""
        self.s300.status = True
        self.s300.version = self.s300.device = self.s300.entry_point = None
        with mock.patch(
            "devices.s300.s300.S300._read_from_device"
        ) as m__read_from_device, mock.patch(
            "devices.s300.s300.S300.__init__"
        ) as m___init__:
            m__read_from_device.side_effect = error
            self.s300._update()
        assert self.s300.status is status_result
        assert m___init__.called is init_called_result

    def test_eth(self):
        self.s300.version = constants.S3003_ID
        self.s300.data5[constants.S3003_ETH] = 50

        assert self.s300.eth == 50

    def test_flt(self):
        self.s300.version = constants.S3003_ID
        self.s300.data5[constants.S3003_FLT] = 50

        assert self.s300.flt == {"celsius": 10, "fahrenheit": 50.0}

    def test_bat(self):
        self.s300.version = constants.S3003_ID
        self.s300.data6[constants.S3003_BAT] = 12.4

        assert self.s300.bat == 0.7400000000000002

    @pytest.mark.parametrize(
        "value, result",
        (
            (25, 0),
            (255, 115),
        ),
    )
    def test_tps(self, value, result):
        self.s300.version = constants.S3003_ID
        self.s300.data6[constants.S3003_TPS] = value

        assert self.s300.tps == result

    def test_gear(self):
        self.s300.version = constants.S3003_ID
        self.s300.data6[constants.S3003_GEAR] = 1

        assert self.s300.gear == 1

    @pytest.mark.parametrize(
        "value, result",
        (
            (0, False),
            (1, True),
        ),
    )
    def test_fanc(self, value, result):
        self.s300.version = constants.S3003_ID
        self.s300.data6[constants.S3003_FANC] = value

        assert self.s300.fanc == result

    def test_rpm(self):
        self.s300.version = constants.S3003_ID
        self.s300.data6[constants.S3003_RPM1] = 100
        self.s300.data6[constants.S3003_RPM2] = 100

        assert self.s300.rpm == 25700

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result",
        (
            (
                constants.S3003_ID,
                constants.S3003_VSS1,
                constants.S3003_VSS2,
                220,
                8,
                {"kmh": 100, "mph": 62},
            ),
            (
                constants.S3003_ID,
                constants.S3003_VSS1,
                constants.S3003_VSS2,
                0,
                0,
                {"kmh": 0, "mph": 0},
            ),
        ),
    )
    def test_vss(self, version, index1, index2, value1, value2, result):
        self.s300.version = version
        self.s300.data6[index1] = value1
        self.s300.data6[index2] = value2

        assert self.s300.vss == result

    def test_o2(self):
        self.s300.version = constants.S3003_ID
        self.s300.data6[constants.S3003_AFR] = 128

        assert self.s300.o2 == {"afr": 14.757147922437671, "lambda": 1.0038876137712702}

    @pytest.mark.parametrize(
        "version, index, values",
        (
            (None, 0, (None, 0, 0)),
            (constants.S3003_ID, constants.S3003_ECT, temp_sensor_argvalues[0]),
            (constants.S3003_ID, constants.S3003_ECT, temp_sensor_argvalues[1]),
            (constants.S3003_ID, constants.S3003_ECT, temp_sensor_argvalues[2]),
            (constants.S3003_ID, constants.S3003_ECT, temp_sensor_argvalues[0]),
            (constants.S3003_ID, constants.S3003_ECT, temp_sensor_argvalues[1]),
            (constants.S3003_ID, constants.S3003_ECT, temp_sensor_argvalues[2]),
        ),
    )
    def test_ect(self, version, index, values):
        self.s300.version = version
        self.s300.data6[index] = values[0]

        assert self.s300.ect["celsius"] == values[1]
        assert self.s300.ect["fahrenheit"] == values[2]

    @pytest.mark.parametrize(
        "version, index, values",
        (
            (None, 0, (None, 0, 0)),
            (constants.S3003_ID, constants.S3003_IAT, temp_sensor_argvalues[0]),
            (constants.S3003_ID, constants.S3003_IAT, temp_sensor_argvalues[1]),
            (constants.S3003_ID, constants.S3003_IAT, temp_sensor_argvalues[2]),
            (constants.S3003_ID, constants.S3003_IAT, temp_sensor_argvalues[0]),
            (constants.S3003_ID, constants.S3003_IAT, temp_sensor_argvalues[1]),
            (constants.S3003_ID, constants.S3003_IAT, temp_sensor_argvalues[2]),
        ),
    )
    def test_iat(self, version, index, values):
        self.s300.version = version
        self.s300.data6[index] = values[0]

        assert self.s300.iat["celsius"] == values[1]
        assert self.s300.iat["fahrenheit"] == values[2]

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, channel, result",
        (
            (
                constants.S3003_ID,
                constants.S3003_AN0_1,
                constants.S3003_AN0_2,
                3,
                52,
                0,
                1.0009765625,
            ),
            (
                constants.S3003_ID,
                constants.S3003_AN1_1,
                constants.S3003_AN1_2,
                3,
                52,
                1,
                1.0009765625,
            ),
            (
                constants.S3003_ID,
                constants.S3003_AN2_1,
                constants.S3003_AN2_2,
                3,
                52,
                2,
                1.0009765625,
            ),
            (
                constants.S3003_ID,
                constants.S3003_AN3_1,
                constants.S3003_AN3_2,
                3,
                52,
                3,
                1.0009765625,
            ),
            (
                constants.S3003_ID,
                constants.S3003_AN4_1,
                constants.S3003_AN4_2,
                3,
                52,
                4,
                1.0009765625,
            ),
            (
                constants.S3003_ID,
                constants.S3003_AN5_1,
                constants.S3003_AN5_2,
                3,
                52,
                5,
                1.0009765625,
            ),
            (
                constants.S3003_ID,
                constants.S3003_AN6_1,
                constants.S3003_AN6_2,
                3,
                52,
                6,
                1.0009765625,
            ),
            (
                constants.S3003_ID,
                constants.S3003_AN7_1,
                constants.S3003_AN7_2,
                3,
                52,
                7,
                1.0009765625,
            ),
        ),
    )
    def test_analog_input(
        self, version, index1, index2, value1, value2, channel, result
    ):
        self.s300.version = version
        self.s300.data5[index2] = value2
        self.s300.data5[index1] = value1

        assert self.s300.analog_input(channel) == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, constants.S3003_MIL, None, False),
            (constants.S3003_ID, constants.S3003_MIL, 0, False),
            (constants.S3003_ID, constants.S3003_MIL, 32, True),
        ),
    )
    def test_mil(self, version, index, value, result):
        self.s300.version = version
        self.s300.data6[index] = value

        assert self.s300.mil == result

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result",
        (
            (
                constants.S3003_ID,
                constants.S3003_MAP1,
                constants.S3003_MAP2,
                100,
                0,
                {"bar": 1.0, "mbar": 1000.0, "psi": 14.503773773},
            ),
        ),
    )
    def test_map(self, version, index1, index2, value1, value2, result):
        self.s300.version = version
        self.s300.data6[index1] = value1
        self.s300.data6[index2] = value2

        assert self.s300.map == result

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result",
        (
            (
                constants.S3003_ID,
                constants.S3003_SERIAL1,
                constants.S3003_SERIAL2,
                210,
                4,
                1234,
            ),
        ),
    )
    def test_serial(self, version, index1, index2, value1, value2, result):
        self.s300.version = version
        self.s300.data4[index1] = value1
        self.s300.data4[index2] = value2

        assert self.s300.serial == result

    @pytest.mark.parametrize(
        "version, index1, index2, value1, value2, result",
        (
            (
                constants.S3003_ID,
                constants.S3003_FIRM1,
                constants.S3003_FIRM2,
                10,
                0,
                "10.00",
            ),
        ),
    )
    def test_firmware(self, version, index1, index2, value1, value2, result):
        self.s300.version = version
        self.s300.data4[index1] = value1
        self.s300.data4[index2] = value2

        assert self.s300.firmware == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.S3003_ID, constants.S3003_SCS, 0, False),
            (constants.S3003_ID, constants.S3003_SCS, 32, True),
        ),
    )
    def test_scs(self, version, index, value, result):
        self.s300.version = version
        self.s300.data6[index] = value

        assert self.s300.scs == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.S3003_ID, constants.S3003_BKSW, 0, False),
            (constants.S3003_ID, constants.S3003_BKSW, 2, True),
        ),
    )
    def test_bksw(self, version, index, value, result):
        self.s300.version = version
        self.s300.data6[index] = value

        assert self.s300.bksw == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.S3003_ID, constants.S3003_VTP, 0, False),
            (constants.S3003_ID, constants.S3003_VTP, 1, True),
        ),
    )
    def test_vtp(self, version, index, value, result):
        self.s300.version = version
        self.s300.data6[index] = value

        assert self.s300.vtp == result

    @pytest.mark.parametrize(
        "version, index, value, result",
        (
            (None, 0, None, False),
            (constants.S3003_ID, constants.S3003_VTS, 0, False),
            (constants.S3003_ID, constants.S3003_VTS, 1, True),
        ),
    )
    def test_vts(self, version, index, value, result):
        self.s300.version = version
        self.s300.data6[index] = value

        assert self.s300.vts == result

    @pytest.mark.parametrize(
        "version, vtp_index, vts_index, vtp_value, vts_value, result",
        (
            (None, 0, 0, 0, 0, "off"),
            (constants.S3003_ID, constants.S3003_VTP, constants.S3003_VTS, 1, 1, "on"),
            (
                constants.S3003_ID,
                constants.S3003_VTP,
                constants.S3003_VTS,
                1,
                0,
                "malfunction",
            ),
            (
                constants.S3003_ID,
                constants.S3003_VTP,
                constants.S3003_VTS,
                0,
                1,
                "malfunction",
            ),
            (constants.S3003_ID, constants.S3003_VTP, constants.S3003_VTS, 0, 0, "off"),
        ),
    )
    def test_vtec(self, version, vtp_index, vts_index, vtp_value, vts_value, result):
        self.s300.version = version
        self.s300.data6[vtp_index] = vtp_value
        self.s300.data6[vts_index] = vts_value

        assert self.s300.vtec == result
