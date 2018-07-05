from sql.sql import SQL
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


def main():

    try:
        opt = LetMeInParser().optparse()

        if opt.showVersionNumber:
            from lib.settings import VERSION_STRING, VERSION

            print(VERSION.format(VERSION_STRING))
            exit(0)

        print(BANNER)

        info("initializing")
        _, stored_password = store_key(MAIN_DIR)

        if not compare(stored_password):
            secure_delete(MAIN_DIR)
            warning("ALL DATA HAS BEEN REMOVED")
        else:
            stored_key, _ = store_key(MAIN_DIR, grab_key=True)
            info("password accepted!")
            conn, cursor = SQL(db_file=DATABASE_FILE).create_connection()

            if opt.showAllStoredPasswords:
                password_data = SQL(cursor=cursor).select_all_data()
                if password_data is not None:
                    info("gathered {} password(s) total".format(len(password_data)))
                    info("decrypting stored information")
                    display_formatted_list_output(
                        password_data, stored_key, prompting=opt.doNotPrompt, answer=opt.promptAnswer
                    )
                else:
                    fatal("received no password data from the database, is there anything in there?")
            elif opt.showOnlyThisPassword is not None:
                results = SQL(information=opt.showOnlyThisPassword, cursor=cursor).show_single_password()
                if len(results) == 0:
                    warning("no information could be found with the provided string, you should check all first")
                else:
                    info("found what you are looking for")
                    try:
                        display_formatted_list_output(
                            results, stored_key, prompting=opt.doNotPrompt, answer=opt.promptAnswer
                        )
                    except TypeError:
                        print("INFO: {}\tSTORED PASSWORD: {}\n\n{}".format(
                            results[0], AESCipher(stored_key).decrypt(results[1]), "-" * 30
                        ))
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

                status = SQL(
                    connection=conn, cursor=cursor, information=password_information,
                    enc_password=encrypted_password
                ).create_new_row()
                if status == "ok":
                    info("password stored successfully")
                elif status == "exists":
                    warning(
                        "provided information already exists in the database. "
                        "if you are trying to update the information use the `-u/--update` switch"
                    )
                else:
                    fatal("unable to add row to database, received an error: {}".format(status))
            elif opt.regexToSearch is not None:
                data = SQL(regex=opt.regexToSearch, connection=conn, cursor=cursor).display_by_regex()
                if len(data) == 0:
                    error("no items matched your search")
                else:
                    info("a total of {} item(s) matched your search".format(len(data)))
                    display_formatted_list_output(
                        data, stored_key, prompting=opt.doNotPrompt, answer=opt.promptAnswer
                    )
            elif opt.updateExistingPassword is not None:
                apparent_possible_passwords = SQL(
                    regex=opt.updateExistingPassword, connection=conn, cursor=cursor
                ).display_by_regex()
                if len(apparent_possible_passwords) == 0:
                    fatal("no apparent existing passwords found with given string")
                else:
                    info("{} possible passwords found to edit".format(len(apparent_possible_passwords)))
                    for i, item in enumerate(apparent_possible_passwords):
                        print("[{}] {}".format(i, item[0]))
                    choice = prompt("choose an item to edit[0-{}]: ".format(len(apparent_possible_passwords) - 1))
                    if int(choice) in range(len(apparent_possible_passwords)):
                        information = prompt("enter the new information for the update: ")
                        password = prompt("enter the new password to update: ", hide=True)
                        result = SQL(
                            connection=conn, cursor=cursor,
                            to_update=(information, AESCipher(stored_key).encrypt(password)),
                            information=apparent_possible_passwords[int(choice)]
                        ).update_existing_column()
                        if result == "ok":
                            info("password updated successfully")
                        else:
                            fatal("issue updating password: {}".format(result))
            elif opt.batchStore:
                to_store = create_data_tuples(stored_key)
                info("storing {} encrypted password(s)".format(len(to_store)))
                for item in to_store:
                    SQL(
                        connection=conn, cursor=cursor, regex=item[0], information=item[0], enc_password=item[1]
                    ).create_new_row()
                info("information stored")
            elif opt.cleanHomeFolder:
                secure_delete(MAIN_DIR)
                info("all data has been deleted")
            exit(0)
    except KeyboardInterrupt:
        error("user quit")
