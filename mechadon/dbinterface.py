import sqlite3

class DebugRow(sqlite3.Row):
    def __repr__(self):
        key_values = []
        for key in self.keys():
            key_values.append('\'{}\': {}'.format(key, str(self[key])))

        return '<DebugRow: {{{}}}>'.format(', '.join(key_values))

class DBInterface():

    db_path = None

    def __init__(self, path=None):
        if path is None:
            path = self.db_path

        connection             = sqlite3.connect(path)
        connection.row_factory = DebugRow

        self.connection = connection
        self.cursor     = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.close()

    @staticmethod
    def list_to_sql_vars(list_):
        return ', '.join('?' for element in list_)

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
    
    def get(self, table, columns='*'):
        columns = DBInterface.list_to_sql(columns)
        sql     = 'SELECT {} FROM `{}`'.format(columns, table)
        self.cursor.execute(sql)

        return self.cursor.fetchall()
    def get_by(self, table, data_find, columns='*'):
        columns = DBInterface.list_to_sql(columns)
        cond    = DBInterface.list_to_sql(data_find.keys(), setter=True)
        params  = tuple(data_find.values())
        sql     = 'SELECT {} FROM `{}` WHERE {}'.format(columns, table, cond)
        self.cursor.execute(sql, params)

        return self.cursor.fetchall()

    def set_by(self, table, data_find, data_new):
        columns = DBInterface.list_to_sql(data_new.keys(), setter=True)
        cond    = DBInterface.list_to_sql(data_find.keys(), setter=True)
        params  = list(data_new.values())
        params.extend(list(data_find.values()))
        sql     = 'UPDATE `{}` SET {} WHERE {}'.format(table, columns, cond)

        return self.cursor.execute(sql, params)

    def delete_by(self, table, data_find):
        cond   = DBInterface.list_to_sql(data_find.keys(), setter=True)
        params = list(data_find.values())
        sql    = 'DELETE FROM `{}` WHERE {}'.format(table, cond)

        return self.cursor.execute(sql, params)

    def get_by_id(self, table, id_, columns='*'):
        return self.get_by(table, {'id': id_}, columns)

    def set_by_id(self, table, id_, data_new):
        if len(self.get_by_id(table, id_, ['id'])) == 0:
            self.insert_id(table, id_)

        return self.set_by(table, {'id': id_}, data_new)

    def delete_by_id(self, table, id_):
        return self.delete_by(table, {'id': id_})

    def insert(self, table, id_, data_new={}):
        data_new['id'] = id_
        columns        = DBInterface.list_to_sql(data_new.keys())
        values         = DBInterface.list_to_sql_vars(data_new.keys())
        params         = list(data_new.values())
        sql            = 'INSERT INTO `{}`({}) VALUES ({})'.format(table, columns, values)

        return self.cursor.execute(sql, params)

