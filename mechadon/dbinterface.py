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
        if list_ == '*':
            return list_

        format_ = '`{}`'

        if setter:
            format_ += '=?'

        return ', '.join(format_.format(element) for element in list_)

    def execute(self, script):
        self.cursor.executescript(script)

    def commit(self):
        self.connection.commit()

    def get_by(self, table, data_find, columns='*'):
        columns = DBInterface.list_to_sql(columns)
        cond    = DBInterface.list_to_sql(data_find.keys(), setter=True)
        params  = tuple(data_find.values())
        sql     = 'SELECT {} FROM {} WHERE {}'.format(columns, table, cond)
        self.cursor.execute(sql, params)

        return self.cursor.fetchall()

    def set_by(self, table, data_find, data_new):
        columns = DBInterface.list_to_sql(data_new.keys(), setter=True)
        cond    = DBInterface.list_to_sql(data_find.keys(), setter=True)
        params  = list(data_new.values())
        params.extend(list(data_find.values()))
        sql     = 'UPDATE {} SET {} WHERE {}'.format(table, columns, cond)

        return self.cursor.execute(sql, params)

    def get_by_id(self, table, id_, columns='*'):
        return self.get_by(table, {'id': id_}, columns)

    def set_by_id(self, table, id_, data_new):
        if len(self.get_by_id(table, id_, ['id'])) == 0:
            self.insert_id(table, id_)
            print('inserted')
        return self.set_by(table, {'id': id_}, data_new)

    def insert_id(self, table, id_):
        sql = 'INSERT INTO {}(`id`) VALUES (?)'.format(table)

        return self.cursor.execute(sql, (id_,))
