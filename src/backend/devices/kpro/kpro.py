import threading

import usb.core
import usb.util
from numpy import interp

from backend.devices.formula import Formula
from backend.devices.kpro import constants

from time import sleep

MAX_CONNECTION_RETRIES = 10


class Kpro:
    def __init__(self):
        self.data0 = self.data1 = self.data2 = self.data3 = self.data4 = self.data5 = self.data6 = []
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
        # S300 v3       
        elif usb.core.find(
            idVendor=constants.S300V3_ID_VENDOR, idProduct=constants.S300V3_ID_PRODUCT,
        ):
            device = usb.core.find(
                idVendor=constants.S300V3_ID_VENDOR,
                idProduct=constants.S300V3_ID_PRODUCT,
            )
            version = constants.S300V3_ID
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

    @staticmethod
    def _read_from_device(version, device, entry_point):
        data0 = data1 = data2 = data3 = data4 = data5 = data6 = []
        if version == constants.KPRO4_ID:
            entry_point.write("\x40")
            data4 = device.read(0x82, 1000)  # kpro v4
        elif version == constants.KPRO23_ID:
            entry_point.write("\x40")
            data4 = device.read(0x81, 1000)  # kpro v2 & v3
        elif version == constants.S300V3_ID:
            entry_point.write("\x40")
            data4 = device.read(0x82, 1000)  # s300 v3
        
        entry_point.write("\x60")
        if version == constants.KPRO23_ID:
            data0 = device.read(0x81, 1000)  # kpro v3
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
        elif version == constants.S300V3_ID:
            entry_point.write(bytes([176]))
            data5 = device.read(0x82, 128, 1000)  # s300 v3
        else:  # for v3 only, v2 will not return anything meaningful
            entry_point.write("\xb0")
            data5 = device.read(0x81, 1000)
#            
#        print("data5: ")
#        print(str(data5))
#        print('\n')
        
#        entry_point.write("\x90")
        entry_point.write(bytes([144]))
        if version == constants.S300V3_ID:
            data6 = device.read(0x82, 1000, 1000)  # s300 v3
        
#        sleep(1)
        
        return data0, data1, data2, data3, data4, data5, data6

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
                    self.data6,
                ) = self._read_from_device(
                    self.version, self.kpro_device, self.entry_point
                )
            except usb.core.USBError as e:
                # error 60 (operation timed out), just continue to try again
                if e.args[0] != 60:
                    # if there's an error while gathering the data, stop the update and try to reconnect usb again
                    self.status = False  # redundant?
                    self.__init__()

    def get_value_from_kpro(self, indexes, data, default=0):
        """
        Get the value from the chosen index and data array depending on the current K-Pro version.
        If something goes wrong return a predefined default value.
        """
        try:
            return data[indexes[self.version]]
        except (KeyError, IndexError):
            return default

    @property
    def bat(self):
        """
        Battery voltage
        return unit: volts
        """
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_BAT,
            constants.KPRO4_ID: constants.KPRO4_BAT,
            constants.S300V3_ID: constants.S300V3_BAT,
        }
