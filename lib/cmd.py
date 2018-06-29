import sys
import time
import argparse

from lib.output import error


class LetMeInParser(argparse.ArgumentParser):

    def __init__(self):
        super(LetMeInParser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "-P", "--password", metavar="PASSWORD", dest="passwordToProcess",
                            help="provide a plaintext password to store (*default=prompt)")
        parser.add_argument("-i", "-I", "--info", metavar="INFORMATION", dest="passwordInformation",
                            help="provide information about the password to store alongside "
                                 "(*default=prompt)")
        parser.add_argument("-S", "--show-all", action="store_true", dest="showAllStoredPasswords",
                            help="display all stored passwords")
        parser.add_argument("-s", "--show", metavar="INFORMATION-STRING", dest="showOnlyThisPassword",
                            help="provided the information string stored alongside the password "
                                 "to show the stored password")
        parser.add_argument("-R", "--regex", metavar="REGEX", dest="regexToSearch",
                            help="provided a string that will be searched as a regular expression and pull "
                                 "all the passwords that match the given expression")
        parser.add_argument("-W", "--store", action="store_true", dest="storeProvidedPassword",
                            help="store a password in the database")
        parser.add_argument("-u", "--update", metavar="INFO", dest="updateExistingPassword",
                            help="update an existing password by looking for the associated information string")
        parser.add_argument("--clean", action="store_true", dest="cleanHomeFolder",
                            help="erase everything in the home folder")
        opts = parser.parse_args()

        if len(sys.argv) == 1:
            error("no arguments passed, dropping to help page")
            time.sleep(3)
            parser.print_help()
            exit(1)
        return opts