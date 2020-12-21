from os import urandom
from base64 import b64encode


def randomKey():
    return b64encode(urandom(32)).decode()
