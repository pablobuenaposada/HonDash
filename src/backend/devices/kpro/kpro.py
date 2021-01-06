import threading

import usb.core
import usb.util
from numpy import interp

from backend.devices.ecu_utils import (
    establish_connection,
    find_device,
    get_value_from_ecu,
)
from backend.devices.formula import Formula
from backend.devices.kpro import constants

MAX_CONNECTION_RETRIES = 10
USB_IDS = (
    {
        "version": constants.KPRO23_ID,
        "id_vendor": constants.KPRO23_ID_VENDOR,
        "id_product": constants.KPRO23_ID_PRODUCT,
    },
    {
        "version": constants.KPRO4_ID,
        "id_vendor": constants.KPRO4_ID_VENDOR,
        "id_product": constants.KPRO4_ID_PRODUCT,
    },
)


class Kpro:
    NAME = "K-Pro"

    def __init__(self):
        self.data0 = self.data1 = self.data2 = self.data3 = self.data4 = self.data5 = []
        self.kpro_device = self.version = self.entry_point = None
        self.status = False

        self.find_and_connect()

    def find_and_connect(self):
        connection_tries = 0

        while not self.status and connection_tries < MAX_CONNECTION_RETRIES:
            connection_tries += 1
            # let's see if we can find a recognized kpro device
            self.kpro_device, self.version = find_device(USB_IDS)

            if self.kpro_device:  # if kpro device is found
                try:
                    self.entry_point = establish_connection(self.kpro_device)
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
        data0 = data1 = data2 = data3 = data5 = []

        if version == constants.KPRO4_ID:
            entry_point.write("\x40")
            data4 = device.read(0x82, 1000)  # kpro v4
        else:
            entry_point.write("\x40")
            data4 = device.read(0x81, 1000)  # kpro v2 & v3

        entry_point.write("\x60")
        if version == constants.KPRO23_ID:
            data0 = device.read(0x81, 1000)  # kpro v2 & v3
        elif version == constants.KPRO4_ID:
            data0 = device.read(0x82, 1000)  # kpro v4

        entry_point.write("\x61")
        # found on kpro2 that sometimes len=44, normally 16
        if version == constants.KPRO23_ID:
            data1 = device.read(0x81, 1000)  # kpro v2 & v3
        elif version == constants.KPRO4_ID:
            data1 = device.read(0x82, 1000)  # kpro v4

        entry_point.write("\x62")
        if version == constants.KPRO23_ID:
            data2 = device.read(0x81, 1000)  # kpro v2 & v3
        elif version == constants.KPRO4_ID:
            data2 = device.read(0x82, 1000)  # kpro v4

        if version == constants.KPRO4_ID:
            entry_point.write("\x65")
            data3 = device.read(0x82, 128, 1000)  # kpro v4
        else:  # for v3 only, v2 will not return anything meaningful
            entry_point.write("\xb0")
            data5 = device.read(0x81, 1000)

        return data0, data1, data2, data3, data4, data5

    def _update(self):
        while self.status:
            try:
                (
                    self.data0,
                    self.data1,
                    self.data2,
                    self.data3,
                    self.data4,
                    self.data5,
                ) = self._read_from_device(
                    self.version, self.kpro_device, self.entry_point
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
            constants.KPRO23_ID: constants.KPRO23_BAT,
            constants.KPRO4_ID: constants.KPRO4_BAT,
        }
        return get_value_from_ecu(self.version, indexes, self.data1) * 0.1

    @property
    def eth(self):
        """
        Ethanol content
        return unit: per cent
        """
        indexes = {
            constants.KPRO4_ID: constants.KPRO4_ETH,
        }
        return get_value_from_ecu(self.version, indexes, self.data3)

    @property
    def flt(self):
        """Fuel temperature
        TODO: RETURN {"celsius": 0, "fahrenheit": 0} if fails
        """
        indexes = {constants.KPRO4_ID: constants.KPRO4_FLT}
        flt_celsius = get_value_from_ecu(self.version, indexes, self.data3)
        flt_fahrenheit = Formula.celsius_to_fahrenheit(flt_celsius)
        return {"celsius": flt_celsius, "fahrenheit": flt_fahrenheit}

    @property
    def o2(self):
        """Oxygen sensor"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_AFR1,
            constants.KPRO4_ID: constants.KPRO4_AFR1,
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_AFR2,
            constants.KPRO4_ID: constants.KPRO4_AFR2,
        }
        try:
            o2_lambda = 32768.0 / (
                256 * get_value_from_ecu(self.version, indexes_2, self.data0)
                + get_value_from_ecu(self.version, indexes_1, self.data0)
            )
        except ZeroDivisionError:  # something happen collecting the value then return 0
            return {"afr": 0, "lambda": 0}
        o2_afr = o2_lambda * 14.7
        return {"afr": o2_afr, "lambda": o2_lambda}

    @property
    def tps(self):
        """
        Throttle position sensor
        return unit: 0-100%
        """
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_TPS,
            constants.KPRO4_ID: constants.KPRO4_TPS,
        }
        return int(
            interp(
                get_value_from_ecu(self.version, indexes, self.data0),
                [21, 229],
                [0, 100],
            )
        )

    @property
    def vss(self):
        """Vehicle speed sensor"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_VSS,
            constants.KPRO4_ID: constants.KPRO4_VSS,
        }
        vss_kmh = get_value_from_ecu(self.version, indexes, self.data0)
        vss_mph = Formula.kmh_to_mph(vss_kmh)
        return {"kmh": vss_kmh, "mph": int(vss_mph)}

    @property
    def rpm(self):
        """
        Revs per minute
        return unit: revs per minute
        """
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_RPM1,
            constants.KPRO4_ID: constants.KPRO4_RPM1,
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_RPM2,
            constants.KPRO4_ID: constants.KPRO4_RPM2,
        }
        return int(
            (
                (256 * get_value_from_ecu(self.version, indexes_2, self.data0))
                + get_value_from_ecu(self.version, indexes_1, self.data0)
            )
            * 0.25
        )

    @property
    def cam(self):
        """
        VTC cam angle
        return units: degrees
        """
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_CAM,
            constants.KPRO4_ID: constants.KPRO4_CAM,
        }
        data_from_kpro = get_value_from_ecu(self.version, indexes, self.data0, None)
        if data_from_kpro is not None:
            return (data_from_kpro - 40) * 0.5
        else:
            return 0

    @property
    def ect(self):
        """Engine coolant temperature"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_ECT,
            constants.KPRO4_ID: constants.KPRO4_ECT,
        }
        data_from_kpro = get_value_from_ecu(
            self.version, indexes, self.data1, {"celsius": 0, "fahrenheit": 0}
        )
        if isinstance(data_from_kpro, int):
            return Formula.kpro_temp(data_from_kpro)
        else:
            return data_from_kpro

    @property
    def iat(self):
        """Intake air temperature"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_IAT,
            constants.KPRO4_ID: constants.KPRO4_IAT,
        }
        data_from_kpro = get_value_from_ecu(
            self.version, indexes, self.data1, {"celsius": 0, "fahrenheit": 0}
        )
        if isinstance(data_from_kpro, int):
            return Formula.kpro_temp(data_from_kpro)
        else:
            return data_from_kpro

    @property
    def gear(self):
        """Gear"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_GEAR,
            constants.KPRO4_ID: constants.KPRO4_GEAR,
        }
        return get_value_from_ecu(self.version, indexes, self.data0)

    @property
    def eps(self):
        """Electric power steering"""
        mask = 0x20
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_EPS,
            constants.KPRO4_ID: constants.KPRO4_EPS,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def scs(self):
        """Service connector"""
        mask = 0x10
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_SCS,
            constants.KPRO4_ID: constants.KPRO4_SCS,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def rvslck(self):
        """Reverse gear lock"""
        mask = 0x01
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_RVSLCK,
            constants.KPRO4_ID: constants.KPRO4_RVSLCK,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def bksw(self):
        """Brake switch"""
        mask = 0x02
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_BKSW,
            constants.KPRO4_ID: constants.KPRO4_BKSW,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def acsw(self):
        """A/C switch"""
        mask = 0x04
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_ACSW,
            constants.KPRO4_ID: constants.KPRO4_ACSW,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def accl(self):
        """A/C clutch"""
        mask = 0x08
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_ACCL,
            constants.KPRO4_ID: constants.KPRO4_ACCL,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def flr(self):
        """Fuel relay"""
        mask = 0x40
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_FLR,
            constants.KPRO4_ID: constants.KPRO4_FLR,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def fanc(self):
        """Fan switch"""
        mask = 0x80
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_FANC,
            constants.KPRO4_ID: constants.KPRO4_FANC,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data0) & mask)

    @property
    def map(self):
        """Manifold absolute pressure"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_MAP,
            constants.KPRO4_ID: constants.KPRO4_MAP,
        }
        data_from_kpro = get_value_from_ecu(
            self.version, indexes, self.data0, {"bar": 0, "mbar": 0, "psi": 0}
        )
        if isinstance(data_from_kpro, int):
            map_bar = data_from_kpro / 100.0
            map_mbar = map_bar * 1000
            map_psi = Formula.bar_to_psi(map_bar)
            return {"bar": map_bar, "mbar": map_mbar, "psi": map_psi}
        return data_from_kpro

    @property
    def mil(self):
        """Malfunction indicator light also known as check engine light"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_MIL,
            constants.KPRO4_ID: constants.KPRO4_MIL,
        }
        if self.version == constants.KPRO23_ID:
            data_from_kpro = get_value_from_ecu(self.version, indexes, self.data0)
            if data_from_kpro == 9:
                return True
            return False
        elif self.version == constants.KPRO4_ID:
            data_from_kpro = get_value_from_ecu(self.version, indexes, self.data3)
            if data_from_kpro >= 36:
                return True
            return False
        return False

    @property
    def ecu_type(self):
        """Model of ECU"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_ECU_TYPE,
            constants.KPRO4_ID: constants.KPRO4_ECU_TYPE,
        }
        data_from_kpro = get_value_from_ecu(self.version, indexes, self.data4)
        if data_from_kpro == 3:  # TODO the rest of ecu types
            return "RSX - PRB"
        return "unknown"

    @property
    def ign(self):
        """Ignition status"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_IGN,
            constants.KPRO4_ID: constants.KPRO4_IGN,
        }
        data_from_kpro = get_value_from_ecu(self.version, indexes, self.data4, 0)

        if data_from_kpro == 1:
            return True
        return False

    @property
    def serial(self):
        """K-Pro serial number"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_SERIAL1,
            constants.KPRO4_ID: constants.KPRO4_SERIAL1,
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_SERIAL2,
            constants.KPRO4_ID: constants.KPRO4_SERIAL2,
        }
        return (
            256 * get_value_from_ecu(self.version, indexes_2, self.data4, 0)
        ) + get_value_from_ecu(self.version, indexes_1, self.data4, 0)

    @property
    def firmware(self):
        """Firmware version"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_FIRM1,
            constants.KPRO4_ID: constants.KPRO4_FIRM1,
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_FIRM2,
            constants.KPRO4_ID: constants.KPRO4_FIRM2,
        }

        return "{}.{:02d}".format(
            get_value_from_ecu(self.version, indexes_2, self.data4, 0),
            get_value_from_ecu(self.version, indexes_1, self.data4, 0),
        )

    def analog_input(self, channel):
        """
        Analog inputs
        return unit: volts
        """
        indexes_1 = (
            {
                constants.KPRO23_ID: constants.KPRO3_AN0_1,
                constants.KPRO4_ID: constants.KPRO4_AN0_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN1_1,
                constants.KPRO4_ID: constants.KPRO4_AN1_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN2_1,
                constants.KPRO4_ID: constants.KPRO4_AN2_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN3_1,
                constants.KPRO4_ID: constants.KPRO4_AN3_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN4_1,
                constants.KPRO4_ID: constants.KPRO4_AN4_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN5_1,
                constants.KPRO4_ID: constants.KPRO4_AN5_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN6_1,
                constants.KPRO4_ID: constants.KPRO4_AN6_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN7_1,
                constants.KPRO4_ID: constants.KPRO4_AN7_1,
            },
        )
        indexes_2 = (
            {
                constants.KPRO23_ID: constants.KPRO3_AN0_2,
                constants.KPRO4_ID: constants.KPRO4_AN0_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN1_2,
                constants.KPRO4_ID: constants.KPRO4_AN1_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN2_2,
                constants.KPRO4_ID: constants.KPRO4_AN2_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN3_2,
                constants.KPRO4_ID: constants.KPRO4_AN3_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN4_2,
                constants.KPRO4_ID: constants.KPRO4_AN4_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN5_2,
                constants.KPRO4_ID: constants.KPRO4_AN5_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN6_2,
                constants.KPRO4_ID: constants.KPRO4_AN6_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN7_2,
                constants.KPRO4_ID: constants.KPRO4_AN7_2,
            },
        )

        if self.version == constants.KPRO4_ID:
            return interp(
                (
                    256
                    * get_value_from_ecu(
                        self.version, indexes_1[channel], self.data3, 0
                    )
                )
                + get_value_from_ecu(self.version, indexes_2[channel], self.data3, 0),
                [0, 4096],
                [0, 5],
            )
        elif self.version == constants.KPRO23_ID:
            return interp(
                (
                    256
                    * get_value_from_ecu(
                        self.version, indexes_1[channel], self.data5, 0
                    )
                )
                + get_value_from_ecu(self.version, indexes_2[channel], self.data5, 0),
                [0, 1024],
                [0, 5],
            )
        else:
            return 0
