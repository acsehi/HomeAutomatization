from TemperatureMonitor import TemperatureMonitor
import presence as ha
import time
import wificonnecteddevices
import AzureDataServices as azure
import logging
import os
import IPAddress as ip


def setup_log():
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(asctime)s: %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    file_formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]: %(message)s")
    file_handler = logging.FileHandler("presence.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def update_presence():
        change = presence.get_presence_change()
        if change:
            logger.info(change)
            presence_data_service.insert_presence(change)
            print 'Presence updated'


def update_temperature():
    oldTemp = temperature_service.actual_temp
    oldHum = temperature_service.actual_humidity
    o = temperature_service.get_observation()
    if oldTemp != o.temp and oldHum != o.humidity:
        temperature_data_service.insert_data(o)
        print 'Temperature updated'


def update_ip():
    old_ip = ip_address_service.actualIP
    new_ip = ip_address_service.get_ip()

    if new_ip != '' and old_ip != new_ip:
        ip_data_service.insert_data(ip.IPAddress(new_ip))
        ip_data_service.update_or_insert(ip.IPAddress(new_ip), 'latest')
        print 'IP updated'
    
if __name__ == '__main__':
    print 'Started'
    if os.environ.get("raspberry") is None:
        print 'raspberry system environment not detected'
    logger = setup_log()

    users = ha.init_users_from_file()
    wifi = wificonnecteddevices.WifiConnectedDevices('http://192.168.0.1/sky_attached_devices.html')
    
    presence_data_service = azure.AzureDataServices('presence')
    presence_data_service.create_table()

    temperature_service = TemperatureMonitor()
    temperature_data_service = azure.AzureDataServices('temperature')
    temperature_data_service.create_table()

    ip_address_service = ip.IPAddressService()
    ip_data_service = azure.AzureDataServices('address')
    ip_data_service.create_table()
    
    presence = ha.Presence(users, wifi)
    i = 0
    while True:
        if i % 60 == 0:
            update_temperature()
            update_ip()
        if i % 6 == 0:
            update_presence()
        i += 1
        if i >= 1000:
            i = 0
        time.sleep(10)