import threading

import usb.core
import usb.util
from numpy import interp

from devices.formula import Formula
from devices.kpro import constants

MAX_CONNECTION_RETRIES = 10


class Kpro:
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
            self.kpro_device, self.version = self._find_device()

            if self.kpro_device:  # if kpro device is found
                try:
                    self.entry_point = self._establish_connection(self.kpro_device)
                except usb.core.USBError:
                    # if there's an error while connecting to the usb device we just want to try again
                    #  so let's ensure that we keep in the while loop
                    self.status = False
                else:
                    self.status = True
                    # connection is made, try to get the latest data forever
                    threading.Thread(target=self._update).start()

    @staticmethod
    def _find_device():
        device = version = None
        # kpro v2 and v3
        if usb.core.find(
            idVendor=constants.KPRO23_ID_VENDOR, idProduct=constants.KPRO23_ID_PRODUCT,
        ):
            device = usb.core.find(
                idVendor=constants.KPRO23_ID_VENDOR,
                idProduct=constants.KPRO23_ID_PRODUCT,
            )
            version = constants.KPRO23_ID
        # kpro v4
        elif usb.core.find(
            idVendor=constants.KPRO4_ID_VENDOR, idProduct=constants.KPRO4_ID_PRODUCT,
        ):
            device = usb.core.find(
                idVendor=constants.KPRO4_ID_VENDOR,
                idProduct=constants.KPRO4_ID_PRODUCT,
            )
            version = constants.KPRO4_ID

        return device, version

    @staticmethod
    def _establish_connection(device):
        device.set_configuration()
        cfg = device.get_active_configuration()
        intf = cfg[(0, 0)]
        entry_point = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_OUT,
        )
        return entry_point

    def _update(self):
        while self.status:
            try:
                if self.version == constants.KPRO4_ID:
                    self.entry_point.write("\x40")
                    self.data4 = self.kpro_device.read(0x82, 1000)  # kpro v4
                else:
                    self.entry_point.write("\x40")
                    self.data4 = self.kpro_device.read(0x81, 1000)  # kpro v2 & v3

                self.entry_point.write("\x60")
                if self.version == constants.KPRO23_ID:
                    self.data0 = self.kpro_device.read(0x81, 1000)  # kpro v2 & v3
                elif self.version == constants.KPRO4_ID:
                    self.data0 = self.kpro_device.read(0x82, 1000)  # kpro v4

                self.entry_point.write("\x61")
                # found on kpro2 that sometimes len=44, normally 16
                if self.version == constants.KPRO23_ID:
                    self.data1 = self.kpro_device.read(0x81, 1000)  # kpro v2 & v3
                elif self.version == constants.KPRO4_ID:
                    self.data1 = self.kpro_device.read(0x82, 1000)  # kpro v4

                self.entry_point.write("\x62")
                if self.version == constants.KPRO23_ID:
                    temp = self.kpro_device.read(0x81, 1000)  # kpro v2 & v3
                    if len(temp) == 68:
                        self.data2 = temp
                elif self.version == constants.KPRO4_ID:
                    temp = self.kpro_device.read(0x82, 1000)  # kpro v4
                    if len(temp) == 25:
                        self.data2 = temp

                if self.version == constants.KPRO4_ID:
                    self.entry_point.write("\x65")
                    self.data3 = self.kpro_device.read(0x82, 128, 1000)  # kpro v4
                else:  # for v3 only, v2 will not return anything meaningful
                    self.entry_point.write("\xb0")
                    self.data5 = self.kpro_device.read(0x81, 1000)

            except usb.core.USBError as e:
                # error 60 (operation timed out), just continue to try again
                if e.args[0] == 60:
                    pass
                else:
                    # if there's an error while gathering the data, stop the update and try to reconnect usb again
                    self.status = False  # redundant?
                    self.__init__()

    @property
    def bat(self):
        """
        Battery voltage
        return unit: volts
        """
        try:
            if self.version == constants.KPRO23_ID:
                return self.data1[constants.KPRO23_BAT] * 0.1
            elif self.version == constants.KPRO4_ID:
                return self.data1[constants.KPRO4_BAT] * 0.1
        except IndexError:
            return 0

    @property
    def eth(self):
        """
        Ethanol content
        return unit: per cent
        """
        try:
            if self.version == constants.KPRO4_ID:
                return self.data3[constants.KPRO4_ETH]
        except IndexError:
            return 0

    @property
    def flt(self):
        """Fuel temperature"""
        try:
            if self.version == constants.KPRO4_ID:
                index = constants.KPRO4_FLT
            else:
                return {"celsius": 0, "fahrenheit": 0}
            flt_celsius = self.data3[index]
            flt_fahrenheit = Formula.celsius_to_fahrenheit(flt_celsius)
            return {"celsius": flt_celsius, "fahrenheit": flt_fahrenheit}
        except IndexError:
            return 0

    @property
    def o2(self):
        """Oxygen sensor"""
        try:
            if self.version == constants.KPRO23_ID:
                index_1 = constants.KPRO23_AFR2
                index_2 = constants.KPRO23_AFR1
            elif self.version == constants.KPRO4_ID:
                index_1 = constants.KPRO4_AFR2
                index_2 = constants.KPRO4_AFR1
            else:
                return {"afr": 0, "lambda": 0}
            o2_lambda = 32768.0 / ((256 * self.data0[index_1]) + self.data0[index_2])
            o2_afr = o2_lambda * 14.7
            return {"afr": o2_afr, "lambda": o2_lambda}
        except (IndexError, ZeroDivisionError):
            return {"afr": 0, "lambda": 0}

    @property
    def tps(self):
        """
        Throttle position sensor
        return unit: 0-100%
        """
        try:
            if self.version == constants.KPRO23_ID:
                return int(
                    interp(self.data0[constants.KPRO23_TPS], [21, 229], [0, 100])
                )
            elif self.version == constants.KPRO4_ID:
                return int(interp(self.data0[constants.KPRO4_TPS], [21, 229], [0, 100]))
            else:
                return 0
        except IndexError:
            return 0

    @property
    def vss(self):
        """Vehicle speed sensor"""
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_VSS
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_VSS
            else:
                return {"kmh": 0, "mph": 0}
            vss_kmh = self.data0[index]
            vss_mph = Formula.kmh_to_mph(vss_kmh)
            return {"kmh": vss_kmh, "mph": int(vss_mph)}
        except IndexError:
            return {"kmh": 0, "mph": 0}

    @property
    def rpm(self):
        """
        Revs per minute
        return unit: revs per minute
        """
        try:
            if self.version == constants.KPRO23_ID:
                return int(
                    (
                        (256 * self.data0[constants.KPRO23_RPM2])
                        + self.data0[constants.KPRO23_RPM1]
                    )
                    * 0.25
                )
            elif self.version == constants.KPRO4_ID:
                return int(
                    (
                        (256 * self.data0[constants.KPRO4_RPM2])
                        + self.data0[constants.KPRO4_RPM1]
                    )
                    * 0.25
                )
        except IndexError:
            return 0

    @property
    def cam(self):
        """
        VTC cam angle
        return units: degrees
        """
        try:
            if self.version == constants.KPRO23_ID:
                return (self.data0[constants.KPRO23_CAM] - 40) * 0.5
            elif self.version == constants.KPRO4_ID:
                return (self.data0[constants.KPRO4_CAM] - 40) * 0.5
        except IndexError:
            return 0

    @property
    def ect(self):
        """Engine coolant temperature"""
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_ECT
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_ECT
            else:
                return {"celsius": 0, "fahrenheit": 0}
            return Formula.kpro_temp(self.data1[index])
        except IndexError:
            return {"celsius": 0, "fahrenheit": 0}

    @property
    def iat(self):
        """Intake air temperature"""
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_IAT
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_IAT
            else:
                return {"celsius": 0, "fahrenheit": 0}
            return Formula.kpro_temp(self.data1[index])
        except IndexError:
            return {"celsius": 0, "fahrenheit": 0}

    @property
    def gear(self):
        """Gear"""
        try:
            if self.version == constants.KPRO23_ID:
                gear = self.data0[constants.KPRO23_GEAR]
            elif self.version == 4:
                gear = self.data0[constants.KPRO4_GEAR]
            else:
                return "N"

            if gear == 0:
                return "N"
            else:
                return gear
        except IndexError:
            return "N"

    @property
    def eps(self):
        """Electric power steering"""
        mask = 0x20
        if self.version == constants.KPRO23_ID:
            return bool(self.data0[constants.KPRO23_EPS] & mask)
        elif self.version == constants.KPRO4_ID:
            return bool(self.data0[constants.KPRO4_EPS] & mask)
        else:
            return False

    @property
    def scs(self):
        """Service connector"""
        mask = 0x10
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_SCS] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_SCS] & mask)
            else:
                return False
        except IndexError:
            return False

    @property
    def rvslck(self):
        """Reverse gear lock"""
        mask = 0x01
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_RVSLCK] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_RVSLCK] & mask)
            else:
                return False
        except IndexError:
            return False

    @property
    def bksw(self):
        """Brake switch"""
        mask = 0x02
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_BKSW] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_BKSW] & mask)
            else:
                return False
        except IndexError:
            return False

    @property
    def acsw(self):
        """A/C switch"""
        mask = 0x04
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_ACSW] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_ACSW] & mask)
        except IndexError:
            return False

    @property
    def accl(self):
        """A/C clutch"""
        mask = 0x08
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_ACCL] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_ACCL] & mask)
        except IndexError:
            return False

    @property
    def flr(self):
        """Fuel relay"""
        mask = 0x40
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_FLR] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_FLR] & mask)
        except IndexError:
            return False

    @property
    def fanc(self):
        """Fan switch"""
        mask = 0x80
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_FANC] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_FANC] & mask)
        except IndexError:
            return False

    @property
    def map(self):
        """Manifold absolute pressure"""
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_MAP
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_MAP
            else:
                return {"bar": 0, "mbar": 0, "psi": 0}
            map_bar = self.data0[index] / 100.0
            map_mbar = map_bar * 1000
            map_psi = Formula.bar_to_psi(map_bar)
            return {"bar": map_bar, "mbar": map_mbar, "psi": map_psi}
        except IndexError:
            return {"bar": 0, "mbar": 0, "psi": 0}

    @property
    def mil(self):
        """Malfunction indicator light also known as check engine light"""
        try:
            if self.version == constants.KPRO23_ID:
                mil = self.data0[constants.KPRO23_MIL]
                if mil == 9:
                    return True
                elif mil == 1:
                    return False
            elif self.version == constants.KPRO4_ID:
                mil = self.data3[constants.KPRO4_MIL]
                if mil >= 36:
                    return True
                else:
                    return False
            else:
                return False
        except IndexError:
            return False

    @property
    def ecu_type(self):
        """Model of ECU"""
        try:
            if self.version == constants.KPRO23_ID:
                type = self.data4[constants.KPRO23_ECU_TYPE]
            elif self.version == constants.KPRO4_ID:
                type = self.data4[constants.KPRO4_ECU_TYPE]
            else:
                return "unknown"

            if type == 3:  # TODO the rest of ecu types
                return "RSX - PRB"
            else:
                return "unknown"
        except IndexError:
            return "unknown"

    @property
    def ign(self):
        """Ignition status"""
        try:
            if self.version == constants.KPRO23_ID:
                ign = self.data4[constants.KPRO23_IGN]
            elif self.version == constants.KPRO4_ID:
                ign = self.data4[constants.KPRO4_IGN]
            else:
                return False

            if ign == 1:
                return True
            else:
                return False
        except IndexError:
            return False

    @property
    def serial(self):
        try:
            if self.version == constants.KPRO23_ID:
                serial1 = self.data4[constants.KPRO23_SERIAL1]
                serial2 = self.data4[constants.KPRO23_SERIAL2]
            elif self.version == constants.KPRO4_ID:
                serial1 = self.data4[constants.KPRO4_SERIAL1]
                serial2 = self.data4[constants.KPRO4_SERIAL2]
            else:
                return 0

            return (256 * serial2) + serial1
        except IndexError:
            return 0

    @property
    def firmware(self):
        """Firmware version"""
        try:
            if self.version == constants.KPRO23_ID:
                firm1 = self.data4[constants.KPRO23_FIRM1]
                firm2 = self.data4[constants.KPRO23_FIRM2]
            elif self.version == constants.KPRO4_ID:
                firm1 = self.data4[constants.KPRO4_FIRM1]
                firm2 = self.data4[constants.KPRO4_FIRM2]
            else:
                return 0

            return "{}.{:02d}".format(firm2, firm1)
        except IndexError:
            return 0

    def analog_input(self, channel):
        """
        Analog inputs
        return unit: volts
        """
        if self.version == constants.KPRO4_ID:
            if channel == 0:
                index_1 = constants.KPRO4_AN0_1
                index_2 = constants.KPRO4_AN0_2
            elif channel == 1:
                index_1 = constants.KPRO4_AN1_1
                index_2 = constants.KPRO4_AN1_2
            elif channel == 2:
                index_1 = constants.KPRO4_AN2_1
                index_2 = constants.KPRO4_AN2_2
            elif channel == 3:
                index_1 = constants.KPRO4_AN3_1
                index_2 = constants.KPRO4_AN3_2
            elif channel == 4:
                index_1 = constants.KPRO4_AN4_1
                index_2 = constants.KPRO4_AN4_2
            elif channel == 5:
                index_1 = constants.KPRO4_AN5_1
                index_2 = constants.KPRO4_AN5_2
            elif channel == 6:
                index_1 = constants.KPRO4_AN6_1
                index_2 = constants.KPRO4_AN6_2
            elif channel == 7:
                index_1 = constants.KPRO4_AN7_1
                index_2 = constants.KPRO4_AN7_2
            else:
                return 0

            try:
                return interp(
                    (256 * self.data3[index_1]) + self.data3[index_2], [0, 4096], [0, 5]
                )
            except IndexError:
                return 0

        elif self.version == constants.KPRO23_ID:
            if channel == 0:
                index_1 = constants.KPRO3_AN0_1
                index_2 = constants.KPRO3_AN0_2
            elif channel == 1:
                index_1 = constants.KPRO3_AN1_1
                index_2 = constants.KPRO3_AN1_2
            elif channel == 2:
                index_1 = constants.KPRO3_AN2_1
                index_2 = constants.KPRO3_AN2_2
            elif channel == 3:
                index_1 = constants.KPRO3_AN3_1
                index_2 = constants.KPRO3_AN3_2
            elif channel == 4:
                index_1 = constants.KPRO3_AN4_1
                index_2 = constants.KPRO3_AN4_2
            elif channel == 5:
                index_1 = constants.KPRO3_AN5_1
                index_2 = constants.KPRO3_AN5_2
            elif channel == 6:
                index_1 = constants.KPRO3_AN6_1
                index_2 = constants.KPRO3_AN6_2
            elif channel == 7:
                index_1 = constants.KPRO3_AN7_1
                index_2 = constants.KPRO3_AN7_2
            else:
                return 0

            try:
                return interp(
                    (256 * self.data5[index_1]) + self.data5[index_2], [0, 1024], [0, 5]
                )
            except IndexError:
                return 0
        else:
            return 0
