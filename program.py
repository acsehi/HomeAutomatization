import homeauto as ha
import logging
import os
import time

if __name__ == '__main__':
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

    users = []
    with open('users', 'r') as u:
        lines = u.readlines()
    for line in lines:
        users.append(ha.User.from_string(line))

    presence = ha.Presence(users)

    while True:
        time.sleep(2)
        users_present = presence.get_presence()
        for user in users_present:
            logger.info(user)
