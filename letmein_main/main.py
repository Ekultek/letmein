from lib.cmd import LetMeInParser
from encryption.aes_encryption import AESCipher
from lib.output import (
    warning,
    info,
    prompt,
    error,
    fatal
)
from lib.settings import (
    store_key,
    MAIN_DIR,
    BANNER,
    compare,
    secure_delete,
    DATABASE_FILE,
    display_formatted_list_output,
    create_data_tuples
)
from sql.sql import (
    create_connection,
    select_all_data,
    create_new_row,
    display_by_regex,
    update_existing_column,
    show_single_password
)


def main():

    try:
        print(BANNER)

        info("initializing")
        _, stored_password = store_key(MAIN_DIR)

        if not compare(stored_password):
            secure_delete(MAIN_DIR)
            warning("ALL DATA HAS BEEN REMOVED")
        else:
            stored_key, _ = store_key(MAIN_DIR, grab_key=True)
            opt = LetMeInParser().optparse()

            info("password accepted!")
            conn, cursor = create_connection(DATABASE_FILE)
            if opt.showAllStoredPasswords:
                password_data = select_all_data(cursor, "encrypted_data")
                if password_data is not None:
                    info("gathered {} password(s) total".format(len(password_data)))
                    info("decrypting stored information")
                    display_formatted_list_output(
                        password_data, stored_key, prompting=opt.doNotPrompt, answer=opt.promptAnswer
                    )
                else:
                    fatal("received no password data from the database, is there anything in there?")
            elif opt.showOnlyThisPassword is not None:
                results = show_single_password(opt.showOnlyThisPassword, cursor)
                if len(results) == 0:
                    warning("no information could be found with the provided string, you should check all first")
                else:
                    info("found what you are looking for")
                    display_formatted_list_output(results, stored_key, prompting=opt.doNotPrompt, answer=opt.promptAnswer)
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

                status = create_new_row(conn, cursor, password_information, encrypted_password)
                if status == "ok":
                    info("password stored successfully")
                elif status == "exists":
                    warning(
                        "provided information already exists in the database. if you are trying to update the information "
                        "use the `-u/--update` switch"
                    )
                else:
                    fatal("unable to add row to database, received an error: {}".format(status))
            elif opt.regexToSearch is not None:
                data = display_by_regex(opt.regexToSearch, conn, cursor)
                if len(data) == 0:
                    error("no items matched your search")
                else:
                    info("a total of {} item(s) matched your search".format(len(data)))
                    display_formatted_list_output(
                        data, stored_key, prompting=opt.doNotPrompt, answer=opt.promptAnswer
                    )
            elif opt.updateExistingPassword is not None:
                apparent_possible_passwords = display_by_regex(opt.updateExistingPassword, conn, cursor)
                if len(apparent_possible_passwords) == 0:
                    warning("no apparent existing passwords found with given string")
                else:
                    info("{} possible passwords found to edit".format(len(apparent_possible_passwords)))
                    for i, item in enumerate(apparent_possible_passwords):
                        print("[{}] {}".format(i, item[0]))
                    choice = prompt("choose an item to edit[0-{}]: ".format(len(apparent_possible_passwords) - 1))
                    if int(choice) in range(len(apparent_possible_passwords)):
                        information = prompt("enter the new information for the update: ")
                        password = prompt("enter the new password to update: ", hide=True)
                        result = update_existing_column(
                            conn, cursor, (information, AESCipher(stored_key).encrypt(password)),
                            apparent_possible_passwords[int(choice)]
                        )
                        if result == "ok":
                            info("password updated successfully")
                        else:
                            fatal("issue updating password: {}".format(result))
            elif opt.batchStore:
                to_store = create_data_tuples(stored_key)
                info("storing {} encrypted password(s)".format(len(to_store)))
                for item in to_store:
                    create_new_row(conn, cursor, item[0], item[1])
                info("information stored")
            elif opt.cleanHomeFolder:
                secure_delete(MAIN_DIR)
                info("all data has been deleted")
            exit(0)
    except KeyboardInterrupt:
        error("user quit")