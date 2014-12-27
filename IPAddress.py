import urllib2
import json
import sys

class IPAddress:


    @staticmethod
    def get_ip():
        """Gets the actual IP of the public network"""
        try:
            my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
            return my_ip
        except:
            return IPAddress.__get_ip2()

    @staticmethod
    def __get_ip2():
        """Gets the actual IP of the public network - backup service"""
        try:
            response = urllib2.urlopen('http://httpbin.org/ip')
            ip = json.load(response)['origin']
            return ip
        except:
            return ''