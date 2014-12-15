import urllib as url
import re
from requests.auth import HTTPBasicAuth
import requests

class WifiConnectedDevices:
    """
    Gets the connected devices on the wifi network
    """
    def __init__(self, host):
        self._user, self._password = WifiConnectedDevices.__read_credential()
        self._host = host

    @staticmethod
    def __read_credential():
        """
        Reads the credentials
        No encryption for now
        """
        with open('cred.txt') as f:
            lines = f.readlines()
        return lines[0].strip(), lines[1].strip()

    def get_devices(self):
        """
        Gets the devices on the network
        :return: Array of Device class
        """
        try:
            r = requests.get(self._host, auth=HTTPBasicAuth(self._user, self._password))
            html = r.text
            return self.__parse(html)
        except Exception as a:
            print a
            return
    @staticmethod
    def __parse(data):
        """
        Parses out the devices from html
        :param data: Html response from the wifi router
        :return:Array of Device class
        """
        match = re.search('attach_dev = \\\'([^\']*)', data)
        if match:
            lines = match.group(1).split('<lf>')
            devices = []
            for line in lines:
                d = line.split('<br>')
                device = Device(d[0], d[1], d[2])
                devices.append(device)
            return devices
        return


class Device:
    """
    Represent a wifi connected device
    """
    def __init__(self, ip, name, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

    def __str__(self):
        return "%s %s %s" % (self.ip, self.name, self.mac)