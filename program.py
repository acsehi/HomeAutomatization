import homeauto as ha
import time
import wificonnecteddevices
import AzureDataServices as azure
import logging
import os


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

if __name__ == '__main__':
    logger = setup_log()
    
    users = ha.init_users_from_file()
    wifi = wificonnecteddevices.WifiConnectedDevices('http://192.168.0.1/sky_attached_devices.html')
    
    data_service = azure.AzureDataServices()
    data_service.create_table()
    
    presence = ha.Presence(users, wifi)
    
    while True:
        change = presence.get_presence_change()
        if change != None:
            logger.info(change)
            data_service.insert_presence(change)
            t = data_service.get_presence()
        time.sleep(10)