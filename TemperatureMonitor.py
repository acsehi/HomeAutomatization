import time
from azure.storage import Entity
import Adafruit_DHT

class TemperatureObservation(Entity):
    def __init__(self, temp, humidity, datetime):
        self.temp = temp
        self.datetime = datetime
        self.humidity = humidity


class TemperatureMonitor:

    def __init__(self):
        self.actual_temp = -1
        self.actual_humidity = -1

    def get_observation(self):
        sensor = Adafruit_DHT.DHT11
        pin = 4
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            self.actual_temp = temperature
            self.actual_humidity = humidity
        except RuntimeError:
            # Code not running on PI
            return TemperatureObservation(0, 0, t)

        print temperature, humidity

        return TemperatureObservation(temperature,humidity,t)