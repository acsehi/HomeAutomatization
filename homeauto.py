import wificonnecteddevices as wifi

class Presence:
    def __init__(self, users):
        # encryption to be added

        cred = self.__read_credential()
        userName = cred[0].rstrip()
        password = cred[1].rstrip()
        self._wifi = wifi.WifiConnectedDevices('http://192.168.0.1/sky_attached_devices.html', userName, password)

        self._users = users

    def get_presence(self):
        """
        Gets the users present
        :return:Array of User class
        """
        usersPresent = {}
        devices = self._wifi.get_devices();

        for user in self._users:
            for device in devices:
                if (user.has_device(device)):
                    usersPresent[user] = user

        return usersPresent

    @staticmethod
    def __read_credential():
        """
        Reads the credentials
        No encryption for now
        """
        f = open('cred.txt')
        lines = f.readlines()
        f.close()
        cred = [lines[0], lines[1]];

        return cred


class User:
    """
    Represents an User
    """

    def __init__(self, name, macs):
        self._name = name
        self._macs = macs

    def __str__(self):
        return self._name

    @staticmethod
    def from_string(s):
        """
        Creates an User from a string
        :param s: string (name:mac1,mac2...)
        :return: User
        """
        l = s.split(':')
        u = User(l[0],l[1].split(','))

        return  u

    def has_mac(self, mac):
        """
        Returns true if the user has a device with the give MAC address
        :param mac: MAC address
        :return:bool
        """
        for m in self._macs:
            if m == mac:
                return True
        return False

    def has_device(self, device):
        """
        Returns true of the user owns the device
        :param device: Device to be checked
        :return:bool
        """
        return self.has_mac(device.mac)
