import os
import sys
import struct
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
VERSION = "0.0.1.8({})"
VERSION_STRING = "\033[31m\033[1m*beta\033[0m" if VERSION.count(".") == 3 else "\033[1m\033[36m~alpha\033[0m" if VERSION.count(".") == 2 else "\033[1m\033[32m+stable\033[0m"
INIT_FILE = "{}/.init".format(MAIN_DIR)
BANNER = """\n\033[32m
   __      _                _____\033[0m\033[32m      
  / /  ___| |_  /\/\   ___  \_   \ \033[0m
 / /  / _ \ __|/    \ / _ \  / /\/ '_ \ \033[0m\033[32m 
/ /__|  __/ |_/ /\/\ \  __/\/ /_ | | | | \033[0m
\____/\___|\__\/    \/\___\____/ |_| |_| \033[0m\033[32m[]\033[0m[]\033[0m\033[32m[]\033[0m[]
Version: v{}\033[0m
\n""".format(VERSION.format(VERSION_STRING))


def sha256_rounds(raw, rounds=1500000, salt="vCui3d8,?j;%Rm#'zPs'Is53U:43DS%8rs$_FBsrLD_nQ"):
    """
    encrypt a string using 1.5 million rounds of PBKDF2-HMAC-SHA-256
    """
    obj = hashlib.pbkdf2_hmac
    return obj("sha256", raw, salt, rounds)


def secure_delete(path, triple_fill=True, passes=3):
    """
    securely delete a file by passing it through both random and null filling
    """
    files = os.listdir(path)
    for i, f in enumerate(files):
        files[i] = "{}/{}".format(path, f)
    for item in files:
        length = os.path.getsize(item)
        data = open(item, "w")
        if triple_fill:
            # fill with random printable characters
            for _ in xrange(passes):
                data.seek(0)
                data.write(''.join(random.choice(string.printable) for _ in range(length)))
            # fill with random data from the OS
            for _ in xrange(passes):
                data.seek(0)
                data.write(os.urandom(length))
            # fill with null bytes
            for _ in xrange(passes):
                data.seek(0)
                data.write(struct.pack("B", 0) * length)
        data.close()
        os.remove(item)


def write_init_file(filename, files, path):
    """
    configure the init file on your first run
    """
    retval = []
    for item in files:
        retval.append("{}/{}".format(path, item))
    with open(filename, "a+") as data:
        for item in retval:
            change_time = os.stat(item).st_mtime
            data.write(str(change_time) + "\n")


def store_key(path, grab_key=False):
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
        write_init_file(INIT_FILE, os.listdir(MAIN_DIR), MAIN_DIR)
        info(
            "letmein has been initialized. you will need to re-run the program."
        )
        exit(-1)
    else:
        check_for_file_change()
        with open(password_file) as data:
            retval = data.read()
            amount = retval.split(":")[-1]
            edited = retval[16:]
            edited = edited[:int(amount)]
        if grab_key:
            with open(key_file) as data:
                retval = encryption.aes_encryption.AESCipher(edited).decrypt(data.read())
        else:
            retval = None

        return retval, edited


def compare(stored):
    """
    compare the provided key hash with the stored key hash
    """

    def complex_verification(provided, stored):
        """
        a complex comparison of two different strings
        compares the following:
         * checking the length of the strings match
         * checking if each character in the strings matches
         * checking the system size of the strings
         * checking if the random nth end characters of the strings match
        """
        random_int_check = random.choice(range(len(provided)))

        if not len(stored) == len(provided):
            return False

        for char in zip(list(provided), list(stored)):
            if char[0] != char[1]:
                return False

        if sys.getsizeof(provided) != sys.getsizeof(stored):
            return False

        if provided[-random_int_check] != stored[-random_int_check]:
            return False

        return True

    tries = 3

    while True:
        provided_key = prompt(
            "enter your encryption password, {} tries left: ".format(tries), hide=True
        )
        stored_key = base64.urlsafe_b64decode(stored)
        provided_key = sha256_rounds(provided_key)
        if stored_key == provided_key:
            if not complex_verification(provided_key, stored_key):
                return False
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
        print(separator + "\n")
        for row in data:
            print("INFO: {}\nSTORED PASSWORD: {}\n".format(
                row[0], encryption.aes_encryption.AESCipher(key).decrypt(row[1])
            ))
        print(separator)
    else:
        print(separator + "\n")
        for row in data:
            print(
                "INFO: {}\nSTORED PASSWORD: {}\n".format(
                    row[0], "*" * 7
                )
            )
        print(separator)


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


def check_for_file_change():
    """
    check if a file has been changed or not, if it has, delete all the data in the home directory
    """
    if not os.path.exists(INIT_FILE):
        fatal("init file does not exist, will not continue")
        exit(-1)
    if open(INIT_FILE).read() == "":
        fatal("init file has been edited, will not continue")
        exit(-1)

    accepted = []
    files_to_check = [
        "{}/.key".format(MAIN_DIR),
        "{}/.pass".format(MAIN_DIR)
    ]
    current_caches = open(INIT_FILE).read().split("\n")
    try:
        current_caches.pop()
    except:
        pass
    for item in zip(current_caches, files_to_check):
        change_time = os.stat(item[1]).st_mtime
        if str(change_time) != item[0]:
            accepted.append("nogo")
        else:
            accepted.append("go")
    if "nogo" in accepted:
        fatal("a file has been changed since initialization assuming compromised and deleting data")
        secure_delete(MAIN_DIR)
        exit(-1)


def create_data_tuples(key):
    """
    create the tuples for storing multiple passwords at a time
    """
    stop = False
    retval = []
    info("press CNTRL-C to finish")
    while not stop:
        try:
            information = prompt("enter password information: ")
            password = prompt("enter password to store with the information ({}): ".format(information), hide=True)
            retval.append((information, encryption.aes_encryption.AESCipher(key).encrypt(password)))
        except KeyboardInterrupt:
            stop = True
            print()
    return retval