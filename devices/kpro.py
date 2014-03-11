import usb.core
import usb.util
from numpy import interp

KPRO2_IAT = 4
KPRO2_BAT = 56
KPRO2_TPS = 8
KPRO2_AFR1 = 0
KPRO2_AFR2 = 0
KPRO2_VSS = 6
KPRO2_RPM1 = 0
KPRO2_RPM2 = 0
KPRO2_CAM = 10

KPRO4_ECT = 2
KPRO4_IAT = 3
KPRO4_BAT = 4
KPRO4_TPS = 5
KPRO4_AFR1 = 16
KPRO4_AFR2 = 17
KPRO4_VSS = 4
KPRO4_RPM1 = 2
KPRO4_RPM2 = 3
KPRO4_CAM = 8


class Kpro:
    def __init__(self):
        self.data0 = []
        self.data1 = []
        self.data2 = []
        self.dev = None
        self.version = 0
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
            except:
                pass

    def update(self):
        try:
            assert self.ep is not None
            self.ep.write('\x60')
            if self.version == 2:
                temp = self.dev.read(0x81, 10000, 1000)  # kpro2
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
            elif self.version == 4:
                temp = self.dev.read(0x82, 10000, 1000)  # kpro4
                if len(temp) == 16:
                    self.data1 = temp
        except:
            self.__init__()

    def bat(self):
        try:
            if self.version == 2:
                return self.data1[KPRO2_BAT] * 0.1
            elif self.version == 4:
                return self.data1[KPRO4_BAT] * 0.1
        except:
            return 0

    def iat(self):
        try:
            if self.version == 2:
                return self.data1[KPRO2_IAT]
            elif self.version == 4:
                return self.data1[KPRO4_IAT]
        except:
            return 0

    def afr(self):
        try:
            if self.version == 2:
                return 32768.0 / ((256 * self.data0[KPRO2_AFR2]) + self.data0.data0[KPRO2_AFR1])
            elif self.version == 4:
                return 32768.0 / ((256 * self.data0[KPRO4_AFR2]) + self.data0.data0[KPRO4_AFR1])
        except:
            return 0

    def tps(self):
        try:
            if self.version == 2:
                return interp(self.data0[KPRO2_TPS], [21, 229], [0, 100])
            elif self.version == 4:
                return interp(self.data0[KPRO4_TPS], [21, 229], [0, 100])
        except:
            return 0

    def vss(self):
        try:
            if self.version == 2:
                return self.data0[KPRO2_VSS]
            elif self.version == 4:
                return self.data0[KPRO4_VSS]
        except:
            return 0

    def rpm(self):
        try:
            if self.version == 2:
                return ((256*self.data0[KPRO2_RPM2])+KPRO2_RPM1)*0.25
            elif self.version == 4:
                return ((256*self.data0[KPRO4_RPM2])+KPRO4_RPM1)*0.25
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