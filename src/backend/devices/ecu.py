from backend.devices.kpro.kpro import Kpro
from backend.devices.s300.s300 import S300

WAIT_FOR_RECONNECTION = 100


class Ecu:
    def __init__(self):
        self.retries = 0
        kpro = Kpro()
        if kpro.status:
            self.ecu = kpro
        else:
            s300 = S300()
            self.ecu = s300 if s300.status else None

    def _get_value_from_ecu(self, value, fallback=0):
        if self.ecu is not None and self.ecu.status:
            try:
                return getattr(self.ecu, value)
            except AttributeError:  # maybe the ecu doesn't have that value
                return fallback
        else:
            if self.retries > WAIT_FOR_RECONNECTION:
                self.__init__()
            else:
                self.retries += 1
            return fallback

    @property
    def vss(self):
        return self._get_value_from_ecu("vss", {"kmh": 0, "mph": 0})

    @property
    def tps(self):
        return self._get_value_from_ecu("tps")

    @property
    def bat(self):
        return self._get_value_from_ecu("bat")

    @property
    def gear(self):
        return self._get_value_from_ecu("gear")

    @property
    def iat(self):
        return self._get_value_from_ecu("iat", {"celsius": 0, "fahrenheit": 0})

    @property
    def ect(self):
        return self._get_value_from_ecu("ect", {"celsius": 0, "fahrenheit": 0})

    @property
    def rpm(self):
        return self._get_value_from_ecu("rpm")

    @property
    def map(self):
        return self._get_value_from_ecu("map", {"bar": 0, "mbar": 0, "psi": 0})

    @property
    def o2(self):
        return self._get_value_from_ecu("o2", {"afr": 0, "lambda": 0})

    @property
    def cam(self):
        return self._get_value_from_ecu("cam")

    @property
    def eth(self):
        return self._get_value_from_ecu("eth")

    @property
    def flt(self):
        return self._get_value_from_ecu("flt", {"celsius": 0, "fahrenheit": 0})

    @property
    def mil(self):
        return self._get_value_from_ecu("mil", False)

    @property
    def fanc(self):
        return self._get_value_from_ecu("fanc", False)

    @property
    def bksw(self):
        return self._get_value_from_ecu("bksw", False)

    @property
    def flr(self):
        return self._get_value_from_ecu("flr", False)

    @property
    def scs(self):
        return self._get_value_from_ecu("scs", False)

    @property
    def eps(self):
        return self._get_value_from_ecu("eps", False)

    @property
    def rvslck(self):
        return self._get_value_from_ecu("rvslck", False)

    @property
    def acsw(self):
        return self._get_value_from_ecu("acsw", False)

    @property
    def accl(self):
        return self._get_value_from_ecu("accl", False)

    @property
    def ign(self):
        return self._get_value_from_ecu("ign", False)

    @property
    def firmware(self):
        return self._get_value_from_ecu("firmware")

    @property
    def serial(self):
        return self._get_value_from_ecu("serial")

    @property
    def ecu_type(self):
        return self._get_value_from_ecu("ecu_type", "unknown")

    @property
    def name(self):
        if self.ecu is not None and self.ecu.status:
            return self.ecu.NAME
        else:
            return "unknown"

    def analog_input(self, channel):
        result = self._get_value_from_ecu("analog_input")
        if isinstance(result, int):  # if something went wrong we will get a 0
            return result
        else:
            return result(channel)
    """----------------------------------------------------------------------------------
    AJ Edits go below here
    """
    @property
    def inj(self):
        return self._get_value_from_ecu("inj")   #TODO Needs Units

    @property
    def injduty(self):
        return self._get_value_from_ecu("injduty")

    @property
    def igadv(self):
        return self._get_value_from_ecu("igadv")
        
    @property
    def pho2sv(self):
        return self._get_value_from_ecu("pho2sv")
        
    @property
    def strim(self):
        return self._get_value_from_ecu("strim")
       
    @property
    def ltrim(self):
       return self._get_value_from_ecu("ltrim")

    @property
    def iatc(self):
        return self._get_value_from_ecu("iatc")

    @property
    def ectc(self):
        return self._get_value_from_ecu("ectc")

    @property
    def wbv(self):
        return self._get_value_from_ecu("wbv")

    @property
    def egrlv(self):
        return self._get_value_from_ecu("egrlv")

    @property
    def b6v(self):
        return self._get_value_from_ecu("b6v")

    @property
    def baro(self):
        return self._get_value_from_ecu("baro", {"bar": 0, "mbar": 0, "psi": 0})

    @property
    def eld(self):
        return self._get_value_from_ecu("eld")

    @property
    def psp(self):
        return self._get_value_from_ecu("psp", False)
        
    @property
    def vtp(self):
        return self._get_value_from_ecu("vtp", False)        

    @property
    def a10(self):
        return self._get_value_from_ecu("a10", False)

    @property
    def cl(self):
        return self._get_value_from_ecu("cl", False)

    @property
    def altc(self):
        return self._get_value_from_ecu("altc", False)

    @property
    def iab(self):
        return self._get_value_from_ecu("iab", False)

    @property
    def pcs(self):
        return self._get_value_from_ecu("pcs", False)

    @property
    def vts(self):
        return self._get_value_from_ecu("vts", False)

    @property
    def n1arm(self):
        return self._get_value_from_ecu("n1arm", False)

    @property
    def n1on(self):
        return self._get_value_from_ecu("n1on", False)

    @property
    def n2arm(self):
        return self._get_value_from_ecu("n2arm", False)

    @property
    def n2on(self):
        return self._get_value_from_ecu("n2on", False)

    @property
    def n3arm(self):
        return self._get_value_from_ecu("n3arm", False)

    @property
    def n3on(self):
        return self._get_value_from_ecu("n3on", False)

    @property
    def disterr(self):
        return self._get_value_from_ecu("disterr", False)

    @property
    def sectbl(self):
        return self._get_value_from_ecu("sectbl", False)

    @property
    def secinj(self):
        return self._get_value_from_ecu("secinj", False)

    @property
    def revl(self):
        return self._get_value_from_ecu("revl", False)

    @property
    def lnchc(self):
        return self._get_value_from_ecu("lnchc", False)

    @property
    def lnchr(self):
        return self._get_value_from_ecu("lnchr", False)

    @property
    def bstc(self):
        return self._get_value_from_ecu("bstc", False)

    @property
    def shftc(self):
        return self._get_value_from_ecu("shftc", False)

    @property
    def ignc(self):
        return self._get_value_from_ecu("ignc", False)

    @property
    def obdl(self):
        return self._get_value_from_ecu("obdl", False)

    @property
    def pwm(self):           
        return self._get_value_from_ecu("pwm", False)
