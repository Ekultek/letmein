import re
import sqlite3


class SQL(object):

    """
    class to call SQL commands from
    """

    def __init__(self, **kwargs):
        self.tablename = "encrypted_data"
        self.db_file = kwargs.get("db_file", None)
        self.enc_password = kwargs.get("enc_password", None)
        self.connection = kwargs.get("connection", None)
        self.cursor = kwargs.get("cursor", None)
        self.information = kwargs.get("information", None)
        self.to_update = kwargs.get("to_update", None)
        self.regex = kwargs.get("regex", None)

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            sql_command = "CREATE TABLE IF NOT EXISTS {} (info STR, data STR);".format(self.tablename)
            cursor = conn.cursor()
            cursor.execute(sql_command)
            conn.commit()
            return conn, cursor
        except Exception:
            return None

    def select_all_data(self):
        try:
            sql_command = "SELECT * FROM {};".format(self.tablename)
            self.cursor.execute(sql_command)
            rows = self.cursor.fetchall()
            retval = []
            if len(rows) == 0:
                return None
            for row in rows:
                retval.append(row)
            return retval
        except Exception:
            return None

    def create_new_row(self, regex=None):
        sql_insert_command = "INSERT INTO {table} (info, data) VALUES ('{password_info}', '{password_data}');".format(
            table=self.tablename, password_info=self.information, password_data=self.enc_password
        )
        available = self.display_by_regex(provided_regex=regex)
        try:
            for item in available:
                if self.information.lower() == item[0].lower():
                    return "exists"
        except TypeError:
            pass
        self.cursor.execute(sql_insert_command)
        self.connection.commit()
        return "ok"

    def update_existing_column(self):
        update_info_command = "UPDATE {} SET info = '{}' WHERE info = '{}';".format(
            self.tablename, self.to_update[0], self.information[0]
        )
        update_password_command = "UPDATE {} SET data = '{}' WHERE data = '{}';".format(
            self.tablename, self.to_update[1], self.information[1]
        )
        try:
            self.cursor.execute(update_info_command)
            self.cursor.execute(update_password_command)
            self.connection.commit()
            return "ok"
        except Exception as e:
            return e

    def display_by_regex(self, provided_regex=None):

        if provided_regex is not None:
            regex_to_use = provided_regex
        else:
            regex_to_use = self.regex

        def regexp(expr, item):
            try:
                matcher = re.compile(expr)
                return matcher.search(item) is not None
            except TypeError:
                # little issue fixed
                return False

        sql_command = "SELECT info, data FROM {} WHERE info REGEXP {};".format(
            self.tablename, '"{}"'.format(regex_to_use)
        )
        try:
            self.connection.create_function("REGEXP", 2, regexp)
            self.cursor.execute(sql_command)
            results = self.cursor.fetchall()
        except Exception:
            results = None
        return results

    def show_single_password(self):
        sql_command = "SELECT info, data FROM {};".format(self.tablename)
        self.cursor.execute(sql_command)
        results = self.cursor.fetchall()
        for row in results:
            if row[0] == self.information:
                return row[0], row[1]
        return []

