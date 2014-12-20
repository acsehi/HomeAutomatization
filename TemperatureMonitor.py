import time
from azure.storage import Entity
import Adafruit_DHT

class TemperatureObservation(Entity):
    def __init__(self, temp, humidity, datetime):
        self.temp = temp
        self.datetime = datetime
        self.humidity = humidity


class TemperatureMonitor:

    @staticmethod
    def get_observation():
        sensor = Adafruit_DHT.DHT11
        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        print temperature, humidity
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        return TemperatureObservation(temperature,humidity,t)