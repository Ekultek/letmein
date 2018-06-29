import os
import base64
import hashlib

import encryption.aes_encryption
from lib.output import info, warning, error, fatal, prompt

try:
    xrange
except:
    xrange = range

HOME = os.path.expanduser("~")
MAIN_DIR = "{}/.letmein".format(HOME)
DATABASE_FILE = "{}/letmein.db".format(MAIN_DIR)


def sha256_rounds(raw, rounds=2000000, salt="vCui3d8,?j;%Rm#'zPs'Is53U:43DS%8rs$_FBsrLD_nQ"):
    obj = hashlib.pbkdf2_hmac
    return obj("sha256", raw, salt, rounds)


def secure_delete(path, random_fill=True, null_fill=True, passes=3):
    with open(path, "wr") as data:
        length = data.tell()
        if random_fill:
            for _ in xrange(passes):
                data.seek(0)
                data.write(os.urandom(length))
        if null_fill:
            for _ in xrange(passes):
                data.seek(0)
                data.write("\x00" * length)
    os.remove(path)


def store_key(path):
    key_file = "{}/.key".format(path)
    if not os.path.exists(key_file):
        provided_key = prompt(
            "you have not provided an encryption key, please provide one: ", hide=True
        )
        key = base64.urlsafe_b64encode(sha256_rounds(provided_key))
        length = len(key)
        with open(key_file, "a+") as key_:
            front_salt, back_salt = os.urandom(16), os.urandom(16)
            key_.write("{}{}{}:{}".format(front_salt, key, back_salt, length))
        info(
            "key has been stored successfully and securely. you will be given three attempts to successfully "
            "enter your stored key at each login, after three attempts all data in the programs home directory "
            "will be securely erased"
        )
        exit(-1)
    else:
        retval = open(key_file).read()
        amount = retval.split(":")[-1]
        edited = retval[16:]
        edited = edited[:int(amount)]
        return edited


def compare(stored):
    tries = 3

    while True:
        provided_key = prompt(
            "enter your encryption key, {} tries left: ".format(tries), hide=True
        )
        stored_key = base64.urlsafe_b64decode(stored)
        provided_key = sha256_rounds(provided_key)
        if stored_key == provided_key:
            return True
        else:
            tries -= 1
            if tries == 0:
                break
            elif tries == 1:
                fatal("you have one chance left to provide the correct key or all data will be deleted")
            else:
                warning("incorrect key".format(tries))
    return False


def display_formatted_list_output(data, key):
    seperator = "-" * 30

    print(seperator)
    for row in data:
        print(
            "INFO: {0: <30}\tSTORED PASSWORD: {1: <40}".format(
                row[0],
                encryption.aes_encryption.AESCipher(key).decrypt(row[1])
            )
        )
    print(seperator)
    warning("all output is displayed in plaintext")

