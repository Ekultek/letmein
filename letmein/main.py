import os

from lib.cmd import LetMeInParser
from encryption.aes_encryption import AESCipher
from lib.output import warning, info, prompt, error
from lib.settings import store_key, MAIN_DIR, compare, secure_delete, DATABASE_FILE, display_formatted_list_output
from sql.sql import create_connection, select_all_data, create_new_column, display_by_regex


def main():
    stored_key = store_key(MAIN_DIR)

    if not compare(stored_key):
        for item in os.listdir(MAIN_DIR):
            path = "{}/{}".format(MAIN_DIR, item)
            secure_delete(path)
        warning("ALL DATA HAS BEEN REMOVED")
    else:
        opt = LetMeInParser().optparse()
        info("key accepted!")
        conn, cursor = create_connection(DATABASE_FILE)
        if opt.showAllStoredPasswords:
            password_data = select_all_data(cursor, "encrypted_data")
            info("gathered {} password(s) total".format(len(password_data)))
            info("decrypting stored information")
            display_formatted_list_output(password_data, stored_key)
        elif opt.storeProvidedPassword:
            if opt.passwordInformation is not None:
                password_information = opt.passwordInformation
            else:
                password_information = prompt("enter the information string associated with this password: ")

            if opt.passwordToProcess is not None:
                encrypted_password = AESCipher(stored_key).encrypt(opt.passwordToProcess)
            else:
                password = prompt("enter the password to store: ", hide=True)
                encrypted_password = AESCipher(stored_key).encrypt(password)

            create_new_column(conn, cursor, password_information, encrypted_password)
            info("password stored successfully")
        elif opt.regexToSearch is not None:
            data = display_by_regex(opt.regexToSearch, conn, cursor)
            if len(data) == 0:
                error("no items matched your search")
            else:
                info("a total of {} item(s) matched your search".format(len(data)))
                display_formatted_list_output(data, stored_key)
        elif opt.updateExistingPassword is not None:
            print("update existing (TODO)")
        else:
            print("No arguments passed dropping into terminal")
        exit(0)


