import base64
import string
import random

from Crypto import Random
from Crypto.Cipher import AES

from lib.settings import (
    sha256_rounds,
    MAIN_DIR
)


class AESCipher(object):

    """
    implementation of the AES Cipher using PyCrypto
    """

    def __init__(self, key):
        self.key = sha256_rounds(key)
        self.block_size = AES.block_size
        self.pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])]

    def encrypt(self, plaintext):
        raw = self.pad(plaintext)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, encrypted):
        enc = base64.b64decode(encrypted)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))

    def generate_key(self, raw):
        contingent_length = random.choice(range(100, 500))
        acceptable_padding = list(string.printable)
        length = len(raw)
        half = length / 2
        new_raw = raw[:half]
        if half != contingent_length:
            while half != contingent_length:
                new_raw += random.choice(acceptable_padding)
                half = len(new_raw) / 2
        salt = Random.get_random_bytes(78)
        new_raw = "$letmein_main${}${}".format(new_raw, salt)
        with open("{}/.key".format(MAIN_DIR), "a+") as keyfob:
            key = self.encrypt(new_raw)
            keyfob.write(key)
