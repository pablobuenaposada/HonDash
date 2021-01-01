import threading

import usb
from numpy import interp

from backend.devices.ecu_utils import (
    establish_connection,
    find_device,
    get_value_from_ecu,
)
from backend.devices.formula import Formula
from backend.devices.s300 import constants

MAX_CONNECTION_RETRIES = 10
USB_IDS = (
    {
        "version": constants.S3003_ID,
        "id_vendor": constants.S3003_ID_VENDOR,
        "id_product": constants.S3003_ID_PRODUCT,
    },
)


class S300:
    NAME = "S300"

    def __init__(self):
        self.data4 = self.data5 = self.data6 = []
        self.device = self.version = self.entry_point = None
        self.status = False

        self.find_and_connect()

    def find_and_connect(self):
        connection_tries = 0

        while not self.status and connection_tries < MAX_CONNECTION_RETRIES:
            connection_tries += 1
            # let's see if we can find a recognized s300 device
            self.device, self.version = find_device(USB_IDS)

            if self.device:  # if s300 device is found
                try:
                    self.entry_point = establish_connection(self.device)
                except usb.core.USBError:
                    # if there's an error while connecting to the usb device we just want to try again
                    #  so let's ensure that we keep in the while loop
                    self.status = False
                else:
                    self.status = True
                    # connection is made, try to get the latest data forever
                    threading.Thread(target=self._update).start()

    @staticmethod
    def _read_from_device(version, device, entry_point):
        entry_point.write(b"\x90")
        data6 = device.read(0x82, 1000, 1000)

        entry_point.write(b"\xB0")
        data5 = device.read(0x82, 128, 1000)

        entry_point.write(b"\x40")
        data4 = device.read(0x82, 1000)

        return data4, data5, data6

    def _update(self):
        while self.status:
            try:
                self.data4, self.data5, self.data6 = self._read_from_device(
                    self.version, self.device, self.entry_point
                )

            except usb.core.USBError as e:
                # error 60 (operation timed out), just continue to try again
                if e.args[0] != 60:
                    # if there's an error while gathering the data, stop the update and try to reconnect usb again
                    self.status = False  # redundant?
                    self.__init__()

    @property
    def bat(self):
        """
        Battery voltage
        return unit: volts
        """
        indexes = {
            constants.S3003_ID: constants.S3003_BAT,
        }
        return get_value_from_ecu(self.version, indexes, self.data6) * 0.1 - 0.5

    @property
    def tps(self):
        """
        Throttle position sensor
        return unit: 0-100%
        """
        indexes = {
            constants.S3003_ID: constants.S3003_TPS,
        }
        return int(
            interp(
                get_value_from_ecu(self.version, indexes, self.data6),
                [25, 255],
                [0, 115],
            )
        )

    @property
    def rpm(self):
        """
        Revs per minute
        return unit: revs per minute
        """
        indexes_1 = {
            constants.S3003_ID: constants.S3003_RPM1,
        }
        indexes_2 = {
            constants.S3003_ID: constants.S3003_RPM2,
        }
        return int(
            (256 * get_value_from_ecu(self.version, indexes_2, self.data6))
            + get_value_from_ecu(self.version, indexes_1, self.data6)
        )

    @property
    def o2(self):
        """Oxygen sensor"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_AFR,
        }
        o2_lambda = (
            get_value_from_ecu(self.version, indexes_1, self.data6) - 1.1588
        ) / 126.35
        o2_afr = o2_lambda * 14.7
        return {"afr": o2_afr, "lambda": o2_lambda}

    @property
    def fanc(self):
        """Fan switch"""
        mask = 0x80
        indexes = {
            constants.S3003_ID: constants.S3003_FANC,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def bksw(self):
        """Brake switch"""
        mask = 0x02
        indexes = {
            constants.S3003_ID: constants.S3003_BKSW,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def scs(self):
        """Service connector"""
        mask = 0x10
        indexes = {
            constants.S3003_ID: constants.S3003_SCS,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def eth(self):
        """
        Ethanol content
        return unit: per cent
        """
        indexes = {
            constants.S3003_ID: constants.S3003_ETH,
        }
        return get_value_from_ecu(self.version, indexes, self.data5)

    @property
    def flt(self):
        """Fuel temperature"""
        indexes = {constants.S3003_ID: constants.S3003_FLT}
        flt_celsius = get_value_from_ecu(self.version, indexes, self.data5) - 40
        flt_fahrenheit = Formula.celsius_to_fahrenheit(flt_celsius)
        return {"celsius": flt_celsius, "fahrenheit": flt_fahrenheit}

    @property
    def ect(self):
        """Engine coolant temperature"""
        indexes = {
            constants.S3003_ID: constants.S3003_ECT,
        }
        data_from_kpro = get_value_from_ecu(
            self.version, indexes, self.data6, {"celsius": 0, "fahrenheit": 0}
        )
        if isinstance(data_from_kpro, int):
            return Formula.kpro_temp(data_from_kpro)
        else:
            return data_from_kpro

    @property
    def gear(self):
        """Gear"""
        indexes = {
            constants.S3003_ID: constants.S3003_GEAR,
        }
        return get_value_from_ecu(self.version, indexes, self.data6)

    @property
    def vss(self):
        """Vehicle speed sensor"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_VSS1,
        }
        indexes_2 = {
            constants.S3003_ID: constants.S3003_VSS2,
        }
        try:
            vss_kmh = int(
                227125
                / (
                    256 * get_value_from_ecu(self.version, indexes_2, self.data6)
                    + get_value_from_ecu(self.version, indexes_1, self.data6)
                )
            )
        except ZeroDivisionError:
            vss_kmh = 0
        vss_mph = Formula.kmh_to_mph(vss_kmh)
        return {"kmh": vss_kmh, "mph": int(vss_mph)}

    @property
    def iat(self):
        """Intake air temperature"""
        indexes = {
            constants.S3003_ID: constants.S3003_IAT,
        }
        data_from_s300 = get_value_from_ecu(
            self.version, indexes, self.data6, {"celsius": 0, "fahrenheit": 0}
        )
        if isinstance(data_from_s300, int):
            return Formula.kpro_temp(data_from_s300)
        else:
            return data_from_s300

    @property
    def map(self):
        """Manifold absolute pressure"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_MAP1,
        }
        indexes_2 = {
            constants.S3003_ID: constants.S3003_MAP2,
        }
        data_from_s300 = (
            256 * get_value_from_ecu(self.version, indexes_2, self.data6)
        ) + get_value_from_ecu(self.version, indexes_1, self.data6)
        map_bar = data_from_s300 / 100.0
        map_mbar = map_bar * 1000
        map_psi = Formula.bar_to_psi(map_bar)
        return {"bar": map_bar, "mbar": map_mbar, "psi": map_psi}

    @property
    def serial(self):
        """S300 serial number"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_SERIAL1,
        }
        indexes_2 = {
            constants.S3003_ID: constants.S3003_SERIAL2,
        }
        return (
            256 * get_value_from_ecu(self.version, indexes_2, self.data4, 0)
        ) + get_value_from_ecu(self.version, indexes_1, self.data4, 0)

    @property
    def firmware(self):
        """Firmware version"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_FIRM1,
        }
        indexes_2 = {
            constants.S3003_ID: constants.S3003_FIRM2,
        }

        return "{}.{:02d}".format(
            get_value_from_ecu(self.version, indexes_1, self.data4),
            get_value_from_ecu(self.version, indexes_2, self.data4),
        )

    @property
    def mil(self):
        """Malfunction indicator light also known as check engine light"""
        indexes = {
            constants.S3003_ID: constants.S3003_MIL,
        }
        mask = 0x20
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    def analog_input(self, channel):
        return 0
