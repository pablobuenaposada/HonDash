import threading

import pytemperature
import usb.core
import usb.util
from numpy import interp

from devices.formula import Formula
from devices.kpro import constants


class Kpro:
    def __init__(self):
        self.data0 = []
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.data5 = []
        self.kpro_device = None
        self.version = 0

        # let's see if we can find a recognized kpro device
        while self.kpro_device is None:
            if usb.core.find(idVendor=constants.KPRO23_ID_VENDOR, idProduct=constants.KPRO23_ID_PRODUCT) is not None:  # kpro v2/3
                self.kpro_device = usb.core.find(idVendor=constants.KPRO23_ID_VENDOR, idProduct=constants.KPRO23_ID_PRODUCT)
                self.version = constants.KPRO23_ID
            elif usb.core.find(idVendor=constants.KPRO4_ID_VENDOR, idProduct=constants.KPRO4_ID_PRODUCT) is not None:  # kpro v4
                self.kpro_device = usb.core.find(idVendor=constants.KPRO4_ID_VENDOR, idProduct=constants.KPRO4_ID_PRODUCT)
                self.version = constants.KPRO4_ID

            if self.kpro_device is not None:  # if kpro device is found
                try:
                    self.kpro_device.set_configuration()
                    cfg = self.kpro_device.get_active_configuration()
                    intf = cfg[(0, 0)]
                    self.ep = usb.util.find_descriptor(
                        intf,
                        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
                    threading.Thread(target=self.update).start()
                except usb.core.USBError:
                    # if there's an error while connecting to the usb device we just want to try again so let's ensure
                    # that we keep in the while loop condition
                    self.kpro_device = None

    def update(self):
        usb_status = True
        while usb_status:
            try:
                assert self.ep is not None

                if self.version == constants.KPRO4_ID:
                    self.ep.write('\x40')
                    self.data4 = self.kpro_device.read(0x82, 1000)  # kpro v4

                self.ep.write('\x60')
                if self.version == constants.KPRO23_ID:
                    self.data0 = self.kpro_device.read(0x81, 1000)  # kpro v2 & v3
                elif self.version == constants.KPRO4_ID:
                    self.data0 = self.kpro_device.read(0x82, 1000)  # kpro v4

                self.ep.write('\x61')
                # found on kpro2 that sometimes len=44, normally 16
                if self.version == constants.KPRO23_ID:
                    self.data1 = self.kpro_device.read(0x81, 1000)  # kpro v2 & v3
                elif self.version == constants.KPRO4_ID:
                    self.data1 = self.kpro_device.read(0x82, 1000)  # kpro v4

                self.ep.write('\x62')
                if self.version == constants.KPRO23_ID:
                    temp = self.kpro_device.read(0x81, 1000)  # kpro v2 & v3
                    if len(temp) == 68:
                        self.data2 = temp
                elif self.version == constants.KPRO4_ID:
                    temp = self.kpro_device.read(0x82, 1000)  # kpro v4
                    if len(temp) == 25:
                        self.data2 = temp

                if self.version == constants.KPRO4_ID:
                    self.ep.write('\x65')
                    self.data3 = self.kpro_device.read(0x82, 128, 1000)  # kpro v4
                else:  # for v3 only, v2 will not return anything meaningful
                    self.ep.clear_halt()
                    self.ep.write('\xb0')
                    self.data5 = self.kpro_device.read(0x81, 1000)

            except usb.core.USBError as e:
                if e.args[0] == 60:  # error 60 (operation timed out), just continue to try again
                    pass
                else:
                    # if there's an error while gathering the data, stop the update and try to reconnect usb again
                    usb_status = False
                    self.__init__()

    def bat(self):
        """
        Battery voltage
        """
        # return unit: volts
        try:
            if self.version == constants.KPRO23_ID:
                return self.data1[constants.KPRO23_BAT] * 0.1
            elif self.version == constants.KPRO4_ID:
                return self.data1[constants.KPRO4_BAT] * 0.1
        except IndexError:
            return 0

    def eth(self):
        """
        Ethanol content
        """
        # return unit: per cent
        try:
            if self.version == constants.KPRO4_ID:
                return self.data3[constants.KPRO4_ETH]
        except IndexError:
            return 0

    def flt(self):
        try:
            if self.version == constants.KPRO4_ID:
                index = constants.KPRO4_FLT
            else:
                return {'celsius': 0, 'fahrenheit': 0}
            flt_celsius = self.data3[index]
            flt_fahrenheit = pytemperature.c2f(flt_celsius)
            return {'celsius': flt_celsius, 'fahrenheit': flt_fahrenheit}
        except IndexError:
            return 0

    def o2(self):
        """
        Oxygen sensor
        """
        # return unit: afr and lambda
        try:
            if self.version == constants.KPRO23_ID:
                index_1 = constants.KPRO23_AFR2
                index_2 = constants.KPRO23_AFR1
            elif self.version == constants.KPRO4_ID:
                index_1 = constants.KPRO4_AFR2
                index_2 = constants.KPRO4_AFR1
            else:
                return {'afr': 0, 'lambda': 0}
            o2_lambda = 32768.0 / ((256 * self.data0[index_1]) + self.data0[index_2])
            o2_afr = o2_lambda * 14.7
            return {'afr': o2_afr, 'lambda': o2_lambda}
        except (IndexError, ZeroDivisionError):
            return {'afr': 0, 'lambda': 0}

    def tps(self):
        """
        Throttle position sensor
        """
        # return unit: 0-100%
        try:
            if self.version == constants.KPRO23_ID:
                return int(interp(self.data0[constants.KPRO23_TPS], [21, 229], [0, 100]))
            elif self.version == constants.KPRO4_ID:
                return int(interp(self.data0[constants.KPRO4_TPS], [21, 229], [0, 100]))
            else:
                return 0
        except IndexError:
            return 0

    def vss(self):
        """
        Vehicle speed sensor
        """
        # return unit: km/h and mph
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_VSS
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_VSS
            else:
                return {'kmh': 0, 'mph': 0}
            vss_kmh = self.data0[index]
            vss_mph = Formula.kmh_to_mph(vss_kmh)
            return {'kmh': vss_kmh, 'mph': int(vss_mph)}
        except IndexError:
            return {'kmh': 0, 'mph': 0}

    def rpm(self):
        # return unit: revs. per minute
        try:
            if self.version == constants.KPRO23_ID:
                return int(((256 * self.data0[constants.KPRO23_RPM2]) + self.data0[constants.KPRO23_RPM1]) * 0.25)
            elif self.version == constants.KPRO4_ID:
                return int(((256 * self.data0[constants.KPRO4_RPM2]) + self.data0[constants.KPRO4_RPM1]) * 0.25)
        except IndexError:
            return 0

    def cam(self):
        # return units: degree
        try:
            if self.version == constants.KPRO23_ID:
                return (self.data0[constants.KPRO23_CAM] - 40) * 0.5
            elif self.version == constants.KPRO4_ID:
                return (self.data0[constants.KPRO4_CAM] - 40) * 0.5
        except IndexError:
            return 0

    def ect(self):
        """
        Engine coolant temperature
        """
        # return units: celsius and fahrenheit
        temperature = [302, 302, 298, 294, 289, 285, 282, 278, 273, 269, 266, 262, 258, 253, 249, 246, 242, 239, 235,
                       231, 226, 222, 219, 215, 212, 208, 206, 203, 201, 199, 197, 194, 192, 190, 188, 185, 183, 181,
                       179, 177, 177, 176, 174, 172, 170, 168, 167, 165, 165, 163, 161, 159, 158, 158, 156, 156, 154,
                       152, 152, 150, 149, 149, 147, 147, 145, 143, 143, 141, 141, 140, 138, 138, 136, 134, 134, 132,
                       132, 131, 131, 129, 129, 127, 127, 125, 125, 125, 123, 123, 122, 122, 122, 120, 120, 118, 118,
                       116, 116, 116, 114, 114, 113, 113, 111, 111, 111, 109, 109, 107, 107, 107, 105, 105, 104, 104,
                       102, 102, 102, 100, 100, 98, 98, 96, 96, 96, 95, 95, 93, 93, 91, 91, 91, 89, 89, 87, 87, 87, 86,
                       86, 84, 84, 82, 82, 82, 80, 80, 78, 78, 77, 77, 77, 75, 75, 73, 73, 73, 71, 71, 69, 69, 68, 68,
                       68, 66, 66, 64, 64, 62, 62, 62, 60, 60, 59, 59, 57, 57, 57, 55, 55, 53, 53, 53, 51, 51, 50, 50,
                       48, 48, 48, 46, 46, 44, 44, 42, 42, 42, 41, 41, 39, 39, 39, 37, 37, 35, 35, 33, 33, 32, 32, 30,
                       30, 28, 26, 26, 24, 24, 23, 21, 21, 19, 19, 17, 15, 15, 14, 14, 12, 10, 10, 8, 8, 6, 5, 3, 1, 0,
                       -4, -5, -7, -9, -11, -13, -14, -18, -20, -22, -23, -25, -27, -31, -32, -34, -38, -40, -40, -40,
                       -40]
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_ECT
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_ECT
            else:
                return {'celsius': 0, 'fahrenheit': 0}
            ect_fahrenheit = temperature[self.data1[index]]
            ect_celsius = pytemperature.f2c(ect_fahrenheit)
            return {'celsius': ect_celsius, 'fahrenheit': ect_fahrenheit}
        except IndexError:
            return {'celsius': 0, 'fahrenheit': 0}

    def iat(self):
        """
        Intake air temperature
        """
        # return units: celsius and fahrenheit
        temperature = [302, 302, 298, 294, 289, 285, 282, 278, 273, 269, 266, 262, 258, 253, 249, 246, 242, 239, 235,
                       231, 226, 222, 219, 215, 212, 208, 206, 203, 201, 199, 197, 194, 192, 190, 188, 185, 183, 181,
                       179, 177, 177, 176, 174, 172, 170, 168, 167, 165, 165, 163, 161, 159, 158, 158, 156, 156, 154,
                       152, 152, 150, 149, 149, 147, 147, 145, 143, 143, 141, 141, 140, 138, 138, 136, 134, 134, 132,
                       132, 131, 131, 129, 129, 127, 127, 125, 125, 125, 123, 123, 122, 122, 122, 120, 120, 118, 118,
                       116, 116, 116, 114, 114, 113, 113, 111, 111, 111, 109, 109, 107, 107, 107, 105, 105, 104, 104,
                       102, 102, 102, 100, 100, 98, 98, 96, 96, 96, 95, 95, 93, 93, 91, 91, 91, 89, 89, 87, 87, 87, 86,
                       86, 84, 84, 82, 82, 82, 80, 80, 78, 78, 77, 77, 77, 75, 75, 73, 73, 73, 71, 71, 69, 69, 68, 68,
                       68, 66, 66, 64, 64, 62, 62, 62, 60, 60, 59, 59, 57, 57, 57, 55, 55, 53, 53, 53, 51, 51, 50, 50,
                       48, 48, 48, 46, 46, 44, 44, 42, 42, 42, 41, 41, 39, 39, 39, 37, 37, 35, 35, 33, 33, 32, 32, 30,
                       30, 28, 26, 26, 24, 24, 23, 21, 21, 19, 19, 17, 15, 15, 14, 14, 12, 10, 10, 8, 8, 6, 5, 3, 1, 0,
                       -4, -5, -7, -9, -11, -13, -14, -18, -20, -22, -23, -25, -27, -31, -32, -34, -38, -40, -40, -40,
                       -40]
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_IAT
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_IAT
            else:
                return {'celsius': 0, 'fahrenheit': 0}
            iat_fahrenheit = temperature[self.data1[index]]
            iat_celsius = pytemperature.f2c(iat_fahrenheit)
            return {'celsius': iat_celsius, 'fahrenheit': iat_fahrenheit}
        except IndexError:
            return {'celsius': 0, 'fahrenheit': 0}

    def gear(self):
        try:
            if self.version == constants.KPRO23_ID:
                gear = self.data0[constants.KPRO23_GEAR]
            elif self.version == 4:
                gear = self.data0[constants.KPRO4_GEAR]
            else:
                return 'N'

            if gear == 0:
                return 'N'
            else:
                return gear
        except IndexError:
            return 'N'

    def eps(self):
        """
        Electric power steering
        """
        mask = 0x20
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_EPS] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_EPS] & mask)
        except IndexError:
            return False

    def scs(self):
        mask = 0x10
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_SCS] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_SCS] & mask)
        except IndexError:
            return False

    def rvslck(self):
        """
        Reverse gear lock
        """
        mask = 0x01
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_RVSLCK] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_RVSLCK] & mask)
        except IndexError:
            return False

    def bksw(self):
        """
        Brake switch
        """
        mask = 0x02
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_BKSW] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_BKSW] & mask)
        except IndexError:
            return False

    def acsw(self):
        """
        Aircon switch
        """
        mask = 0x04
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_ACSW] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_ACSW] & mask)
        except IndexError:
            return False

    def accl(self):
        mask = 0x08
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_ACCL] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_ACCL] & mask)
        except IndexError:
            return False

    def flr(self):
        """
        Fuel relay
        """
        mask = 0x40
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_FLR] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_FLR] & mask)
        except IndexError:
            return False

    def fanc(self):
        """
        Fan switch
        """
        mask = 0x80
        try:
            if self.version == constants.KPRO23_ID:
                return bool(self.data0[constants.KPRO23_FANC] & mask)
            elif self.version == constants.KPRO4_ID:
                return bool(self.data0[constants.KPRO4_FANC] & mask)
        except IndexError:
            return False

    def map(self):
        """
        Manifold absolute pressure
        """
        # return unit: bar, mbar and psi
        try:
            if self.version == constants.KPRO23_ID:
                index = constants.KPRO23_MAP
            elif self.version == constants.KPRO4_ID:
                index = constants.KPRO4_MAP
            else:
                return {'bar': 0, 'mbar': 0, 'psi': 0}
            map_bar = self.data0[index] / 100.0
            map_mbar = map_bar * 1000
            map_psi = Formula.bar_to_psi(map_bar)
            return {'bar': map_bar, 'mbar': map_mbar, 'psi': map_psi}
        except IndexError:
            return {'bar': 0, 'mbar': 0, 'psi': 0}

    def mil(self):
        """
        Malfunction indicator light also known as check engine light
        """
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

    def ecu_type(self):
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

    def ign(self):
        """
        Ignition timing
        """
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

    def firmware(self):
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
        # return unit: volts
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
                return interp((256 * self.data3[index_1]) + self.data3[index_2], [0, 4096], [0, 5])
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
                return interp((256 * self.data5[index_1]) + self.data5[index_2], [0, 1024], [0, 5])
            except IndexError:
                return 0
        else:
            return 0
