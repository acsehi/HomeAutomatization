import homeauto as ha
import time

if __name__ == '__main__':
    users = []
    with open('users', 'r') as u:
        lines = u.readlines()
    for line in lines:
        users.append(ha.User.from_string(line))

    presence = ha.Presence(users)

    while True:
        time.sleep(2)
        users_present = presence.get_presence()
        with open('presence.log', 'a') as f:
            for user in users_present:
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                entry = '%s: %s\n' % (ts, user)
                f.write(entry)
                print(entry)
