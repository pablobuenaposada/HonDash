import functools

from backend.devices.kpro.kpro import Kpro, KproException
from backend.devices.s300.s300 import S300


class Ecu:
    def handle_exceptions(default):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except KproException:
                    #self.__init__()
                    return default

            return wrapper

        return actual_decorator

    def __init__(self):
        kpro = Kpro()
        if kpro.status:
            self.ecu = kpro
        else:
            s300 = S300()
            self.ecu = s300 if s300.status else None

    @property
    @handle_exceptions({"kmh": 0, "mph": 0})
    def vss(self):
        return getattr(self.ecu, "vss")

    @property
    @handle_exceptions(0)
    def tps(self):
        return getattr(self.ecu, "tps")

    @property
    @handle_exceptions(0)
    def bat(self):
        return getattr(self.ecu, "bat")

    @property
    @handle_exceptions(0)
    def gear(self):
        return getattr(self.ecu, "gear")

    @property
    @handle_exceptions({"celsius": 0, "fahrenheit": 0})
    def iat(self):
        return getattr(self.ecu, "iat")

    @property
    @handle_exceptions({"celsius": 0, "fahrenheit": 0})
    def ect(self):
        return getattr(self.ecu, "ect")

    @property
    @handle_exceptions(0)
    def rpm(self):
        return getattr(self.ecu, "rpm")

    @property
    @handle_exceptions({"bar": 0, "mbar": 0, "psi": 0})
    def map(self):
        return getattr(self.ecu, "map")

    @property
    @handle_exceptions({"afr": 0, "lambda": 0})
    def o2(self):
        return getattr(self.ecu, "o2")

    @property
    @handle_exceptions(0)
    def cam(self):
        return getattr(self.ecu, "cam")

    @property
    @handle_exceptions(0)
    def eth(self):
        return getattr(self.ecu, "eth")

    @property
    @handle_exceptions({"celsius": 0, "fahrenheit": 0})
    def flt(self):
        return getattr(self.ecu, "flt")

    @property
    @handle_exceptions(False)
    def mil(self):
        return getattr(self.ecu, "mil")

    @property
    @handle_exceptions(False)
    def fanc(self):
        return getattr(self.ecu, "fanc")

    @property
    @handle_exceptions(False)
    def bksw(self):
        return getattr(self.ecu, "bksw")

    @property
    @handle_exceptions(False)
    def flr(self):
        return getattr(self.ecu, "flr")

    @property
    @handle_exceptions(False)
    def scs(self):
        return getattr(self.ecu, "scs")

    @property
    @handle_exceptions(False)
    def eps(self):
        return getattr(self.ecu, "eps")

    @property
    @handle_exceptions(False)
    def rvslck(self):
        return getattr(self.ecu, "rvslck")

    @property
    @handle_exceptions(False)
    def acsw(self):
        return getattr(self.ecu, "acsw")

    @property
    @handle_exceptions(False)
    def accl(self):
        return getattr(self.ecu, "accl")

    @property
    @handle_exceptions(False)
    def ign(self):
        return getattr(self.ecu, "ign")

    @property
    @handle_exceptions("0.00")
    def firmware(self):
        return getattr(self.ecu, "firmware")

    @property
    @handle_exceptions(0)
    def serial(self):
        return getattr(self.ecu, "serial")

    @property
    @handle_exceptions("unknown")
    def ecu_type(self):
        return getattr(self.ecu, "ecu_type")

    @property
    def name(self):
        if self.ecu is not None and self.ecu.status:
            return self.ecu.NAME
        else:
            return "unknown"

    @handle_exceptions(0)
    def analog_input(self, channel):
        result = getattr(self.ecu, "analog_input")
        if isinstance(result, int):  # if something went wrong we will get a 0
            return result
        else:
            return result(channel)
