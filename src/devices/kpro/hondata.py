import json
import websocket
try:
    import thread
except ImportError:
    import _thread as thread

class HondataBluetooth:
    message = None
    bluetoothAddress = None

    def __init__(self, bluetoothAddress):
        self.message = None
        self.bluetoothAddress = bluetoothAddress
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://localhost:8081/datalog?deviceAddress={}".format(self.bluetoothAddress),
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close)
        ws.on_open = self.on_open
        def run(*args):
            ws.run_forever()
            print("thread terminating...")
        thread.start_new_thread(run, ())

    def on_message(ws, message):
        print("received message {} ".format(message))
        ws.message = json.loads(message)
        print(ws.message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        print("## opened ## ")

    def get(self, field, default):
        #print("trying to get field '{}' ... ".format(field))
        if self.message is None:
            print("trying to get field '{}' failed! message not set ".format(field))
            return default
        else:
            try:
                val = self.message.get(field)
                #print("'{}' =  {} ... ".format(field, val))
                return val
            except IndexError:
                print("failed to get field '{}' ... ".format(field))
                return default

    def bat(self):
        """
        Battery voltage
        """
        # return unit: volts
        return self.get('bat', 0)

    def eth(self):
        """
        Ethanol content
        """
        # return unit: per cent
        return 0

    def flt(self):
        return {"celsius": 0, "fahrenheit": 0}

    def o2(self):
        """
        Oxygen sensor
        """
        # return unit: afr and lambda
        return {"afr": 0, "lambda": 0}

    def tps(self):
        """
        Throttle position sensor
        """
        return self.get('tps', 0)

    def vss(self):
        """
        Vehicle speed sensor
        """
        # return unit: km/h and mph
        return {"kmh": 0, "mph": 0}

    def rpm(self):
        # return unit: revs. per minute
        return self.get('rpm', 0)

    def cam(self):
        # return units: degree
        return 0

    def ect(self):
        """
        Engine coolant temperature
        """
        # return units: celsius and fahrenheit
        return {"celsius": 0, "fahrenheit": 0}

    def iat(self):
        """
        Intake air temperature
        """
        # return units: celsius and fahrenheit
        return {"celsius": 0, "fahrenheit": 0}

    def gear(self):
        gear = self.get('gear', 0)
        if gear == 0:
            return "N"
        else:
            return gear

    def eps(self):
        """
        Electric power steering
        """
        return False

    def scs(self):
        return False

    def rvslck(self):
        """
        Reverse gear lock
        """
        return False

    def bksw(self):
        """
        Brake switch
        """
        return False

    def acsw(self):
        """
        Aircon switch
        """
        return False

    def accl(self):
        return False

    def flr(self):
        """
        Fuel relay
        """
        return False

    def fanc(self):
        """
        Fan switch
        """
        return False

    def map(self):
        """
        Manifold absolute pressure
        """
        # return unit: bar, mbar and psi
        return {"bar": 0, "mbar": 0, "psi": 0}

    def mil(self):
        """
        Malfunction indicator light also known as check engine light
        """
        return False

    def ecu_type(self):
        return "unknown"

    def ign(self):
        """
        Ignition timing
        """
        return False

    def serial(self):
        return 0

    def firmware(self):
        return 0

    def analog_input(self, channel):
        return 0
