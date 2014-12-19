import time
from azure.storage import Entity
import Adafruit_DHT

class TemperatureObservation(Entity):
    def __init__(self, temp, humidity, datetime):
        self.temp = temp
        self.datetime = datetime
        self.humidity = humidity


class TemperatureMonitor:
    sensor = Adafruit_DHT.DHT22
    pin = 6

    @staticmethod
    def get_observation(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        return TemperatureObservation(temperature,humidity,t)