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
        map_bar = data_from_s300 / 1000
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

    """
    def analog_input(self, channel):
        return 0
    """

    def analog_input(self, channel):
        """
        Analog inputs
        return unit: volts
        edited by AJ
        """
        indexes_1 = (
            {
                constants.S3003_ID: constants.S3003_AN0_1,
            },
            {
                constants.S3003_ID: constants.S3003_AN1_1,
            },
            {
                constants.S3003_ID: constants.S3003_AN2_1,
            },
            {
                constants.S3003_ID: constants.S3003_AN3_1,
            },
            {
                constants.S3003_ID: constants.S3003_AN4_1,
            },
            {
                constants.S3003_ID: constants.S3003_AN5_1,
            },
            {
                constants.S3003_ID: constants.S3003_AN6_1,
            },
            {
                constants.S3003_ID: constants.S3003_AN7_1,
            }
        )
        indexes_2 = (
            {
                constants.S3003_ID: constants.S3003_AN0_2,
            },
            {
                constants.S3003_ID: constants.S3003_AN1_2,
            }, 
            {
                constants.S3003_ID: constants.S3003_AN2_2,
            },
            {
                constants.S3003_ID: constants.S3003_AN3_2,
            },
            {
                constants.S3003_ID: constants.S3003_AN4_2,
            },
            {
                constants.S3003_ID: constants.S3003_AN5_2,
            },
            {
                constants.S3003_ID: constants.S3003_AN6_2,
            },
            {
                constants.S3003_ID: constants.S3003_AN7_2,
            }
        )
        if self.version == constants.S3003_ID:
            return interp(
                (
                    256 
                    * get_value_from_ecu(
                        self.version, indexes_1[channel], self.data5, 0
                    )
                )
                + get_value_from_ecu(self.version, indexes_2[channel], self.data5, 0),
                [0, 4096],
                [0, 5],
            )
        else:
            return 0

    """----------------------------------------------------------------------------------
    AJ Edits go below here
    """
    @property
    def acsw(self):
        """A/C switch"""
        mask = 0x02
        indexes = {
            constants.S3003_ID: constants.S3003_ACSW,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
 
    @property
    def accl(self):
        """
        A/C clutch
        Output inverted on S300?
        """
        mask = 0x08
        indexes = {
            constants.S3003_ID: constants.S3003_ACCL,
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def inj(self):
        """Injector Pulse Width, in ms; S300"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_INJ1
        }
        indexes_2 = {
            constants.S3003_ID: constants.S3003_INJ2
        }
        return(
            ((256 * get_value_from_ecu(self.version, indexes_2, self.data6))
            + get_value_from_ecu(self.version, indexes_1, self.data6)) / 250
        )
            
    @property 
    def injduty(self):
        """Injector Duty Cycle, in %; S300"""
        # TODO This formula is close but not 100% right
        indexes_1 = {
            constants.S3003_ID: constants.S3003_DUTY1
        }
        indexes_2 = {
            constants.S3003_ID: constants.S3003_DUTY2
        }
        return(
            (250 * get_value_from_ecu(self.version, indexes_2, self.data6))
            + (get_value_from_ecu(self.version, indexes_1, self.data6)) / 20
        )
    
    @property
    def igadv(self):
        """Ignition Advance; S300"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_IGADV
        }
        return(
            (get_value_from_ecu(self.version, indexes_1, self.data6) / 4) - 5
        )
        
    @property
    def pho2sv(self):
        """Primary Heated Oxygen Sensor Voltage; S300"""
        indexes = {
            constants.S3003_ID: constants.S3003_O2V,
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes, self.data6)
        if isinstance(data_from_ecu, int):
            return Formula.adc_to_volts(16 * data_from_ecu)
        
    @property
    def strim(self):
        """Short Term Fuel Trim; S300"""
        indexes = {constants.S3003_ID: constants.S3003_STRIM,
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes, self.data6)    
        return round((data_from_ecu * .78125) - 100, 2)
       
    @property
    def ltrim(self):
        """Long Term Fuel Trim; S300"""
        # TODO Untested - having trouble stimulating on bench
        indexes = {
            constants.S3003_ID: constants.S3003_LTRIM,
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes, self.data6)    
        return round((data_from_ecu * .78125) - 100, 2)
                
    @property
    def iatc(self):
        """Intake Air Temperature Correction; S300"""
        indexes = {
            constants.S3003_ID: constants.S3003_IATC,
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes, self.data6
        )    
        return round((data_from_ecu * .78125) - 100, 2)
                
    @property
    def ectc(self):
        """Coolant Temperature Correction; S300"""
        indexes = {
            constants.S3003_ID: constants.S3003_ECTC,
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes, self.data6)    
        return round((data_from_ecu * .78125) - 100, 2)
        
    @property
    def wbv(self):
        """Wideband Oxygen (lambda) Sensor Voltage; S300"""
        indexes = {
            constants.S3003_ID: constants.S3003_WBV,
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes, self.data6)
        if isinstance(data_from_ecu, int):
            return Formula.adc_to_volts(16 * data_from_ecu)

    @property
    def egrlv(self):
        """EGR Lift Sensor Voltage, also used for Analog Input 1; S300"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_EGRLV
        }
        data_from_ecu = get_value_from_ecu(slef.version, indexes_1, self.data6
        )
        if isinstance(data_from_ecu, int):
            return Formula.adc_to_volts(16 * data_from_ecu) 

    @property
    def b6v(self):
        """B6 Input voltage, also used for Analog Input 2; S300"""
        indexes_1 = {
            constants.S3003_ID: constants.S3003_B6V
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes_1, self.data6)
        if isinstance(data_from_ecu, int):
            return Formula.adc_to_volts(16 * data_from_ecu)
        
    @property
    def baro(self):
        """
        ECU Baro Sensor; S300 - Can be used as rudimentary altimeter too, but 
        is only a 8 bit channel so resolution is not great (~400ft per step)
        """
        indexes_1 = {
            constants.S3003_ID: constants.S3003_BARO
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes_1, self.data6
        )
        if isinstance(data_from_ecu, int):
            baro_mbar = round((367 * (data_from_ecu / 51) - 45), 2)
            baro_kpa = round((baro_mbar / 10), 2)
            baro_bar = round((baro_mbar / 1000), 2)
            baro_psi = round(Formula.bar_to_psi(baro_bar), 2)
        #TODO    baro_alt = Formula.baro_to_altitude(baro_mbar)
        return {"bar": baro_bar, "mbar": baro_mbar, "psi": baro_psi}         
    
    @property
    def eld(self):
        """
        Electrical Load Detector, can be used as a monitor for system amps
        with following formula:
        amps = -17.5*ELDV + 78.75; S300
        """
        indexes_1 = {
            constants.S3003_ID: constants.S3003_ELD
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes_1, self.data6
        )
        if isinstance(data_from_ecu, int):
            eldv = Formula.adc_to_volts(16 * data_from_ecu)
        #TODO elda = (-17.5 * eldv) + 78.5
        return (eldv)
                    
    @property
    def psp(self):
        """Power Steering Pressure Switch; S300"""
        mask = 0x10
        indexes = {
            constants.S3003_ID: constants.S3003_PSP,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
        
    @property
    def vtp(self):
        """VTEC Pressure Switch; S300"""
        mask = 0x01
        indexes = {
            constants.S3003_ID: constants.S3003_VTP,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
                
    @property
    def a10(self):
        """A10 Aux Ouput; S300"""
        mask = 0x10
        indexes = {
            constants.S3003_ID: constants.S3003_A10,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
                
    @property
    def cl(self):
        """Closed Loop active Indicator; S300"""
        mask = 0x01
        indexes = {
            constants.S3003_ID: constants.S3003_CL,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def altc(self):
        """Alternator Control Out; S300"""
        mask = 0x80
        indexes = {
            constants.S3003_ID: constants.S3003_ALTC,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)  
        
    @property
    def iab(self):
        """Intake Air Bypass Out; S300"""
        mask = 0x40
        indexes = {
            constants.S3003_ID: constants.S3003_IAB,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
        
    @property
    def pcs(self):
        """Evap Purge Control Solenoid Out; S300"""
        mask = 0x10
        indexes = {
            constants.S3003_ID: constants.S3003_PCS,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
        
    @property
    def vts(self):
        """VTEC Solenoid Out; S300"""
        mask = 0x01
        indexes = {
            constants.S3003_ID: constants.S3003_VTS,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
        
    @property
    def n1arm(self):
        """Nitrous/AUX1 Output 'Armed' Flag; S300"""
        mask = 0x01
        indexes = {
            constants.S3003_ID: constants.S3003_N1ARM,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def n1on(self):
        """Nitrous/AUX1 Output 'On' Flag; S300"""
        mask = 0x02
        indexes = {
            constants.S3003_ID: constants.S3003_N1ON,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def n2arm(self):
        """Nitrous/AUX2 Output 'Armed' Flag; S300"""
        mask = 0x04
        indexes = {
            constants.S3003_ID: constants.S3003_N2ARM,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def n2on(self):
        """Nitrous/AUX2 Output 'On' Flag; S300"""
        mask = 0x08
        indexes = {
            constants.S3003_ID: constants.S3003_N2ON,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def n3arm(self):
        """Nitrous/AUX3 Output 'Armed' Flag; S300"""
        mask = 0x01
        indexes = {
            constants.S3003_ID: constants.S3003_N3ARM,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def n3on(self):
        """Nitrous/AUX3 Output 'On' Flag; S300"""
        mask = 0x02
        indexes = {
            constants.S3003_ID: constants.S3003_N3ON,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def disterr(self):
        """Distributor Error Flag; S300"""
        mask = 0x40 
        indexes = {
            constants.S3003_ID: constants.S3003_DISTERR,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def sectbl(self):
        """Secondary Tables Active Flag; S300"""
        mask = 0x80
        indexes = {
            constants.S3003_ID: constants.S3003_SECTBL,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def secinj(self):
        """Secondary Injectors Active Flag; S300"""
        mask = 0x20
        indexes = {
            constants.S3003_ID: constants.S3003_SECINJ,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def revl(self):
        """Rev Limiter Active Flag; S300"""
        mask = 0x08
        indexes = {
            constants.S3003_ID: constants.S3003_REVL,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def lnchc(self):
        """Launch Cut Active Flag; S300"""
        mask = 0x80
        indexes = {
            constants.S3003_ID: constants.S3003_LNCHC,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
        
    @property
    def lnchr(self):
        """Launch Retard Active Flag; S300"""
        mask = 0x40
        indexes = {
            constants.S3003_ID: constants.S3003_LNCHR,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def bstc(self):
        """Boost Cut Active Flag; S300"""
        mask = 0x08
        indexes = {
            constants.S3003_ID: constants.S3003_BSTC,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def shftc(self):
        """Shift Cut Cut Active Flag; S300"""
        mask = 0x10
        indexes = {
            constants.S3003_ID: constants.S3003_SHFTC,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)
        
    @property
    def ignc(self):
        """Ignition Cut Active Flag; S300"""
        mask = 0x20
        indexes = {
            constants.S3003_ID: constants.S3003_IGNC,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def obdl(self):
        """Onboard Logging Active Flag; S300"""
        mask = 0x10
        indexes = {
            constants.S3003_ID: constants.S3003_DL,            
        }
        return bool(get_value_from_ecu(self.version, indexes, self.data6) & mask)

    @property
    def pwm(self):
        """PWM Boost Solenoid Duty Cycle %; S300"""
        indexes = {
            constants.S3003_ID: constants.S3003_PWM,            
        }
        data_from_ecu = get_value_from_ecu(self.version, indexes, self.data6
        )
        if isinstance(data_from_ecu, int):
            return round(
                interp(
                    data_from_ecu, [0, 255], [0, 100]
                    ), 2
            )
            

