import urllib2
import json
from azure.storage import Entity

class IPAddressService:
    """
    Gets the external IP address
    """

    def __init__(self):
        self.actualIP = ''

    def __set_ip(self, ip):
        self.actualIP = ip
        return  ip

    def get_ip(self):
        """Gets the actual IP of the public network"""
        try:
            my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
            return self.__set_ip(my_ip)
        except:
            return self.__set_ip(IPAddress.__get_ip2())

    def __get_ip2(self):
        """Gets the actual IP of the public network - backup service"""
        try:
            response = urllib2.urlopen('http://httpbin.org/ip')
            ip = json.load(response)['origin']
            return ip
        except:
            return ''


class IPAddress(Entity):
    """
    Stores an ip address
    """
    def __init__(self, ip):
        self.ip = ip