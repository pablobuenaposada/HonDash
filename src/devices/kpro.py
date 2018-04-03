import threading

import usb.core
import usb.util
from numpy import interp
import pytemperature


KPRO2_TPS = 8
KPRO2_AFR1 = 0
KPRO2_AFR2 = 0
KPRO2_VSS = 6
KPRO2_RPM1 = 0
KPRO2_RPM2 = 0
KPRO2_CAM = 10
KPRO2_GEAR = None
KPRO2_EPS = None
KPRO2_SCS = None
KPRO2_RVSLCK = None
KPRO2_BKSW = None
KPRO2_ACSW = None
KPRO2_ACCL = None
KPRO2_FLR = None

KPRO2_ECT = None
KPRO2_IAT = 4
KPRO2_BAT = 56

KPRO3_TPS = 7
KPRO3_RPM1 = 4
KPRO3_RPM2 = 5
KPRO3_MAP = 8

KPRO3_ECT = 4
KPRO3_IAT = 5
KPRO3_BAT = 6

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

KPRO4_ECT = 2
KPRO4_IAT = 3
KPRO4_BAT = 4

KPRO4_AN0_1 = 67
KPRO4_AN0_2 = 66

class Kpro:
    def __init__(self):
        self.data0 = []
        self.data1 = []
        self.data2 = []
        self.data3 = []
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
                self.ep.write('\x60')
                if self.version == 2:
                    temp = self.dev.read(0x81, 10000, 1000)  # kpro2
                    if len(temp) == 52:
                        self.data0 = temp
                elif self.version == 3:
                    temp = self.dev.read(0x81, 10000, 1000)  # kpro3
                    if len(temp) == 52:
                        self.data0 = temp
                elif self.version == 4:
                    temp = self.data0 = self.dev.read(0x82, 10000, 1000)  # kpro4
                    if len(temp) == 50:
                        self.data0 = temp

                self.ep.write('\x61')
                if self.version == 2:
                    temp = self.dev.read(0x81, 10000, 1000)  # kpro2
                    if len(temp) == 68:
                        self.data1 = temp
                elif self.version == 3:
                    temp = self.dev.read(0x81, 10000, 1000)  # kpro3
                    if len(temp) == 16:
                        self.data1 = temp
                elif self.version == 4:
                    temp = self.dev.read(0x82, 10000, 1000)  # kpro4
                    if len(temp) == 14: #antes estaba a 16
                        self.data1 = temp

                self.ep.write('\x62')
                if self.version == 2:
                    temp = self.dev.read(0x81, 10000, 1000)  # kpro2
                    if len(temp) == 68:
                        self.data2 = temp
                elif self.version == 3:
                    temp = self.dev.read(0x81, 10000, 1000)  # kpro3
                    if len(temp) == 68:
                        self.data2 = temp
                elif self.version == 4:
                    temp = self.dev.read(0x82, 10000, 1000)  # kpro4
                    if len(temp) == 25:
                        self.data2 = temp

                self.ep.write('\x65')
                if self.version == 4:
                    temp = self.dev.read(0x82, 128, 1000)  # kpro4
                    self.data3 = temp
            except:
                self.__init__()

    def bat(self):
        try:
            if self.version == 2:
                return self.data1[KPRO2_BAT] * 0.1
            elif self.version == 3:
                return self.data1[KPRO3_BAT] * 0.1
            elif self.version == 4:
                return self.data1[KPRO4_BAT] * 0.1
        except:
            return 0

    def afr(self):
        try:
            if self.version == 2:
                return 32768.0 / ((256 * self.data0[KPRO2_AFR2]) + self.data0[KPRO2_AFR1])
            elif self.version == 4:
                return 32768.0 / ((256 * self.data0[KPRO4_AFR2]) + self.data0[KPRO4_AFR1])
        except:
            return 0

    def tps(self):
        try:
            if self.version == 2:
                return int(interp(self.data0[KPRO2_TPS], [21, 229], [0, 100]))
            elif self.version == 3:
                return int(interp(self.data0[KPRO3_TPS], [21, 229], [0, 100]))
            elif self.version == 4:
                return int(interp(self.data0[KPRO4_TPS], [21, 229], [0, 100]))
        except:
            return 0

    def vss(self):
        try:
            if self.version == 2:
                return self.data0[KPRO2_VSS]
            elif self.version == 4:
                return self.data0[KPRO4_VSS]
            else:
                return 0
        except:
            return 0

    def rpm(self):
        try:
            if self.version == 2:
                return ((256*self.data0[KPRO2_RPM2])+self.data0[KPRO2_RPM1])*0.25
            elif self.version == 3:
                return ((256 * self.data0[KPRO3_RPM2]) + self.data0[KPRO3_RPM1]) * 0.25
            elif self.version == 4:
                return ((256*self.data0[KPRO4_RPM2])+self.data0[KPRO4_RPM1])*0.25
        except:
            return 0

    def cam(self):
        try:
            if self.version == 2:
                return (self.data0[KPRO2_CAM]-40)*0.5
            elif self.version == 4:
                return (self.data0[KPRO4_CAM]-40)*0.5
        except:
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
        except:
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
        except:
            return 0

    def gear(self):
        try:
            if self.version == 2:
                return self.data0[KPRO2_GEAR]
            elif self.version == 4:
                return self.data0[KPRO4_GEAR]
        except:
            return 0

    def eps(self):
        mask = 0x20
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_EPS] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_EPS] & mask)
        except:
            return False

    def scs(self):
        mask = 0x10
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_SCS] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_SCS] & mask)
        except:
            return False

    def rvslck(self):
        mask = 0x01
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_RVSLCK] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_RVSLCK] & mask)
        except:
            return False

    def bksw(self):
        mask = 0x02
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_BKSW] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_BKSW] & mask)
        except:
            return False

    def acsw(self):
        mask = 0x04
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_ACSW] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_ACSW] & mask)
        except:
            return False

    def accl(self):
        mask = 0x08
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_ACCL] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_ACCL] & mask)
        except:
            return False

    def flr(self):
        mask = 0x40
        try:
            if self.version == 2:
                return bool(self.data0[KPRO2_FLR] & mask)
            elif self.version == 4:
                return bool(self.data0[KPRO4_FLR] & mask)
        except:
            return False

    def map(self):
        try:
            if self.version == 3:
                return self.data0[KPRO3_MAP]/100.0
        except:
            return 0

    def analog_input(self, channel):
        if self.version == 4:
            if channel == 0:
                index_1 = KPRO4_AN0_1
                index_2 = KPRO4_AN0_2
            else:
                return 0
        else:
            return 0

        try:
            return interp((256 * self.data3[index_1]) + self.data3[index_2], [0, 4096], [0, 5])
        except IndexError:
            return 0
