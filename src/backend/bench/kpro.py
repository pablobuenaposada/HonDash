# sudo python bench/test.py
from __future__ import print_function
from reprint import output
from time import sleep

import sys
sys.path.append('/home/pi/HonDash/src/')
#sys.path

from backend.devices.kpro.kpro import Kpro

kpro = Kpro()
with output(output_type="dict", initial_len=1, interval=0) as output_list:
    while True:
#        sleep(1)
#        output_list["ETH"] = str(kpro.eth)
#        output_list["FLT"] = str(kpro.flt)
#        output_list["BAT"] = str(kpro.bat)  # done
#        output_list["CAM"] = str(kpro.cam)  # NA for S300
#        output_list["O2"] = str(kpro.o2)  # done
#        output_list["IAT"] = str(kpro.iat)  # done
#        output_list["RPM"] = str(kpro.rpm)  # done
#        output_list["TPS"] = str(kpro.tps)  # done
#        output_list["VSS"] = str(kpro.vss)  # done
#        output_list["ECT"] = str(kpro.ect)  # done
#        output_list["GEAR"] = str(kpro.gear)  # done
#        output_list["EPS"] = str(kpro.eps)  # NA for S300
#        output_list["SCS"] = str(kpro.scs)  # done
#        output_list["PSP"] = str(kpro.psp)  # done
#        output_list["VTP"] = str(kpro.vtp)  # done
#        output_list["RVSLCK"] = str(kpro.rvslck)  # NA for S300
#        output_list["BKSW"] = str(kpro.bksw) # done
#        output_list["ACSW"] = str(kpro.acsw)  # done
#        output_list["ACCL"] = str(kpro.accl)  # done
#        output_list["FLR"] = str(kpro.flr) #need to confirm oncar
#        output_list["FANC"] = str(kpro.fanc) # done
#        output_list["MAP"] = str(kpro.map)  # done
#        output_list["AN0"] = str(kpro.analog_input(0))  # done
#        output_list["AN1"] = str(kpro.analog_input(1))  # done
#        output_list["AN2"] = str(kpro.analog_input(2))  # done
#        output_list["AN3"] = str(kpro.analog_input(3))  # done
#        output_list["AN4"] = str(kpro.analog_input(4))  # done
#        output_list["AN5"] = str(kpro.analog_input(5))  # done
#        output_list["AN6"] = str(kpro.analog_input(6))  # done
#        output_list["AN7"] = str(kpro.analog_input(7))  # done
#        output_list["MIL"] = str(kpro.mil)  # done
#        output_list["ECU_TYPE"] = str(kpro.ecu_type)
#        output_list["IGN"] = str(kpro.ign)
#        output_list["INJ"] = str(kpro.inj)  # S300 param; done
#        output_list["INJ%"] = str(kpro.injduty)  # S300 param; likely done
#        output_list["SERIAL"] = str(kpro.serial)
#        output_list["FIRMWARE"] = str(kpro.firmware)
#        output_list["IGADV"] = str(kpro.igadv)  # s300 param; done        
#        output_list["PHO2SV"] = str(kpro.pho2sv)  # S300 param; done
#        output_list["LVOLT"] = str(kpro.wbv)  # S300 param; done
#        output_list["EGRLV"] = str(kpro.egrlv)  # S300 param; done
#        output_list["B6V"] = str(kpro.b6v)  # S300 param; done
#        output_list["B54"] = str(kpro.byte54)  # S300 param
#        output_list["ELD"] = str(kpro.eld)  # S300 param; done
#        output_list["PATM"] = str(kpro.baro)  # S300 param; done
#        output_list["S.TRIM"] = str(kpro.strim)  # S300 param; done
#        output_list["L.TRIM"] = str(kpro.ltrim)  # S300 param; needs verification in-car
#        output_list["IATC"] = str(kpro.iatc)  # S300 param; done 
#        output_list["ECTC"] = str(kpro.ectc)  # S300 param; done
#        output_list["IAB"] = str(kpro.iab)  #S300 param; done
#        output_list["A10"] = str(kpro.a10)  #S300 param; done
#        output_list["CL"] = str(kpro.cl)  #S300 param; done 
#        output_list["ALTC"] = str(kpro.altc)  #S300 param; done
#        output_list["PCS"] = str(kpro.pcs)  #S300 param; done
#        output_list["VTS"] = str(kpro.vts)  #S300 param; done
#        output_list["N1_ARM"] = str(kpro.n1arm)  #S300 param; done
#        output_list["N1_ON"] = str(kpro.n1on)  #S300 param; done        
#        output_list["N2_ARM"] = str(kpro.n2arm)  #S300 param; done
#        output_list["N2_ON"] = str(kpro.n2on)  #S300 param; done 
#        output_list["N3_ARM"] = str(kpro.n3arm)  #S300 param; done
#        output_list["N3_ON"] = str(kpro.n3on)  #S300 param; done
#        output_list["DISTERR"] = str(kpro.disterr)  #S300 param; done
#        output_list["SECTBL"] = str(kpro.sectbl)  #S300 param; done
#        output_list["SECINJ"] = str(kpro.secinj)  #S300 param; done
#        output_list["REVL"] = str(kpro.revl)  #S300 param; done
#        output_list["IGNC"] = str(kpro.ignc)  #S300 param; done
#        output_list["LNCHC"] = str(kpro.lnchc)  #S300 param; done
#        output_list["LNCHR"] = str(kpro.lnchr)  #S300 param; done
#        output_list["BSTC"] = str(kpro.bstc)  #S300 param; done
#        output_list["SHFTC"] = str(kpro.shftc)  #S300 param; done
#        output_list["OBDL"] = str(kpro.obdl)  #S300 param; done
#        output_list["PWM"] = str(kpro.pwm)  # S300 param; done
#        output_list["BITS17"] = str(kpro.bits17)
#        output_list["BITS18"] = str(kpro.bits18)
#        output_list["BITS19"] = str(kpro.bits19)
#        output_list["BITS20"] = str(kpro.bits20)
#        output_list["BITS49"] = str(kpro.bits49)
#        output_list["BITS50"] = str(kpro.bits50)
#        output_list["BITS58"] = str(kpro.bits58)
