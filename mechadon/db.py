import sqlite3

from iteration_utilities import deepflatten

def list_to_sql_vars(l):
    return ', '.join(['?'] * len(l))

def list_to_sql(l, setter=False, where=False):
    if l == '*':
        return l
    format = '`{}`'
    if setter:
        format += '=?'
    seperator = ' and ' if where else ', '
    return seperator.join([format.format(e) for e in l])

def dict_to_sql(d, setter=False, where=False):
    if d == '*':
        return d
    format = '`{}`'
    setters = {
        'str': '=?',
        'list': ' IN (?)',
    }
    seperator = ' and ' if where else ', '
    if setter:
        format += '{}'
        result = []
        for k in d:
            if isinstance(d[k], list):
                result.append('`{}` IN ({})'.format(
                    k, ', '.join(['?'] * len(d[k]))
                ))
            else:
                result.append('`{}`=?'.format(k))
        return seperator.join(result)
    return seperator.join([format.format(k) for k in d])

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

    def execute(self, script):
        self.cursor.executescript(script)

    def commit(self):
        self.connection.commit()

    def get(self, table, search=None, columns='*', asc=None, desc=None):
        if asc and desc:
            raise ArithmeticError('Can not order by both ASC and DESC')
        columns = list_to_sql(columns)
        sql     = 'SELECT {} FROM `{}`'.format(columns, table)
        if search and not isinstance(search, dict):
            search = {'id': search}
        if search:
            sql += ' WHERE {}'.format(
                dict_to_sql(search, setter=True, where=True)
            )
            search = tuple(deepflatten(search.values(), types=list))
        if asc:
            sql += 'ORDER BY {} ASC'.format(asc)
        if desc:
            sql += 'ORDER BY {} DESC'.format(desc)
        print('sql: ', sql)
        print(search)
        self.cursor.execute(sql, search)
        return self.cursor.fetchall()

    def set(self, table, search, new):
        if len(self.get(table, search)) == 0:
            return self.insert(table, new)
        if not isinstance(search, dict):
            search = {'id': search}
        columns = list_to_sql(new.keys(), setter=True)
        cond    = list_to_sql(search.keys(), setter=True, where=True)
        params  = list(new.values())
        params.extend(list(search.values()))
        sql     = 'UPDATE `{}` SET {} WHERE {}'.format(table, columns, cond)
        return self.cursor.execute(sql, params)

    def delete(self, table, search):
        if not isinstance(search, dict):
            search = {'id', search}
        cond   = list_to_sql(search.keys(), setter=True, where=True)
        params = list(search.values())
        sql    = 'DELETE FROM `{}` WHERE {}'.format(table, cond)
        return self.cursor.execute(sql, params)

    def insert(self, table, data):
        columns        = list_to_sql(data.keys())
        values         = list_to_sql_vars(data.keys())
        params         = list(data.values())
        sql            = 'INSERT INTO `{}`({}) VALUES ({})'.format(table, columns, values)
        print(sql)
        return self.cursor.execute(sql, params)

