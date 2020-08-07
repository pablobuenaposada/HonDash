# sudo python bench/test.py
from __future__ import print_function

from reprint import output

#import sys
#sys.path.append('/home/pi/Desktop/HonDash/src/')

from backend.devices.kpro.kpro import Kpro

kpro = Kpro()
with output(output_type="dict", initial_len=1, interval=0) as output_list:
    while True:
#        output_list["ETH"] = str(kpro.eth)
#        output_list["FLT"] = str(kpro.flt)
        output_list["BAT"] = str(kpro.bat)
#        output_list["CAM"] = str(kpro.cam)  # NA for S300
#        output_list["O2"] = str(kpro.o2)
#        output_list["IAT"] = str(kpro.iat)
#        output_list["RPM"] = str(kpro.rpm)
#        output_list["TPS"] = str(kpro.tps)
#        output_list["VSS"] = str(kpro.vss)
#        output_list["ECT"] = str(kpro.ect)
#        output_list["GEAR"] = str(kpro.gear)
#        output_list["EPS"] = str(kpro.eps)  # NA for S300
#        output_list["SCS"] = str(kpro.scs)  
#        output_list["RVSLCK"] = str(kpro.rvslck)  # NA for S300
#        output_list["BKSW"] = str(kpro.bksw)
#        output_list["ACSW"] = str(kpro.acsw)
#        output_list["ACCL"] = str(kpro.accl)
#        output_list["FLR"] = str(kpro.flr)
#        output_list["FANC"] = str(kpro.fanc)
#        output_list["MAP"] = str(kpro.map)
#        output_list["AN0"] = str(kpro.analog_input(0))
#        output_list["AN1"] = str(kpro.analog_input(1))
#        output_list["AN2"] = str(kpro.analog_input(2))
#        output_list["AN3"] = str(kpro.analog_input(3))
#        output_list["AN4"] = str(kpro.analog_input(4))
#        output_list["AN5"] = str(kpro.analog_input(5))
#        output_list["AN6"] = str(kpro.analog_input(6))
#        output_list["AN7"] = str(kpro.analog_input(7))
#        output_list["MIL"] = str(kpro.mil)
#        output_list["ECU_TYPE"] = str(kpro.ecu_type)
#        output_list["IGN"] = str(kpro.ign)
#        output_list["SERIAL"] = str(kpro.serial)
#        output_list["FIRMWARE"] = str(kpro.firmware)
        
        """S300 Params I added below here"""
#        output_list["PSP"] = str(kpro.psp)
#        output_list["VTP"] = str(kpro.vtp)
#        output_list["VTS"] = str(kpro.vts)
#        output_list["INJ"] = str(kpro.inj)
#        output_list["INJ%"] = str(kpro.injduty)
#        output_list["IGADV"] = str(kpro.igadv)
#        output_list["PHO2SV"] = str(kpro.pho2sv)
#        output_list["LVOLT"] = str(kpro.wbv)
#        output_list["EGRLV"] = str(kpro.egrlv)
#        output_list["B6V"] = str(kpro.b6v)
#        output_list["ELD"] = str(kpro.eld)
#        output_list["PATM"] = str(kpro.baro)
#        output_list["S.TRIM"] = str(kpro.strim)
#        output_list["L.TRIM"] = str(kpro.ltrim)  # needs verification in-car
#        output_list["IATC"] = str(kpro.iatc)
#        output_list["ECTC"] = str(kpro.ectc)
#        output_list["IAB"] = str(kpro.iab)
#        output_list["A10"] = str(kpro.a10)
#        output_list["CL"] = str(kpro.cl)
#        output_list["ALTC"] = str(kpro.altc)
#        output_list["PCS"] = str(kpro.pcs)
#        output_list["N1_ARM"] = str(kpro.n1arm)
#        output_list["N1_ON"] = str(kpro.n1on)
#        output_list["N2_ARM"] = str(kpro.n2arm)
#        output_list["N2_ON"] = str(kpro.n2on)
#        output_list["N3_ARM"] = str(kpro.n3arm)
#        output_list["N3_ON"] = str(kpro.n3on)
#        output_list["DISTERR"] = str(kpro.disterr)
#        output_list["SECTBL"] = str(kpro.sectbl)
#        output_list["SECINJ"] = str(kpro.secinj)
#        output_list["REVL"] = str(kpro.revl)
#        output_list["IGNC"] = str(kpro.ignc)
#        output_list["LNCHC"] = str(kpro.lnchc)
#        output_list["LNCHR"] = str(kpro.lnchr)
#        output_list["BSTC"] = str(kpro.bstc)
#        output_list["SHFTC"] = str(kpro.shftc)
#        output_list["OBDL"] = str(kpro.obdl)
#        output_list["PWM"] = str(kpro.pwm)
        
        # for testing
#        output_list["BITFIELD"] = str(kpro.bits)
#        output_list["BYTE"] = str(kpro.byte)
#        output_list["PACKET"] = str(kpro.packet)