#        return self.get_value_from_kpro(indexes, self.data1) * 0.1
        if self.version == constants.S300V3_ID:
            return self.get_value_from_kpro(indexes, self.data6) * 0.0963
        else:
            return self.get_value_from_kpro(indexes, self.data1) * 0.1

    @property
    def eth(self):
        """
        Ethanol content
        return unit: per cent
        """
        indexes = {
            constants.KPRO4_ID: constants.KPRO4_ETH,
            constants.S300V3_ID: constants.S300V3_ETH,
        }
        return self.get_value_from_kpro(indexes, self.data3)

    @property
    def flt(self):
        """Fuel temperature"""
        indexes = {constants.KPRO4_ID: constants.KPRO4_FLT,
                   constants.S300V3_ID: constants.S300V3_FLT,
       }
        flt_celsius = self.get_value_from_kpro(indexes, self.data3)
        flt_fahrenheit = Formula.celsius_to_fahrenheit(flt_celsius)
        return {"celsius": flt_celsius, "fahrenheit": flt_fahrenheit}

    @property
    def o2(self):
        """Oxygen sensor"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_AFR1,
            constants.KPRO4_ID: constants.KPRO4_AFR1,
            constants.S300V3_ID: constants.S300V3_AFR,
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_AFR2,
            constants.KPRO4_ID: constants.KPRO4_AFR2,
#            constants.S300V3_ID: constants.S300V3_54
        }
        if self.version == constants.S300V3_ID:
            o2_lambda = (self.get_value_from_kpro(indexes_1, self.data6) - 1.1588)/126.35
#            try:
#                    o2_lambda = 32768.0 / (
#                        256 * self.get_value_from_kpro(indexes_2, self.data6)
#                        + self.get_value_from_kpro(indexes_1, self.data6)
#                    )
#            except ZeroDivisionError:  # something happen collecting the value then return 0
#                return {"afr": 0, "lambda": 0}
        else:
            try:
                o2_lambda = 32768.0 / (
                    256 * self.get_value_from_kpro(indexes_2, self.data0)
                    + self.get_value_from_kpro(indexes_1, self.data0)
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
            constants.S300V3_ID: constants.S300V3_TPS,
        }
        if self.version == constants.S300V3_ID:
            return int(
#                interp(self.get_value_from_kpro(indexes, self.data6), [0,255], [0,5]) # TPSV
#                (25 * (self.get_value_from_kpro(indexes, self.data6) - 12.5))
                interp(self.get_value_from_kpro(indexes, self.data6), [21, 229], [0, 100])
            )            
        else:
            return int(
                interp(self.get_value_from_kpro(indexes, self.data0), [21, 229], [0, 100])
            )

    @property
    def vss(self):
        """Vehicle speed sensor"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_VSS,
            constants.KPRO4_ID: constants.KPRO4_VSS,
            constants.S300V3_ID: constants.S300V3_VSS1,
        }
        indexes_2 = {
            constants.S300V3_ID: constants.S300V3_VSS2,
        }
        
        if self.version == constants.S300V3_ID:
            if self.get_value_from_kpro(indexes_2, self.data6) == 255:
                vss_kmh = 0
            elif self.get_value_from_kpro(indexes_2, self.data6) == 0:
                vss_kmh = 256
            else:
                vss_kmh = int(
                    227125 /
                    ((256 * self.get_value_from_kpro(indexes_2, self.data6)) 
                    + self.get_value_from_kpro(indexes_1, self.data6))
                )
        else:
            vss_kmh = self.get_value_from_kpro(indexes_1, self.data0)
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
            constants.S300V3_ID: constants.S300V3_RPM1,
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_RPM2,
            constants.KPRO4_ID: constants.KPRO4_RPM2,
            constants.S300V3_ID: constants.S300V3_RPM2,
        }
        if self.version == constants.S300V3_ID:    
            return int(
                    (256 * self.get_value_from_kpro(indexes_2, self.data6))
                    + self.get_value_from_kpro(indexes_1, self.data6)
                )
        else:
            return int(
                (
                    (256 * self.get_value_from_kpro(indexes_2, self.data0))
                    + self.get_value_from_kpro(indexes_1, self.data0)
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
        data_from_kpro = self.get_value_from_kpro(indexes, self.data0, None)
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
            constants.S300V3_ID: constants.S300V3_ECT,

        }
        if self.version == constants.S300V3_ID:
            data_from_kpro = self.get_value_from_kpro(
                    indexes, self.data6, {"celsius": 0, "fahrenheit": 0}
            )
        else:
            data_from_kpro = self.get_value_from_kpro(
                    indexes, self.data1, {"celsius": 0, "fahrenheit": 0}
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
            constants.S300V3_ID: constants.S300V3_IAT,
        }
        if self.version == constants.S300V3_ID:
            data_from_kpro = self.get_value_from_kpro(
                    indexes, self.data6, {"celsius": 0, "fahrenheit": 0}
            )
        else:
            data_from_kpro = self.get_value_from_kpro(
                    indexes, self.data1, {"celsius": 0, "fahrenheit": 0}
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
            constants.S300V3_ID: constants.S300V3_GEAR,
        }
        if self.version == constants.S300V3_ID:
            return self.get_value_from_kpro(indexes, self.data6)
        else:
            return self.get_value_from_kpro(indexes, self.data0)
        
    @property
    def eps(self):
        """Electric power steering"""
        mask = 0x20
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_EPS,
            constants.KPRO4_ID: constants.KPRO4_EPS,
        }
        return bool(self.get_value_from_kpro(indexes, self.data0) & mask)

    @property
    def scs(self):
        """Service connector"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_SCS,
            constants.KPRO4_ID: constants.KPRO4_SCS,
            constants.S300V3_ID: constants.S300V3_SCS,
        }
        if self.version == constants.S300V3_ID:
            mask = 0x20
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        else:
            mask = 0x10
            return bool(self.get_value_from_kpro(indexes, self.data0) & mask)
        
    @property
    def rvslck(self):
        """Reverse gear lock"""
        mask = 0x01
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_RVSLCK,
            constants.KPRO4_ID: constants.KPRO4_RVSLCK,
        }
        return bool(self.get_value_from_kpro(indexes, self.data0) & mask)

    @property
    def bksw(self):
        """Brake switch"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_BKSW,
            constants.KPRO4_ID: constants.KPRO4_BKSW,
            constants.S300V3_ID: constants.S300V3_BKSW,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x04
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        else:
            mask = 0x02
            return bool(self.get_value_from_kpro(indexes, self.data0) & mask)

    @property
    def acsw(self):
        """A/C switch"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_ACSW,
            constants.KPRO4_ID: constants.KPRO4_ACSW,
            constants.S300V3_ID: constants.S300V3_ACSW,
        }
        if self.version == constants.S300V3_ID:
            mask = 0x02
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        else:
            mask = 0x04
        return bool(self.get_value_from_kpro(indexes, self.data0) & mask)

    @property
    def accl(self):
        """A/C clutch"""
        mask = 0x08
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_ACCL,
            constants.KPRO4_ID: constants.KPRO4_ACCL,
            constants.S300V3_ID: constants.S300V3_ACCL,
        }
        if self.version == constants.S300V3_ID:
            #Output inverted on S300?
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        else:
            return bool(self.get_value_from_kpro(indexes, self.data0) & mask)

    @property
    def flr(self):
        """Fuel relay"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_FLR,
            constants.KPRO4_ID: constants.KPRO4_FLR,
            constants.S300V3_ID: constants.S300V3_FLR,

        }
        if self.version == constants.S300V3_ID:
            #engine always in 'run' with this sim, need to test in car
            mask = 0x02
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        else:
            mask = 0x04
            return bool(self.get_value_from_kpro(indexes, self.data0) & mask)

    @property
    def fanc(self):
        """Fan switch"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_FANC,
            constants.KPRO4_ID: constants.KPRO4_FANC,
            constants.S300V3_ID: constants.S300V3_FANC,
        }
        if self.version == constants.S300V3_ID:
            mask = 0x01 
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        else:
            mask = 0x80
            return bool(self.get_value_from_kpro(indexes, self.data0) & mask)

    @property

    def map(self):
        """Manifold absolute pressure"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_MAP,
            constants.KPRO4_ID: constants.KPRO4_MAP,
            constants.S300V3_ID: constants.S300V3_MAP1,            
        }
        indexes_2 = {
            constants.S300V3_ID: constants.S300V3_MAP2
        }
        if self.version == constants.S300V3_ID:
            data_from_kpro = (
                    (256 * self.get_value_from_kpro(indexes_2, self.data6))
                    + self.get_value_from_kpro(indexes_1, self.data6)
            ) #, {"bar": 0, "mbar": 0, "psi": 0}
            map_mbar = int(data_from_kpro)
            map_bar = data_from_kpro / 1000
            map_psi = Formula.bar_to_psi(map_bar)
            return {"bar": map_bar, "mbar": map_mbar, "psi": map_psi}            
        else:
            data_from_kpro = self.get_value_from_kpro(
                indexes_1, self.data0, {"bar": 0, "mbar": 0, "psi": 0}
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
            constants.S300V3_ID: constants.S300V3_MIL,
        }
        if self.version == constants.KPRO23_ID:
            data_from_kpro = self.get_value_from_kpro(indexes, self.data0)
            if data_from_kpro == 9:
                return True
            return False
        elif self.version == constants.KPRO4_ID:
            data_from_kpro = self.get_value_from_kpro(indexes, self.data3)
            if data_from_kpro >= 36:
                return True
            return False
        elif self.version == constants.S300V3_ID:
            mask = 0x20
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        return False

    @property
    def ecu_type(self):
        """Model of ECU"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_ECU_TYPE,
            constants.KPRO4_ID: constants.KPRO4_ECU_TYPE,
        }
        data_from_kpro = self.get_value_from_kpro(indexes, self.data4)
        if data_from_kpro == 3:  # TODO the rest of ecu types
            return "RSX - PRB"
        return "unknown"

    @property
    def ign(self):
        """Ignition status"""
        indexes = {
            constants.KPRO23_ID: constants.KPRO23_IGN,
            constants.KPRO4_ID: constants.KPRO4_IGN,
            constants.S300V3_ID: constants.S300V3_IGN,
        }
        if self.version == constants.S300V3_ID:
            data_from_kpro = self.get_value_from_kpro(indexes, self.data4, 0)
        else:
            data_from_kpro = self.get_value_from_kpro(indexes, self.data4, 1)
        if data_from_kpro == 1:
            return True
        return False

    @property
    def serial(self):
        """K-Pro serial number"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_SERIAL1,
            constants.KPRO4_ID: constants.KPRO4_SERIAL1,
            constants.S300V3_ID: constants.S300V3_SERIAL1,
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_SERIAL2,
            constants.KPRO4_ID: constants.KPRO4_SERIAL2,
            constants.S300V3_ID: constants.S300V3_SERIAL2,
        }
        return (
            256 * self.get_value_from_kpro(indexes_2, self.data4, 0)
        ) + self.get_value_from_kpro(indexes_1, self.data4, 0)

    @property
    def firmware(self):
        """Firmware version"""
        indexes_1 = {
            constants.KPRO23_ID: constants.KPRO23_FIRM1,
            constants.KPRO4_ID: constants.KPRO4_FIRM1,
            constants.S300V3_ID: constants.S300V3_FIRM1,            
        }
        indexes_2 = {
            constants.KPRO23_ID: constants.KPRO23_FIRM2,
            constants.KPRO4_ID: constants.KPRO4_FIRM2,
            constants.S300V3_ID: constants.S300V3_FIRM2,
        }

        return "{}.{:02d}".format(
            self.get_value_from_kpro(indexes_2, self.data4, 0),
            self.get_value_from_kpro(indexes_1, self.data4, 0),
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
                constants.S300V3_ID: constants.S300V3_AN0_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN1_1,
                constants.KPRO4_ID: constants.KPRO4_AN1_1,
                constants.S300V3_ID: constants.S300V3_AN1_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN2_1,
                constants.KPRO4_ID: constants.KPRO4_AN2_1,
                constants.S300V3_ID: constants.S300V3_AN2_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN3_1,
                constants.KPRO4_ID: constants.KPRO4_AN3_1,
                constants.S300V3_ID: constants.S300V3_AN3_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN4_1,
                constants.KPRO4_ID: constants.KPRO4_AN4_1,
                constants.S300V3_ID: constants.S300V3_AN4_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN5_1,
                constants.KPRO4_ID: constants.KPRO4_AN5_1,
                constants.S300V3_ID: constants.S300V3_AN5_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN6_1,
                constants.KPRO4_ID: constants.KPRO4_AN6_1,
                constants.S300V3_ID: constants.S300V3_AN6_1,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN7_1,
                constants.KPRO4_ID: constants.KPRO4_AN7_1,
                constants.S300V3_ID: constants.S300V3_AN7_1,
            },
        )
        indexes_2 = (
            {
                constants.KPRO23_ID: constants.KPRO3_AN0_2,
                constants.KPRO4_ID: constants.KPRO4_AN0_2,
                constants.S300V3_ID: constants.S300V3_AN0_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN1_2,
                constants.KPRO4_ID: constants.KPRO4_AN1_2,
                constants.S300V3_ID: constants.S300V3_AN1_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN2_2,
                constants.KPRO4_ID: constants.KPRO4_AN2_2,
                constants.S300V3_ID: constants.S300V3_AN2_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN3_2,
                constants.KPRO4_ID: constants.KPRO4_AN3_2,
                constants.S300V3_ID: constants.S300V3_AN3_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN4_2,
                constants.KPRO4_ID: constants.KPRO4_AN4_2,
                constants.S300V3_ID: constants.S300V3_AN4_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN5_2,
                constants.KPRO4_ID: constants.KPRO4_AN5_2,
                constants.S300V3_ID: constants.S300V3_AN5_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN6_2,
                constants.KPRO4_ID: constants.KPRO4_AN6_2,
                constants.S300V3_ID: constants.S300V3_AN6_2,
            },
            {
                constants.KPRO23_ID: constants.KPRO3_AN7_2,
                constants.KPRO4_ID: constants.KPRO4_AN7_2,
                constants.S300V3_ID: constants.S300V3_AN7_2,
            },
        )

        if self.version == constants.KPRO4_ID:
            return interp(
                (256 * self.get_value_from_kpro(indexes_1[channel], self.data3, 0))
                + self.get_value_from_kpro(indexes_2[channel], self.data3, 0),
                [0, 4096],
                [0, 5],
            )
        elif self.version == constants.KPRO23_ID:
            return interp(
                (256 * self.get_value_from_kpro(indexes_1[channel], self.data5, 0))
                + self.get_value_from_kpro(indexes_2[channel], self.data5, 0),
                [0, 1024],
                [0, 5],
            )
        elif self.version == constants.S300V3_ID:
            return interp(
                (256 * self.get_value_from_kpro(indexes_1[channel], self.data5, 0))
                + self.get_value_from_kpro(indexes_2[channel], self.data5, 0),
                [0, 4096],
                [0, 5],
            )
        else:
            return 0
        
    """S300 stuff I've added goes below here"""
    
    @property
    def inj(self):
        """Injector Pulse Width, in ms; S300"""
        indexes_1 = {constants.S300V3_ID: constants.S300V3_INJ1
        }
        indexes_2 = {constants.S300V3_ID: constants.S300V3_INJ2
        }
        return(
            ((256 * self.get_value_from_kpro(indexes_2, self.data6))
            + self.get_value_from_kpro(indexes_1, self.data6)) / 250
        )
            
    @property 
    def injduty(self):
        """Injector Duty Cycle, in %; S300"""
        # This formula is close but not 100% right
        indexes_1 = {constants.S300V3_ID: constants.S300V3_DUTY1
        }
        indexes_2 = {constants.S300V3_ID: constants.S300V3_DUTY2
        }
        return(
            (250 * self.get_value_from_kpro(indexes_2, self.data6))
            + (self.get_value_from_kpro(indexes_1, self.data6))
        ) / 20
    
    @property
    def igadv(self):
        """Ignition Advance; S300"""
        indexes_1 = {constants.S300V3_ID: constants.S300V3_IGADV
        }
        return(
            (self.get_value_from_kpro(indexes_1, self.data6) / 4) - 5
        )
        
    @property
    def pho2sv(self):
        """Primary Heated Oxygen Sensor Voltage; S300"""
        indexes = {constants.S300V3_ID: constants.S300V3_O2V,
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes, self.data6
        )
        if isinstance(data_from_kpro, int):
            return Formula.adc_to_volts_8bit(data_from_kpro)
        
    @property
    def strim(self):
        """Short Term Fuel Trim; S300"""
        indexes = {constants.S300V3_ID: constants.S300V3_STRIM,
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes, self.data6
        )    
        return round((data_from_kpro * .78125) - 100, 2)
        
    @property
    def ltrim(self):
        """Long Term Fuel Trim; S300"""
        #Untested - having trouble stimulating on bench
        indexes = {constants.S300V3_ID: constants.S300V3_LTRIM,
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes, self.data6
        )    
        return round((data_from_kpro * .78125) - 100, 2)
    
            
    @property
    def iatc(self):
        """Intake Air Temperature Correction; S300"""
        indexes = {constants.S300V3_ID: constants.S300V3_IATC,
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes, self.data6
        )    
        return round((data_from_kpro * .78125) - 100, 2)
                
    @property
    def ectc(self):
        """Coolant Temperature Correction; S300"""
        indexes = {constants.S300V3_ID: constants.S300V3_ECTC,
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes, self.data6
        )    
        return round((data_from_kpro * .78125) - 100, 2)
        
    @property
    def wbv(self):
        """Wideband Oxygen (lambda) Sensor Voltage; S300"""
        indexes = {constants.S300V3_ID: constants.S300V3_WBV,
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes, self.data6
        )
        if isinstance(data_from_kpro, int):
            return Formula.adc16_to_volts(data_from_kpro)

    @property
    def egrlv(self):
        """EGR Lift Sensor Voltage, also used for Analog Input 1; S300"""
        indexes_1 = {constants.S300V3_ID: constants.S300V3_EGRLV
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes_1, self.data6
        )
        if isinstance(data_from_kpro, int):
            return Formula.adc16_to_volts(data_from_kpro) 


    @property
    def b6v(self):
        """B6 Input voltage, also used for Analog Input 2; S300"""
        indexes_1 = {constants.S300V3_ID: constants.S300V3_B6V
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes_1, self.data6
        )
        if isinstance(data_from_kpro, int):
            return Formula.adc16_to_volts(data_from_kpro)
        
    @property
    def baro(self):
        """
        ECU Baro Sensor; S300 - Can be used as rudimentary altimeter too, but 
        is only a 16 bit channel so resolution is not great (~400ft)
        """
        indexes_1 = {constants.S300V3_ID: constants.S300V3_BARO
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes_1, self.data6
        )
        if isinstance(data_from_kpro, int):
            baro_mbar = round((367 * (data_from_kpro / 51) - 45), 2)
        baro_kpa = round((baro_mbar / 10), 2)
        baro_bar = round((baro_mbar / 1000), 2)
        baro_psi = round(Formula.bar_to_psi(baro_bar), 2)
        baro_alt = Formula.baro_to_altitude(baro_mbar)
        return{
                "mbar": baro_mbar, "kPa": baro_kpa, "bar": baro_bar, 
                "psi": baro_psi, "Alt": baro_alt
        }         
    
    @property
    def eld(self):
        """
        Electrical Load Detector, can be used as a monitor for system amps
        with following formula:
        amps = -17.5*ELDV + 78.75; S300
        """
        indexes_1 = {constants.S300V3_ID: constants.S300V3_ELD
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes_1, self.data6
        )
        if isinstance(data_from_kpro, int):
            eldv = Formula.adc16_to_volts(data_from_kpro)
        elda = (-17.5 * eldv) + 78.5
        return {"eld_v": eldv, "eld_a": elda}
                    
    @property
    def psp(self):
        """Power Steering Pressure Switch; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_PSP,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x10
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        
    @property
    def vtp(self):
        """VTEC Pressure Switch; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_VTP,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x01
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
                
    @property
    def a10(self):
        """A10 Aux Ouput; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_A10,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x10
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
                
    @property
    def cl(self):
        """Closed Loop active Indicator; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_CL,            
        }
        if self.version == constants.S300V3_ID:
