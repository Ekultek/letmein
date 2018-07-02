import os
import base64
import string
import random
import hashlib

import encryption.aes_encryption
from lib.output import (
    info,
    warning,
    fatal,
    prompt
)

try:
    xrange
except:
    xrange = range

HOME = os.path.expanduser("~")
MAIN_DIR = "{}/.letmein".format(HOME)
DATABASE_FILE = "{}/letmein.db".format(MAIN_DIR)
VERSION = "0.0.1.1"
BANNER = """\n\033[32m
   __      _                _____\033[0m\033[32m      
  / /  ___| |_  /\/\   ___  \_   \ \033[0m
 / /  / _ \ __|/    \ / _ \  / /\/ '_ \ \033[0m\033[32m 
/ /__|  __/ |_/ /\/\ \  __/\/ /_ | | | | \033[0m
\____/\___|\__\/    \/\___\____/ |_| |_| \033[0m\033[32m[]\033[0m[]\033[0m\033[32m[]\033[0m[]
Version: v{}\033[0m
\n""".format(VERSION)


def sha256_rounds(raw, rounds=2000000, salt="vCui3d8,?j;%Rm#'zPs'Is53U:43DS%8rs$_FBsrLD_nQ"):
    """
    encrypt a string using 2 million rounds of PBKDF2-HMAC-SHA-256
    """
    obj = hashlib.pbkdf2_hmac
    return obj("sha256", raw, salt, rounds)


def secure_delete(path, random_fill=True, null_fill=True, passes=3):
    """
    securely delete a file by passing it through both random and null filling
    """
    files = os.listdir(path)
    for i, f in enumerate(files):
        files[i] = "{}/{}".format(path, f)
    for item in files:
        with open(item, "wr") as data:
            length = data.tell()
            if random_fill:
                for _ in xrange(passes):
                    data.seek(0)
                    data.write(os.urandom(length))
            if null_fill:
                for _ in xrange(passes):
                    data.seek(0)
                    data.write("\x00" * length)
        os.remove(item)


def store_key(path):
    """
    store the encrypted key or be prompted to create one
    """
    if not os.path.exists(path):
        os.mkdir(path)
    password_file = "{}/.pass".format(path)
    key_file = "{}/.key".format(path)
    if not os.path.exists(password_file):
        provided_key = prompt(
            "you have not provided an encryption key, please provide one: ", hide=True
        )
        key = base64.urlsafe_b64encode(sha256_rounds(provided_key))
        encryption.aes_encryption.AESCipher(key).generate_key(provided_key)
        length = len(key)
        with open(password_file, "a+") as key_:
            front_salt, back_salt = os.urandom(16), os.urandom(16)
            key_.write("{}{}{}:{}".format(front_salt, key, back_salt, length))

        info(
            "key has been stored successfully and securely. you will be given three attempts to successfully "
            "enter your stored key at each login, after three failed attempts all data in the programs home "
            "directory will be securely erased. you will need to re-run the application now."
        )
        exit(-1)
    else:
        with open(password_file) as data:
            retval = data.read()
            amount = retval.split(":")[-1]
            edited = retval[16:]
            edited = edited[:int(amount)]
        with open(key_file) as data:
            retval = encryption.aes_encryption.AESCipher(edited).decrypt(data.read())
        return retval, edited


def compare(stored):
    """
    compare the provided key hash with the stored key hash
    """
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
                warning("incorrect key")
    return False


def display_formatted_list_output(data, key, prompting=True, answer="n"):
    """
    display decrypted data in plaintext
    """
    separator = "-" * 30

    if prompting:
        choice = prompt("display plaintext?[y/N] ")
    else:
        choice = answer

    if choice.lower().startswith("y"):
        warning("all output is displayed in plaintext")
        print(separator)
        for row in data:
            print(
                "INFO: {0: <30}\tSTORED PASSWORD: {1: <40}".format(
                    row[0],
                    encryption.aes_encryption.AESCipher(key).decrypt(row[1])
                )
            )
        print(separator)
    else:
        print(separator)
        for row in data:
            print(
                "INFO: {0: <30}\tSTORED PASSWORD(hidden): {1: <40}".format(
                    row[0],
                    "*" * 7
                )
            )


def random_string(length=5, hard=False):
    """
    create a random string
    """
    if not hard:
        acceptable = string.ascii_letters
    else:
        acceptable = list(string.printable)[:-6]
    retval = []
    for _ in range(length):
        retval.append(random.choice(acceptable))
    return ''.join(retval)
