import wificonnecteddevices as wifi


class Presence:
    def __init__(self, users):
        # encryption to be added

        user_name, password = self.__read_credential()
        self._wifi = wifi.WifiConnectedDevices('http://192.168.0.1/sky_attached_devices.html', user_name, password)

        self._users = users

    def get_presence(self):
        """
        Gets the users present
        :return:Array of User class
        """
        users_present = []
        devices = self._wifi.get_devices()

        for user in self._users:
            for device in devices:
                if user.has_device(device):
                    users_present.append(user)

        return users_present

    @staticmethod
    def __read_credential():
        """
        Reads the credentials
        No encryption for now
        """
        with open('cred.txt') as f:
            lines = f.readlines()
        return lines[0].strip(), lines[1].strip()


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
        name, macs = s.split(':')
        return User(name, macs.split(','))

    def has_mac(self, mac):
        """
        Returns true if the user has a device with the give MAC address
        :param mac: MAC address
        :return:bool
        """
        if mac in self._macs:
            return True
        return False

    def has_device(self, device):
        """
        Returns true of the user owns the device
        :param device: Device to be checked
        :return:bool
        """
        return self.has_mac(device.mac)
