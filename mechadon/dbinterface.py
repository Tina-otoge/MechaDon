import sqlite3

class DBInterface():

    db_path = None

    def __init__(self):
        connection             = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        self.connection = connection
        self.cursor     = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.close()

    @staticmethod
    def list_to_sql(list_, setter=False):
        format_ = '`{}`'

        if setter:
            format_ += '=?'

        return ', '.join(format_.format(element) for element in list_)

    def execute(self, script):
        self.cursor.executescript(script)

    def commit(self):
        self.connection.commit()

    def get_by_id(self, table, id_, columns='*'):
        if columns != '*':
            columns = DBInterface.list_to_sql(columns)

        sql = 'SELECT {} FROM {} WHERE `id`=?'.format(columns, table)
        self.cursor.execute(sql, (id_,))

        return self.cursor.fetchone()

    def set_by_id(self, table, id_, dictionary):
        sql = 'UPDATE {} SET {} WHERE `id`=?'.format(
                table, DBInterface.list_to_sql(dictionary, setter=True))

        values = list(dictionary.values())
        values.append(id_)

        return self.cursor.execute(sql, tuple(values))
