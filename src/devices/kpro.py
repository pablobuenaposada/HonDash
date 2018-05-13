import threading

import usb.core
import usb.util
from numpy import interp
import pytemperature

# command 0x40
KPRO2_ECU_TYPE = 12
KPRO2_IGN = 17
KPRO2_SERIAL1 = 6
KPRO2_SERIAL2 = 7
KPRO2_FIRM1 = 8
KPRO2_FIRM2 = 9

KPRO4_ECU_TYPE = 10
KPRO4_IGN = 15
KPRO4_SERIAL1 = 4
KPRO4_SERIAL2 = 5
KPRO4_FIRM1 = 6
KPRO4_FIRM2 = 7

# command 0x60
KPRO2_TPS = 7
KPRO2_AFR1 = 18
KPRO2_AFR2 = 19
KPRO2_VSS = 6
KPRO2_RPM1 = 4
KPRO2_RPM2 = 5
KPRO2_CAM = 10
KPRO2_GEAR = 37
KPRO2_EPS = 33
KPRO2_SCS = 33
KPRO2_RVSLCK = 33
KPRO2_BKSW = 33
KPRO2_ACSW = 33
KPRO2_ACCL = 33
KPRO2_FLR = 33
KPRO2_MIL = 34

KPRO3_TPS = 7
KPRO3_RPM1 = 4
KPRO3_RPM2 = 5
KPRO3_MAP = 8

KPRO4_TPS = 5
KPRO4_AFR1 = 16
KPRO4_AFR2 = 17
KPRO4_VSS = 4
KPRO4_RPM1 = 2
KPRO4_RPM2 = 3
KPRO4_CAM = 8
KPRO4_GEAR = 35
KPRO4_EPS = 31
KPRO4_SCS = 31
KPRO4_RVSLCK = 31
KPRO4_BKSW = 31
KPRO4_ACSW = 31
KPRO4_ACCL = 31
KPRO4_FLR = 31

# command 0x61
KPRO2_ECT = 4
KPRO2_IAT = 5
KPRO2_BAT = 6

KPRO3_ECT = 4
KPRO3_IAT = 5
KPRO3_BAT = 6

KPRO4_ECT = 2
KPRO4_IAT = 3
KPRO4_BAT = 4

# command 0x65
KPRO4_AN0_1 = 67
KPRO4_AN0_2 = 66
KPRO4_AN1_1 = 69
KPRO4_AN1_2 = 68
KPRO4_AN2_1 = 71
KPRO4_AN2_2 = 70
KPRO4_AN3_1 = 73
KPRO4_AN3_2 = 72
KPRO4_AN4_1 = 75
KPRO4_AN4_2 = 74
KPRO4_AN5_1 = 77
KPRO4_AN5_2 = 76
KPRO4_AN6_1 = 79
KPRO4_AN6_2 = 78
KPRO4_AN7_1 = 81
KPRO4_AN7_2 = 80
KPRO4_MIL = 30


