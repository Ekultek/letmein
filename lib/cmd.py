import sys
import time
import argparse

from lib.output import error


class LetMeInParser(argparse.ArgumentParser):

    def __init__(self):
        super(LetMeInParser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser(
            usage="./letmein -[S|W|R|u|s] [REGEX|INFO STRING] [-pP|iI] [PASSWORD|INFO] [--clean|no-prompt|answer] [ANSWER]"
        )
        mandatory = parser.add_argument_group("mandatory", "arguments that must be passed to run the program")
        mandatory.add_argument("-S", "--show-all", action="store_true", dest="showAllStoredPasswords",
                               help="display all stored passwords")
        mandatory.add_argument("-s", "--show", metavar="INFORMATION-STRING", dest="showOnlyThisPassword",
                               help="provided the information string stored alongside the password "
                                    "to show the stored password")
        mandatory.add_argument("-R", "--regex", metavar="REGEX", dest="regexToSearch",
                               help="provided a string that will be searched as a regular expression and pull "
                                    "all the passwords that match the given expression")
        mandatory.add_argument("-W", "--store", action="store_true", dest="storeProvidedPassword",
                               help="store a password in the database")
        mandatory.add_argument("-u", "--update", metavar="INFO", dest="updateExistingPassword",
                               help="update an existing password by looking for the associated information string")

        information = parser.add_argument_group("information", "arguments you can pass to provide information")
        information.add_argument("-p", "-P", "--password", metavar="PASSWORD", dest="passwordToProcess",
                                 help="provide a plaintext password to store (*default=prompt)")
        information.add_argument("-i", "-I", "--info", metavar="INFORMATION", dest="passwordInformation",
                                 help="provide information about the password to store alongside "
                                      "(*default=prompt)")

        misc = parser.add_argument_group("misc", "arguments that don't fit into any other category")
        misc.add_argument("--clean", action="store_true", dest="cleanHomeFolder",
                          help="erase everything in the home folder")
        misc.add_argument("--no-prompt", action="store_false", dest="doNotPrompt",
                          help="don't prompt to display the passwords in plaintext")
        misc.add_argument("--answer", metavar="ANSWER", default="n", dest="promptAnswer",
                          help="pass the prompt answer in conjunction with `--no-prompt`")
        opts = parser.parse_args()

        if len(sys.argv) == 1:
            error("no arguments passed, dropping to help page")
            time.sleep(3)
            parser.print_help()
            exit(1)
        return opts
