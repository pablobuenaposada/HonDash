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

    def calcTempInCelsius(self,raw):
        raw = raw / 51.
        raw = (0.1423*pow(raw,6)) - (2.4938*pow(raw,5))  + (17.837*pow(raw,4)) - (68.698*pow(raw,3)) + (154.69*pow(raw,2)) - (232.75*raw) + 284.24
        return ((raw - 32.)*5.)/9.

    def __init__(self):
        self.serialPort = SerialPort()

    def getGear(self):
        gearRaw = self.serialPort.getByteFromThree(GEAR_B1_CROME14,GEAR_B2_CROME14,GEAR_B3_CROME14)
        return gearRaw

    def getRpm(self):
        rpmLowRaw=self.serialPort.getByte(RPMLOW_CROME14)
        rpmHighRaw=self.serialPort.getByte(RPMHIGH_CROME14) 
        return 1851562/((rpmHighRaw * 256) + rpmLowRaw)

    def getBattery(self):
        batteryRaw = self.serialPort.getByte(BATT_CROME14)
        return (26.0 * batteryRaw) / 270.0

    def getIat(self):
        iatRaw = self.serialPort.getByte(IAT_CROME14)
        return self.calcTempInCelsius(iatRaw)

    def getEct(self):
        ectRaw = self.serialPort.getByte(ECT_CROME14)
	return self.calcTempInCelsius(ectRaw)

    def getTps(self):
        tpsRaw = self.serialPort.getByte(TPS_CROME14)
        tpsRaw = (0.4716  * tpsRaw) - 11.3184
        return tpsRaw

    def getO2(self):
        o2Raw = self.serialPort.getByte(O2_CROME14)
        return (2*o2Raw) + 10

    def getVss(self):
        vssRaw = self.serialPort.getByte(VSS_CROME14)
        return vssRaw

    def getMap(self):
        mapRaw = self.serialPort.getByte(MAP_CROME14)
        return (1764/255)*mapRaw

    def getInj(self):
        injLowRaw = self.serialPort.getByte(INJLOW_CROME14)
        injHighRaw = self.serialPort.getByte(INJHIGH_CROME14)
        injRaw = (injHighRaw * 256) + injLowRaw;
        return injRaw / 352

    def getIgn(self):
        ignRaw = self.serialPort.getByte(IGN_CROME14)
        return (0.25 * ignRaw) - 6

    def getDutyCycle(self):
        rpm = self.getRpm()
        inj = self.getInj()
        return (rpm * inj) / 1200

    def getVtec(self):
        vtec = self.serialPort.getByte(VTEC_CROME14)
        if (vtec == 67): return True
        else: return False
