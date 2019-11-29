import sqlite3
import logging

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
    if not setter:
        return seperator.join([format.format(k) for k in d])
    format += '{}'
    result = []
    for k in d:
        try:
            if issubclass(d[k], DBCommand):
                result.append('`{}` {}'.format(k, d[k].sql()))
        except TypeError as e:
            if isinstance(d[k], list):
                result.append('`{}` IN ({})'.format(
                    k, ', '.join(['?'] * len(d[k]))
                ))
            else:
                result.append('`{}`=?'.format(k))
    return seperator.join(result)

class DebugRow(sqlite3.Row):
    def __repr__(self):
        key_values = []
        for key in self.keys():
            key_values.append('\'{}\': {}'.format(key, str(self[key])))
        return '<DebugRow: {{{}}}>'.format(', '.join(key_values))

class DBCommand:
    def sql():
        return None

class NotEmpty(DBCommand):
    def sql():
        return 'IS NOT NULL'

def commands_filter(item):
    try:
        return not issubclass(item, DBCommand)
    except TypeError:
        return True

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
            search = list(filter(commands_filter, search.values()))
            search = tuple(deepflatten(search, types=list))
        if asc:
            sql += 'ORDER BY {} ASC'.format(asc)
        if desc:
            sql += 'ORDER BY {} DESC'.format(desc)
        self.cursor.execute(sql, search)
        return self.cursor.fetchall()

    def set(self, table, search, new):
        if not isinstance(search, dict):
            search = {'id': search}
        if len(self.get(table, search)) == 0:
            search.update(new)
            return self.insert(table, search)
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
        return self.cursor.execute(sql, params)

