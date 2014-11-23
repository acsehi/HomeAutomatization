import urllib.request as url
import urllib.error as urlerror
import re

class WifiConnectedDevices:
    _host = ''
    _user = ''
    _password = ''
    
    def __init__ (self, host, user, password):
        self._host = host
        self._user = user
        self._password = password

    def getDevices(self):
        # Create an OpenerDirector with support for Basic HTTP Authentication...
        auth_handler = url.HTTPBasicAuthHandler()
        auth_handler.add_password('Broadband Router',
                                  uri=self._host,
                                  user=self._user,
                                  passwd=self._password)
        opener = url.build_opener(auth_handler)
        # ...and install it globally so it can be used with urlopen.
        url.install_opener(opener)
        try:
            f = url.urlopen(self._host)
            html = f.read().decode()
            return self.parse(html)
        except urlerror.HTTPError as e:
            return

    def parse(self, data):
        match = re.search('attach_dev = \\\'([^\']*)', data)
        if match:
            lines = match.group(1).split('<lf>')
            devices = []
            for line in lines:
                d = line.split('<br>')
                device = Device(d[0],d[1],d[2])
                devices.append(device)
            return devices
        return
        
    
class Device:
        def __init__ (self,ip,name,mac):
            self.name=name
            self.ip=ip
            self.mac=mac
        def print(self):
            print(self.ip,self.name,self.mac)
