import homeauto as ha
import time

users = []
with open('users', 'r') as u:
    lines = u.readlines()
    for l in lines:
        users.append(ha.User.from_string(l))

presence = ha.Presence(users)

while True:
    time.sleep(2)
    aUsers = presence.get_presence()
    with open('presence.log', 'a') as f:
        for user in users:
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            entry = '%s: %s\n' % (ts, user)
            f.write(entry)
            print(entry)
