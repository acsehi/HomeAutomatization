import wificonnecteddevices as wifi
from azure.storage import Entity


def init_users_from_file():
    users = []
    with open('users.txt', 'r') as u:
        lines = u.readlines()
        for l in lines:
            users.append(User.from_string(l))
    return users


class Presence:
    def __init__(self, users, wifi):
        """
        Creates a new Presence object
        :param users: All users in the system
        :param wifi: instance of an WifiConnectedDevices
        """
        self._wifi = wifi

        self._users = users
        self._lastUsers = []

    def get_presence_change(self):
        currentUsers = self.get_presence()
        currentUserNames = []
        pc = PresenceChange()
        hasChange = False
        for u in currentUsers:
            currentUserNames.append(u._name)

        for oldUser in self._lastUsers:
            if oldUser not in currentUserNames:
                print(oldUser + ' has left')
                pc.users_left.append(oldUser)
                hasChange = True

        for currentUser in currentUserNames:
            if currentUser not in self._lastUsers:
                print(currentUser + ' has arrived')
                pc.users_arrived.append(currentUser)
                hasChange = True

        self._lastUsers = currentUserNames
        pc.active_users = currentUsers
       
        if hasChange:
            return pc
        else:
            return None

    def get_presence(self):
        """
        Gets the users present
        :return:Array of User class
        """
        usersPresent = {}
        devices = self._wifi.get_devices()

        for user in self._users:
            for device in devices:
                if user.has_device(device):
                    if usersPresent.get(user._name) == None:
                        user.active_devices.append(device)
                        usersPresent[user._name] = user
                    else:
                        usersPresent[user._name].active_devices.append(device)
        return usersPresent.values()


class PresenceChange:
    def __init__(self):
        self.users_left = []
        self.users_arrived = []
        self.active_users = []


class User:
    """
    Represents an User
    """

    def __init__(self, name, macs):
        self._name = name
        self._macs = macs
        self.active_devices = []

    def __str__(self):
        return self._name

    @staticmethod
    def from_string(s):
        """
        Creates an User from a string
        :param s: string (name:mac1,mac2...)
        :return: User
        """
        name, macs = s.split('#')
        return User(name, macs.split(','))

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