#            mask = 0x04
            mask = 0x01
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def altc(self):
        """Alternator Control Out; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_ALTC,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x80
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)  
        
    @property
    def iab(self):
        """Intake Air Bypass Out; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_IAB,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x40
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        
    @property
    def pcs(self):
        """Evap Purge Control Solenoid Out; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_PCS,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x10 #Might be on a different bitfield 
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        
    @property
    def vts(self):
        """VTEC Solenoid Out; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_VTS,            
        }
        if self.version == constants.S300V3_ID:
            mask = 0x01
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        
    @property
    def n1arm(self):
        """Nitrous/AUX1 Output 'Armed' Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_N1ARM,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x01
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def n1on(self):
        """Nitrous/AUX1 Output 'On' Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_N1ON,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x02
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def n2arm(self):
        """Nitrous/AUX2 Output 'Armed' Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_N2ARM,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x04
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def n2on(self):
        """Nitrous/AUX2 Output 'On' Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_N2ON,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x08
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def n3arm(self):
        """Nitrous/AUX3 Output 'Armed' Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_N3ARM,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x01
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def n3on(self):
        """Nitrous/AUX3 Output 'On' Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_N3ON,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x02
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def disterr(self):
        """Distributor Error Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_DISTERR,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x40
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
    @property
    def sectbl(self):
        """Secondary Tables Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_SECTBL,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x80
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def secinj(self):
        """Secondary Injectors Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_SECINJ,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x20
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def revl(self):
        """Rev Limiter Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_REVL,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x08
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def lnchc(self):
        """Launch Cut Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_LNCHC,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x80
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        
    @property
    def lnchr(self):
        """Launch Retard Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_LNCHR,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x40
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def bstc(self):
        """Boost Cut Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_BSTC,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x08
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def shftc(self):
        """Shift Cut Cut Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_SHFTC,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x10
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)
        
    @property
    def ignc(self):
        """Ignition Cut Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_IGNC,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x20
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)

    @property
    def obdl(self):
        """Onboard Logging Active Flag; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_DL,            
        }
        if self.version == constants.S300V3_ID:            
            mask = 0x10
            return bool(self.get_value_from_kpro(indexes, self.data6) & mask)


    @property
    def pwm(self):
        """PWM Boost Solenoid Duty Cycle %; S300"""
        indexes = {
            constants.S300V3_ID: constants.S300V3_PWM,            
        }
        data_from_kpro = self.get_value_from_kpro(
                indexes, self.data6
        )
        if isinstance(data_from_kpro, int):
            return round(interp(data_from_kpro, [0, 255], [0, 100]), 2)
 