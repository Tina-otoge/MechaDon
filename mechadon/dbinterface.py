import sqlite3

class DBInterface():

    db_path = None

    def __init__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor     = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.close()

    def execute(self, sql):
        self.cursor.executescript(sql)
