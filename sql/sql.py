import re
import sqlite3

from lib.output import warning


def create_connection(db_file, tablename="encrypted_data"):
    try:
        conn = sqlite3.connect(db_file)
        sql_command = "CREATE TABLE IF NOT EXISTS {} (info STR, data STR);".format(tablename)
        cursor = conn.cursor()
        cursor.execute(sql_command)
        conn.commit()
        return conn, cursor
    except Exception:
        pass


def select_all_data(cursor, tablename):
    sql_command = "SELECT * FROM {}".format(tablename)
    cursor.execute(sql_command)
    rows = cursor.fetchall()
    retval = []
    for row in rows:
        retval.append(row)
    return retval


def create_new_column(connection, cursor, information, enc_password, tablename="encrypted_data"):
    sql_insert_command = "INSERT INTO {table} (info, data) VALUES ('{password_info}', '{password_data}');".format(
        table=tablename, password_info=information, password_data=enc_password
    )
    try:
        cursor.execute(sql_insert_command)
        connection.commit()
    except sqlite3.IntegrityError:
        warning("provided data already exists in the database")


def update_existing_column(connection, cursor, to_update, tablename="encrypted_data"):
    pass


def display_by_regex(regex, connection, cursor, tablename="encrypted_data"):
    def regexp(expr, item):
        matcher = re.compile(expr)
        return matcher.search(item) is not None

    sql_command = "SELECT info, data FROM {} WHERE info REGEXP {};".format(
        tablename, '"{}"'.format(regex)
    )
    try:
        connection.create_function("REGEXP", 2, regexp)
        cursor.execute(sql_command)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
        results = None
    return results

