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

    def get_by_id(table=None, id_, columns='*'):
        if table is None:
            raise ValueError('table can not be None')

        if columns != '*':
            columns = ', '.join('`{}`'.format(column) for column in columns)

        sql = 'SELECT {} FROM {} WHERE `id`=?'.format(columns, table)
        self.cursor.execute(sql, tuple(id_))

        return self.cursor.fetchone()
