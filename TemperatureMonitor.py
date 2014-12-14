import time
from azure.storage import Entity
import AzureDataServices as azure

class TemperatureObservation(Entity):
    def __init__(self, temp, datetime):
        self.temp = temp
        self.datetime = datetime


class TemperatureMonitor:

    def get_observation(self):
        #rpi logic here
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        return TemperatureObservation(0, t)

if __name__ == '__main__':
    data_service = azure.AzureDataServices('temperature')
    data_service.create_table()
    tm = TemperatureMonitor()
    o = tm.get_observation()
    data_service.insert_data(o)