class Kpro:
    def __init__(self):
        self.data0 = []
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.dev = None
        self.version = 0

        # if True:
        #     self.dev = usb.core.find(idVendor=0x403, idProduct=0xf5f8)
        #     self.version = 3
        if usb.core.find(idVendor=0x403, idProduct=0xf5f8) is not None:  # kpro2
            self.dev = usb.core.find(idVendor=0x403, idProduct=0xf5f8)
            self.version = 2
        elif usb.core.find(idVendor=0x1c40, idProduct=0x0434) is not None:  # kpro4
            self.dev = usb.core.find(idVendor=0x1c40, idProduct=0x0434)
            self.version = 4
        if self.dev is not None:
            try:
                self.dev.set_configuration()
                cfg = self.dev.get_active_configuration()
                intf = cfg[(0, 0)]
                self.ep = usb.util.find_descriptor(
                    intf,
                    custom_match= \
                        lambda e: \
                            usb.util.endpoint_direction(e.bEndpointAddress) == \
                            usb.util.ENDPOINT_OUT)
                threading.Thread(target=self.update).start()
            except:
                pass

    def update(self):
        while True:
            try:
                assert self.ep is not None

                if self.version == 4:
                    self.ep.write('\x40')
                    self.data4 = self.dev.read(0x82, 1000)  # kpro4
                    self.ep.clear_halt()

                self.ep.write('\x60')
                if self.version == 2:
                    self.data0 = self.dev.read(0x81, 1000)  # kpro2
                elif self.version == 3:
                    self.data0 = self.dev.read(0x81, 1000)  # kpro3
                elif self.version == 4:
                    self.data0 = self.dev.read(0x82, 1000)  # kpro4

                self.ep.clear_halt()

                self.ep.write('\x61')
                # found on kpro2 that sometimes len=44, normally 16
                if self.version == 2:
                    self.data1 = self.dev.read(0x81, 1000)  # kpro2
                elif self.version == 3:
                    self.data1 = self.dev.read(0x81, 1000)  # kpro3
                elif self.version == 4:
                    self.data1 = self.dev.read(0x82, 1000)  # kpro4

                self.ep.clear_halt()

                self.ep.write('\x62')
                if self.version == 2:
                    temp = self.dev.read(0x81, 1000)  # kpro2
                    if len(temp) == 68:
                        self.data2 = temp
                elif self.version == 3:
                    temp = self.dev.read(0x81, 1000)  # kpro3
                    if len(temp) == 68:
                        self.data2 = temp
                elif self.version == 4:
                    temp = self.dev.read(0x82, 1000)  # kpro4
                    if len(temp) == 25:
                        self.data2 = temp

                if self.version == 4:
                    self.ep.write('\x65')
                    self.data3 = self.dev.read(0x82, 128, 1000)  # kpro4

            except Exception as e:
                print("USB problem", e)
                self.__init__()

    def bat(self):
        try:
            if self.version == 2:
                return self.data1[KPRO2_BAT] * 0.1
            elif self.version == 3:
                return self.data1[KPRO3_BAT] * 0.1
            elif self.version == 4:
                return self.data1[KPRO4_BAT] * 0.1
        except IndexError:
            return 0

    def afr(self):
        try:
            if self.version == 2:
                return 32768.0 / ((256 * self.data0[KPRO2_AFR2]) + self.data0[KPRO2_AFR1])
            elif self.version == 4:
                return 32768.0 / ((256 * self.data0[KPRO4_AFR2]) + self.data0[KPRO4_AFR1])
        except IndexError:
            return 0

    def tps(self):
        try:
            if self.version == 2:
                return int(interp(self.data0[KPRO2_TPS], [21, 229], [0, 100]))
            elif self.version == 3:
                return int(interp(self.data0[KPRO3_TPS], [21, 229], [0, 100]))
            elif self.version == 4:
                return int(interp(self.data0[KPRO4_TPS], [21, 229], [0, 100]))
            else:
                return 0
        except IndexError:
            return 0

    def vss(self):
        try:
            if self.version == 2:
                return self.data0[KPRO2_VSS]
            elif self.version == 4:
                return self.data0[KPRO4_VSS]
            else:
                return 0
        except IndexError:
            return 0

    def rpm(self):
        try:
            if self.version == 2:
                return ((256*self.data0[KPRO2_RPM2])+self.data0[KPRO2_RPM1])*0.25
            elif self.version == 3:
                return ((256 * self.data0[KPRO3_RPM2]) + self.data0[KPRO3_RPM1]) * 0.25
            elif self.version == 4:
                return ((256*self.data0[KPRO4_RPM2])+self.data0[KPRO4_RPM1])*0.25
            else:
                return 0
        except IndexError:
            return 0

    def cam(self):
        try:
            if self.version == 2:
                return (self.data0[KPRO2_CAM]-40)*0.5
            elif self.version == 4:
                return (self.data0[KPRO4_CAM]-40)*0.5
        except IndexError:
            return 0

    def ect(self):
        fahrenheit = [302, 302, 298, 294, 289, 285, 282, 278, 273, 269, 266, 262, 258, 253, 249, 246, 242, 239, 235,
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
            if self.version == 2:
                return pytemperature.f2c(fahrenheit[self.data1[KPRO2_ECT]])
            elif self.version == 3:
                return pytemperature.f2c(fahrenheit[self.data1[KPRO3_ECT]])
            elif self.version == 4:
                return pytemperature.f2c(fahrenheit[self.data1[KPRO4_ECT]])
        except IndexError:
            return 0

    def iat(self):
        fahrenheit = [302, 302, 298, 294, 289, 285, 282, 278, 273, 269, 266, 262, 258, 253, 249, 246, 242, 239, 235,
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
            if self.version == 2:
                return pytemperature.f2c(fahrenheit[self.data1[KPRO2_IAT]])
            elif self.version == 3:
                return pytemperature.f2c(fahrenheit[self.data1[KPRO3_IAT]])
            elif self.version == 4:
                return pytemperature.f2c(fahrenheit[self.data1[KPRO4_IAT]])
        except IndexError:
            return 0

    def gear(self):
        try:
            if self.version == 2:
                gear = self.data0[KPRO2_GEAR]
            elif self.version == 4:
                gear = self.data0[KPRO4_GEAR]
            else:
                return 'N'

            if gear == 0:
                return 'N'
            else:
                return gear
        except IndexError:
            return 'N'

    def eps(self):
        mask = 0x20
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_EPS] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_EPS] & mask)
        except IndexError:
            return False

    def scs(self):
        mask = 0x10
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_SCS] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_SCS] & mask)
        except IndexError:
            return False

    def rvslck(self):
        mask = 0x01
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_RVSLCK] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_RVSLCK] & mask)
        except IndexError:
            return False

    def bksw(self):
        mask = 0x02
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_BKSW] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_BKSW] & mask)
        except IndexError:
            return False

    def acsw(self):
        mask = 0x04
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_ACSW] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_ACSW] & mask)
        except IndexError:
            return False

    def accl(self):
        mask = 0x08
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_ACCL] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_ACCL] & mask)
        except IndexError:
            return False

    def flr(self):
        mask = 0x40
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_FLR] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_FLR] & mask)
        except IndexError:
            return False

    def map(self):
        try:
            if self.version == 3:
                return self.data0[KPRO3_MAP]/100.0
        except IndexError:
            return 0

    def mil(self):
        try:
            if self.version == 2:
                mil = self.data0[KPRO2_MIL]
                if mil == 9:
                    return True
                elif mil == 1:
                    return False
            elif self.version == 4:
                mil = self.data3[KPRO4_MIL]
                if mil == 37:
                    return True
                elif mil == 33:
                    return False
            else:
                return False
        except IndexError:
            return False

    def ecu_type(self):
        try:
            if self.version == 2:
                type = self.data4[KPRO2_ECU_TYPE]
            elif self.version == 4:
                type = self.data4[KPRO4_ECU_TYPE]
            else:
                return "unknown"

            if type == 3:  # TODO the rest of ecu types
                return "RSX - PRB"
            else:
                return "unknown"
        except IndexError:
            return "unknown"

    def ign(self):
        try:
            if self.version == 2:
                ign = self.data4[KPRO2_IGN]
            elif self.version == 4:
                ign = self.data4[KPRO4_IGN]
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
            if self.version == 2:
                serial1 = self.data4[KPRO2_SERIAL1]
                serial2 = self.data4[KPRO2_SERIAL2]
            elif self.version == 4:
                serial1 = self.data4[KPRO4_SERIAL1]
                serial2 = self.data4[KPRO4_SERIAL2]
            else:
                return 0

            return (256 * serial2) + serial1
        except IndexError:
            return 0

    def firmware(self):
        try:
            if self.version == 2:
                firm1 = self.data4[KPRO2_FIRM1]
                firm2 = self.data4[KPRO2_FIRM2]
            elif self.version == 4:
                firm1 = self.data4[KPRO4_FIRM1]
                firm2 = self.data4[KPRO4_FIRM2]
            else:
                return 0

            return "{}.{:02d}".format(firm2, firm1)
        except IndexError:
            return 0

    def analog_input(self, channel):
        if self.version == 4:
            if channel == 0:
                index_1 = KPRO4_AN0_1
                index_2 = KPRO4_AN0_2
            elif channel == 1:
                index_1 = KPRO4_AN1_1
                index_2 = KPRO4_AN1_2
            elif channel == 2:
                index_1 = KPRO4_AN2_1
                index_2 = KPRO4_AN2_2
            elif channel == 3:
                index_1 = KPRO4_AN3_1
                index_2 = KPRO4_AN3_2
            elif channel == 4:
                index_1 = KPRO4_AN4_1
                index_2 = KPRO4_AN4_2
            elif channel == 5:
                index_1 = KPRO4_AN5_1
                index_2 = KPRO4_AN5_2
            elif channel == 6:
                index_1 = KPRO4_AN6_1
                index_2 = KPRO4_AN6_2
            elif channel == 7:
                index_1 = KPRO4_AN7_1
                index_2 = KPRO4_AN7_2
            else:
                return 0
        else:
            return 0

        try:
            return interp((256 * self.data3[index_1]) + self.data3[index_2], [0, 4096], [0, 5])
        except IndexError:
            return 0
