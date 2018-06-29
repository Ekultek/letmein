import base64

from Crypto import Random
from Crypto.Cipher import AES

from lib.settings import sha256_rounds


class AESCipher(object):

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