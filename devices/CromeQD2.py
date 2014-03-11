from SerialPort import *

ECT_CROME14 = 0x1D
IAT_CROME14 = 0x1B
O2_CROME14 = 0x20
BARO_CROME14 = 0x1E
MAP_CROME14 = 0x14
TPS_CROME14 = 0x15
RPMLOW_CROME14 = 0x10
RPMHIGH_CROME14 = 0x11
LOCAM_CROME14 = 0x12
HICAM_CROME14 = 0x13
COL_CROME14 = 0x16
VSS_CROME14 = 0x1C
VTEC_CROME14 = 0x22
IGN_CROME14 = 0x19
INJLOW_CROME14 = 0x17
INJHIGH_CROME14 = 0x18
KNOCK_CROME14 = 0x1A
BATT_CROME14 = 0x1F
GEAR_B1_CROME14 = 0x01
GEAR_B2_CROME14 = 0x02
GEAR_B3_CROME14 = 0x4F


class CromeQD2:
    @staticmethod
    def calc_temp_in_celsius(raw):
        raw /= 51.
        raw = (0.1423 * pow(raw, 6)) - (2.4938 * pow(raw, 5)) + (17.837 * pow(raw, 4)) - (68.698 * pow(raw, 3)) + (
            154.69 * pow(raw, 2)) - (232.75 * raw) + 284.24
        return ((raw - 32.) * 5.) / 9.

    def __init__(self):
        self.serialPort = SerialPort()

    def get_gear(self):
        return self.serialPort.get_byte_from_three(GEAR_B1_CROME14, GEAR_B2_CROME14, GEAR_B3_CROME14)

    def get_rpm(self):
        try:
            rpm_low_raw = self.serialPort.get_byte(RPMLOW_CROME14)
            rpm_high_raw = self.serialPort.get_byte(RPMHIGH_CROME14)
            return 1851562 / ((rpm_high_raw * 256) + rpm_low_raw)
        except:
            return 0

    def get_battery(self):
        battery_raw = self.serialPort.get_byte(BATT_CROME14)
        return (26.0 * battery_raw) / 270.0

    def get_iat(self):
        iat_raw = self.serialPort.get_byte(IAT_CROME14)
        return self.calcTempInCelsius(iat_raw)

    def get_ect(self):
        ect_raw = self.serialPort.get_byte(ECT_CROME14)
        return self.calcTempInCelsius(ect_raw)

    def get_tps(self):
        tps_raw = self.serialPort.get_byte(TPS_CROME14)
        tps_raw = (0.4716 * tps_raw) - 11.3184
        return tps_raw

    def get_o2(self):
        o2_raw = self.serialPort.get_byte(O2_CROME14)
        return (2 * o2_raw) + 10

    def get_vss(self):
        vss_raw = self.serialPort.get_byte(VSS_CROME14)
        return vss_raw

    def get_map(self):
        map_raw = self.serialPort.get_byte(MAP_CROME14)
        return (1764 / 255) * map_raw

    def get_inj(self):
        inj_low_raw = self.serialPort.get_byte(INJLOW_CROME14)
        inj_high_raw = self.serialPort.get_byte(INJHIGH_CROME14)
        inj_raw = (inj_high_raw * 256) + inj_low_raw;
        return inj_raw / 352

    def get_ign(self):
        ign_raw = self.serialPort.get_byte(IGN_CROME14)
        return (0.25 * ign_raw) - 6

    def get_duty_cycle(self):
        rpm = self.get_rpm()
        inj = self.get_inj()
        return (rpm * inj) / 1200

    def get_vtec(self):
        vtec = self.serialPort.get_byte(VTEC_CROME14)
        if vtec == 67:
            return True
        else:
            return False
