import re
import sqlite3


def create_connection(db_file, tablename="encrypted_data"):
    try:
        conn = sqlite3.connect(db_file)
        sql_command = "CREATE TABLE IF NOT EXISTS {} (info STR, data STR);".format(tablename)
        cursor = conn.cursor()
        cursor.execute(sql_command)
        conn.commit()
        return conn, cursor
    except Exception:
        return None


def select_all_data(cursor, tablename):
    try:
        sql_command = "SELECT * FROM {}".format(tablename)
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        retval = []
        for row in rows:
            retval.append(row)
        return retval
    except Exception:
        return None


def create_new_row(connection, cursor, information, enc_password, tablename="encrypted_data"):
    sql_insert_command = "INSERT INTO {table} (info, data) VALUES ('{password_info}', '{password_data}');".format(
        table=tablename, password_info=information, password_data=enc_password
    )
    try:
        available = display_by_regex(information, connection, cursor)
        for item in available:
            if information.lower() == item[0].lower():
                return "exists"
        cursor.execute(sql_insert_command)
        connection.commit()
        return "ok"
    except Exception as e:
        return e


def update_existing_column(connection, cursor, to_update, information, tablename="encrypted_data"):
    update_info_command = "UPDATE {} SET info = '{}' WHERE info = '{}';".format(
        tablename, to_update[0], information[0]
    )
    update_password_command = "UPDATE {} SET data = '{}' WHERE data = '{}';".format(
        tablename, to_update[1], information[1]
    )
    try:
        cursor.execute(update_info_command)
        cursor.execute(update_password_command)
        connection.commit()
        return "ok"
    except Exception as e:
        return e


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
    except Exception:
        results = None
    return results


def show_single_password(info, cursor, tablename="encrypted_data"):
    sql_command = "SELECT info, data FROM {} where INFO = {};".format(tablename, info)
    cursor.execute(sql_command)
    results = cursor.fetchall()
    return results

